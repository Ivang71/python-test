import subprocess, random, datetime, time
from time import time, sleep

then = time() - 1

def curl(url):
    now = time()
    wait_time = 1 - (now - then)
    if wait_time > 0:
        sleep(wait_time)
    command = 'curl_chrome' + random.choice(['99', '100', '101', '104', '107', '110', '116'])
    return subprocess.run([command, url, '-sL'], stdout=subprocess.PIPE).stdout.decode('utf-8')


def log_email(to_email, subject, cover_letter):
    with open('sent_emails.txt', 'a') as f:
        f.write(f"{datetime.datetime.now()}\n{to_email}\n{subject}\n\n{cover_letter}\n{'—'*200}\n\n")
    
