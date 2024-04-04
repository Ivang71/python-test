from bs4 import BeautifulSoup
from subprocess import check_output
from utils import curl


def getCompanyUrl(detailsPageUrl):
    print(f"getting page {detailsPageUrl}")
    response = curl(detailsPageUrl)
    soup = BeautifulSoup(response, "html.parser")
    aTag = soup.find("a", class_="profile__website__link")
    return aTag.get('href') if aTag else None


def get(db, pageNumber):
    """Save companies from niche.com by page number"""
    print(f"getting page {pageNumber}")
    result = curl(f"https://www.niche.com/places-to-work/search/technology/?page={pageNumber}")
    soup = BeautifulSoup(result, "html.parser")
    companies = []

    for search_result_link in soup.find_all("a", class_="search-result__link"):
        company = {}
        company['name'] = search_result_link.get("aria-label")
        if (db.does_company_exist(company["name"])): continue
        company["url"] = getCompanyUrl(search_result_link.get("href"))
        if (company['website'].startswith('http:')):
            company['website'] = company['website'].replace("http:", "https:")
        companies.append(company)
    
    return companies


def parseEverything(db):
    for page in range(1, 66):
        for company in get(db, page):
            db.add_company(company['name'], company['url'])
