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
from dateutil import parser


import csvwrite,string_clean
import csv
import db


#New file to rewrite result scraping functions

#Global variable declarations
#URL to check results
url='https://exams.keralauniversity.ac.in/Login/check8'

r=[]                #Requests object of given URL
out=''              #web elements of given URL
recentdate=[]       #String of recentdate
rd=[]               #Date object of recentdate
secondrecentdate=[] #String of secondrecentdate
srd=[]              #Date object of secondrecentdate
status=query=''
savedcount=0
currcount=0
saved_rd=[]
saved_srd=[]
conv_curr_recentdate=[]      #Global date objects
conv_curr_secondrecentdate=[]

# Function to check the new results count.
# Input webpage(out=r.text), query and unique classname of result
# Function fetches data from table data and returns number of results between
# recentdate and secondrecentdate saved in table. 
 
def checkresultcount(out,query="Published on ",classname="displayList"): 
    conn=db.init_conn()
    global savedcount,saved_rd,saved_srd,rd,srd,recentdate, secondrecentdate #Declaring vars as global
    with concurrent.futures.ThreadPoolExecutor() as executor1:
        t1=executor1.submit(db.execute_query_thread,"select * from data")
        res=t1.result()
    

    # Fetching information from table data
    for row in res:
        a=row[0] #recentdate from data table
        b=row[1] #secondrecentdate from data table
        savedcount=row[3] #count from data table (Saving as global)
        
        saved_rd=string_clean.string_to_date(a)     # Saving recentdate from database to global var
        saved_srd=string_clean.string_to_date(b) # Saving secondrecentdate from database to global var

    #c=out.find("Published on "+a) #Start region from rd
    #d=out.find("Published on "+b) #Stop region from srd

    res=re.search(query,out)
    status=res.group(0)
    substring=re.findall(r'>(.*?)<',out)

    #Fetches all dates the results published from result page. Identified by query. (published on)
    alldates = [idx for idx in substring if idx.lower().startswith(query.lower())]

    #Converting recentdate to date object rd and
    #Converting secondrecentdate to date object srd 
    rd=string_clean.string_to_date(alldates[0])
    srd=string_clean.string_to_date(alldates[1])
    
    #Converting datetime obj to string
    recentdate=string_clean.normalizeDate(rd)
    secondrecentdate=string_clean.normalizeDate(srd)

    # Extract recentdate from webpage (Published on dd-mm-YYYY)
    #rd=parser.parse(recentdate,fuzzy=True,dayfirst=True)

    # Extract secondrecentdate from webpage (Published on dd-mm-YYYY)
    #srd=parser.parse(secondrecentdate,fuzzy=True,dayfirst=True)
    

    # If Current recentdate is same as recentdate in data (savedrecentdate)
    # and savedcount!=0, then there are unfetched results (or issue with database updation)
    # ROI[start]=curr_recentdate and ROI[end]=curr_secondrecentdate  
    if(saved_rd==rd and savedcount!=0):
        # Converting datetime obj to string to lookup on website
        a=string_clean.normalizeDate(rd)
        b=string_clean.normalizeDate(srd)

    # If current_recentdate is not same as savedrecentdate and savedrecentdate!=0,
    # Then there are unfetched results. So, we need to extract results between rd and saved_srd
    # ROI[start]=curr_recentdate and ROI[end]=savedrecentdate  
    elif(saved_rd!=rd and savedcount!=0):
        a=string_clean.normalizeDate(rd)
        b=string_clean.normalizeDate(saved_srd)

    # If current_recentdate is not same as savedrecentdate and savedcount==0,
    # Then there are no unfetched results. So, we can extract data between rd and saved_rd
    elif(saved_rd!=rd and savedcount==0):
        a=string_clean.normalizeDate(rd)
        b=string_clean.normalizeDate(saved_rd)


    # Finding Region Of Interest
    c=out.find(query+a) #Start region from rd
    d=out.find(query+b) #Stop region from srd

    #Failsafe.
    if c>d:
        roi=out[d:c] #Region Of Interest between srd and rd
    elif d>c:
        roi=out[c:d] #Region Of Interest between rd and srd

    #count=roi.count("displayList") #displayList is the class name for new result

    # Counting no of results by counting the result classname (classname is displayList by default)
    count=roi.count(classname) #displayList is the class name for new result
    curr_count=count           # Saving count into global variable

    #saving count into table data
    cols=["recentdate","secondrecentdate","lastfetchtime","count"]
    vals=[]
    vals.append(a)
    vals.append(b)
    vals.append(str(datetime.now()))
    vals.append(str(curr_count))

    with concurrent.futures.ThreadPoolExecutor() as executor11:
        t11=executor11.submit(db.update_table_no_where_thread,"data",cols,vals)
    res=t11.result()

    return count

