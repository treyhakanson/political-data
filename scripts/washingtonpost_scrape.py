import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
from unidecode import unidecode

def get_query_url(i):
	return 'https://sitesearchapp.washingtonpost.com/sitesearch-api/search.json?&datefilter=displaydatetime:%5B*+TO+NOW%%2FDAY%2B1DAY%5D&facets.fields=%7B!ex%3Dinclude%7Dcontenttype,%7B!ex%3Dinclude%7Dname&query=politics&sort=&startat=' + str(i*10)

def get_filename(i):
	return '../articles/washington_post/articles_page_%d.csv' %(i)

articles_header = ['Link', 'Title', 'Text']

for i in range(0, 1001):
	json = requests.get(get_query_url(i)).json()
	stories = json['results']['documents']

	articles = []

	for story in stories:
		try:
			title = story['headline']
			link = story['contenturl']

			if story['contenttype'] in 'video':
				print 'skipping: %s' %(link)
				continue
			else:
				print 'SCRAPING: %s' %(link)

			article = [link, title]

			article_html = requests.get(link).content
			article_soup = bs(article_html, 'lxml')

			# text = unidecode(article_soup.select('article > div > div > p')[0].get_text()).replace(r'(\\n|\\t|\\)', '')

			text = unidecode(article_soup.select('article')[0].get_text()).replace(r'(\\n|\\t|\\)', '')

			article.append(text)
			articles.append(article)
		except:
			print '\nFAILED\n'

	filename = get_filename(i)
	df = pd.DataFrame(articles, columns=articles_header)
	df.to_csv(filename, encoding='utf-8', sep='\t')

	print 'iteration %d complete' %(i)
	# exit()


















