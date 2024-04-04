from data.db import JobSearchDatabase
from parsers import niche, Parser
from llm import Llm
from search import find_hr_emails
from utils import curl
import re, urllib.parse, time, random, os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from utils.gmail import Gmail


load_dotenv()
llm_api_key = os.environ.get('GEMINI_API_KEY')


def main():
    pass
    # db = JobSearchDatabase()
    # parser = Parser(db)
    # llm = Llm(llm_api_key)
    gmail = Gmail()
    gmail.send('rewwer356@gmail.com', 'Test 1', 'No credentials found. Please set up Application Default Credentials.')
    # # niche.parseEverything(db)
    
    # companies = db.get_companies()
    # companies = [c for c in companies if c['message_state'] == 'none' and c['website'] != None]
    
    # company = companies[41]
    
    # site_text = parser.getCompanyText(company) # getting text and emails
    # if site_text == None:
    #     db.update_message_state(company['id'], 'client_side_generation')
    #     # continue # website unavailable, skip this company
    # emails = parser.getCompanyEmails(company)
    # # attempts = 5
    # # while(len(emails) < 1):
    # #     emails = parser.getCompanyEmails(company)
    # #     attempts -= 1
        
    # if len(emails) > 1:
    #     emails = llm.pickEmails(emails)
    #     # db.update_company(company['id'], emails=emails)
    
    # resume_text = PdfReader('resume.pdf').pages[0].extract_text().replace('\n', ' ')
    
    # coverLetter = llm.writeCoverLetter(company['name'], resume_text, site_text, random.choice(emails))
    # # send resume to the email
    
    
    # # for company in companies:
    # #     print(company)


if __name__ == "__main__":
    main()
    