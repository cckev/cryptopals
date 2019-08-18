import sys
sys.path.append("../")

from set1.set1 import *
from set2 import *


if __name__ == "__main__":
	key = gen_key()

	"""
	Find block size of encryption algorithm
	"""
	add_user("A@test.com")
	ct_size = len(base64.b64decode(encryption_oracle("A@test.com", key, None, "ecb", False)))
	remove_user("A@test.com") # to avoid filling up our db
	for fuzz, i in fuzz_helper("A",2):
		new_user = fuzz+"@test.com"
		add_user(new_user)
		new_ct_size = len(base64.b64decode(encryption_oracle(new_user, key, None, "ecb", False)))
		remove_user(new_user)
		if new_ct_size > ct_size:
			block_size = new_ct_size - ct_size
			break
	print(f"Block size: {block_size}")

	"""
	Fuzzing with "A"*block_size*3 guarantees detection of AES-ECB even if padding
	is being prepended to the data
	"""
	new_user = "A"*block_size*3+"@test.com"
	add_user(new_user)
	prof = profile_for(new_user)
	print(f"{prof} added to the database")
	encrypted_data = base64.b64decode(encryption_oracle(prof, key, None, "ecb", False))
	remove_user(new_user)
	print(f"{prof} removed")


	"""
	If we detect AES_ECB, proceed with attack
	"""
	if detect_aes_ecb(encrypted_data):
		print("AES_ECB detected. Proceeding with attack.")
		# align first block
		new_user = "aaaa@a.com"
		# craft replacement ciphertext
		new_user += "admin\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b"

		# determine what the "admin\x0b..." block looks like
		add_user(new_user)
		prof = profile_for(new_user)
		print(f"{prof} added to the database")
		encrypted_data = base64.b64decode(encryption_oracle(prof, key, None, "ecb", False))
		remove_user(new_user)
		admin_block = encrypted_data[block_size:block_size*2]
		print(f"{admin_block} is the admin+padding block.")

		"""
		Create a user so that "role=..." is aligned to the end of a block

		First block: "email=aaaaaa@a.c"
		Secondblock: "om&uid=000&role="
		Third block: "admin\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b"

		After oracle generates ciphertext, replace last block with our admin_block
		"""
		new_user = "aaaaaa@a.com"
		add_user(new_user)
		prof = profile_for(new_user)
		print(f"{prof} added to the database")
		encrypted_data = base64.b64decode(encryption_oracle(prof, key, None, "ecb", False))
		remove_user(new_user)
		print(f"{prof} removed")
		print(f"Old payload: {encrypted_data}")

		ct_size = len(encrypted_data)
		payload = encrypted_data[:ct_size-block_size] + admin_block
		print(f"New payload: {payload}")

		# test if generated user is an admin
		print(decrypt_aes_ecb(payload, key, block_size))
		# b'email=aaaaaa@a.com&uid=000&role=admin'