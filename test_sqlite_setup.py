import sqlite3

DB_NAME = "test.db"

def setup():
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()

	try:
		cur.execute("DROP TABLE User")
	except:
		print("Not working")

	cur.execute("CREATE TABLE User (username text, password text, first_name text, last_name text, email text)")
	cur.execute("INSERT INTO User VALUES('Geralt','Witcher','Geralt','of Rivia','geralt@rivia.net')")
	cur.execute("INSERT INTO User VALUES('AdamtheAdamman','50firstdates','Adam','Sandler','asandler@happymadison.com')")
	conn.commit()


