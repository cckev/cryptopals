from set1 import *

with open("4.txt", "r") as f:
	data = f.readlines()
data = [line.strip() for line in data]

for i,line in enumerate(data):
	res = find_xor_chr(line)
	if res:
		print(f"{i}: {res}")