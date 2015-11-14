import urllib2
from bs4 import BeautifulSoup
import json
from urlparse import urlparse
import hashlib
import re

def parse_bloomberg(soup):
	news = soup.find('div', attrs= {'class': 'news__state active'})
	result = ''
	for story in news.find_all('article', attrs = {'class': 'news__story'}):
		for headline in story.find_all('div', attrs = {'class': 'news__story__headline'}):
			date = story.find('time')
			result += date.get('datetime') + ','
			link = story.find('a')
			result += link.get('href') + ',\n'
	return result

def parse_fool(soup):
	articles = soup.find_all('article')
	result = ''
	for article in articles:
		date = article.find('span')
		date_only = re.findall(r'[A-Z][a-z][a-z] \d\d \d\d\d\d', date.text)[0]
		result += date_only +','
		link = article.find('a').get('href')
		result += link[2:] + ',\n'
	return result

def parse_ibtimes(soup):
	result = ''
	content = soup.find('ol', attrs={'class': 'archive-list apachesolr_search'})
	headlines = content.find_all('li', attrs= {'class': 'clearfix'})
	for headline in headlines:
		date = headline.find('div', attrs= {'class':'byline'}).text
		date_only = re.findall(r'\d\d\d\d-\d\d-\d\d', date)[0]
		result += date_only + ','
		link = headline.find('a')
		result += link.get('href') + ',\n'
	return result

def parse():
	scrape = open('scrapeLinks.json')
	files = json.load(scrape)
	scrape.close
	sites = files.keys()
	companies = ['apple', 'microsoft', 'amazon', 'tesla']
	for company in companies:
		filestream = open(company + '.csv', 'w+')
		filestream.write('')
		filestream.close()
	for site in sites:
		for company in companies:
			urls = files[site][company]
			for url in urls:
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

				filename = company + '.csv'
				content = content.encode('ascii', 'ignore')
				filestream = open(filename, 'a+')
				filestream.write(content)
				filestream.close()

parse()

