# Building-a-knowledge-base

This demo of knowledge base and search api is built using Daraz help questions data. The search results are based on document similarity using cosine similarity between the search parameter and the questions present in the knowledgebase.
To learn more about cosine similarity, please [click here](https://en.wikipedia.org/wiki/Cosine_similarity#:~:text=Cosine%20similarity%20is%20a%20measure,to%20both%20have%20length%201.)

The knowledgebase is saved in a sqlite database with 4 fields (title, categories, answers, tag_filtered).


Follow these steps:

1) First clone the repository
#### 2) If you want to try out rebuilding the entire knowledgebase, remove the darazkb.db database file
3) Run the following to install required libraries
  ```
  pip install -r requirements.txt
  ```
4) Run 
  ```
  python basebuild.py
  ```
 5) Once the knowledgebase is built run the following command to fireup the API
  ```
  python search.py
  ```
  
The knowledgebase is represented as a form of table and can be exlored from the home page. Here is a snapshot of how it looks like

![image](https://drive.google.com/uc?export=view&id=1UTeQiVGKxoiHSPghNpXIGt-3sNMhhQ_-)

It is build by scraping the website for questions, answers and categories using requests and BeautifulSoup library. The filtered tags are extracted after removing stopwords and lemmatizing each questions text using WordNetLemmatizer from NLTK library.

Here is a snapshot of API operation (GET method) for relevant question and answers on the basis of document similarity in Postman.
![image](https://drive.google.com/uc?export=view&id=1QsdRdhUOX6KqWcgwdtI9tqnKIbgUnS4F)
