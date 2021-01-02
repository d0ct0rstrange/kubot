import requests
from bs4 import BeautifulSoup as BS
import re,string
import time, os
from datetime import datetime
import queue
from difflib import SequenceMatcher
import concurrent.futures
from datetime import datetime
import datefinder


import csvwrite,string_clean
import csv
import db

conn=db.init_conn()
#Global variable declarations
#URL to check results
url='https://exams.keralauniversity.ac.in/Login/check8'
r=[]
out=''
recentdate=rd=[]
secondrecentdate=srd=[]
status=query=''
savedcount=0


def checkresultcount(out): 
    conn=db.init_conn()
    with concurrent.futures.ThreadPoolExecutor() as executor1:
        t1=executor1.submit(db.execute_query_thread,"select * from data")
        res=t1.result()
    


    for row in res:
        a=row[0] #recentdate
        b=row[1] #secondrecentdate
        global savedcount
        savedcount=row[3] #count
        
    c=out.find("Published on "+a) #Start region from rd
    d=out.find("Published on "+b) #Stop region from srd
    roi=out[c:d] #Region Of Interest between rd and srd
    count=roi.count("displayList") #displayList is the class name for new result
    return count

def worst_case(out,rd,srd,a,b):
    savedrd=datetime.strptime(a, "%d/%m/%Y").date() 
    savedsrd=datetime.strptime(b, "%d/%m/%Y").date() 
    #Extracting Region of Interest from page. i.e, data between rd and srd
    with concurrent.futures.ThreadPoolExecutor() as executor2:
        #roi=string_clean.extract_roi(out,a,b)
  
        t2=executor2.submit(string_clean.extract_roi, out, a, b)
        roi=t2.result()
        count=roi.count("displayList") #displayList is the class name for new result
    
	#To filter result names, we want <td> with attrs valign=true and width=false
    tag="td"
    attributes={'valign':True,'width':False}

    #output is a dictionary with serial number (1,2,...) and Result name as value

    output=string_clean.clean_results_nourl(roi,tag,attributes)
    for results in output.items():
        tempoutlist=results[1]
        resname=tempoutlist[0]
        resurl=tempoutlist[1]
        print("Result: "+resname+" Download from here:"+resurl)
        #New function to write into database
        #db.dict_to_result_thread(output,rd,srd,resname,resurl)
        with concurrent.futures.ThreadPoolExecutor() as executor2:
           t2=executor2.submit(db.dict_to_result_thread,output,a,b,resname,resurl)
        #res=t2.result()
    #Old function to write into CSV
	# csvwrite.write_results(output,a)

	


	#We've successfully fetched results from saved dates.
    #Now we need to catchup with the current recent date
    localrecentdate=string_clean.normalizeDate(rd)
    localsecondrecentdate=string_clean.normalizeDate(savedrd)
    roi=string_clean.extract_roi(out,localrecentdate,localsecondrecentdate)
    output2=string_clean.clean_results_nourl(roi,tag,attributes)
    for results in output2.items():
        tempoutlist=results[1]
        resname=tempoutlist[0]
        resurl=tempoutlist[1]
        print("Result: "+resname+" Download from here:"+resurl)

    
	#Old function to write into CSV
	# csvwrite.write_results(output2,localrecentdate)

	#New function to write into database
    with concurrent.futures.ThreadPoolExecutor() as executor2:
        t2=executor2.submit(db.dict_to_result_thread,output2,localrecentdate)

