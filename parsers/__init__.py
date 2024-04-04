from utils import curl
from bs4 import BeautifulSoup
import re, urllib.parse

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
        # for keyword in ['hr', 'contact', 'info', 'support']:
        domain = re.search(r"(?:https?://)?(?:www\.)?([^\.]+\.[^\.]+)", company['website']).group(1)
        query = f"contact @{domain}"
        searchResult = curl(f'https://www.google.com/search?q={urllib.parse.quote_plus(query)}')
        return list(set(re.findall(r'\b[a-z.]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', searchResult)))
        #     time.sleep(random.randint(1, 2))
    
    
    