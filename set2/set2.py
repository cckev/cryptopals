import sys
sys.path.append("../")

import secrets
import base64
import string
import urllib.parse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from set1 import *
from tinydb import TinyDB, Query, where
db = TinyDB('users.json')


"""
Generate sequence of random bytes using secrets module
Returns random bytes
"""
def gen_key(length=16):
	return secrets.token_bytes(length)


"""
Takes plaintext string as input and returns plaintext padded according to PKCS#7 spec
"""
def pad_pkcs7(data, block_size=16):
	val = block_size-(len(data)%block_size)
	if val == 0: val = block_size
	hex_val = bytes([val])
	return data + hex_val.decode()*val
	

"""
Encrypts data under an unknown key using ECB or CBC
Can append 5-10 bytes before data and after data
Retuns result in base64
"""
def encryption_oracle(data, key=None, iv=None, mode="random", padding=True, format="ascii"):
	if key == None:
		key = gen_key()

	if format == "ascii":
		data = data.encode()
	elif format == "hex":
		data = bytes.fromhex(data)

	if padding == True:
		pad_len = secrets.randbelow(6)+5
		data = secrets.token_bytes(pad_len)+data+secrets.token_bytes(pad_len)

	mode = mode.lower()
	if mode == "random":
		mode = "cbc" if secrets.randbits(1) else "ecb"
	if mode == "cbc":
		if not iv:
			iv = gen_key()
		cipher = AES.new(key, AES.MODE_CBC, iv)
	elif mode == "ecb":
		cipher = AES.new(key, AES.MODE_ECB)
		
	#ct_bytes = cipher.encrypt(pad(data, AES.block_size)) # AES block size is 16 bytes
	ct_bytes = cipher.encrypt(pad(data, len(key)))
	ct = base64.b64encode(ct_bytes).decode('utf-8')
	return ct


"""
Decrypts ciphertext generated with known key and AES-ECB
from raw bytes
"""
def decrypt_aes_ecb(ciphertext, key, block_size):
	cipher = AES.new(key, AES.MODE_ECB)
	pt = unpad(cipher.decrypt(ciphertext), block_size)
	return pt


"""
Detects AES-ECB by looking for repeated ciphertext blocks.
User needs to be able to control plaintext. To guarantee detection,
two identical plaintext blocks need to be encrypted.
"""
def detect_aes_ecb(ciphertext):
	return set1.find_repeating_blocks(ciphertext)


"""
Helper function to fuzz encryption oracle with identical bytes of data
"""
def fuzz_helper(data="A", start=0, end=float('infinity')):
	i = start
	while i < end:
		yield data*i, i
		i+=1


"""
k=v parsing routine
"""
def k_v_parser(data, separator="&"):
	parsed = {}
	data = data.split(separator)

	for i in range(0, len(data)):
		# split on first occurence of "="
		data[i] = data[i].split("=",1)
		# if no "=" found, then there was a separator in the user input
		# we need to put the separator back into prev data and quote the separator
		# then combine current data with prev data
		if len(data[i]) == 1:
			parsed[data[i-1][0]]+=f"{urllib.parse.quote(separator)}{data[i][0]}"
			continue
		else:
			k,v = data[i][0],data[i][1].replace("=",urllib.parse.quote("="))
			parsed[k] = v
	return parsed


"""
Quotes out occurences of specific characters
Characters to remove are provided in a list
"""
def url_quote(data, remove=[]):
	if remove == []:
		return data
	for r in remove:
		data = data.replace(r,urllib.parse.quote(r))
	return data


"""
Encode user data formatted as:

{
  email: 'foo@bar.com',
  uid: 10,
  role: 'user'
}

into:

"email=foo@bar.com&uid=10&role=user"
"""
def k_v_encoder(data):
	encoded = ""
	for k, v in data.items():
		if k == "role":
			encoded += k + "=" + v
		else:
			encoded += k + "=" + v + "&"
	return encoded


"""
Add a user to the db
"""
def add_user(email, role="user"):
	# zero-padded uid to three digits
	uid = f"{len(db):03}"
	email = url_quote(email,['&','='])
	db.insert({'email': email, 'uid': str(uid), 'role': role})


"""
Remove a user from the db
"""
def remove_user(email):
	user = Query()
	doc_id = db.get(user.email == email).doc_id
	db.remove(doc_ids=[doc_id])


"""
Queries the db for a user by email
Returns encoded string if user is found
"""
def profile_for(email):
	user = Query()
	user = db.get(user.email == email)
	if user is None:
		print(f"User with email, {email}, was not found.")
		return
	return k_v_encoder(user)


"""
Validates whether plaintext has valid PKCS7 padding
"""
def validate_pkcs7(plaintext):
	pad_num = ord(plaintext[-1])
	all_padding = plaintext[-pad_num:]
	if all_padding != plaintext[-1]*pad_num:
		raise Exception("Invalid PKCS7 padding")
	else:
		return True


"""
Takes arbitrary input string
Prepends "comment1=cooking%20MCs;userdata="
Appends ";comment2=%20like%20a%20pound%20of%20bacon"
Quotes out the ";" and "=" characters
Pad out the input to the 16-byte AES block length and encrypt it under the random AES key
"""
def build_userdata(data, key=None, iv=None):
	assert key is not None, f"Need valid AES key and IV"
	assert iv is not None, f"Need valid AES IV"
	comment_1 = "comment1=cooking%20MCs;userdata="
	comment_2 = ";comment2=%20like%20a%20pound%20of%20bacon"
	data = comment_1 + url_quote(data,[';','=']) + comment_2
	encrypted_data = base64.b64decode(encryption_oracle(data, key, iv, "cbc", False))
	return encrypted_data


"""
Takes AES-encrypted output of build_userdata() as input
Decrypts the string, parses keys, and looks for 'admin': "true"
"""
def parse_userdata(ciphertext, key=None, iv=None):
	assert key is not None, f"Need valid AES key and IV"
	assert iv is not None, f"Need valid AES IV"
	cipher = AES.new(key, AES.MODE_CBC, iv)
	data = {}
	try:
		pt = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
		print(f"Plaintext was {pt}")
		data = k_v_parser(pt,";")
		print(f"Data was {data}")
		return data.get('admin', "0").lower() == "true"	
	except:
		pt = unpad(cipher.decrypt(ciphertext), AES.block_size)
		print(f"Plaintext was {pt}")
		return b";admin=true;" in pt


"""
Performs xor on the bits of ciphertext[pos] with values 0 to 255
to achieve desired plaintext output
"""
def cbc_flipper(ciphertext, pos):
	for i in range(1,255):
		ciphertext[pos] = ciphertext[pos] ^ i
		yield ciphertext


"""
Xor two byte arrays
"""
def byte_array_xor(arr_1, arr_2):
	# zero extend the smaller byte array
	len_1, len_2 = len(arr_1), len(arr_2)
	if len_1 >= len_2:
		byte_diff = len_1-len_2
		arr_2 = b'\x00'*byte_diff + arr_2
	else:
		byte_diff = len_2-len_1
		arr_1 = b'\x00'*byte_diff + arr_1
	return bytearray(arr_1[i] ^ arr_2[i] for i in range(max(len_1,len_2)))


"""
Prints data block by block
"""
def print_blocks(data, block_size=16):
	for i in range(len(data)//block_size):
		print(f"Block {i}: {data[i*block_size:i*block_size+block_size]}")