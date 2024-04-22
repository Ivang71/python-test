from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


# close all google chrome insteances in your os before running the thing ⚠️⚠️⚠️⚠️⚠️⚠️⚠️
class Gmail:
    driver: webdriver
    baseMessageId: str
    
    # baseMessageId - id of email with the attachment
    def __init__(self, baseEmailId: str) -> None:
        self.baseMessageId = baseEmailId
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
        options.add_argument("--user-data-dir=/home/lao/.config/google-chrome") # provide location where chrome stores profiles
        options.add_argument('--profile-directory=Profile 3') # the profile name with which we want to open browser
        self.driver = webdriver.Chrome(options=options)
    
    def send(self, to: str, subject: str, body: str):
        sent = False
        while not sent:
            try:
                self.driver.get(f'https://mail.google.com/mail/u/0/#inbox/{self.baseMessageId}')
                find = self.driver.find_element
                try:
                    find(By.XPATH, '//span[@id=":1s"]').click() # forward button
                except:
                    # print('There is already a draft for forwarding this message')
                    pass
                sleep(2)
                find(By.XPATH, "//div[@aria-label='Type of response']").click()
                sleep(2)
                find(By.XPATH, "//div[text()='Edit subject']").find_element(By.XPATH, "./parent::*").click()
                find(By.XPATH, "//div[text()='Recipients']").find_element(By.XPATH, "./parent::*").click()
                find(By.XPATH, "//input[@aria-label='To recipients']").send_keys(to)
                subj_el = find(By.XPATH, "//input[@aria-label='Subject']")
                subj_el.clear()
                subj_el.send_keys(subject)
                body_el = find(By.XPATH, "//div[@aria-label='Message Body']")
                body_el.clear()
                body_el.send_keys(body)
                find(By.XPATH, "//div[@aria-label='Send ‪(Ctrl-Enter)‬']").click()
                sent = True
            except:
                sent = False

