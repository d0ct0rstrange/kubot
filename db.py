import sqlite3
from sqlite3 import Error
import string_clean

def init_conn(path='kubot.sqlite'):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query,silent="0"):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        if silent==1:
            print("Query executed successfully")
        return cursor.fetchall()
    except Error as e:
        if silent==1:
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
        sanitized_columns=string_clean.strip_special_from_list_except_space(columns)

        median_values=string_clean.strip_special_from_list_except_space(values)

        sanitized_values=string_clean.enclose_elements_in_list_with_symbol(median_values,'"')

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

def create_table(connection, tablename,columns="courseid,course", types="INT PRIMARY KEY NOT NULL,TEXT NOT NULL"):
    cursor = connection.cursor()
    try:
        
        #Sanitize strings
        sanitized_tablename=string_clean.strip_special_except_space_and_input(tablename,",")
        sanitized_columns=string_clean.strip_special_except_space_and_input(columns,",")
        sanitized_types=string_clean.strip_special_except_space_and_input(types,",")

        #Converting list to sqlite friendly format
        #cols =string_clean.string_to_list(,",")
        list_columns=string_clean.string_to_list(sanitized_columns,",")
        list_types=string_clean.string_to_list(sanitized_types,",")
        colsandvals=string_clean.merge_list_custom_seperator(list_columns,list_types)
       

        sql='CREATE TABLE IF NOT EXISTS %s (%s)' % (sanitized_tablename,colsandvals)
        cursor.execute(sql)
        connection.commit()

        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")  





# conn=create_connection()
# cols=["b./;'[]a","ma./;'""'; ","id"""]
# vals=["englis,./'h","malayalam"";.,//"]
# types=["text","text"]
# create_table(conn,"abcde")
#insert_into_table(conn,"courses./;'[]",cols,vals)