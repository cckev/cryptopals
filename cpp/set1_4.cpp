#include "strencodings.h"
#include "freqanalysis.h"
#include "arith.h"

#include <iostream>
#include <fstream>
#include <limits>
#include <string>
#include <vector>

int main(int argc, char* argv[]) {
	if (argc < 2) {
		std::cerr << "Usage: " << argv[0] << " <input_file>" << std::endl;
		return 0;
	} else {
		std::string input_file = argv[1];
		std::ifstream infs(input_file);
		std::vector<unsigned char> pt;
		double best_score = std::numeric_limits<double>::max();

		if (infs) {
			std::string line;
			while (getline(infs,line)) {
				std::tuple <std::vector<unsigned char>, double> curr = GetSingleCharXorPt(line);
				double this_score = std::get<1>(curr);
				
				if (this_score <= best_score) {
					best_score = this_score;
					pt = std::get<0>(curr);
				}
			}
		}

		infs.close();

		for (const auto &c : pt)
			std::cout << c;
		std::cout << '\n';
		std::cout << best_score;
	}
}