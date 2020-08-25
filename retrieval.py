import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
from config import connect
import numpy as np
import json


def retrieveDF():
	c=connect()
	df = pd.read_sql("select * from KB", con=c)
	c.close()
	return df

stopwords_list = stopwords.words('english')
lemmatizer = WordNetLemmatizer()

def my_tokenizer(doc):
	words = word_tokenize(doc)
	pos_tags = pos_tag(words)
	non_stopwords = [w for w in pos_tags if not w[0].lower() in stopwords_list]
	non_punctuation = [w for w in non_stopwords if not w[0] in string.punctuation]
	lemmas = []
	for w in non_punctuation:
		if w[1].startswith('J'):
			pos = wordnet.ADJ
		elif w[1].startswith('V'):
			pos = wordnet.VERB
		elif w[1].startswith('N'):
			pos = wordnet.NOUN
		elif w[1].startswith('R'):
			pos = wordnet.ADV
		else:
			pos = wordnet.NOUN
		lemmas.append(lemmatizer.lemmatize(w[0], pos))
	return lemmas

def vectorize(df):
	tfidf_vectorizer = TfidfVectorizer(tokenizer=my_tokenizer)
	tfidf_matrix = tfidf_vectorizer.fit_transform(tuple(df['title']))
	return tfidf_vectorizer, tfidf_matrix


def processquestion(question, tfidf_vectorizer,tfidf_matrix,df):
	query_vect=tfidf_vectorizer.transform([question])
	similarity = cosine_similarity(query_vect, tfidf_matrix)
	result = similarity.flatten()
	idx=result.argsort()[-5:][::-1]
	df_results= pd.DataFrame(columns=['questions','answers','similarity'])
	titles=[]
	answers=[]
	similarities=[]
	for i in range(len(idx)):
		if(similarity[0,idx[i]]!=0):
			titles.append(df.iloc[idx[i]]['title'])
			similarities.append(similarity[0, idx[i]])
			answers.append(df.iloc[idx[i]]['answers'])
	df_results['questions']=titles
	df_results['answers']=answers
	df_results['similarity']=similarities
	result=df_results.to_json(orient="records")
	return result

def searchData(question):	
	df=retrieveDF()
	vector,matrix=vectorize(df)
	result=processquestion(question,vector, matrix,df)
	return result