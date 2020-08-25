# Building-a-knwoledge-base

This demo of knowledge base and search api is built using Daraz help questions data. The search results are based on document similarity using cosine similarity between the search parameter and the questions present in the knowledgebase.
To learn more about cosine similarity, please [click here](https://en.wikipedia.org/wiki/Cosine_similarity#:~:text=Cosine%20similarity%20is%20a%20measure,to%20both%20have%20length%201.)


Follow these steps:

1) First clone the repository
2) If you want to try our rebuilding the entire knowledgebase, remove the darazkb.db database file
3) Run the following to install required libraries
  ```
  pip install -r requirements.txt
  ```
  or
  ```
  pip3 install -r requirements.txt
  ```
4) Run 
  ```
  python basebuild.py
  ```
  or
  
  ```
  python3 basebuild.py
  ```
5) Once the knowledgebase is built run the following command to fireup the API
  ```
  python search.py
  ```
  or
  ```
  python3 search.py
  ```
  
