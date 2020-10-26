import csv
from datetime import datetime


def normalizeDate(date):
    d=str(date.day)
    m=str(date.month)
    y=str(date.year)
    out=d+"/"+m+"/"+y
    return out

def write_to_csv(recentdate,secondrecentdate,count):
    recentdate = normalizeDate(recentdate)
    secondrecentdate = normalizeDate(secondrecentdate)

    with open('data.csv', 'w', newline='') as file:
        fieldnames=['recentdate', 'secondrecentdate', 'lastfetchtime','count']
        writer= csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'recentdate': recentdate, 'secondrecentdate': secondrecentdate, 'lastfetchtime': datetime.now(), 'count':count})
    return 1;

def read_from_csv():
    #Syntax read_from_csv(None,None,None) -> return everything
    #       read_from_csv(1,None,None) -> return recentdate only
    #       read_from_csv(None,1,None) -> return secondrecentdate only
    #       read_from_csv(None,None,1) -> return recentdate only

    with open('data.csv', 'r', newline='') as file:
        data=csv.DictReader(file)
        cont={}
        for row in data:
            cont=row
    return cont
			
def write_course(courses):
    a_file = open("courses.csv", "w")
    a_dict = courses
    writer = csv.writer(a_file)
    writer.writerow(['cid', 'course'])
    for key, value in a_dict.items():
        writer.writerow([key, value])
    a_file.close()

def read_course():
    with open('courses.csv', mode='r') as infile:
        reader = csv.reader(infile)
        with open('coors_new.csv', mode='w') as outfile:
            writer = csv.writer(file)
            mydict = {rows[0]:rows[1] for rows in reader}
    return mydict
#a=read_course()
#print(a["['197']"])
#print(len(a))