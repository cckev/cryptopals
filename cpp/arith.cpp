#include "arith.h"

#include <iostream>
#include <vector>
#include <cassert>


std::vector<unsigned char> XorByteArrays(const std::vector<unsigned char> &h1, const std::vector<unsigned char> &h2) {
	assert(h1.size() == h2.size());
	std::size_t n = h1.size();
	std::vector<unsigned char> res;
	res.reserve(n);
	for (std::size_t i = 0; i < n; i++) {
		res.push_back(h1[i] ^ h2[i]);
	}
	return res;
}


/*
* Pass k_index in as starting index of key. Used to save index state in multiline plaintexts.
*/
std::vector<unsigned char> RepeatingKeyXor(const std::vector<unsigned char> &plaintext, const std::vector<unsigned char> &key, int k_index) {
	size_t key_size = key.size();
	size_t pt_size = plaintext.size();
	assert(key_size <= pt_size);
	std::vector<unsigned char> res;
	for (size_t i = 0; i < plaintext.size(); i++) {
			res.push_back(plaintext[i] ^ key[k_index % key_size]);
			k_index++;
	}
	return res;
}

