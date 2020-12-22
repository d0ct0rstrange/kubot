#HIGHLY DANGEROUS FUNCTIONS!
#USE WITH CAUTION
import db

#Function to create table
def create_table(tablename,columns,types):
    conn=db.init_conn()
    res=db.create_table(conn,tablename,columns,types)
    return res

#Function to read the first page of results if results table is empty
#A.K.A Init_results