def update_results():
    global recentdate, secondrecentdate,rd,srd,out,savedcount
    r = requests.get(url)
    out = r.text
    query="Published on "
    res=re.search(query,out)
    status=res.group(0)
    substring=re.findall(r'>(.*?)<',out)

    #Fetches all dates result (published on)
    alldates = [idx for idx in substring if idx.lower().startswith(query.lower())]

    #Recently published data
    recentdate= alldates[0]
    secondrecentdate=alldates[1]
    #Last Fetch time
    now=datetime.now()
    matches = list(datefinder.find_dates(recentdate))
    if len(matches) > 0:
        # date returned will be a datetime.datetime object. here we are only using the first match.
        rd = matches[0]
        rd=rd.date()
        #print(rd.date())
    else:
        print('No rd dates found')
    matches = list(datefinder.find_dates(secondrecentdate))
    if len(matches) > 0:
        # date returned will be a datetime.datetime object. here we are only using the first match.
        srd = matches[0]
        srd=srd.date()
        #print(srd.date())
    else:
        print('No srd dates found')
	
	#This function is threaded under
	#currcount=checkresultcount(out)
	
    with concurrent.futures.ThreadPoolExecutor() as executor1:
        t1=executor1.submit(checkresultcount,out)
    currcount=t1.result()
    

    #New updates are available, Check which course
    #if((currcount>int(savedcount)) and ()):
       # print("New Results available! Fetched at: "+str(datetime.now().time()))

    #Reading saved details from data.csv to match it with cuurent data 
	#Migrated from csv to database  
    #saveddetails=csvwrite.read_from_csv('data.csv')

	#TODO: Write a db function to fetch and return results as dict from table
    with concurrent.futures.ThreadPoolExecutor() as executor4:
        sql="select * from data"
        t4=executor4.submit(db.execute_query_thread,sql)
    saveddetails=t4.result()

    for row2 in saveddetails:
        savedrd=row2[0]
        savedsrd=row2[1]
        savedcount=int(row2[3])
    
    #Converting to same date format as rd
    savedrd = datetime.strptime(savedrd, "%d/%m/%Y").date() 
    savedsrd = datetime.strptime(savedsrd, "%d/%m/%Y").date() 

    #Results handling
    
    #Reverting datetime object to KU site's slash format
	#recentdate in KU Format
    #a=string_clean.normalizeDate(savedrd) 

    with concurrent.futures.ThreadPoolExecutor() as executor2:
        t2=executor2.submit(string_clean.normalizeDate,savedrd)
    a=t2.result()



	#secondrecentdate in KU Format
    #b=string_clean.normalizeDate(savedsrd)
    with concurrent.futures.ThreadPoolExecutor() as executor3:
        t3=executor3.submit(string_clean.normalizeDate,savedsrd)
    b=t3.result() 
    
    #worst_case(out,rd,srd,a,b)
    #Scenario #1. Worst case scenario. Results of more than one day published, including results between
    #savedrd and savedsrd.
    #In this case, actual recent date will be far higher than savedrd
    #There is also discrepencies between actual second rd and savedsrd
    #So, first save the results between savedrd and savedsrd, then
    # update savedrd=currrd, savedsrd=currsrd and fetch the new results.
    #TODO:uncomment any following line in production!
    if((savedrd<rd) and (currcount>savedcount)): 
        worst_case(out,rd,srd,a,b)
    
    #Scenario#2 if results are published in the same day (Best case)
    elif((currcount>savedcount) and (savedrd==rd)): 
        #Extracting Region of Interest from page. i.e, data between rd and srd
        roi=string_clean.extract_roi(out,a,b)
        
        count=roi.count("displayList") #displayList is the class name for new result
        
        #To filter result names, we want <td> with attrs valign=true and width=false
        tag="td"
        attributes={'valign':True,'width':False}

        #output is a dictionary with serial number (1,2,...) and Result name as value
        output=string_clean.clean_results_nourl(roi,tag,attributes)
        for results in output.items():
            tempoutlist=results[1]
            resname=tempoutlist[0]
            resurl=tempoutlist[1]
            print("Result: "+resname+" Download from here:"+resurl)
        #csvwrite.write_results(output,a)
        with concurrent.futures.ThreadPoolExecutor() as executor5:
            t5=executor5.submit(db.dict_to_result_thread,output,a)


    #Scenario#3. If result counts are the same, but results got published on different dates
    elif((currcount==savedcount)and (savedrd!=rd)): 
        worst_case(out,rd,srd,a,b)
    elif((savedrd==rd)and (savedcount==currcount)):
        print("No Updates! Last Fetch time: "+str(datetime.now()))
    else:
        #There has been some issue with count column data in table data
        #The following steps will reset the count column in table data
        print("Unspecified Error! :( Time: "+str(datetime.now()))
        if currcount<savedcount:
            sql="UPDATE data SET count='"+str(currcount)+"'"
            db.execute_query(conn,sql)
    
    
    #Writing dates to data. csv
    try:
        csvwrite.write_to_csv(rd,srd,currcount)
        with concurrent.futures.ThreadPoolExecutor() as executor6:
            clean_rd=string_clean.normalizeDate(rd)
            clean_srd=string_clean.normalizeDate(srd)
            vals=clean_rd+","+clean_srd+","+str(currcount)+","+str(datetime.now())
            arg=['data','recentdate,secondrecentdate,count',vals]
            vals_list=string_clean.string_to_list(vals,",")
            #db.insert_into_table_thread("data",["recentdate","secondrecentdate","count"],vals_list)
            #t6=executor6.submit(db.insert_into_table_thread,"data",["recentdate","secondrecentdate","count"],vals_list)
            #db.update_table_no_where_thread("data",["recentdate","secondrecentdate","count"],vals_list)
            t6=executor6.submit(db.update_table_no_where_thread,"data",["recentdate","secondrecentdate","count","lastfetchtime"],vals_list)

        print("Info successfully wrote to data table!")
    except Exception as e:
       print("Couldn't write info to data table!")
       print(f"The error '{e}' occurred") 

update_results()

