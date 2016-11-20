import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
from unidecode import unidecode

def get_query_url(i):
	return 'http://api.foxnews.com/v1/content/search?q=politics&fields=date,description,title,url,image,type,taxonomy&section.path=fnc&start=%d&cb=20161119183' %(i*10)

def get_filename(i):
	return '../articles/fox/articles_page_%d.csv' %(i)

articles_header = ['Link', 'Title', 'Text']

for i in range(202, 1001):
	json = requests.get(get_query_url(i)).json()
	stories = json['response']['docs']

	articles = []

	for story in stories:
		title = story['title']
		link = story['url'][0]

		if story['type'] in 'video':
			print 'skipping: %s' %(link)
			continue
		else:
			print 'SCRAPING: %s' %(link)

		article = [link, title]

		article_html = requests.get(link).content
		article_soup = bs(article_html, 'lxml')

		# text = unidecode(article_soup.select('article > div > div > p')[0].get_text()).replace(r'(\\n|\\t|\\)', '')

		text = ''
		for chunk in article_soup.select('article > div > div > p'):
			text += unidecode(chunk.get_text()).replace(r'(\\n|\\t|\\)', '')

		article.append(text)
		articles.append(article)

	filename = get_filename(i)
	df = pd.DataFrame(articles, columns=articles_header)
	df.to_csv(filename, encoding='utf-8', sep='\t')

	print 'iteration %d complete' %(i)
	# exit()


