#OBSOLETE. REDUNDANT TO CHECK_RESULT_COUNT()
#Function to fetch web page and check results count.
# Depends on checkresultcount() function
def fetch_results_count(classname="displayList",query="Published on ",url='https://exams.keralauniversity.ac.in/Login/check8'):
    #1. URL => URL from the results to be fetched
    #          ('https://exams.keralauniversity.ac.in/Login/check8' is the default)
    #2. QUERY => Keyword that denotes the date the
    #    results got published. This is also used to mark the start of results.
    #    Recent date marks the start of the results and Second recent date marks the end of results.
    #    We fetch results one by one iterating between the recent date and second recent date.
    #    ("Published on " is the default)
    #3. CLASSNAME => The class name for new result
    #                ("displayList" is the default)
    #4. Along with theses, there are two additional attributes to uniquely identify a result
    #To filter result names, we want <td> with attrs valign=true and width=false
    #        tag="td"
    #        attributes={'valign':True,'width':False}

    #output is a dictionary with serial number (1,2,...) and Result name as value

    global recentdate, secondrecentdate,rd,srd,out,savedcount,currcount
    
    #Fetching webpage from url
    r = requests.get(url)
    #Saving the web(text) elements to "out" variable
    out = r.text

    #query="Published on "

    #Searching for query in extracted web contents
    res=re.search(query,out)
    status=res.group(0)
    substring=re.findall(r'>(.*?)<',out)

    #Fetches all dates the results published from result page. Identified by query. (published on)
    alldates = [idx for idx in substring if idx.lower().startswith(query.lower())]

    #Recently published data
    recentdate= alldates[0]
    secondrecentdate=alldates[1]

    #Finds current time to update the Last Fetch time
    now=datetime.now()
	
	#This function is threaded under
	#currcount=checkresultcount(out)

    with concurrent.futures.ThreadPoolExecutor() as executor1:
        t1=executor1.submit(checkresultcount,out,query,classname)
    currcount=t1.result()
    
    return currcount




def fetch_results(classname="displayList",query="Published on ",url='https://exams.keralauniversity.ac.in/Login/check8'):
    # We have fetched the new results count using fetch_results_count. Now, we want to fetch the new results
    # To do so, first select recentdate,secondrecentdate from data;
    # This function will only be called when fetch_results_count returns num > 0
    # This function will fetch results between recentdate and secondrecentdates saved in table data

    # So, to fetch results, we need to fetch results between recentdate and secondrecentdate
    # Find ROI between those dates from input "out(r.text)".


    #1. URL => URL from the results to be fetched
    #          ('https://exams.keralauniversity.ac.in/Login/check8' is the default)
    #2. QUERY => Keyword that denotes the date the
    #    results got published. This is also used to mark the start of results.
    #    Recent date marks the start of the results and Second recent date marks the end of results.
    #    We fetch results one by one iterating between the recent date and second recent date.
    #    ("Published on " is the default)
    #3. CLASSNAME => The class name for new result
    #                ("displayList" is the default)
    #4. Along with theses, there are two additional attributes to uniquely identify a result
    #To filter result names, we want <td> with attrs valign=true and width=false
    #        tag="td"
    #        attributes={'valign':True,'width':False}

    #output is a dictionary with serial number (1,2,...) and Result name as value


    global recentdate, secondrecentdate,rd,srd,out,savedcount,currcount
    # Db connection object
    conn=db.init_conn()
    


    #Fetching webpage from url
    r = requests.get(url)
    #Saving the web(text) elements to "out" variable
    out = r.text

    with concurrent.futures.ThreadPoolExecutor() as executor1:
        t1=executor1.submit(checkresultcount(out))
    #query="Published on "

    #Searching for query in extracted web contents
    res=re.search(query,out)
    status=res.group(0)
    substring=re.findall(r'>(.*?)<',out)

    #Fetches all dates the results published from result page. Identified by query. (published on)
    alldates = [idx for idx in substring if idx.lower().startswith(query.lower())]

