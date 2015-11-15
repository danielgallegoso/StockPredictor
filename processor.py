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
	return result, tokens[0]

	
def get_prices():
	csvfile = open('prices.csv', 'rU')
	reader = csv.reader(csvfile, delimiter = ',', dialect=csv.excel_tab)
	prices = {}
	header = next(reader, None)
	for i in xrange(1, len(header)):
		prices[header[i]] = {}
	prev = None
	for row in reader:
		for i in xrange(1, len(row)):
			prices[header[i]][row[0]] = row[i]
	csvfile.close()
	return prices



def main(argv):
	dictfile = open('dictionary.txt', 'r+')
	dictionary = dictfile.read().split()
	dictfile.close()
	prices = get_prices()
	rows = []
	ys = []
	for filename in os.listdir(os.getcwd() + '/' + argv[1] + '/raw'):
		if filename.endswith('.DS_Store') is False:
			row, date = get_freq_array(dictionary, argv[1] + '/raw/' + filename)
			ys.append(prices[argv[1]][date])
			rows.append(row)

	rows = zip(*rows)

	csvfile = open(argv[1] + '/x.csv', 'wb')
	writer = csv.writer(csvfile, delimiter = ',')
	for row in rows:
		writer.writerow(row)
	csvfile.close()
	csvfile = open(argv[1] + '/y.csv', 'wb')
	csv.writer(csvfile, delimiter = ',').writerow(ys)
	csvfile.close()

			
			

if __name__ == "__main__":
    main(sys.argv)