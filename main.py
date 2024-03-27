from data.db import JobSearchDatabase
import subprocess
from parsers import niche
from search import find_hr_emails
from utils import curl
from bs4 import BeautifulSoup

if __name__ == "__main__":
    db = JobSearchDatabase()    
    # niche.parseWholeNiche()
    
    
    
    companies = db.get_companies()
    companies = [company for company in companies if company['message_state'] == 'none']
    
    c = companies[49]
    if (c['website'] == None):
        pass
    if (c['website'].startswith('http:')):
        c['website'] = c['website'].replace("http:", "https:")
    # company_text = curl(c['website'])
    # print(company_text)
    
    for company in companies:
        pass
    