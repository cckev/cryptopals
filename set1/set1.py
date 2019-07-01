
import base64

# frequency taken from http://en.wikipedia.org/wiki/Letter_frequency
FREQ_TABLE = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}

# default table for building an alphabetic histogram from a document
DEF_TABLE = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}

# used to hold candidates for single key xors
CHARS = ['0x01', '0x02', '0x03', '0x04', '0x05', '0x06', '0x07', '0x08', '0x09', '0x0a', '0x0b', '0x0c', '0x0d', '0x0e', '0x0f', '0x10', '0x11', '0x12', '0x13', '0x14', '0x15', '0x16', '0x17', '0x18', '0x19', '0x1a', '0x1b', '0x1c', '0x1d', '0x1e', '0x1f', '0x20', '0x21', '0x22', '0x23', '0x24', '0x25', '0x26', '0x27', '0x28', '0x29', '0x2a', '0x2b', '0x2c', '0x2d', '0x2e', '0x2f', '0x30', '0x31', '0x32', '0x33', '0x34', '0x35', '0x36', '0x37', '0x38', '0x39', '0x3a', '0x3b', '0x3c', '0x3d', '0x3e', '0x3f', '0x40', '0x41', '0x42', '0x43', '0x44', '0x45', '0x46', '0x47', '0x48', '0x49', '0x4a', '0x4b', '0x4c', '0x4d', '0x4e', '0x4f', '0x50', '0x51', '0x52', '0x53', '0x54', '0x55', '0x56', '0x57', '0x58', '0x59', '0x5a', '0x5b', '0x5c', '0x5d', '0x5e', '0x5f', '0x60', '0x61', '0x62', '0x63', '0x64', '0x65', '0x66', '0x67', '0x68', '0x69', '0x6a', '0x6b', '0x6c', '0x6d', '0x6e', '0x6f', '0x70', '0x71', '0x72', '0x73', '0x74', '0x75', '0x76', '0x77', '0x78', '0x79', '0x7a', '0x7b', '0x7c', '0x7d', '0x7e', '0x7f', '0x80', '0x81', '0x82', '0x83', '0x84', '0x85', '0x86', '0x87', '0x88', '0x89', '0x8a', '0x8b', '0x8c', '0x8d', '0x8e', '0x8f', '0x90', '0x91', '0x92', '0x93', '0x94', '0x95', '0x96', '0x97', '0x98', '0x99', '0x9a', '0x9b', '0x9c', '0x9d', '0x9e', '0x9f', '0xa0', '0xa1', '0xa2', '0xa3', '0xa4', '0xa5', '0xa6', '0xa7', '0xa8', '0xa9', '0xaa', '0xab', '0xac', '0xad', '0xae', '0xaf', '0xb0', '0xb1', '0xb2', '0xb3', '0xb4', '0xb5', '0xb6', '0xb7', '0xb8', '0xb9', '0xba', '0xbb', '0xbc', '0xbd', '0xbe', '0xbf', '0xc0', '0xc1', '0xc2', '0xc3', '0xc4', '0xc5', '0xc6', '0xc7', '0xc8', '0xc9', '0xca', '0xcb', '0xcc', '0xcd', '0xce', '0xcf', '0xd0', '0xd1', '0xd2', '0xd3', '0xd4', '0xd5', '0xd6', '0xd7', '0xd8', '0xd9', '0xda', '0xdb', '0xdc', '0xdd', '0xde', '0xdf', '0xe0', '0xe1', '0xe2', '0xe3', '0xe4', '0xe5', '0xe6', '0xe7', '0xe8', '0xe9', '0xea', '0xeb', '0xec', '0xed', '0xee', '0xef', '0xf0', '0xf1', '0xf2', '0xf3', '0xf4', '0xf5', '0xf6', '0xf7', '0xf8', '0xf9', '0xfa', '0xfb', '0xfc', '0xfd', '0xfe', '0xff']

 
"""
Convert ascii string to hex string
Returns hex string, no prefix
"""
def ascii_to_hex(str):
	res = ""
	for c in str:
		res += "{0:02x}".format(ord(c))
	return res


