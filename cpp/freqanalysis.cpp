#include "freqanalysis.h"
#include "arith.h"
#include "strencodings.h"

#include <string>
#include <vector>
#include <tuple>
#include <limits>

double ScorePlaintext(std::vector<unsigned char> plaintext) {
	double score = 0;
	std::map<unsigned char, double> plaintext_table = DEFAULT_TABLE;
	unsigned int total_chars = plaintext.size();
	for (const auto &c : plaintext) {		
		if (isalpha(c)) {
			std::map<unsigned char, double>::iterator it = plaintext_table.find(toupper(c));
			it->second += 1;
		}
		else if (c == ' ') {
			continue;
		}
		else {
			// Penalize for anything other than english character
			score++;
		}
	}

	double len = plaintext.size();
	// Normalize all frequencies
	for (auto &c : plaintext_table) {
		c.second = c.second/len;
		score += abs((FREQ_TABLE.find(c.first))->second - c.second);
	}

	return score;
}


std::tuple<std::vector<unsigned char>, double> GetSingleCharXorPt(std::string plaintext) {
	std::vector<unsigned char> pre_xor = ParseHex(plaintext);
	unsigned int len = pre_xor.size();
	double best_score = std::numeric_limits<double>::max();
	std::vector<unsigned char> pt;
	for (std::size_t i = 0; i < 256; i++) {
		std::vector<unsigned char> key(len, i);
		std::vector<unsigned char> post_xor = XorByteArrays(pre_xor, key);
		double curr_score = ScorePlaintext(post_xor);
		if (curr_score < best_score) {
			best_score = curr_score;
			pt = post_xor;
		}
	}
	
	return std::make_tuple(pt, best_score);
}
