import requests
from bs4 import BeautifulSoup as BS
import re,string
import csvwrite,string_clean
import time, os
from datetime import datetime
import queue

def number_to_word(string):
    numbers={
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
    return_numbers=[]
    return_words=[]
    for i in string_list:
        lower_string.append(i.lower())
    for j in lower_string:    
        if j in numbers.keys():
                    return_words.append(j)
                    return_numbers.append(numbers[j])
    return return_numbers

print(number_to_word("abcA 123 3"))