import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

base_url = 'https://en.wikipedia.org'
query_url = 'https://en.wikipedia.org/wiki/List_of_current_United_States_Senators'
html = requests.get(query_url).content
soup = bs(html, 'lxml')

senators_table = soup.select('table:nth-of-type(7)')[0]
senator_rows = senators_table.find_all('tr')

header = ['Link']
for col in senator_rows.pop(0).find_all('th')[1:]:
	header.append(col.get_text())

senate_data = []

for senator in senator_rows:
	cols = senator.find_all('td')
	cols.pop(0)
	senator_data = [base_url + cols[3].select('span > span > a')[0]['href']]
	for col in cols:
		senator_data.append(col.get_text())
	senate_data.append(senator_data)

filename = '../senate/senator_data.csv'
df = pd.DataFrame(senate_data, columns=header)
df.to_csv(filename, encoding='utf-8', sep='\t')