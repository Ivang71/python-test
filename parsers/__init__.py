from utils import curl
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import re
from time import sleep
from random import randint

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
            # if '<H1>302 Moved</H1>' in searchResult:
            #     print('googling too often')
            if len(searchResult) < 1e4:
                print('Triggered captcha')
                sleep(randint(67, 89))
                continue # start this iteration again
            emails.extend(list(set(re.findall(r'\b[a-z.]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', searchResult))))
            i += 1
            print(f'searched {query}, emails {emails}')
            sleep(randint(4, 7))
            
        if emails:
            forbidden_emails = ['last', '.doe']
            emails = [email for email in emails if email not in forbidden_emails]
        
        return emails if emails else None
    
    
    