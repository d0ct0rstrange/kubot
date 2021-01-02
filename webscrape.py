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

#Function to check the new results count.
# Input i 
def checkresultcount(out,query="Published on ",classname="displayList"): 
    conn=db.init_conn()
    with concurrent.futures.ThreadPoolExecutor() as executor1:
        t1=executor1.submit(db.execute_query_thread,"select * from data")
        res=t1.result()
    


    for row in res:
        a=row[0] #recentdate
        b=row[1] #secondrecentdate
        global savedcount
        savedcount=row[3] #count
        
    #c=out.find("Published on "+a) #Start region from rd
    #d=out.find("Published on "+b) #Stop region from srd

    c=out.find(query+a) #Start region from rd
    d=out.find(query+b) #Stop region from srd

    if c>d:
        roi=out[d:c] #Region Of Interest between srd and rd
    elif d>c:
        roi=out[c:d] #Region Of Interest between rd and srd

    #count=roi.count("displayList") #displayList is the class name for new result

    count=roi.count(classname) #displayList is the class name for new result

    return count

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

    global recentdate, secondrecentdate,rd,srd,out,savedcount
    
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
        t1=executor1.submit(checkresultcount,out,query,classname)
    currcount=t1.result()
    print(currcount)
    return currcount



def fetch_results(classname="displayList",query="Published on ",url='https://exams.keralauniversity.ac.in/Login/check8'):
    # We have fetched the new results count using fetch_results_count. Now, we want to fetch the new results
    # To do so, first select recentdate,secondrecentdate from data;
    # Find ROI between 


    #1. URL => URL from the results to be fetched
    #          ('https://exams.keralauniversity.ac.in/Login/check8' is the default)
    #2. QUERY => Keyword that denotes the date the
    #    results got published. This is also used to mark the start of results.
    #    Recent date marks the start of the results and Second recent date marks the end of results.
    #    We fetch results one by one iterating between the recent date and second recent date.
    #    ("Published on " is the default)
    #3. CLASSNAME => The class name for new result
    #                ("displayList" is the default)

    global recentdate, secondrecentdate,rd,srd,out,savedcount
    
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


    
    


fetch_results_count()


