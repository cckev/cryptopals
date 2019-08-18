from set1 import *

with open("6.txt","r") as f:
	data = f.readlines()
s = "".join(data).replace("\n","")
s = b64_to_hex(s)

 # contains keysize guess and avg hamming distance between two blocks
hams = {}

# keysizes need to be in multiples of two since we are reading hex
for size in range(4,82,2):
	num_slices = len(s)//size
	score = 0
	iterations = 0
	for i in range(num_slices-1):
		block_1 = s[i*size:i*size+size]
		block_2 = s[i*size+size:i*size+size*2]
		#print(f"{block_1}, {block_2}, {ham_dist(block_1,block_2,'hex')/size}")
		score += ham_dist(block_1,block_2,"hex")/size
		iterations += 1
	hams[size//2] = score/iterations

# keysizes sorted by shortest average hamming distance between two blocks
sorted_hams = sorted(hams.items(), key=lambda x:(x[1],x[0]))
# print(sorted_hams)

# item[0] is keysize, item[1] is hamming dist
for item in sorted_hams[:3]:
	test_blocks = data_to_blocks(s, int(item[0]))
	#print(test_blocks)
	
	transposed_blocks = transpose_blocks(test_blocks)
	#print(transposed_blocks)
	
	print(f"Finding candidate key for keysize: {item[0]}")
	key = ""
	for block in transposed_blocks:
		block_len = len(block)
		key+=find_xor_chr(block)[1]

	pkey = bytes.fromhex(key).decode("utf-8")
	ptext = bytes.fromhex(repeating_key_xor(s, key, "hex")).decode("utf-8")

	print(f"key: {pkey}\nplaintext: {ptext}")
		

