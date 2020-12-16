import requests
from bs4 import BeautifulSoup as BS
import re,string
import csvwrite, string_clean
import db
import time
import itertools


def enumerate_courses():
    #Initiating Database connection
    connec=db.init_conn()

    #proxies for burp debugging
    proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "https://127.0.0.1:8080"
    }

    #URL to retrieve Streams list (Mtech, Btech)
    url='https://exams.keralauniversity.ac.in/Login/stud_session.php'
    r = requests.get(url)
    out = r.text
    soup=BS(r.text, 'html.parser')
    rows=soup.findAll('option', {"value": re.compile(r"^[0-9]{3}$")})
    streamlist=[] #ID of streams
    streamname=[] #Name of streams

    for row in rows:
        streamlist.append(row.get('value')) 
        streamname.append(row.get_text()) 
    streamlist = list(dict.fromkeys(streamlist)) #Dictionary of stream_id=>stream_name



    #Fetching PHPSESSID cookie for valid requests

    #If the following header is not specified, request won't pass through
    headers={
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    #PHPSESSID only gets renewed via this URL
    #This URL also retrieves Course list, given stream_id via selMCourse POST variable
    url = 'https://exams.keralauniversity.ac.in/Login/getAjaxdetails.php'
    with requests.Session() as s:
            
            #Request with proxy ON
            #r = s.post(url,headers=headers, proxies=proxies, verify=False)

            #Request with proxy OFF
            r = s.post(url,headers=headers, verify=False)
            #Fetched cookie. COOKIE is set in below line
            cookie = {'name':'value','PHPSESSID': requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']}

    #Initiliazing global variables.
    courselist={} #balance variable. No use. Ignore
    coursevalue=[] #Course_id
    var=[]         #variable for course_name processing
    cid=[]          #variable for course_id processing
    final=[]        ##balance variable. No use. Ignore
    coursename=[]   #course_name

    #Dicionary to merge stream_id with stream_name
    streams=dict(zip(streamlist,streamname))

    #Fetching course_list by providing stream_id
    #Eg: Msc(101). Select course_list from db, where stream_id=101. 
    #Ouput: Msc Computer science(1020), Msc Psychology (1021) etc
    for optionvalue in streamlist:
        url = 'https://exams.keralauniversity.ac.in/Login/check4'
        payload = {'selMCourse': optionvalue,'btnCrs':'Show+Courses'} #test case number 301,flag always 1
        with requests.Session() as s:
            r = s.post(url,cookies=cookie,headers=headers, verify=False, data=payload)

            #Time is used to delay requests. Use it to avoid DoSing the server
            #time.sleep(1)
    #Extracting course name. Identified by button class 'accordion' 
    # TODO: make this class and tag dynamic        
        soup=BS(r.text, 'html.parser')
        rows=soup.findAll('button',{'class':'accordion'})
        
        #Getting current stream_id
        z=str(optionvalue)
        sname=streams[z]

        #Cleaning stream_name, as it contains \n\r control chars
        sname_filtered = string_clean.clean_string(sname)  


        isstreamset=sname_filtered

        #If there exists a stream name, but no course name
        #For example, BFA and Other
        if len(rows)==0 and isstreamset!=None:
                #Resetting streamid
                streamid=None

                #Getting coursename and course id
                #course_name is isstreamset and stream id is streamid
                for option in soup.find_all('option',text=isstreamset):
                    streamid='value: {}'.format(option['value']) #course_id
                #print(streamid)
                
                if streamid:
                    median_streamid=str(re.findall(r'\d+',streamid))
                    coursevalue.append(str(string_clean.stripstring(median_streamid)))
                    formatted_streamid=string_clean.strip_string(median_streamid)
                    coursename.append(isstreamset+isstreamset)


                    mix=''+str(formatted_streamid)+','+str(isstreamset)+','+str(isstreamset)
                    mix_list=string_clean.string_to_list_sql_safe(mix,",")
                    if string_clean.if_substring_in_list(mix_list,"\\\\"):
                        returned_mix=string_clean.replace_string_from_list_elements(mix_list,"\\\\","\\")
                    print(returned_mix)
                    #Saving the course list to database
                    db.insert_into_table(connec,"courses",string_clean.string_to_list("cid,sname,cname",","),returned_mix)


                
                #Resetting isstream set
                isstreamset=None
                
        else:
            for row in rows:
                #Getting coursename and course id
                cname=row.get_text()    #course_name
                cval=re.findall(r'[0-9]+', cname) #course_id
                coursevalue.append(str(cval))
                
                #Cleaning course_name, as it contains \n\r control chars
                cname_filtered = string_clean.clean_string(cname)  

                #Merging stream_name with course-name
                #eg: Msc + computer science= Msc computer science
                coursename.append(sname_filtered+cname_filtered)

                cname_median=cname_filtered.replace(",","\,")
                cname_sql_safe=string_clean.string_to_list_sql_safe(cname_median,",")

                mix=''+str(cval[0])+','+str(sname_filtered)+','+str(cname_sql_safe)
                mix_list=string_clean.string_to_list_sql_safe(mix,",")
                if string_clean.if_substring_in_list(mix_list,"\\\\"):
                    returned_mix=string_clean.replace_string_from_list_elements(mix_list,"\\\\","\\")
                print(returned_mix)

                #Saving the course list to database
                db.insert_into_table(connec,"courses",string_clean.string_to_list("cid,sname,cname",","),returned_mix)

        #Resetting isstream set
        isstreamset=None
            
    #sanitized_streams=string_clean.striplist(streamname)


    ##IF WE WANT TO WRITE OUTPUT TO CSV (OR TO JUST DEBUG)

    #Creating dictionary with all course_id and course_name        
    # courses={}



    # for (i,j) in zip(coursename,coursevalue):
    #     courses[j]=i
    # print(courses)

    # cid = list(dict.fromkeys(cid))
    # courselist = dict(zip(cid,coursename))

    # #print(courses["['197']"]) #number format is ['$course_id']. Too lazy to correct it! :/
    # #Write output to csv file
    # csvwrite.write_course(courses)
     

    #DON'T REMEMBER WHAT THI IS.
    # query="Course Category"
    # res=re.search(query,out)
    # status=res.group(0)
    # substring=re.findall(r'value=\D(\d{3})\D(.*?)</option',out)
    #print(substring)

enumerate_courses()

def generate_keywords():
    conn=db.init_conn()
    sql="select sname,cname from courses"
    rows=db.execute_query(conn,sql)
    for row in rows:
        print(row)

#generate_keywords()