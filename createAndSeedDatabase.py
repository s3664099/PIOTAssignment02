import sqlite3

DB_NAME = "reception.db"

connection = sqlite3.connect(DB_NAME)

with connection:
    #connection.execute("""
     #   create table Users (UserName text not null primary key, FirstName text not null, LastName text not null)
      #  """)

    #connection.execute("""
     #   insert into Users (UserName, FirstName, LastName) values ('mbolger', 'Matthew', 'Bolger')
    #    """)
    #connection.execute("""
     #   insert into Users (UserName, FirstName, LastName) values ('shekhar', 'Shekhar', 'Kalra')
      #  """)
    connection.execute("""
        insert into Users (UserName, FirstName, LastName) values ('Bhavi', 'Bhavi', 'Mehta')
        """)

connection.close()
