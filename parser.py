import urllib2
from bs4 import BeautifulSoup
import json
from urlparse import urlparse
import hashlib
import csv
import sys
from multiprocessing import Pool
import os


'''
To use this parser from the terminal call it like this:

python parser.py parsing_files/filename

or to parse all the files in parsing_files:

python parser.py

WARNING: can't stop the parser once it starts

'''

def parse_bloomberg(soup):
	content = soup.find('div', attrs = {'class': 'article-body__content'})
	result = ''
	for p in content.find_all('p'):
		result += p.text + ' '
	return result
	

def parse_techcrunch(soup):
	content = soup.find('script', attrs = {'type': 'application/ld+json'})
	body = json.loads(content.text)['articleBody']
	return body.replace('\n',' ').replace('\t',' ').replace('\r',' ')


def parse_ibtimes(soup):
	content = soup.find('div', attrs = {'class': 'article-content'})
	result = ''
	for p in content.find_all('p'):
		result += p.text + ' '
	return result

def parse_fool(soup):
	content = soup.find('section', attrs = {'class': 'usmf-new article-body'})
	result = ''
	for p in content.find_all('p'):
		result += p.text + ' '
	return result




def parse(row):
	date = row[0]
	url = row[1]
	company = row[2]
	try:
		html = urllib2.urlopen(url).read()
		soup = BeautifulSoup(html, "html.parser")
		domain =  urlparse(url).netloc
		if domain == 'techcrunch.com':
			content = parse_techcrunch(soup)
		elif domain == 'www.bloomberg.com':
			content = parse_bloomberg(soup)
		elif domain == 'www.ibtimes.com':
			content = parse_ibtimes(soup)
		elif domain == 'www.fool.com':
			content = parse_fool(soup)
		filename = company + '/raw/' + str(hashlib.sha224(url).hexdigest())
		content = content.encode('ascii', 'ignore')
		filestream = open(filename, 'w+')
		filestream.write(date + ' ' + content)
		filestream.close()
		print url

	except Exception as e:
		print e




def main(argv):
	files = []
	if len(argv) is 2:
		files.append(argv[1])
	else:
		for filename in os.listdir(os.getcwd() + '/parsing_files'):
			files.append('parsing_files/' + filename)

	rows = []
	for filename in files:
		csvfile = open(filename, 'rU')
		reader = csv.reader(csvfile, delimiter = ',', dialect=csv.excel_tab)
		header = next(reader, None)
		company = header[2]
		for row in reader:
			row = [row[0], row[1], company]
			rows.append(row)
		csvfile.close()

	p = Pool(10)
	p.map(parse, rows)


if __name__ == "__main__":
    main(sys.argv)


