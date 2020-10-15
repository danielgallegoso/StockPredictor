import os
import sys
import string

'''
python frequency_table.py msft
Creates frequency_table.txt in company's respective folder. Company ticker
must be passed as the argument. Each company uses the same dictionary previously generated
by create_dictionary for its own frequency table.

python create_sentiment_dictionary.py 100  aapl msft amzn tsla

'''

def get_sentiments():
	neg = open('neg_words.txt', 'r+')
	words = neg.read().split()
	pos = open('pos_words.txt', 'r+')
	words += pos.read().split()
	result = {}
	for word in words:
		result[word] = 0
	return result


def main(argv):
	freq = get_sentiments()
	for i in xrange(2,len(argv)):
		for filename in os.listdir(os.getcwd() + '/' + argv[i] + '/stemmed'):
			if filename.endswith('.DS_Store') is False:
				entry = open(argv[i] + '/stemmed/' + filename, 'r')
				tokens =  entry.read().split()
				for token in tokens:
					if token.isalpha():
						if freq.get(token) != None:
							freq[token] += 1
				entry.close()

	keys = freq.keys()
	keys = sorted(keys, key = lambda token: freq[token])
	freq_file = open(os.getcwd() + '/dictionary.txt', 'wb')
	for i in xrange(len(keys) - int(argv[1]), len(keys)):
		freq_file.write(keys[i] + '\n')
	freq_file.close()

if __name__ == "__main__":
    main(sys.argv)