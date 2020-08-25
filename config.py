import sqlite3
database = "darazkb.db"

def connect():
	conn = sqlite3.connect(database)
	return conn
