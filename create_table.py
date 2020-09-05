import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text UNIQUE, password text)"
cursor.execute(create_table)
connection.commit()
# select_query = "SELECT * FROM users"
# result = cursor.execute(select_query)
# for user in result:


connection.close()