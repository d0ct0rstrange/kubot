import dateutil as dparser
from dateutil import parser
import concurrent.futures
import datetime, datefinder

import db,string_clean

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

def string_to_date(string):
    matches = list(datefinder.find_dates(string))
    temp_date_obj=matches[0]
    if len(matches) > 0:
        # date returned will be a datetime.datetime object. here we are only using the first match.
        temp_date_time_obj = matches[0]
        date_time_obj=temp_date_time_obj.date()
    return date_time_obj

print(string_clean.similarity_between_strings(f,g))