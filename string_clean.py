import requests
from bs4 import BeautifulSoup as BS
import re,string
import csvwrite
import time, os, itertools
import datetime

#variable that stores current date and time at script start
now = datetime.datetime.now()


#function to extract region of interest from html
#out=r.text
#a=rd
#b=srd

#Function to Strip special chars except space and &
def strip_special_except_space_and(string):
    for k in string.split("\n"):
        string_clean=re.sub(r"[^a-zA-Z0-9&]+", ' ', k)
    return string_clean

#Function to extract years
def word_to_year(string):
    yearslist=list(range(2000,now.year+1)) #list of years from 2000 to current year

    #To strip string of special chars
    string_clean=strip_special_except_space_and(string)

    temp=[int(s) for s in string_clean.split() if s.isdigit()]
    year=list([y for y in temp if y in yearslist])
    return year

#Function to return numbers according to the corresponding word
#Eg:. First => 1, Second=>2 etc
#Requires a dictionary numbers={} to be declared first
def word_to_number(string):
    numbers={
		    "zeroth":"0",
		    "first":"1",
		    "second":"2",
		    "third":"3",
		    "fourth":"4",
		    "fifth":"5",
		    "sixth":"6",
		    "seventh":"7",
		    "eighth":"8",
		    "nineth":"9",
		    "tenth":"10",
		    "eleventh":"11",
		    "twelveth":"12",
		    "thirteenth":"13",
		    "fourteenth":"14",
		    "fifteenth":"15"
		    
		    }
    string_list=string.split()
    lower_string=[]
    return_numbers=[]
    return_words=[]
    for i in string_list:
        lower_string.append(i.lower())
    for j in lower_string:    
        if j in numbers.keys():
                    return_words.append(j)
                    return_numbers.append(numbers[j])
    return return_numbers


#Function to return strings according to the corresponding number
#Eg:. 1 => First, 2=>Second etc
#Requires a dictionary strings={} to be declared first
def number_to_word(string):
    strings={
		    "0":"zeroth",
		    "1":"first",
		    "2":"second",
		    "3":"third",
		    "4":"fourth",
		    "5":"fifth",
		    "6":"sixth",
		    "7":"seventh",
		    "8":"eighth",
		    "9":"nineth",
		    "10":"tenth",
		    "11":"eleventh",
		    "12":"twelveth",
		    "13":"thirteenth",
		    "14":"fourteenth",
		    "15":"fifteenth"
		    
		    }
    string_list=string.split()
    lower_string=[]
    return_string=[]
    return_words=[]
    for i in string_list:
        lower_string.append(i.lower())
    for j in lower_string:    
        if j in strings.keys():
                    return_words.append(j)
                    return_string.append(strings[j])
    return return_string

#Function to determine the result is of semester or year
def sem_or_year(string):
    s=string.lower()
    return_string=[]
    if "semester" in s:
        return_string.append("semester")
    elif "year" in s:
        return_string.append("year")
    else:
        return_string.append("No semester or year found in result!")
    return return_string

#Extract semester/year numbers from result
def which_sem_or_year(string):
    nums=""
    sy=sem_or_year(string)
    numslist=word_to_number(string)
    nums=listToString(numslist)
    return number_to_word(nums)
    
#find word before specific word     
def word_before_word(string,keyword):
    s=string.lower()
    keyword=keyword[0]
    keyword=keyword.lower()
    return_string=[]
    bef=re.findall(r"\w+(?= "+keyword+")", s)
    return_string.append(bef)
    return return_string

#Function to find previous words untill a matched key in a string
def string_upto_key(string,key="Degree"):
	b=[]
	string_list=string.split()
	for  i in string_list:
		#print(i)
		b.append(i)
		if i==key:
			break
	return b

#Function to find previous word from a matched key in a string
def word_before_key(string,key):
    b=[]
    string_list=string.split()
    for  i in string_list:
        prev_id=string_list.index(i)-1
        prev=string_list[prev_id]
        b.append(i)
        #print(prev)
        if i==key:
            break
    return prev

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