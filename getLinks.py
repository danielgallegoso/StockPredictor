import urllib2
from bs4 import BeautifulSoup
import json
from urlparse import urlparse
import hashlib
import re
import datetime


def parse_bloomberg(soup, company):
	news = soup.find('div', attrs= {'class': 'news__state active'})
	result = ''
	for story in news.find_all('article', attrs = {'class': 'news__story'}):
		for headline in story.find_all('div', attrs = {'class': 'news__story__headline'}):
			date = story.find('time')
			date_only = re.findall(r'\d\d\d\d-\d\d-\d\d', date.get('datetime'))[0]
			result += date_only + ','
			link = story.find('a')
			result += link.get('href') + ','
			result += company + ',\n'
	return result

def parse_fool(soup, company):
	articles = soup.find_all('article')
	result = ''
	for article in articles:
		date = article.find('span')
		date_only = re.findall(r'[A-Z][a-z][a-z] \d\d \d\d\d\d', date.text)[0]
		date_only = datetime.datetime.strptime(date_only, '%b %d %Y').strftime('%Y-%m-%d')
		result += date_only +','
		link = article.find('a').get('href')
		result += link[2:] + ','
		result += company + ',\n'
	return result

def parse_ibtimes(soup, company):
	result = ''
	content = soup.find('ol', attrs={'class': 'archive-list apachesolr_search'})
	headlines = content.find_all('li', attrs= {'class': 'clearfix'})
	for headline in headlines:
		date = headline.find('div', attrs= {'class':'byline'}).text
		date_only = re.findall(r'\d\d\d\d-\d\d-\d\d', date)[0]
		result += date_only + ','
		link = headline.find('a')
		result += link.get('href') + ','
		result += company + ',\n'
	return result

def parse():
	scrape = open('scrapeLinks.json')
	files = json.load(scrape)
	scrape.close
	sites = files.keys()
	companies = ['aapl', 'msft', 'amzn', 'tsla']
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
					content = parse_techcrunch(soup, company)
				elif domain == 'www.bloomberg.com':
					content = parse_bloomberg(soup, company)
				elif domain == 'www.ibtimes.com':
					content = parse_ibtimes(soup, company)
				elif domain == 'www.fool.com':
					content = parse_fool(soup, company)

				filename = company + '.csv'
				content = content.encode('ascii', 'ignore')
				filestream = open(filename, 'a+')
				filestream.write(content)
				filestream.close()

parse()

