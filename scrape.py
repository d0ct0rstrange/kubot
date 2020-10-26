import requests
from bs4 import BeautifulSoup as BS
import re
import bot
from datetime import datetime
import datefinder
import csvwrite,string_clean


#Global variable declarations
#URL to check results
url='https://exams.keralauniversity.ac.in/Login/check8'
r=[]
out=''
recentdate=rd=[]
secondrecentdate=srd=[]
status=query=''
savedcount=0

#Function to Verify if new result has been published or not. 
#Returns total results count between recent and second recent date

def checkresultcount(): 
    res=csvwrite.read_from_csv()
    #print(res)
    a=res["recentdate"]
    b=res["secondrecentdate"]
    global savedcount
    savedcount=res["count"]
    c=out.find("Published on "+a) #Start region from rd
    d=out.find("Published on "+b) #Stop region from srd
    roi=out[c:d] #Region Of Interest between rd and srd
    count=roi.count("displayList") #displayList is the class name for new result
    return count


#Function to fetch dates from results page
#Then update csv with recent, second recent date, last fetch time and results count.
#Extracting date from "Published on xx/xx/xxxx" and saving it to data. csv
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

    currcount=checkresultcount()

    #New updates are available, Check which course
    #if((currcount>int(savedcount)) and ()):
       # print("New Results available! Fetched at: "+str(datetime.now().time()))

    #Reading saved details from data.csv to match it with cuurent data   
    saveddetails=csvwrite.read_from_csv()
    savedrd=saveddetails['recentdate']
    savedsrd=saveddetails['secondrecentdate']
    savedcount=int(saveddetails['count'])
    
    #Converting to same date format as rd
    savedrd = datetime.strptime(savedrd, "%d/%m/%Y").date() 
    savedsrd = datetime.strptime(savedsrd, "%d/%m/%Y").date() 

    #Worst case scenario. Results of more than one day published, including results between
    #savedrd and savedsrd.
    #In this case, actual recent date will be far higher than savedrd
    #There is also discrepencies between actual second rd and savedsrd
    #So, first save the results between savedrd and savedsrd, then
    # update savedrd=currrd, savedsrd=currsrd and fetch the new results.
    
    #Reverting datetime object to KU site's slash format
    a=csvwrite.normalizeDate(savedrd) #recentdate in KU Format
    b=csvwrite.normalizeDate(savedsrd) #secondrecentdate in KU Format

    #TODO:uncomment this!
    if((savedrd<rd) and currcount>savedcount): 

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
        
        #We've successfully fetched results from saved dates.
        #Now we need to catchup with the current recent date
        localrecentdate=csvwrite.normalizeDate(rd)
        localsecondrecentdate=csvwrite.normalizeDate(savedrd)
        roi=string_clean.extract_roi(out,localrecentdate,localsecondrecentdate)
        output2=string_clean.clean_results_nourl(roi,tag,attributes)
        for results in output2.items():
            tempoutlist=results[1]
            resname=tempoutlist[0]
            resurl=tempoutlist[1]
            print("Result: "+resname+" Download from here:"+resurl)

    elif(currcount>savedcount): 
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

    elif((currcount==savedcount)and (savedrd!=rd)): 
        localrecentdate=csvwrite.normalizeDate(rd)
        localsecondrecentdate=csvwrite.normalizeDate(savedrd)
        roi=string_clean.extract_roi(out,localrecentdate,localsecondrecentdate)
        output2=string_clean.clean_results_nourl(roi,tag,attributes)
        for results in output2.items():
            tempoutlist=results[1]
            resname=tempoutlist[0]
            resurl=tempoutlist[1]
            print("Result: "+resname+" Download from here:"+resurl)
    else:
        print("No Updates! Last Fetch time: "+str(datetime.now()))
    
    
    
    #Writing dates to data. csv
    #csvwrite.write_to_csv(rd,srd,currcount) 

update_results()


#Debug prints

#print(now) #Current Time 
print("Recent date: "+str(recentdate))    
print("Secod Recent date: "+str(secondrecentdate))    
print("Status: "+status)
print("Query: "+query)
#print("Out: "+out)

#Write last fetched details to file
#f= open("nowfile","w") #last fetched date and time
#f.write(str(now))
#f.close()






#Function to check for subscribed courses in published results
def check_subscribed_results():
    print("\n")



#TODO: Move following to a new class (bot.py)
#sending telegram notification
if(status!=query):
    botres=bot.telegram_bot_sendtext(msg)
    print(botres)

#If botres is not defined
try:
    botres
except NameError:    
    print("Message not sent!")
else:
    print("Message sent!")

#f = open("out", "a")
#f.write(out)
#f.close()
