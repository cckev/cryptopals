#include "strencodings.h"
#include "freqanalysis.h"
#include "utils.h"
#include "arith.h"

#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <vector>

int main(int argc, char* argv[]) {
	if (argc < 2) {
		std::cerr << "Usage: " << argv[0] << " <input_file>" << std::endl;
		return 0;
	} else {
		std::string input_file = argv[1];
		std::cout << "Type the key here: ";

		std::string line;
		std::getline(std::cin, line);
		std::vector<unsigned char> key(line.begin(), line.end());


		std::vector<std::string> ct;
		unsigned char pt;
		int k_index = 0;
		std::ifstream infile(input_file);

		while (std::getline(infile, line)) {
			line += "\n";
			std::vector<unsigned char> pt_vec(line.begin(), line.end());
			ct.push_back(HexStr(RepeatingKeyXor(pt_vec, key, k_index)));
			k_index += pt_vec.size();
		}

		// removes the last newline from ct
		ct.back() = ct.back().substr(0, ct.back().length()-2);
		for (const auto &c : ct)
			std::cout << c << "\n";
	}
}