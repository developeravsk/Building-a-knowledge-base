from bs4 import BeautifulSoup
import requests
import csv, json
import pandas as pandas
import string
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import pos_tag
import sqlite3
from config import connect
import pandas as pd

def getCategory():
	print('Extracting category')
	source = requests.get("https://helpcenter.daraz.com.np/page/home/config/category?pageId=3&ids=1000001250,1000001261,1000001254,1000001266,1000001270,1000001272,1000001259,1000001275").text
	# Saving category name and id to a dataframe
	df = json.loads(source)
	d=df['data']
	df_category=pd.DataFrame(d.items(), columns=['id', 'Category'])
	return df_category,d

def getQuestions(df_category,d):
	print('Retrieving questions')
	categoryId=df_category['id'].tolist()
	df_questions= pd.DataFrame(columns=['title','categoryId','id','category'])
	for x in range(len(categoryId)):
		source1 = requests.get('https://helpcenter.daraz.com.np/knowledge/queryKnowledgeByCategory?pageId=13&categoryId='+categoryId[x]+'&currPage=1&pageSize=20&language=en&fbclid=IwAR17OTmlp8jJ8i3W7do2ITEian_xBK8Lj6LkU6lXtxJy5-dg7PzJQFtqABw').text
		df = json.loads(source1)
		questions=df['data']
		for i in questions:
			df_questions = df_questions.append({"title":i['title'], 
                    "categoryId":i['categoryId'],
                       "id":i['id'],
                        'category':d.get(categoryId[x])},ignore_index = True)
	return df_questions

def getAnswer(df_questions):
	print('Retrieving answers. This might take some time')
	answerid=df_questions['id'].tolist()
	categorylist=df_questions['category'].tolist()
	df_answers= pd.DataFrame(columns=['title','content','categoryId','id'])
	for x in range(len(answerid)):
		source1 = requests.get('https://helpcenter.daraz.com.np/knowledge/queryKnowledge?pageId=13&knowledgeId='+str(answerid[x])+'&fbclid=IwAR10h1J2d7E1Gc3leCk6oINozwont9a0vWAFZyXuYWjAFrx4qy4WCH5r3TM').text
		df = json.loads(source1)
		answers=df['data']
		df_answers = df_answers.append({"title":answers['title'], "content":answers['content'],"categoryId":answers['categoryId'],"id":answers['id']},ignore_index = True)
	df_answers['category']=categorylist
	content=df_answers['content'].tolist()
	edited_content=[]
	for i in range(len(content)):
		soup = BeautifulSoup(content[i],'lxml')
		one_content=[]
		for p_tag in soup.find_all('p'):
			one_content.append(p_tag.text)
		edited_content.append(one_content)
	df_answers['actual_answers']=edited_content
	df_answers['answers'] = [','.join(map(str, l)) for l in df_answers['actual_answers']]
	df_answers=df_answers.drop(['content','categoryId','id','actual_answers'],axis=1)
	return df_answers

def addTags(df_answers):
	print('Building knowledgebase')
	stopwords_list = stopwords.words('english')
	lemmatizer = WordNetLemmatizer()
	all_tags=[]
	for i in range(len(nontok)):
		words = word_tokenize(nontok[i])
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
		all_tags.append(lemmas)
	df_answers['tags']=all_tags
	df_answers['tags_filtered'] = [','.join(map(str, l)) for l in df_answers['tags']]
	df_answers=df_answers.drop(['tags'],axis=1)
	return df_answers

def saveDB(df_answers):
	print('Saving database')
	c=connect().cursor()
	c.execute('CREATE TABLE KB (title text, Category text, answers text, tags_filtered text)')
	connect().commit()
	df_answers.to_sql('KB', connect(), if_exists='replace', index = False)
	return

def execute():
	a,x=getCategory()
	b=getQuestions(a,x)
	c=getAnswer(b)
	saveDB(c)
	print('Knowledge base built')