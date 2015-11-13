import urllib2
from bs4 import BeautifulSoup
import json
from urlparse import urlparse
import hashlib
import csv
import sys



'''
To use this parser from the terminal call it like this:

python parser.py parsing_files/filename

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

def main(argv):
	filename = argv[1]
	csvfile = open(filename, 'rU')
	reader = csv.reader(csvfile, delimiter = ',', dialect=csv.excel_tab)
	header = next(reader, None)
	company = header[2]

	for row in reader:
		date = row[0]
		url = row[1]
		html = urllib2.urlopen(url).read()
		soup = BeautifulSoup(html, "html.parser")
		domain =  urlparse(url).netloc
		
		try:
			if domain == 'techcrunch.com':
				content = parse_techcrunch(soup)
			elif domain == 'www.bloomberg.com':
				content = parse_bloomberg(soup)
			elif domain == 'www.ibtimes.com':
				content = parse_ibtimes(soup)
			elif domain == 'www.fool.com':
				content = parse_fool(soup)
		except AttributeError as e:
			print e 

		filename = company + '/' + str(hashlib.sha224(url).hexdigest())
		content = content.encode('ascii', 'ignore')
		filestream = open(filename, 'w+')
		filestream.write(date + ' ' + content)
		filestream.close()
		print url

	csvfile.close()

if __name__ == "__main__":
    main(sys.argv)


