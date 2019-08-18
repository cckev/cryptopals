from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64


with open("7.txt","r") as f:
	data = f.readlines()
s = "".join(data).replace("\n","").encode() # argument should be a bytes-like object or ASCII string

key = b"YELLOW SUBMARINE"
cipher = AES.new(key, AES.MODE_ECB)
ct = base64.b64decode(s)
pt = unpad(cipher.decrypt(ct), AES.block_size).decode("utf-8") # AES block size is 16 bytes
print(f"Plaintext:\n{pt}")
