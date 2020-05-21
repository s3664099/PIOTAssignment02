"""
.. module:: sqlite_setup
    
"""
import sys
sys.path.append('../')

import sqlite3
import login

DB_NAME = "reception.db"

def setup():
    """
    Setup sqlite
    
    """
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()

	try:
		cur.execute("DROP TABLE User")
	except:
		print("Not working")

	cur.execute("CREATE TABLE User (username text, password text, first_name text, last_name text, email text)")
	cur.execute("INSERT INTO User VALUES('Geralt','"+login.hash_password('Witcher')+"','Geralt','of Rivia','geralt@rivia.net')")
	cur.execute("INSERT INTO User VALUES('AdamtheAdamman','"+login.hash_password('50firstdates')+"','Adam','Sandler','asandler@happymadison.com')")
	conn.commit()

setup()


