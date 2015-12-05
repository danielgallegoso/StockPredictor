import os
import sys
import string

'''
python frequency_table.py msft
Creates frequency_table.txt in company's respective folder. Company ticker
must be passed as the argument. Each company uses the same dictionary previously generated
by create_dictionary for its own frequency table.
'''

def main(argv):
	freq = {}
	for i in xrange(1,len(argv)):
		for filename in os.listdir(os.getcwd() + '/' + argv[i] + '/stemmed'):
			if filename.endswith('.DS_Store') is False:
				entry = open(argv[i] + '/stemmed/' + filename, 'r')
				tokens =  entry.read().split()
				for token in tokens:
					if token.isalpha():
						if freq.get(token) is None:
							freq[token] = 1
						else:
							freq[token] += 1
				entry.close()
	remove = ['by', 'with', 'is', 'on', 'for', 'from', 'it', 'a', 'in', 'to', 'of', 'the', 'and', 'or', 'are', 'us', 'has', 'an']
	for generic in remove:
		if freq.get(generic) is not None:
			del freq[generic]
	for key in freq.keys():
		if len(key) == 1:
			del freq[key]
			
	keys = freq.keys()
	keys = sorted(keys, key = lambda token: freq[token])
	freq_file = open(os.getcwd() + '/dictionary.txt', 'wb')
	for i in xrange(len(keys) - 250, len(keys)):
		freq_file.write(keys[i] + '\n')
	freq_file.close()

if __name__ == "__main__":
    main(sys.argv)