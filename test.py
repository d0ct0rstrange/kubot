import requests
from bs4 import BeautifulSoup as BS
import re,string
import time, os
from datetime import datetime
import queue
from difflib import SequenceMatcher

import csvwrite,string_clean
import csv
import db

def similarity_between_strings(a,b):
	return SequenceMatcher(None, a, b).ratio()

print(similarity_between_strings(".b.s.c.","!b!s!c!"))