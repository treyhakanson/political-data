import pandas as pd
import numpy as np

txt_file = '../text/slate_data.txt'

for i in range(1, 101):
	filename = '../articles/slate/articles_page_%d.csv' %(i)
	data = pd.read_csv(filename, sep='\t')
	all_text = data['Text']
	all_text.to_csv(txt_file, header=None, index=None, sep=' ', mode='a')

