import sys
sys.path.append("../")

from set1.set1 import *
from set2 import *

"""
Break AES-CBC
"""
if __name__ == "__main__":
	key = gen_key()
	iv = gen_key()
	cipher = AES.new(key, AES.MODE_CBC, iv)
	 
	print("=====Approach 1=====")
	user_input = ":admin<true"
	ct = build_userdata(user_input, key, iv)
	ct = bytearray(ct)
	print("Old ciphertext. Check bytes 0 and 6 of block 1:")
	print_blocks(ct)
	# flip bits of first byte in second block to modify first byte in third block
	for new_ct in cbc_flipper(ct, 16):
		pt = unpad(cipher.decrypt(new_ct), AES.block_size)
		if bytes([pt[32]]) == b";":
			ct = new_ct
			break
	# flip bits of first byte in second block to modify first byte in third block
	for new_ct in cbc_flipper(ct, 22):
		pt = unpad(cipher.decrypt(new_ct), AES.block_size)
		if bytes([pt[38]]) == b"=":
			ct = new_ct
			break
	print("New ciphertext. Check bytes 0 and 6 of block 1:")
	print_blocks(ct)
	passed = parse_userdata(ct, key, iv)
	print(passed)


	print("=====Approach 2=====")
	user_input = ":admin<true"
	ct = build_userdata(user_input, key, iv)
	ct = bytearray(ct)
	print("Old ciphertext. Check bytes 0 and 6 of block 1:")
	print_blocks(ct)
	# second block pre-modification
	pre_mod_prev_ct = ct[16:32]
	# intermediate state
	curr_pre_encrypt = byte_array_xor(pre_mod_prev_ct, bytearray(b":admin<true;comm"))
	# derive desired ciphertext of previous block
	post_mod_prev_ct = byte_array_xor(curr_pre_encrypt, bytearray(b";admin=true;comm"))
	# replace old previous ciphertext block with new previous ciphertext block
	new_ct = ct[0:16] + post_mod_prev_ct + ct[32:]
	print("New ciphertext. Check bytes 0 and 6 of block 1:")
	print_blocks(new_ct)
	passed = parse_userdata(new_ct, key, iv)
	print(passed)


