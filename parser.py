import urllib2
from bs4 import BeautifulSoup

def parse_bloomberg(url):
	html = urllib2.urlopen("http://www.bloomberg.com/news/articles/2015-10-07/amazon-seeks-cloud-computing-growth-with-new-data-products").read()
	soup = BeautifulSoup(html, "html.parser")
	content = soup.find('div', attrs = {'class': 'article-body__content'})
	result = ''
	for p in content.find_all('p'):
		result += p.text
	print result