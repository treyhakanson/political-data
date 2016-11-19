import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

base_url = 'https://en.wikipedia.org'
query_url = 'https://en.wikipedia.org/wiki/Current_members_of_the_United_States_House_of_Representatives'
html = requests.get(query_url).content
soup = bs(html, 'lxml')

house_table = soup.select('table')[6]
house_rows = house_table.find_all('tr')

header = ['Link']
for col in house_rows.pop(0).find_all('th'):
	header.append(col.get_text())

house_data = []

for rep in house_rows:
	cols = rep.find_all('td')
	cols.pop(2)
	rep_data = [base_url + cols[1].select('span > span > a')[0]['href']]
	for (i, col) in enumerate(cols):
		if i is 1:
			rep_data.append(col.select('span > span')[0].get_text())
		else:
			rep_data.append(col.get_text())
	house_data.append(rep_data)

filename = '../house/house_data.csv'
df = pd.DataFrame(house_data, columns=header)
df.to_csv(filename, encoding='utf-8', sep='\t')