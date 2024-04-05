import subprocess, random, datetime


def curl(url):
    command = 'curl_chrome' + random.choice(['99', '100', '101', '104', '107', '110', '116'])
    return subprocess.run([command, url, '-sL'], stdout=subprocess.PIPE).stdout.decode('utf-8')


def log_email(to_email, subject, cover_letter):
    with open('sent_emails.txt', 'a') as f:
        f.write(f"{datetime.datetime.now()}\n{to_email}\n{subject}\n\n{cover_letter}\n{'—'*200}\n\n")
    