"""
Convert hex string to base64
Returns a base64 encoded string
"""
def hex_to_b64(hex_str):
	data = bytearray.fromhex(hex_str)
	return base64.b64encode(data).decode()


"""
Convert base64 to hex
Returns hex string
"""
def b64_to_hex(b64_str):
	return base64.b64decode(b64_str).hex()


"""
Xor two hex strings
Returns result in hex, no prefix
"""
def xor_hex(hex1, hex2):
	return hex(int(hex1,16)^int(hex2,16)).replace("0x","")



"""
Returns byte representation of an int
"""
def int_to_bytes(num):
	return (num).to_bytes(1, byteorder="big")


"""
Determine which single character a hex string was xor'ed with
Returns the most likely candidate based on agreement with 'normal' english histogram distribution
"""
def find_xor_chr(hex_str):
	candidates = []
	for key in CHARS:
		score = 0
		desired_len = len(hex_str)
		candidate_key = key.replace("0x","") * (desired_len//2)
		candidate_str = xor_hex(hex_str, candidate_key)

		if len(candidate_str) < desired_len:
			candidate_str = "0" * (desired_len-len(candidate_str)) + candidate_str
		try:
			candidate_str = bytes.fromhex(candidate_str).decode("utf-8")
		except:
			continue

		hist = DEF_TABLE
		# build a histogram of alphabetic freq values for candidate_str
		for c in candidate_str:
			if c.upper() in hist:
				hist[c.upper()] += 1
			elif c == " ":
				continue
			else:
				score += 1

		# normalize freq values
		# penalize by subtracting resultant freq from target freq
		denom = len(candidate_str)
		for k,v in hist.items():
			hist[k] /= denom
			score += abs(FREQ_TABLE[k]-hist[k])

		candidates.append((candidate_str, candidate_key[:2], score))
	
	if len(candidates) > 0:
		#print(sorted(candidates,key=lambda x:x[2]))
		return sorted(candidates,key=lambda x:x[2])[0]
	else:
		return 0


"""
Xor plaintext with key
Returns result
"""
def repeating_key_xor(data, key, format="plain"):
	res = ""
	len_key = len(key)
	key_it = 0
	if format == "plain":	
		for c in data:
			res += xor_hex(ascii_to_hex(c), ascii_to_hex(key[key_it])).zfill(2)
			key_it+=1
			key_it = key_it%len_key
	elif format == "hex":
		for j in range(0,len(data),2):
			res += xor_hex(data[j:j+2],key[key_it:key_it+2]).zfill(2)
			key_it+=2
			key_it = key_it%len_key
	return res


"""
Returns hamming distance of two plaintext strings
"""
def ham_dist(str1, str2, format="plain"):
	if format == "plain":
		bin_dist = bin(int(repeating_key_xor(str1, str2), 16))[2:]
	elif format == "hex":
		bin_dist = bin(int(xor_hex(str1,str2), 16))[2:]
	return bin_dist.count("1")


"""
Splits string of data on <blocksize> blocks
Returns a list of strings
"""
def data_to_blocks(data, blocksize, format="hex"):
	if format == "hex":
		blocksize *= 2 # reading hex strings
		m = [data[i:i+blocksize] for i in range(0,len(data),blocksize)]
	return m


"""
Takes list of blocks of strings as input
Returns transposed list
"""
def transpose_blocks(data, blocksize=0):
	if not blocksize:
		blocksize = len(data[0])//2
	m=[]
	for i in range(blocksize):
		m.append("")
	for block in data:
		for i in range(0,blocksize):
			ind = i*2
			m[i]+=block[ind:ind+2]
	return m


"""
Finds number of repeating blocks in a given plaintext string
Returns number of repeats
"""
def find_repeating_blocks(data, blocksize=16):
	block_set = set()
	res=0
	for i in range(len(data)//blocksize-1):
		curr = data[i*blocksize:i*blocksize+blocksize]
		if curr in block_set:
			res+=1
		else:
			block_set.add(curr)
	return res


