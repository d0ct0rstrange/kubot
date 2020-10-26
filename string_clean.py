import requests
from bs4 import BeautifulSoup as BS
import re,string
import csvwrite
import time, os, itertools

#function to extract region of interest from html
#out=r.text
#a=rd
#b=srd

def extract_roi(out,a,b):
    c=out.find("Published on "+str(a)) #Start region from rd
    d=out.find("Published on "+str(b)) #Stop region from srd
    roi=out[c:d] #Region Of Interest between rd and srd
    return roi

#To merge two lists as tuple. list3=[(list1[0],list2[0]),(list1[1],list2[1])]
def merge(list1, list2): 
      
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))] 
    return merged_list 

#Function to convert multiple elemted list back to  single line string
def listToString(s):  
    
    # initialize an empty string 
    str1 = " " 
    
    # return string   
    return (str1.join(s)) 


#To clean \n and \r from strings
#Better function for this is defined below
def clean_string(sname):
    #sub_list = ["\n", "\r"] 
    #sname=" BCA\r\n BCA\r\n . (332)"
    sname=sname.splitlines()
    sname_filtered = listToString(sname)
    sname_filtered=str(sname_filtered)
    #print(sname_filtered)
    return sname_filtered

#TODO: function to dynamically clean timetable and download
def clean_timetable_nourl(url,tag,classname,regexvalue=r"^[0-9]{3}$"):
    #URL to retrieve Streams list (Mtech, Btech)
    #url='https://exams.keralauniversity.ac.in/Login/stud_session.php'
    r = requests.get(url)
    out = r.text
    soup=BS(r.text, 'html.parser')
    rows=soup.findAll(tag, {classname: re.compile(regexvalue)})
    id=[] #ID of streams
    name=[] #Name of streams
    for row in rows:
        id.append(row.get('value')) 
        name.append(row.get_text()) 
    final=dict(zip(id,name))
    return final

def clean_html(url,tag,classname,value):
    #URL to retrieve Streams list (Mtech, Btech)
    #url='https://exams.keralauniversity.ac.in/Login/stud_session.php'
    r = requests.get(url)
    out = r.text
    soup=BS(r.text, 'html.parser')
    rows=soup.findAll(tag, {classname: value})
    ids=[] #ID of tag
    name=[] #value of tag
    for row in rows:
        ids.append(row.get('value')) 
        name.append(row.get_text()) 
    final=dict(zip(ids,name))
    return final

#Function to clean badchars from string 
def stripstring(badstring):
    badchars=['\n','\r','\t','\xa0']
    for i in badchars:
        badstring=badstring.replace(i,'')
    goodstring=badstring.strip()
    return goodstring

#Function to clean badchars from all strings inside a list
def striplist(badlist):
    goodlist=[stripstring(i) for i in badlist if (i!='')]
    return goodlist


#Function to extract Result and URL
def clean_results_nourl(r,tag,attributes):
    #URL to retrieve Streams list (Mtech, Btech)
    #url='https://exams.keralauniversity.ac.in/Login/stud_session.php'
    #'valign':True,'width':False (Attribute for attrds={} in findAll)
    #Extract result name
    soup=BS(r, 'html.parser')
    rows=soup.findAll(tag,attributes)

    #Extract result pdf download urls
    soup2=BS(r, 'html.parser')
    rows2=soup2.findAll('a', {'href': re.compile(r'.+\.pdf$')})

    ids=[] #ID of tag (N/A)
    name=[] #result name
    download=[] #download url of result

    #extract individual results and urls
    for (row,row2) in zip(rows,rows2):
        download.append(row2.get('href'))
        ids.append(row.get('valign')) 
        name.append(row.get_text())
 
    #for cleaning null and control characters from result name
    name=[stripstring(i) for i in name if (i!='')]

    final={}
    serial=range(len(name))

    #Final is a dictionary with serial number and tuple(result,downloadurl)
    #First element in final can be accessed from list=final[0]
    #First element in list can be accessed from list[0]
    #list[0]=Result
    #list[1]=ResultDownloadURL
    final=dict(zip(serial,merge(name,download)))
    
    # l=final[0]
    # print(l[1])
    return final