import sys
sys.path.append("../")

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from set1.set1 import *
from set2 import *
import base64

# minimum number of repeated bytes to guarantee two repeated blocks under AES
s = "A"*47

ct = encryption_oracle(s)
decoded = base64.b64decode(ct)
print_blocks(decoded)
if find_repeating_blocks(decoded):
	print(f"AES in ECB mode detected.")
else:
	print(f"AES in CBC mode likely.")