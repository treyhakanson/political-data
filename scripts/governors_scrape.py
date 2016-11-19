import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

base_url = 'https://en.wikipedia.org'
query_url = 'https://en.wikipedia.org/wiki/List_of_current_United_States_governors'
html = requests.get(query_url).content
soup = bs(html, 'lxml')

governors_table = soup.select('table')[1]
governors_rows = governors_table.find_all('tr')
governors_rows.pop(0)

header = ['Link']
for col in governors_rows.pop(0).find_all('th'):
	if col.get_text() in 'Image':
		continue
	header.append(col.get_text())

governors_data = []

for governor in governors_rows:
	cols = governor.find_all('td')
	cols.pop(3)
	cols.pop(1)
	governor_data = [base_url + cols[1].select('span > span > a')[0]['href']]
	for (i, col) in enumerate(cols):
		if i is 1:
			governor_data.append(col.select('span > span')[0].get_text())
		else:
			governor_data.append(col.get_text())
	governors_data.append(governor_data)

filename = '../governors/governors_data.csv'
df = pd.DataFrame(governors_data, columns=header)
df.to_csv(filename, encoding='utf-8', sep='\t')