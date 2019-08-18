// Copyright (c) 2009-2010 Satoshi Nakamoto
// Copyright (c) 2009-2018 The Bitcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include "strencodings.h"

#include <algorithm>
#include <cstdlib>
#include <cstring>
#include <errno.h>
#include <limits>

static const std::string CHARS_ALPHA_NUM = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

static const std::string SAFE_CHARS[] = {
	CHARS_ALPHA_NUM + " .,;-_/:?@()", // SAFE_CHARS_DEFAULT
	CHARS_ALPHA_NUM + " .,;-_?@", // SAFE_CHARS_UA_COMMENT
	CHARS_ALPHA_NUM + ".-_", // SAFE_CHARS_FILENAME
	CHARS_ALPHA_NUM + "!*'();:@&=+$,/?#[]-_.~%", // SAFE_CHARS_URI
};

std::string SanitizeString(const std::string &str, int rule) {
	std::string res;
	for (std::string::size_type i = 0; i < str.size(); i++) {
		if (SAFE_CHARS[rule].find(str[i]) != std::string::npos)
			res.push_back(str[i]);
	}
	return res;
}

const signed char p_util_hexdigit[256] = { 
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	0,1,2,3,4,5,6,7,8,9,-1,-1,-1,-1,-1,-1,
	-1,0xa,0xb,0xc,0xd,0xe,0xf,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,0xa,0xb,0xc,0xd,0xe,0xf,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
	-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1
};

signed char HexDigit(char c) {
	return p_util_hexdigit[(unsigned char)c];
}

bool IsHexNumber(const std::string& str) {
	size_t starting_location = 0;
	if (str.size() > 2 && *str.begin() == '0' && *(str.begin() + 1) == 'x') {
		starting_location = 2;
	}
	for (const char c : str.substr(starting_location)) {
		if (HexDigit(c) < 0) return false;
	}
	// Return false for empty string or "0x".
	return (str.size() > starting_location);
}

std::vector<unsigned char> ParseHex(const char *psz) {
	// convert hex dump to vector
	std::vector<unsigned char> vch;
	while (true) {
		while (IsSpace(*psz))
			psz++;
		signed char c = HexDigit(*psz++);
		if (c == (signed char)-1)
			break;
		unsigned char n = (c << 4);
		c = HexDigit(*psz++);
		if (c == (signed char)-1)
			break;
		n |= c;
		vch.push_back(n);
	}
	return vch;
}

std::vector<unsigned char> ParseHex(const std::string &str) {
	return ParseHex(str.c_str());
}

std::string EncodeBase64(const unsigned char *pch, size_t len) {
	static const char *pbase64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	std::string str;
	str.reserve(((len + 2) / 3) * 4);
	ConvertBits<8, 6, true>([&](int v) { str += pbase64[v]; }, pch, pch + len);
	while (str.size() % 4) str += '=';
	return str;
}

std::string EncodeBase64(const std::string& str) {
	return EncodeBase64((const unsigned char*)str.c_str(), str.size());
}

std::vector<unsigned char> DecodeBase64(const char *p, bool *pf_invalid) {
	static const int decode64_table[256] = {
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
		-1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1,
		-1, -1, -1, -1, -1,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14,
		15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28,
		29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
		49, 50, 51, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
	};

	const char *e = p;
	std::vector<uint8_t> val;
	val.reserve(strlen(p));
	while (*p != 0) {
		int x = decode64_table[(unsigned char)*p];
		if (x == -1) break;
		val.push_back(x);
		++p;
	}

	std::vector<unsigned char> ret;
	ret.reserve((val.size() * 3) / 4);
	bool valid = ConvertBits<6, 8, false>([&](unsigned char c) { ret.push_back(c); }, val.begin(), val.end());

	const char *q = p;
	while (valid && *p != 0) {
		if (*p != '=') {
			valid = false;
			break;
		}
		++p;
	}
	valid = valid && (p - e) % 4 == 0 && p - q < 4;
	if (pf_invalid) *pf_invalid = !valid;

	return ret;
}

std::string DecodeBase64(const std::string &str, bool *pf_invalid) {
	std::vector<unsigned char> vch_ret = DecodeBase64(str.c_str(), pf_invalid);
	return std::string((const char*)vch_ret.data(), vch_ret.size());
}

std::string ToLower(const std::string &str) {
	std::string r;
	for (auto ch : str) r += ToLower((unsigned char)ch);
	return r;
}

std::string ToUpper(const std::string& str) {
	std::string r;
	for (auto ch : str) r += ToUpper((unsigned char)ch);
	return r;
}

std::string Capitalize(std::string str) {
	if (str.empty()) return str;
	str[0] = ToUpper(str.front());
	return str;
}