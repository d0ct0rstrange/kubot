import requests
from bs4 import BeautifulSoup as BS
import re,string
import csvwrite,string_clean
import time, os
from datetime import datetime
import queue
import csv
import db

def course_keywords(filename='courses.csv'):
	conn=db.init_conn()
	course_dict={}
	#Reading from course list
	mydict=csvwrite.read_from_csv_clean(filename)
	for i in mydict.items():
		#Extracting course names
		cname=i[1]
		#print(cname) 

		#splitting the words
		cname_split=cname.split()
		#print(cname_split) 
		course_dict[cname_split[0]]=cname_split[1:]

		#first name is the core course (ba, ma, bcom etc)
		#We need to extract the core course and save their subsidiaries under it.
		#save the first name as key in dictionary and everything else as value
		#alter_table_courses="ALTER TABLE courses ADD COLUMN "+cname_split[0]+" TEXT;"
		


		#We are going to create 
		course_name="bba"
		course_type="text"
		course_id="123"
		id_type="text"
		sqlconnections.create_table(conn,)

course_keywords()

