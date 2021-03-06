import requests
from bs4 import BeautifulSoup as BS
import re,string
import csvwrite,string_clean, itertools
import time, os
from datetime import datetime
import queue
import concurrent.futures
import csv

#Itereates through all results and extracts results
#can be used for finding correct keywords related to courses
#for eg: B.sc can be written as B Sc, b.sc, B .Sc, b.sc etc

def iterate_result_pages(starturl='https://exams.keralauniversity.ac.in/Login/check8',page_count=0):
    visited_pages=[]
    urls=[]
    #Pages handling
    if page_count==0:
        urls.append(starturl)
        url=starturl
    r = requests.get(url)
    out = r.text
    r=out
    a="pagetitle1"
    b="tableHeading"
    roi=string_clean.extract_roi(out,a,b)
    tag="a"
    attributes={'href':True,'style':False,'class':False}
    temp_my_list=my_list=temp_my_list2=my_list2=[]
    temp_link_text ={} 
    link_text={}
    while url:
        r = requests.get(url)
        out = r.text
        r=out
        soup2=BS(r, 'html.parser')
        rows2=soup2.findAll('a', {'href': re.compile(r'==')})

        for row in rows2:
            temp_my_list.append(row.get('href'))
            url_address=row.get('href')
            page_num=row.get_text()
            page_num=page_num.strip()
            if (url_address not in visited_pages):
                if page_num not in link_text.keys():
                    link_text[page_num]=row.get('href') #ahref text, ahref url
 
        for j,k in link_text.items():

            if k==url:
                print(j)
                break
         
        if page_count!=0:
            if("<<" in link_text.keys()):
                del link_text["<<"]
        if(">>" in link_text.keys()):
            del link_text[">>"]

        
        tag="td"
        attributes={'valign':True,'width':False}
        res=csvwrite.read_from_csv('data.csv')
        #print(res)
        recentdate=res["recentdate"]
        #output is a dictionary with serial number (1,2,...) and Result name as value
        output=string_clean.clean_results_nourl(out,tag,attributes)

        #Line count of keywords.csv file
        keywords_file='keywords.csv'
        if os.path.isfile(keywords_file):
            c = int(len(open(keywords_file).readlines()))
        else:
            with open(keywords_file, 'w') as fp:
                pass
                c=0
                a_file = open(keywords_file, "a")
                writer = csv.writer(a_file)
                writer.writerow(['id', 'course','url','date'])
                a_file.close()
        final=[]
        final_dict={}
        for results in output.items():
            c=c+1
            tempoutlist=results[1]
            resname=tempoutlist[0]
            resurl=tempoutlist[1]
            #print("Result: "+resname+" Download from here:"+resurl)
    
            final_dict[c]= tempoutlist
        csvwrite.write_results(final_dict,recentdate,"keywords.csv")

                
        visited_pages.append(url)
            
        temp_dict=link_text
        for keys,values in dict(temp_dict).items():
            if values in visited_pages:
                link=link_text[keys]
                del link_text[keys]
                if link in urls:
                    urls.remove(link)


        if starturl in urls:
            urls.remove(starturl)
        for keys in link_text:
            link=link_text[keys]
            urls.append(link)
        temp_urls=urls
        #urls=[i for n, i in enumerate(temp_urls) if i not in urls[:n]]
        if url in temp_urls:
            urls.remove(url)

        for values in visited_pages:
            if values in urls:
                urls.remove(values)
        try:
            url=urls[0]  #raises index error on result empty
        except IndexError:
            print ("Execution finished! All results have been saved to keywords.csv file!")
            return 1
        page_count+=1

def iskeywordinstring(key,string):
    key = "abc@gmail.com"
    string = ["hotmail", "gmail", "yahoo"]

    string_contains_key = any(word in key for word in string)
    #print(string_contains_key)
    return string_contains_key


def keyword_enum(filename="keywords.csv"):
    #TODO: Currently this reads only last result. Make that whole list.
    # Opens csv in a new thread
    with concurrent.futures.ThreadPoolExecutor() as executor1:
        t1=executor1.submit(csvwrite.read_from_csv,filename)
        #res=csvwrite.read_from_csv('data.csv') #original (without threading)
    res=t1.result()

    #Reading text, url and id from saved keywords.csv file  
    for results in res.items():
        print(results[1])

    #Year found in result title
    with concurrent.futures.ThreadPoolExecutor() as executor2:
        t2=executor2.submit(string_clean.word_to_year,res['course'])
    years=t2.result()  
    
    #Semester/Year found in result title
    with concurrent.futures.ThreadPoolExecutor() as executor3:
        t3=executor3.submit(string_clean.sem_or_year,res['course'])
    sy=t3.result()
    
    #Extracting Semester/Year number from result title
    with concurrent.futures.ThreadPoolExecutor() as executor4:
        t4=executor4.submit(string_clean.which_sem_or_year,res['course'])
    num=t4.result()
    print(num)

#keyword_enum() 
#iterate_result_pages()
                

x="Career Related First Degree Programme under CBCSS Group 2(b) FIRST SEMESTER BBA (195) (2019 ADMISSION REGULAR, 2018 ADMISSION: IMPROVEMENT 2017, 2016, 2015 & 2014 ADMISSION SUPPLEMENTARY ONLY Degree Examination, November, 2019  "
y=string_clean.strip_special_except_space_and(x)
print(y)