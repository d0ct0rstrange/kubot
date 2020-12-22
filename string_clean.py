import requests
from bs4 import BeautifulSoup as BS
import re,string
import csvwrite
import time, os, itertools
import datetime
from difflib import SequenceMatcher

#variable that stores current date and time at script start
now = datetime.datetime.now()


#Similarity between strings. If it returns val >=0.5, it is similar
def similarity_between_strings(a,b):
	return SequenceMatcher(None, a, b).ratio()

#Extract numbers from string
def string_to_int(string):
    res = [int(i) for i in string.split() if i.isdigit()] 
    return str(res)


#Convert two lists to dictionary. a=[1,2,3] b=[a,b,c]. Dict c=> [1:a, 2:b, 3:c]
def lists_to_dic(list1,list2):
    return dict(zip(list1,list2))
    

#Convert two lists to list. a=[1,2,3] b=[a,b,c]. Dict c=> [1,a, 2,b, 3,c]
def lists_to_list(list1,list2):
    return str(list(zip(list1,list2)))
    
#Enclose string elements in list with provided symbol
def enclose_elements_in_list_with_symbol(badlist,symbol):
    goodlist=[]
    for i in badlist:
        y=''+symbol+''+i+''+symbol+''
        goodlist.append(y)
    return goodlist

#If substring exists in any element of a list
def if_substring_in_list(searchlist,substring):
    return_list=[]
    for i in searchlist:
        search=i.find(substring)
        if search:
            return_list.append(i)
    return return_list

#Replace sub string if it occurs in an element of a list
def replace_string_from_list_elements(badlist,element_to_find,element_to_replace):
    goodlist=[]
    for element in badlist:
        goodlist.append(element.replace(element_to_find,element_to_replace))
    return goodlist

#Convert string to list.
def string_to_list(string,seperator):
    li = list(string.split(seperator))
    return li 

#Convert string to sql safe list.
def string_to_list_sql_safe(string,seperator,escape_char="\\"):
    #a=string.partition(seperator)[0]
    #b=a[-1]
    pattern=escape_char+seperator
    a=string.find(pattern)
    b=string[a]
    #Check if the string contains the escape character before the seperator
    #If escape character is found before separator, then exclude the convertion of that separator in string
    if b==escape_char:
        unique_string="!ELLIOTWASHERE!"
        string2=string.replace(pattern,unique_string) #Replacing --> \, <-- with a unique string

        #Converting the string without the character to be excluded
        temp_li= list(string2.split(seperator))

        #Reintroducing the escaped character by replacing the unique string with the saved character
        li=replace_string_from_list_elements(temp_li,unique_string,pattern)

    #If escape character is not found before separator, then convert the string normally
    else:
        li= list(string.split(seperator))
    return li 

#Lists to character separated single string
def lists_to_character_separated_string(list1,list2,separator=","):
    a=[]
    s1=stripstring(list1)

    temp_s2=",".join(strip_special_from_list(list2))
    s2=stripstring(temp_s2)

    final_string=s1+separator+s2
    return final_string

#Merging two list with custom delimiter.
def merge_list_custom_seperator(list1,list2,separator=","):
    merged=""
    mixed=""
    for i,j in zip(list1,list2):
        mixed+=i+" "+j+separator
    merged=mixed[:-1]
    return merged

#function to extract region of interest from html
#out=r.text
#a=rd
#b=srd

#Function to Strip special chars except space
def strip_special_except_space(string):
    for k in string.split("\n"):
        string_clean=re.sub(r"[^a-zA-Z0-9]+", ' ', k)
    return string_clean

#Function to Strip special chars except space and (input)
def strip_special_except_space_and_input(string,exception):
    for k in string.split("\n"):
        string_clean=re.sub(r"[^a-zA-Z0-9"+exception+"]+", ' ', k)
    return string_clean

#Function to Strip special chars except space and &
def strip_special_except_space_and(string):
    for k in string.split("\n"):
        string_clean=re.sub(r"[^a-zA-Z0-9&]+", ' ', k)
    return string_clean

#Function to Strip special chars including space
def strip_string(string):
    for k in string.split("\n"):
        string_clean=re.sub(r"[^a-zA-Z0-9]+", '', k)
    return string_clean


#Function to Strip special chars including space from all strings inside a list
def strip_special_from_list(badlist):
    goodlist=[strip_string(i) for i in badlist if (i!='')]
    return goodlist

#Function to Strip special chars except space from all strings inside a list
def strip_special_from_list_except_space(badlist):
    goodlist=[strip_special_except_space_and(i) for i in badlist if (i!='')]
    return goodlist

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

def sanitize_sql_query(some_string):
    c= ''.join(char for char in some_string if char.isalnum())
    print(c)
    return c