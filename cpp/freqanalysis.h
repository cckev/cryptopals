#ifndef FREQ_ANALYSIS_H
#define FREQ_ANALYSIS_H

#include <map>
#include <vector>
#include <tuple>

static const std::string CHARS_ALPHA_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

/*
* Frequency taken from http://en.wikipedia.org/wiki/Letter_frequency
*/
static std::map<char, double> FREQ_TABLE = {
	{'E', 12.70}, {'T', 9.06}, {'A', 8.17}, {'O', 7.51}, 
	{'I', 6.97}, {'N', 6.75}, {'S', 6.33}, {'H', 6.09}, 
	{'R', 5.99}, {'D', 4.25}, {'L', 4.03}, {'C', 2.78}, 
	{'U', 2.76}, {'M', 2.41}, {'W', 2.36}, {'F', 2.23}, 
	{'G', 2.02}, {'Y', 1.97}, {'P', 1.93}, {'B', 1.29}, 
	{'V', 0.98}, {'K', 0.77}, {'J', 0.15}, {'X', 0.15}, 
	{'Q', 0.10}, {'Z', 0.07}
};

/*
* Default table for building an alphabetic histogram from a document
*/
static std::map<unsigned char, double> DEFAULT_TABLE = {
	{'E', 0}, {'T', 0}, {'A', 0}, {'O', 0}, 
	{'I', 0}, {'N', 0}, {'S', 0}, {'H', 0}, 
	{'R', 0}, {'D', 0}, {'L', 0}, {'C', 0}, 
	{'U', 0}, {'M', 0}, {'W', 0}, {'F', 0}, 
	{'G', 0}, {'Y', 0}, {'P', 0}, {'B', 0}, 
	{'V', 0}, {'K', 0}, {'J', 0}, {'X', 0}, 
	{'Q', 0}, {'Z', 0}
};

/*
* Builds a frequency table of characters in plaintext and compares against 
* "normal" English document letter frequency. A score of 0 is a perfect match.
* Higher scores indicate a greater deviation from normal frequency.
*/
double ScorePlaintext(std::vector<unsigned char> plaintext);


/*
* Returns the most likely byte array result of single character XOR encoding and its score
*/
std::tuple <std::vector<unsigned char>, double> GetSingleCharXorPt(std::string plaintext);


#endif // FREQ_ANALYSIS_H