import pandas as pd 
import re
import os
import json
import ast

def getTopics():
	global topics
	try:
		return topics
	except:
		topics = set([
			'abortion', 
			'creation', 
			'gay', 
			# 'gay rights', 
			'guns', 
			'god', 
			'healthcare'])
		return topics

def findTopics(wordset):
	return set.intersection(wordset, globals().get('topics', getTopics()))

def getTerms():
	global terms, termsDict
	try:
		return terms
	except:
		print 'failed'
	
		termPanda = pd.read_csv('./unique_terms.csv', sep='\t')
		terms = set(termPanda.Last)
		termsDict = termPanda.set_index('Last').to_dict()
		return terms

def findTerms(wordset):
	return set.intersection(wordset, globals().get('terms', getTerms()))

def getTermTuple(terms):
	global termsDict
	return list(map(lambda term: (term, termsDict[term]), terms))

def analyzeChunk(chunk):
	wordset = set(map(
		lambda word: word.lower(),
		chunk))
	terms = findTerms(wordset)
	topics = findTopics(wordset)
	if result:
		return (chunk, getTermTuple(terms))
	return None

def getArticles():
	rootDir = '../articles/slate/'
	csvRegex = re.compile('.+[0-9]\.csv')
	df2 = pd.DataFrame()
	for dirName, subdirList, fileList in os.walk(rootDir):
		print dirName
		for fname in fileList:
			if csvRegex.match(fname):
				print fname
				fullname = dirName+fname
				df = pd.read_csv(fullname, sep='\t')
				df['Terms'] = None
				df['Topics'] = None
				for index, row in df.iterrows():
					try:
						wordlist = row['Text'].replace('.', ' ').split()
						wordset = set(wordlist)
						lowerWordset = set(map(lambda word: word.lower(), wordlist))

						df['Terms'][index] = list(findTerms(wordset))
						df['Topics'][index] = list(findTopics(lowerWordset))
					except:
						print 'Fuck that article... ', index
				df.to_csv(fullname.replace('.csv', '_parsed.csv'), sep='\t')


def eval_bias(link):
	article = evaluateArticleText(link)
	df1 = preprocess(article)


def getTrainingData():
	pass


getArticles()

# termPanda = pd.read_csv('./terms.csv')
# termPanda['Last'] = termPanda.apply(
# 	lambda row: row['Name'].split()[-1], axis=1)
# termPanda = termPanda.drop_duplicates(subset=['Last'],keep=False)
# termPanda.to_csv('./unique_terms.csv', sep='\t')
# table = pd.read_csv('../articles/breitbart/articles_page_10_parsed.csv', sep='\t')
# for index, row in table.iterrows():
# 	print ast.literal_eval(row['Terms'])
























