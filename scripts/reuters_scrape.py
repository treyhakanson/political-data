import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
from unidecode import unidecode

def get_query_url(i):
	return 'http://www.reuters.com/news/archive/politicsNews?view=page&page=%d&pageSize=10' %(i)

def get_filename(i):
	return '../articles/reuters/articles_page_%d.csv' %(i)

base_url = 'http://reuters.com'

for i in range(1, 501):
	query_url = get_query_url(i)
	html = requests.get(query_url).content
	soup = bs(html, 'lxml')

	articles_header = ['Link', 'Title', 'Text']
	articles = []

	stories = soup.select('h3.story-title')
	for story in stories:
		atag = story.find('a')
		title = atag.get_text()
		link = base_url + atag['href']

		article = [link, title]

		article_html = requests.get(link).content
		article_soup = bs(article_html, 'lxml')
		
		text = unidecode(article_soup.select('#article-text')[0].get_text()).replace(r'(\\n|\\t|\\)', '')
		article.append(text)
		articles.append(article)

	filename = get_filename(i)
	df = pd.DataFrame(articles, columns=articles_header)
	df.to_csv(filename, encoding='utf-8', sep='\t')

	print 'iteration %d complete' %(i)



