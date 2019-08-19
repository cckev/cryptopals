#include "strencodings.h"
#include "arith.h"

#include <iostream>
#include <string>
#include <vector>

int main() {
	std::vector<unsigned char> hex_1 = ParseHex("1c0111001f010100061a024b53535009181c");
	std::vector<unsigned char> hex_2 = ParseHex("686974207468652062756c6c277320657965");
	std::vector<unsigned char> temp = XorByteArrays(hex_1, hex_2);
	std::string res = HexStr(temp.begin(), temp.end());
	std::cout << res;
	return 0;
}