import re
import requests
from googlesearch import search

def findCompanyWebsiteUrl(company_name):
    query = f'{company_name} website'
    searchResults = search(query, num_results=1)
    for result in searchResults:
        if 'http' in result:  # Filter out non-link results
            return result

    return []

def extractEmails(url):
    response = requests.get(url)
    htmlContent = response.text
    emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.findall(emailRegex, htmlContent)

def filterEmails(emailList):
    unwantedWords = ["help", "support", "customer"]
    return [email for email in emailList if not any(word in email.lower() for word in unwantedWords)]


def getEmailsByCompanyName(companyName):
    companyWebsite = findCompanyWebsiteUrl(companyName)
    emails = extractEmails(companyWebsite)
    filteredEmails = filterEmails(emails)
    return filteredEmails

# emails = set()
# emails.update(getEmailsForCompany('CloEE'))
# print(emails)

import requests
from bs4 import BeautifulSoup

countriesList = [
    "austrian", "belgian", "bulgarian", "croatian", "cyprus", "czech",
    "danish", "estonian", "finnish", "french", "german", "greek",
    "hungarian", "irish", "italian", "latvian", "lithuanian", "luxembourg-based",
    "maltese", "dutch", "norwegian", "polish", "portuguese", "romanian",
    "slovakia", "slovenian", "spanish", "swedish", "switzerland", "british"
]

baseUrl = "https://www.eu-startups.com/directory/wpbdp_category/"

for country in countriesList:
    page = 1

    while True:
        url = f"{baseUrl}{country}-startups/page/{page}"
        response = requests.get(url)
        page += 1

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            divs = soup.find_all("div", class_="listing-title")
            companyNames = [div.get_text().strip() for div in divs]
            emailsLists = [getEmailsByCompanyName(name) for name in companyNames]
            emails = set([item for sublist in emailsLists for item in sublist])
            with open("emails.txt", "w") as f:
                [f.write(email + "\n") for email in emails]
            print('iteration completed')    
        else:
            break
    
        
