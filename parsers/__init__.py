from utils import curl
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import re, time, random

class Parser:
    db = None
    
    
    def __init__(self, db) -> None:
        self.db = db
    
    
    def getCompanyText(self, company):
        response = curl(company['website'])
        text = BeautifulSoup(response, "html.parser").get_text(' ').replace("\t", "").replace("\n", "")
        text = ' '.join(text.split()) 
        if (len(text) < 300): # if the page has client side rendering and does not have enough content
            # self.db.update_message_state(company['id'], 'client_side_generation')
            return None
        return text
    
    
    def getCompanyEmails(self, company):
        domain = re.search(r"(?:https?://)?(?:www\.)?([^\.]+\.[^\.]+)", company['website']).group(1)
        emails = []
        # keywords = ['hr', 'email', 'contact', 'info', 'support']
        keywords = ['hr', 'email', 'contact']
        i = 0
        while(len(emails) < 4 and i < len(keywords)):
            query = f"{keywords[i]} @{domain}"
            searchResult = curl(f'https://www.google.com/search?q={quote_plus(query)}')
            emails.extend(list(set(re.findall(r'\b[a-z.]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', searchResult))))
            i += 1
            time.sleep(random.randint(1, 2))
        
        return emails if emails else None
    
    
    