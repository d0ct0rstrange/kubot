import sqlite3
from sqlite3 import Error

def create_connection(path='kubot.sqlite'):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
cname="ma"
#create_users_table = "CREATE TABLE IF NOT EXISTS courses (id SERIAL PRIMARY KEY, "+cname+" TEXT NOT NULL)"
alter_table_courses="ALTER TABLE courses ADD COLUMN "+cname+" TEXT;"
insert_into_courses="""
INSERT INTO
  courses (name, age, gender, nationality)
VALUES
  ('James', 25, 'male', 'USA'),
  ('Leila', 32, 'female', 'France'),
  ('Brigitte', 35, 'female', 'England'),
  ('Mike', 40, 'male', 'Denmark'),
  ('Elizabeth', 21, 'female', 'Canada');
"""
#execute_query(create_connection(),alter_table_courses)