#ifndef ARITH_H
#define ARITH_H

#include <vector>
#include <valarray>

std::vector<unsigned char> XorHex(std::vector<unsigned char> h1, std::vector<unsigned char> h2) {
	std::valarray<unsigned char> h_1(h1.data(), h1.size());
	std::valarray<unsigned char> h_2(h2.data(), h2.size());
	std::valarray<unsigned char> temp = h_1 ^ h_2;
	std::vector<unsigned char> res;
	res.assign(std::begin(temp), std::end(temp));
	return res;
}

#endif // ARITH_H