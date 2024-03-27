import subprocess
import random

def curl(url):
    command = 'curl_chrome' + random.choice(['99', '100', '101', '104', '107', '110', '116'])
    return subprocess.run([command, url, '-s'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    
    