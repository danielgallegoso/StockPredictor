import urllib2
from bs4 import BeautifulSoup
import json
from urlparse import urlparse
import hashlib

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

def parse():
	scrape = open('scrape.json')
	files = json.load(scrape)
	scrape.close
	companies = files.keys()
	for company in companies:
		for url in files[company]:
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

			filename = company + '/' + str(hashlib.sha224(url).hexdigest())
			content = content.encode('ascii', 'ignore')
			filestream = open(filename, 'w+')
			filestream.write(content)
			filestream.close()


parse()

