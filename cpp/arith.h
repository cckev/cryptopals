#ifndef ARITH_H
#define ARITH_H

#include <vector>

std::vector<unsigned char> XorByteArrays(const std::vector<unsigned char> &h1, const std::vector<unsigned char> &h2);

std::vector<unsigned char> RepeatingKeyXor(const std::vector<unsigned char> &plaintext, const std::vector<unsigned char> &key, int s_index);

#endif // ARITH_H