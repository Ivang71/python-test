from data.db import CompaniesDb
from parsers import niche, Parser
from llm import Llm
from search import find_hr_emails
from utils import curl, log_email
from utils.gmail import Gmail
import re, urllib.parse, time, random, os
from dotenv import load_dotenv
from PyPDF2 import PdfReader


load_dotenv()
llm_api_key = os.environ.get('GEMINI_API_KEY')


def main():
    db = CompaniesDb()
    parser = Parser(db)
    llm = Llm(llm_api_key)
    gmail = Gmail('QgrcJHsTgszpflPjFXgXBSvjvPxZRdhRjDB')
    # db.update_message_state(131, 'none')
    # niche.parseEverything(db)
    
    companies = db.get_companies()
    companies = [c for c in companies if
                 c['website'] != None
                 and c['message_state'] == 'none']

    for company in companies:
        print(f"wokring on {company['id']} {company['name']}")
        
        if company['id'] > 500:
            break
        
        # Website text
        site_text = parser.getCompanyText(company)
        if site_text == None:
            db.update_message_state(company['id'], 'client_side_generation')
            continue # website unavailable, skip this company
        
        # Emails
        emails = parser.getCompanyEmails(company)
        if not emails:
            print(f"\033[1;31m skipping {company['name']} because did not find emails \033[0m")
            # db.update_message_state(company['id'], 'did_not_find_email')
            continue # couldn't get any emails, skip
        if len(emails) > 1:
            emails = llm.pickEmails(emails)
            db.update_company(company['id'], emails=emails)
        
        # Cover letter
        resume_text = PdfReader('resume.pdf').pages[0].extract_text().replace('\n', ' ')
        to_email = random.choice(emails)
        cover_letter = llm.writeCoverLetter(company['name'], resume_text, site_text, to_email)
        
        # Mailing
        subject = f"Frontend Developer seeking opportunity at {company['name']}"
        gmail.send(to_email, subject, cover_letter)
        log_email(to_email, subject, cover_letter)
        db.update_message_state(company['id'], 'send_first_email')


if __name__ == "__main__":
    main()
    