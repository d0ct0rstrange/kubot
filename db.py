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

#Function to execute a query
def execute_query(connection,query,silent="0"):
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


#Function to execute a query, but inside a thread
def execute_query_thread(query,silent="0"):
    connection=init_conn()
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



def insert_into_table(connection, tablename,columns,values,silent=0):
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

        if silent==0:
            print("Query executed successfully")
    except Error as e:
        if silent==0:
            print(f"The error '{e}' occurred")  


#Insert into table, but for thread
def insert_into_table_thread(tablename,columns,values,silent=0):
    connection=init_conn()
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

        if silent==0:
            print("Query executed successfully")
    except Error as e:
        if silent==0:
            print(f"The error '{e}' occurred")  


# Insert into table, but for thread and except some characters from values
def insert_into_table_strip_val_except_space_and_input_thread(tablename,columns,values,exception='.',silent=0):
    connection=init_conn()
    cursor = connection.cursor()
    try:
        
        #Sanitize strings
        sanitized_tablename=string_clean.strip_string(tablename)
        sanitized_columns=string_clean.strip_special_from_list_except_space(columns)

        median_values=string_clean.strip_special_from_list_except_space_and_input(values,exception)

        sanitized_values=string_clean.enclose_elements_in_list_with_symbol(median_values,'"')

        #Converting list to sqlite friendly format
        cols = ','.join(sanitized_columns)
        vals = ','.join(sanitized_values)
        #number_of_values = ','.join(['?'] * len(sanitized_values))

        
        sql='INSERT INTO %s (%s) values(%s)' % (sanitized_tablename,cols,vals)
        cursor.execute(sql)
        connection.commit()

        if silent==0:
            print("Query executed successfully")
    except Error as e:
        if silent==0:
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

#Function to save dictionary as table
def dict_to_table(conn,dictionary,recentdate,tablename,columns,values,silent=0):
    #Dev block. Remove on production
    conn=init_conn()
    #tablename="results"
    #columns="id,course,url,date"
    #End of Dev block

    for key, value in dictionary.items():
        #rid=id in results table
        rid=str(key)

        #values is a list of result name and url
        #value[0]=res_name, value[1]=res_url

        #res_name=value[0]
        #res_url=value[1]

        vals=rid+","+",".join(value)
        insert_into_table(conn,tablename,columns,values,silent)




#Function to save dictionary as table into results, but for threading
def dict_to_result_thread(dictionary,recentdate,secondrecentdate,resname,resurltablename="results",silent=0):
    
    conn=init_conn()
    
    recentdate = string_clean.normalizeDate(recentdate)
    secondrecentdate = string_clean.normalizeDate(secondrecentdate)

    #Dev block. Remove on production
    tablename="results"
    columns=["course","url","date"]
    #End of Dev block

    for key, value in dictionary.items():
        #rid=id in results table
        rid=str(key)

        #values is a list of result name and url
        #value[0]=res_name, value[1]=res_url

        #res_name=value[0]
        #res_url=value[1]

        for results in dictionary.items():
            tempoutlist=results[1]
            resname=tempoutlist[0]
            resurl=tempoutlist[1]
            print("Result: "+resname+" Download from here:"+resurl)

        #vals=rid+","+",".join(value)

        vals=[]
        #vals.append(rid)
        vals.append(resname)
        vals.append(resurl)
        vals.append(recentdate)
        insert_into_table_strip_val_except_space_and_input_thread(tablename,columns,vals,silent)

#TODO: Unfinished Function      
#Function to fetch information from data table as dictionary
def table_to_dictionary(tablename,columns="*",where=''):
    conn=init_conn()
    sql="select "+columns+" from "+tablename+" "+where
    res=execute_query(conn,sql)
    return res
    
#Function to update a table
def update_table(connection,tablename,columns,values,exception='.',silent=1):
    cursor = connection.cursor()
    try:
        #Placeholder wheres. Ignore for now
        where="1"
        where_value="1"

        #Sanitize strings
        sanitized_tablename=string_clean.strip_string(tablename)
        sanitized_columns=string_clean.strip_special_from_list_except_space(columns)

        median_values=string_clean.strip_special_from_list_except_space_and_input(values,exception)

        sanitized_values=string_clean.enclose_elements_in_list_with_symbol(median_values,'"')

        sanitized_where=string_clean.strip_string(where)
        sanitized_where_value=string_clean.strip_string(where_value)

        #Converting list to sqlite friendly format
        cols = ','.join(sanitized_columns)
        vals = ','.join(sanitized_values)
        #number_of_values = ','.join(['?'] * len(sanitized_values))
        if(len(sanitized_values)>1):
            for i,j in zip(sanitized_columns,sanitized_values):
                sql='UPDATE %s SET %s=%s' % (sanitized_tablename,i,j)
                cursor.execute(sql)
                connection.commit()
                if silent==0:
                    print("Query executed successfully")
        elif(len(sanitized_values)==1):
            sql='UPDATE %s SET %s=%s' % (sanitized_tablename,cols,vals)
            cursor.execute(sql)
            connection.commit()
            if silent==0:
                print("Query executed successfully")
    except Error as e:
        if silent==0:
            print(f"The error '{e}' occurred")
        


#Function to update a table without where clause, but in thread
def update_table_no_where_thread(tablename,columns,values,silent=1):
    connection=init_conn()
    cursor = connection.cursor()
    try:
        
        #Sanitize strings
        sanitized_tablename=string_clean.strip_string(tablename)
        sanitized_columns=string_clean.strip_special_from_list_except_space(columns)

        #median_values=string_clean.strip_special_from_list_except_space(values)

        #Not stripping because it messes up date. Will fix this later
        sanitized_values=values

        #sanitized_where=string_clean.strip_string(where)
        #sanitized_where_value=string_clean.strip_string(where_value)

        #Converting list to sqlite friendly format
        cols = ','.join(sanitized_columns)
        vals = ','.join(sanitized_values)
        #number_of_values = ','.join(['?'] * len(sanitized_values))

        cols_list=string_clean.string_to_list(cols,",")
        vals_list=string_clean.string_to_list(vals,",")
        for i,j in zip(cols_list,vals_list):
            sql="UPDATE %s SET %s='%s'" % (sanitized_tablename,i,j)
            cursor.execute(sql)
            connection.commit()
            if silent==0:
                print("Query executed successfully")
    except Error as e:
        if silent==0:
            print(f"The error '{e}' occurred")



# conn=create_connection()
# cols=["b./;'[]a","ma./;'""'; ","id"""]
# vals=["englis,./'h","malayalam"";.,//"]
# types=["text","text"]
# create_table(conn,"abcde")
#insert_into_table(conn,"courses./;'[]",cols,vals)