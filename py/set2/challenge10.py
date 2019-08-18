import sys
sys.path.append("../")

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from set1 import *
from set2 import *
import base64


with open("10.txt","r") as f:
	data = f.readlines()
s = "".join(data).replace("\n","").encode() # argument should be a bytes-like object or ASCII string

key = b"YELLOW SUBMARINE"
iv = b"\x00"*AES.block_size
cipher = AES.new(key, AES.MODE_CBC, iv)
ct = base64.b64decode(s)
pt = unpad(cipher.decrypt(ct), AES.block_size).decode("utf-8") # AES block size is 16 bytes
print(f"Plaintext:\n{pt}")



