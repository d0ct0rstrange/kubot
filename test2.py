import dateutil as dparser
from dateutil import parser
import concurrent.futures
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

res=string_clean.similarity_between_strings(a,d)
str_res=str(res)
if(res<=0.60 and res>=0.58):
    print(res)
else:
    print("Not correct. Result:"+str_res)


resu=parser.parse("monkey 21/12/2020 love banana",fuzzy=True)
print(resu.date())