# If recentdate from data is same as new recent date,
# saved_srd==srd but savedcount!=0, then there are new and unfetched results
# This is the usual case.
    if(saved_rd==rd and saved_srd==srd and savedcount!=0 ):
        a=recentdate
        b=secondrecentdate
# If saved_srd!=secondrecentdate, then there are previously unfetched results
    elif (saved_srd!=srd and savedcount!=0):
        a=recentdate
        b=string_clean.normalizeDate(saved_srd)

# If saved_rd != rd, then there are unfetched results,
# Refresh the results count and call this function again
    elif(saved_rd!=rd):
        fetch_results_count()
        fetch_results()
        return 0



    with concurrent.futures.ThreadPoolExecutor() as executor2:
        t2=executor2.submit(string_clean.extract_roi, out, a, b)
    roi=t2.result()
    count=roi.count(classname) #displayList is the class name for new result

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

        # Insert result into table results
        # Results table has name,url,date columns and id=>AUTO_INCREMENT
        cols=["name","url","date"]
        vals=[]
        vals.append(resname)
        vals.append(resurl)
        vals.append(recentdate)
        vals=string_clean.enclose_elements_in_list_with_symbol(vals,"'")
        with concurrent.futures.ThreadPoolExecutor() as executor3:
            t3=executor3.submit(db.insert_into_table_strip_val_except_space_and_input_thread,"results",cols,vals,"/.:")
    

    # After every new result has been stored in database, reset the count variable to zero in table data
    
    columns=["recentdate","secondrecentdate","lastfetchtime","count"]  
    values=[]
    now=str(datetime.now())
    values.append(recentdate)
    values.append(secondrecentdate)
    values.append(now)
    values.append("0")
    db.update_table(conn,"data",columns,values,"/:.-")


# Function to check if a result is present in database, given a list of keywords
#

def check_for_results(keywords,badlist):
    result_words=""
    
    found_words=[]
    results=[]

    ret=[]
    #keys=keywords[0]
    #keys=string_clean.string_to_list(keys,",")

    keys=keywords

    with concurrent.futures.ThreadPoolExecutor() as executor1:
        sql="select * from results"
        t1=executor1.submit(db.execute_query_thread,sql,1)
    res=t1.result()
    for r in res:
        result_words=r[1].lower()
        for k in keys:
            if(k in result_words and k not in badlist):
                print(result_words)
                results.append(result_words)
                print(k)
                if(k not in found_words):
                    found_words.append(k)
    if(len(found_words)>0):   
        ret.extend(found_words)
        ret.extend(results)
        # The first value of ret is the keyword found.
        # Everything else are the results.
        return ret
                
        


fetch_results()



# TODO: create another fuction to fetch keywords and calling check_for_results()
# create a config.db to store vars like badlist and fetch badlist from db

# Function that takes keywords, fetches badlist from table 'config' and passes the keywords and badlist
# to check_for_results() function.
# is_result_published() function is the function that should be used to check for results by keyword
# TODO: For now, keys is the argument and is statically given. I should replace the argument with
# sname(stream_name) or some other unique name and fetch keywords related to that stream from 'courses'
  
def is_result_published(cid='630'):
    badlist=[]
    
    #keys=['m. sc.','M. Sc.','M. Sc','m.sc', 'Physics', 'with', 'specialization', 'in', 'applied', 'electronics', 'CSS', '840'])
    #badlist=['in','with','and']

    with concurrent.futures.ThreadPoolExecutor() as executor1:
        sql="select badlist from config"
        t1=executor1.submit(db.execute_query_thread,sql,0)
    temp_badlist=t1.result()
    for i in temp_badlist: # Populating badlist from table 'config'
        badlist.append(string_clean.strip_string(str(i)))
    
    res=db.execute_query(db.init_conn(),"select keywords from courses where cid='"+cid+"'",1)

    for key in res:
        #k=['m.sc','m sc','zoology']
        print(key)

        # Converting tuple key to iterable variable.
        key=string_clean.string_to_list_sql_safe(key[0],",")
        ret=check_for_results(key,badlist)

        found_word=ret[0]
        key=string_clean.replace_string_from_list_elements(key,found_word,'')
        ret=check_for_results(key,badlist)
        
        print(ret)


is_result_published()