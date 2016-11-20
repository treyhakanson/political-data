import pandas as pd 
import numpy as np
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
		path = '/'.join((os.path.dirname(os.path.realpath(__file__)), 'unique_terms.csv'))
		termPanda = pd.read_csv(path, sep='\t')
		terms = set(termPanda.Last)
		termsDict = termPanda.set_index('Last').to_dict()['Party']
		return termsDict

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

def getData(publication):
	rootDir = '/'.join((os.path.dirname(os.path.realpath(__file__)), publication))
	termsDict = getTerms()
	csvRegex = re.compile('.+parsed\.csv')
	df2 = pd.DataFrame()
	for dirName, subdirList, fileList in os.walk(rootDir):
		for fname in fileList:
			if csvRegex.match(fname):
				fullname = '/'.join((dirName,fname))
				df = pd.read_csv(fullname, sep='\t')
				for index, row in df.dropna(subset=['Terms', 'Topics']).iterrows():
					text = row['Text']


					article = []
					for sentence in re.split(r' *[\.\?!][\'"\)\]]* *', row['Text']):
						lowerWordSet = set(map(lambda word: word.lower(), sentence.split()))
						wordSet = set(sentence.split())

						topics = findTopics(lowerWordSet)
						terms = getTermTuple(findTerms(wordSet))
						if terms:
							# yield (sentence, terms)
							article.append((sentence, terms))
					if article:
						yield article


					# title = row['Title']
					# terms = getTermTuple(ast.literal_eval(row['Terms']))
					# # topics = ast.literal_eval(row['Topics'])
					# yield (text, terms,title)
					


# generator = getData('slate')
# while True:
# 	data = next(generator)
# 	print data
# 	break

















