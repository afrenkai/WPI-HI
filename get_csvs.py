import re
import os
import requests
from bs4 import BeautifulSoup

if not os.path.exists('Data'):
    os.makedirs('Data')


#thoughts: make dir, fetch csv, write to corresponding file. 


            
def fetch_csv(link):
    print(f"Fetching CSV from: {link}")
    response = requests.get(link)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Failed to fetch CSV from {link} (Status code: {response.status_code})")


with open('content.txt', 'r') as f:
    content_links = f.readlines()
    for link in content_links:
        link = link.replace("?locale=en", ".csv?locale=en")
        fetch_csv(link.strip())