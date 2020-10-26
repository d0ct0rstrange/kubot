import requests
from bs4 import BeautifulSoup as BS
import re,string
import csvwrite
import time, os


def listToString(s):  
    
    # initialize an empty string 
    str1 = " " 
    
    # return string   
    return (str1.join(s)) 

def clean_string(sname):
    #sub_list = ["\n", "\r"] 
    #sname=" BCA\r\n BCA\r\n . (332)"
    for subs in sub_list:
        sname_filtered = listToString(sname.splitlines())
    sname_filtered=str(sname_filtered)
    print(sname_filtered)
    return sname_filtered