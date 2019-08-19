#include "arith.h"

#include <iostream>
#include <vector>
#include <cassert>

std::vector<unsigned char> XorByteArrays(std::vector<unsigned char> h1, std::vector<unsigned char> h2) {
	assert(h1.size() == h2.size());
	std::size_t n = h1.size();
	std::vector<unsigned char> res;
	res.reserve(n);
	for (std::size_t i = 0; i < n; i++) {
		res.push_back(h1[i] ^ h2[i]);
	}
	return res;
}