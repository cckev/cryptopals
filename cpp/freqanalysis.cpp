#include "freqanalysis.h"

#include <vector>

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