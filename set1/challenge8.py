from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from set1 import *

data = []
with open("8.txt","r") as f:
	for line in f:
		data.append(line.replace("\n",""))

res = {}
for line in data:
	res[line] = find_repeating_blocks(line)

print(sorted(res.items(), key=lambda x:(x[1], x[0]), reverse=True)[0])



