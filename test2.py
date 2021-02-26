import dateutil as dparser
from dateutil import parser
import concurrent.futures
import datetime, datefinder
import concurrent.futures

import db,string_clean
import csvwrite

ax="1"

#with concurrent.futures.ThreadPoolExecutor() as executor1:
#    t1=executor1.submit(db.execute_query,"select * from courses")
#    res=t1.result()


#print(res)
a="Published on .21/12/2020"
b="Published on 22/12/2020"
c="Published on 1/1/2021"
d="21/12/2020"
e="Published on 04/01/2021"
f="a sc"
g="a.sc"

res=string_clean.similarity_between_strings(a,d)
str_res=str(res)
if(res<=0.60 and res>=0.58):
    #print(res)
    a=a
else:
    #print("Not correct. Result:"+str_res)
    b=b


resu=parser.parse("monkey 21/12/2020 love banana",fuzzy=True)
#print(resu.date())
x=resu.date()

# code block that checks for keywords in result string
# ignores strings mentioned in badlist
# x= result_string
# keys=keywords for a course
# badlist= strings_to_ignore

x=' fourth semester post graduate degree examinations july 2020 m. sc. zoology regular supplementary '
keys=['m. sc.','MSc', 'Physics', 'with', 'specialization', 'in', 'applied', 'electronics', 'CSS', '840']
badlist=['in','with']
for k in keys:

    if(k in x and k not in badlist):
        print(k)
        print(x)
# END of code block 

def course_keyword_generator(string_list):
    k_list=[]
    with concurrent.futures.ThreadPoolExecutor() as executor11:
        sql="select sname from courses"
        t11=executor11.submit(db.execute_query_thread,sql)
    res=t11.result()
    for r in res:
        print(r)
        # TODO: Add spaces and dots between words to create possible values
        # possibilities
        # 'abc', "a.bc","a bc","a. bc","a bc.","a. bc","a. bc."
        # There are also b.a.m.s, l.l.b etc with multiple dots
        # 1. f= extract first letter
        # 2. s= extract letters except first letter
        # 3. add . and space at end of first letter
        # 4. add space to beginning and end of second part
        r=string_clean.strip_string(str(r))
        first_part=r[0:1]
        second_part=r[1:len(r)]
        symbols=["."," "]

        string=""
        for i in r[:-1]:
            string+=i+"."
        string+=r[-1]

        if string not in k_list:
            k_list.append(string)

        # a.bc
        string=first_part+"."+second_part
        if string not in k_list:
            k_list.append(string)
        
        # "a.bc "
        string=first_part+"."+second_part+" "
        if string not in k_list:
            k_list.append(string)
        
        # a bc
        string=first_part+" "+second_part
        if string not in k_list:
            k_list.append(string)

        # "a bc "
        string=first_part+" "+second_part+" "
        if string not in k_list:
            k_list.append(string)

        # "a bc."
        string=first_part+" "+second_part+"."
        if string not in k_list:
            k_list.append(string)

        # "a bc. "
        string=first_part+" "+second_part+". "
        if string not in k_list:
            k_list.append(string)

        # "a. bc"
        string=first_part+". "+second_part
        if string not in k_list:
            k_list.append(string)

        # "a. bc "
        string=first_part+". "+second_part+" "
        if string not in k_list:
            k_list.append(string)

        # "a. bc. "
        string=first_part+". "+second_part+". "
        if string not in k_list:
            k_list.append(string)



    print(k_list)

#course_keyword_generator(keys)

