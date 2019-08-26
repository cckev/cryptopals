#include "strencodings.h"
#include "freqanalysis.h"
#include "arith.h"

#include <iostream>
#include <limits>
#include <string>
#include <vector>
#include <tuple>

int main() {
	std::tuple <std::vector<unsigned char>, double> res = GetSingleCharXorPt("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736");
	
	for (const auto &c : std::get<0>(res))
		std::cout << c;
	std::cout << '\n';
	std::cout << std::get<1>(res);
}