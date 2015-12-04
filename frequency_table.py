import os
import sys
import string
from stemming.porter2 import stem

'''
python frequency_table.py msft
Creates frequency_table.txt in company's respective folder. Company ticker
must be passed as the argument. Each company uses the same dictionary previously generated
by create_dictionary for its own frequency table.
'''

def main(argv):
	freq = {}
	with open("dictionary.txt","r") as text:
		for word in text:
			freq[word[:-1]] = 0
	for filename in os.listdir(os.getcwd() + '/' + argv[1] + '/raw'):
		if filename.endswith('.DS_Store') is False:
			entry = open(argv[1] + '/raw/' + filename, 'r')
			tokens =  entry.read().split()
			for token in tokens:
				token = token.translate(string.maketrans("",""), string.punctuation)
				token = stem(token.lower())
				if token.isalpha():
					if freq.get(token) is not None:
						freq[token] += 1
			entry.close()
	keys = freq.keys()
	keys = sorted(keys, key = lambda token: freq[token])
	keys = sorted(keys)
	freq_file = open(os.getcwd() + '/' + argv[1] + '/frequency_table.txt', 'wb')
	for key in keys:
		freq_file.write(key + ' ' + str(freq[key]) + '\n')
	freq_file.close()

if __name__ == "__main__":
    main(sys.argv)