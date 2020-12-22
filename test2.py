import concurrent.futures
import db


with concurrent.futures.ThreadPoolExecutor() as executor1:
    t1=executor1.submit(db.execute_query,"select * from courses")
    res=t1.result()

print(res)