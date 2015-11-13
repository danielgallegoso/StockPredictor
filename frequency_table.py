import os
import sys


'''
python frequency_table.py msft
'''

def main(argv):
	freq = {}
	for filename in os.listdir(os.getcwd() + '/' + argv[1] + '/raw'):
		if filename.endswith('.DS_Store') is False:
			entry = open(argv[1] + '/raw/' + filename, 'r')
			tokens =  entry.read().split()
			for token in tokens:
				if freq.get(token) is None:
					freq[token] = 1
				else:
					freq[token] += 1
			entry.close()
	keys = freq.keys()
	keys = sorted(keys, key = lambda token: freq[token])
	for key in keys:
		print key, freq[key]


if __name__ == "__main__":
    main(sys.argv)