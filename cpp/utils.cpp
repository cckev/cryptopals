#include "utils.h"

#include <fstream>
#include <iterator>
#include <vector>
#include <string>

std::vector<unsigned char> ReadFile(const std::string &filename) {
	// open file
	std::ifstream file(filename, std::ios::binary);

	// prevents eating new lines in binary mode
	file.unsetf(std::ios::skipws);

	file.seekg(0, std::ios::end);
	size_t file_size = file.tellg();
	file.seekg(0, std::ios::beg);

	std::vector<unsigned char> data;
	data.reserve(file_size);

	// read data
	data.insert(data.begin(), 
				std::istream_iterator<unsigned char>(file),
				std::istream_iterator<unsigned char>());

	return data;
}