import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
from unidecode import unidecode

def get_filename(i):
	return '../articles/slate/articles_page_%d.csv' %(i)

url = 'http://www.slate.com/articles/news_and_politics/politics.%d.html'
articleRegex = re.compile('(http://www.slate.com/articles/).*20[0-9]{1}[0-9]{1}.*')
hrefs = set()

for page in range(25, 501):
	print 'Scraping from page ', page
	pageArticles = []
	soup = bs(requests.get(url % (page)).content, "html.parser")
	for href in map(lambda a: a['href'], soup.find_all('a', href=True)):
		if articleRegex.match(href) and href not in hrefs:
			print href
			hrefs.add(href)
			articleSoup = bs(requests.get(href).content, "html.parser")
			textList = []
			i = 1
			while True:
				try:
					textList.append(unidecode(
						articleSoup.select('div.text-%s > p' % (str(i)))[0].get_text())\
						.replace(r'(\\n|\\r|\\t|\\)', '').strip())
					i += 1
				except:
					break
			pageArticles.append({
				'Title': unidecode(articleSoup.select('h1')[0].get_text()),
				'Link': href,
				'Text': ' '.join(textList)})
	pd.DataFrame(pageArticles).to_csv(get_filename(page), sep='\t')

			

# stopped last run at page 117, date was 2009/7




	
