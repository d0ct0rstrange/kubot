import requests
from bs4 import BeautifulSoup as BS
import re,string
import csvwrite,string_clean
import time, os
from datetime import datetime
import queue

#to do iterate using row.get_text()
test=[]
tempresname=tempresurl=[]
#Reading saved details from data.csv to match it with cuurent data   
saveddetails=csvwrite.read_from_csv('data.csv')
savedrd=saveddetails['recentdate']
savedsrd=saveddetails['secondrecentdate']
savedcount=int(saveddetails['count'])

#Converting to same date format as rd
savedrd = datetime.strptime(savedrd, "%d/%m/%Y").date() 
savedsrd = datetime.strptime(savedsrd, "%d/%m/%Y").date() 



visited_pages=[]
#Pages handling
url='https://exams.keralauniversity.ac.in/Login/check8/'
r = requests.get(url)
out = r.text
r=out
a="pagetitle1"
b="tableHeading"
roi=string_clean.extract_roi(out,a,b)
tag="a"
attributes={'href':True,'style':False,'class':False}

soup2=BS(r, 'html.parser')
rows2=soup2.findAll('a', {'href': re.compile(r'==')})
temp_my_list=my_list=temp_my_list2=my_list2=[]
temp_link_text = link_text={}
for row in rows2:
    temp_my_list.append(row.get('href'))
    link_text[row.get_text()]=row.get('href') #ahref text, ahref url

#deleting duplicates
my_list=[i for n, i in enumerate(temp_my_list) if i not in my_list[:n]]
page_count=0
urls=[]
# if("<< " in link_text.keys()):
#     del link_text["<< "]
if(" >> " in link_text.keys()):
     del link_text[" >> "]
for keys in link_text:
     urls.append(link_text[keys])


while urls:
    url=urls[page_count]
    for j,k in link_text.items():
        if k==url:
            print(j)
            break
    #Results handling
    #Reverting datetime object to KU site's slash format
    a=csvwrite.normalizeDate(savedrd) #recentdate in KU Format
    b=csvwrite.normalizeDate(savedsrd) #secondrecentdate in KU Format

    #displayList is the class name for new result

    #To filter result names, we want <td> with attrs valign=true and width=false
    tag="td"
    attributes={'valign':True,'width':False}
    #output is a dictionary with serial number (1,2,...) and Result name as value
    output=string_clean.clean_results_nourl(out,tag,attributes)
    for results in output.items():
        tempoutlist=results[1]
        resname=tempoutlist[0]
        resurl=tempoutlist[1]
        tempresname.append(resname)
        tempresurl.append(resurl)
        #print("Result: "+resname+" Download from here:"+resurl)
    test.append(string_clean.merge(tempresname,tempresurl))
    xxx=found=0
    for i, j in link_text.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if xxx!=0:
            break
        if j == url:
            found+=1
            if found==1:
                index_found=i
                xxx+=1

    
    
    if page_count>0:
        if(index_found in link_text.keys()):
            val=link_text[index_found]
            del link_text[index_found]
        if index_found not in visited_pages:
            visited_pages.append(index_found)
        for x in visited_pages:
            if x in link_text.keys():
                del link_text[x]
        
        url2=link_text[i]
        r2 = requests.get(url2)
        out2 = r2.text
        r2=out2
        soup2=BS(r2, 'html.parser')
        rows2=soup2.findAll('a', {'href': re.compile(r'==')})
        temp_my_list=my_list=temp_my_list2=my_list2=[]
        temp_link_text = link_text={}
        for row in rows2:
            temp_my_list.append(row.get('href'))
            link_text[row.get_text()]=row.get('href') #ahref text, ahref url
        
        if("<< " in link_text.keys()):
            del link_text["<< "]
        if(" >> " in link_text.keys()):
            del link_text[" >> "]
        if len(visited_pages)!=1:
            for x in visited_pages:
                if x in link_text.keys():
                    temp=link_text[x]
                    if temp in urls:
                        urls.remove(temp)
                        del link_text[x]
                
            for keys in link_text:
                urls.append(link_text[keys])
    page_count+=1



