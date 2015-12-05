import sys
import os
import string
from stemming.porter2 import stem

def main(argv):
	companies = ['aapl', 'amzn', 'msft', 'tsla']
	for company in companies:
		for filename in os.listdir(os.getcwd() + '/' + company + '/raw'):
			if filename.endswith('.DS_Store') is False:
				filepath = company + '/raw/' + filename
				rawContent = open(filepath, 'r')
				rawStr = rawContent.read()
				date = rawStr.split()[0]
				tokens =  rawStr.replace('-',' ').split()
				tokens[0] = date
				rawContent.close()
				stemmedContent = ''
				for token in tokens[1:]:
					token = token.translate(string.maketrans("",""), string.punctuation)
					token = stem(token.lower())
					stemmedContent += ' ' + token
				stemmedFileName = company + '/stemmed/' + filename
				stemmedContent = stemmedContent.encode('ascii', 'ignore')
				filestream = open(stemmedFileName, 'w+')
				filestream.write(date + ' ' + stemmedContent)
				filestream.close()

if __name__ == "__main__":
	main(sys.argv)