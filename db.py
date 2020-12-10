import sqlite3
from sqlite3 import Error
import string_clean

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


#Use the following format to dynamically add column names and values
#cursor.execute("INSERT INTO {tn} ({f1}, {f2}) VALUES (?, ?)".format(tn='testable', f1='foo', f1='bar'), ('test', 'test2',))

def add_column(connection,tablename,columnname,columntype):
    cursor = connection.cursor()
    try:
        
        sanitized_tablename=string_clean.strip_string(tablename)
        sanitized_columnname=tablename=string_clean.strip_string(columnname)
        sanitized_columntype=tablename=string_clean.strip_string(columntype)

        cursor.execute("ALTER TABLE {tn} ADD COLUMN {f1} {f2}".format(tn=sanitized_tablename, f1=sanitized_columnname, f2=sanitized_columntype))

        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")       



def insert_into_table(connection, tablename,columns,values):
    cursor = connection.cursor()
    try:
        
        #Sanitize strings
        sanitized_tablename=string_clean.strip_string(tablename)
        sanitized_columns=string_clean.strip_special_from_list(columns)
        sanitized_values=string_clean.strip_special_from_list(values)

        #Converting list to sqlite friendly format
        cols = ','.join(sanitized_columns)
        vals = ','.join(sanitized_values)
        #number_of_values = ','.join(['?'] * len(sanitized_values))

        sql='INSERT INTO %s (%s) values(%s)' % (sanitized_tablename,cols,vals)
        cursor.execute(sql)
        connection.commit()
        
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")  


conn=create_connection()
cols=["b./;'[]a","ma./;'""'; ","id"]
vals=["english","malayalam"]
insert_into_table(conn,"courses./;'[]",cols,vals)