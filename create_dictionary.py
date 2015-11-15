import os
import sys
import string
from stemming.porter2 import stem

'''
python create_dictionary.py will create dictionary.txt, which has 300 
of the most frequently used tokens in all articles from all four companies.
For each token, removes punctuation then stems the word before insertion insertion
into the dictionary. 
'''

def main():
	freq = {}
	companies = ['aapl', 'amzn', 'msft', 'tsla']
	dictionary = set()
	for company in companies:
		for filename in os.listdir(os.getcwd() + '/' + company + '/raw'):
			if filename.endswith('.DS_Store') is False:
				entry = open(company + '/raw/' + filename, 'r')
				tokens =  entry.read().split()
				for token in tokens:
					token = token.translate(string.maketrans("",""), string.punctuation)
					token = stem(token.lower())
					if token.isalpha():
						if freq.get(token) is None:
							freq[token] = 1
						else:
							freq[token] += 1
				entry.close()
	remove = ['by', 'with', 'is', 'on', 'for', 'from', 'it', 'a', 'in', 'to', 'of', 'the', 'and', 'or', 'are', 'us', 'has', 'an']
	for generic in remove:
		if freq.get(token) is not None:
			del freq[generic]
	keys = freq.keys()
	keys = sorted(keys, key = lambda token: freq[token], reverse = True)[:300]
	keys = sorted(keys)
	txtfile = open('dictionary.txt', 'w')
	for key in keys:
		txtfile.write(key + '\n')
	txtfile.close()
	# for key in keys:
	# 	print key, freq[key]


if __name__ == "__main__":
    main()