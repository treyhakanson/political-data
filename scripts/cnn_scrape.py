import pandas as pd
import requests
import re
import json
from bs4 import BeautifulSoup as bs
from unidecode import unidecode

def get_filename(i):
	return '../articles/cnn/articles_page_%d.csv' %(i)

def get_cnn_url(suffix):
	return 'http://www.cnn.com%s' % (suffix)

url = 'http://searchapp.cnn.com/search/query.jsp?sort=date&start=%d&section=politics&collection=STORIES'

for page in range(1, 5001):
	print 'Scraping from page ', page
	pageArticles = []
	soup = bs(requests.get(url % (page*10)).content, "html.parser")
	articles = json.loads(soup.find('textarea', {'id': 'jsCode'}).get_text())['results'][0]
	for article in articles:
		articleUrl = get_cnn_url(article['url'])
		articleSoup = bs(requests.get(articleUrl).content, "html.parser")
		pageArticles.append({
			'Title': unidecode(article['title']),
			'Link': articleUrl,
			'Text': ''.join(map(
						lambda block: getattr(block, 'get_text')(), 
						articleSoup.find_all('div', {'class': 'zn-body__paragraph'})))
			})
		
	pd.DataFrame(pageArticles).to_csv(get_filename(page), sep='\t', encoding="utf-8")

			



	
