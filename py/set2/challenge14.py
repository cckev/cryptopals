import sys
sys.path.append("../")

from set1.set1 import *
from set2 import *

global_key = gen_key()

"""
Break AES-ECB
"""
if __name__ == "__main__":
	# generate some random string between 1-16 bytes long
	random_padding = secrets.token_urlsafe(16)[:secrets.randbelow(16)+1]
	unknown_s = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
	unknown_decoded = base64.b64decode(unknown_s).decode('utf-8')

	"""
	Find block size of encryption algorithm
	"""
	ct_size = len(base64.b64decode(encryption_oracle(random_padding+unknown_decoded, global_key, None, "ecb", False)))
	for fuzz, i in fuzz_helper("A",1):
		new_ct_size = len(base64.b64decode(encryption_oracle(random_padding+fuzz+unknown_decoded, global_key, None, "ecb", False)))
		if new_ct_size > ct_size:
			block_size = new_ct_size - ct_size
			break

	"""
	If AES-ECB detected, try to crack it
	"""
	decoded = ""
	if detect_aes_ecb(base64.b64decode(encryption_oracle("A"*47+unknown_decoded, global_key, None, "ecb", False))):
		# find padding required to pad first block to block_size
		for fuzz, i in fuzz_helper("A",1):
			if detect_aes_ecb(base64.b64decode(encryption_oracle(random_padding+fuzz+unknown_decoded, global_key, None, "ecb", False))):
				padding_required = i
				break
		# aligns first block
		padding_required = padding_required-(block_size*2)
		aligned_padding = random_padding+"A"*padding_required
		for i in range(1,ct_size+1):
			decoder = {}
			block_num = (i//block_size)+1
			prepend = "A"*(block_size-(i%block_size))
			# set start and end indices
			start = block_num*block_size
			end = block_num*block_size+block_size
			# build decoder
			for printable in string.printable:	
				data = aligned_padding+prepend+decoded+printable
				ct = base64.b64decode(encryption_oracle(data, global_key, None, "ecb", False))
				curr_block = ct[start:end]
				# add block to decoder
				if curr_block not in decoder:
					decoder[curr_block] = printable
			# find ct[block_num] in decoder
			data = aligned_padding+prepend+unknown_decoded
			ct = base64.b64decode(encryption_oracle(data, global_key, None, "ecb", False))
			curr_block = ct[start:end]
			if curr_block not in decoder:
				print(f"Broke at i={i}/{ct_size+1}. Likely hit PCKS7 padding.\n")
				break
			else:
				decoded += decoder[curr_block]
		print(decoded)
