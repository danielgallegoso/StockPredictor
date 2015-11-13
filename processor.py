import os
import sys
import csv

'''
TODO: make csv for y's

Based on dictionary.txt will create frequency csv

python processor.py msft


'''

def get_freq_array(dictionary, filename):
	result = []
	entry = open(filename, 'r')
	tokens =  entry.read().split()
	entry.close()
	for i in xrange(0,len(dictionary)):
		result.append(0)
		for token in tokens:
			if token.lower() == dictionary[i].lower():
				result[i] += 1
	return result

	

def main(argv):
	dictfile = open('dictionary.txt', 'r+')
	dictionary = dictfile.read().split()
	dictfile.close()
	rows = []
	for filename in os.listdir(os.getcwd() + '/' + argv[1] + '/raw'):
		if filename.endswith('.DS_Store') is False:
			rows.append(get_freq_array(dictionary, argv[1] + '/raw/' + filename))
	rows = zip(*rows)

	csvfile = open(argv[1] + '/x.csv', 'wb')
	writer = csv.writer(csvfile, delimiter = ',')
	for row in rows:
		writer.writerow(row)
	csvfile.close()
			
			

if __name__ == "__main__":
    main(sys.argv)