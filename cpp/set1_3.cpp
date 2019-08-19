#include "strencodings.h"
#include "freqanalysis.h"
#include "arith.h"

#include <iostream>
#include <limits>
#include <string>
#include <vector>

int main() {
	std::vector<unsigned char> pre_xor = ParseHex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736");
	unsigned int len = pre_xor.size();
	int best_score = std::numeric_limits<int>::max();
	std::vector<unsigned char> res;
	for (std::size_t i = 0; i < 256; i++) {
		std::vector<unsigned char> key(len, i);
		std::vector<unsigned char> post_xor = XorByteArrays(pre_xor, key);
		int curr_score = ScorePlaintext(post_xor);
		if (curr_score < best_score) {
			best_score = curr_score;
			res = post_xor;
		}
	}
	
	for (const auto &c : res)
		std::cout << c;
	std::cout << '\n';
	std::cout << best_score;
}