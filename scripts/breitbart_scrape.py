import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
from unidecode import unidecode

def get_query_url(i):
	return 'http://www.breitbart.com/big-government/page/%d/' %(i)

def get_filename(i):
	return '../articles/breitbart/articles_page_%d.csv' %(i)

for i in range(2, 100):
	query_url = get_query_url(i)
	html = requests.get(query_url).content
	soup = bs(html, 'lxml')

	articles_header = ['Link', 'Title', 'Text']
	articles = []

	stories = soup.select('h2.title > a')
	for story in stories:
		title = story.get_text()
		link = story['href']

		article = [link, title]

		article_html = requests.get(link).content
		article_soup = bs(article_html, 'lxml')
		
		text = ''
		for chunk in article_soup.select('.entry-content')[0].select('h1, h2, h3, h4, p, blockquote, span'):
			text += unidecode(chunk.get_text()).replace(r'(\\n|\\t|\\)', '')

		article.append(text)
		articles.append(article)

	filename = get_filename(i)
	df = pd.DataFrame(articles, columns=articles_header)
	df.to_csv(filename, encoding='utf-8', sep='\t')

	print 'iteration %d complete' %(i)

















