from subprocess import check_output
from bs4 import BeautifulSoup
import re
import urllib.parse
from utils import curl

def find_hr_emails(url):
    term = urllib.parse.quote_plus('hr @promodel.com')
    response = curl(f"https://www.google.com/search?q={term}")
    email_regex = r'[a-z]{2,}+@[\w-]+\.[\w.-]+'
    return list(set(re.findall(email_regex, response, flags=re.UNICODE)))
    

