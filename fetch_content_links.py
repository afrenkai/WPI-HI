import requests
from bs4 import BeautifulSoup
import re

BASE_URL = 'https://digital.wpi.edu/collections/hi?locale=en&page='
LINK_PATTERN = re.compile(r'^https://digital\.wpi\.edu/concern/generic_works/[A-Za-z0-9]+\?locale=en$')

def fetch_links(page_number: int):
    url = f'{BASE_URL}{page_number}'
    print(f'Fetching page: {url}')
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [
            a['href'] for a in soup.find_all('a', href=True)
            if '/concern/generic_works/' in a['href'] and a['href'].endswith('?locale=en')
        ]
        return [f'https://digital.wpi.edu{link}' for link in links]
    else:
        print(f'Failed to fetch page {page_number} (Status code: {response.status_code})')
        return []

def fetch_content(link):
    print(f'Fetching content from: {link}')
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup.prettify())
        print('\n' + '=' * 80 + '\n') 
    else:
        print(f'Failed to fetch content from {link} (Status code: {response.status_code})')

def fetch_csv(link):
    # print(f'Fetching CSV from: {link}')
    response = requests.get(f'{link}.csv')
    if response.status_code == 200:
        print(response.text)
    else:
        print(f'Failed to fetch CSV from {link} (Status code: {response.status_code})')



def get_end_page(html: str) -> int:
    base_page = BeautifulSoup(html, 'html.parser')
    page_num_unextract = str(base_page.find_all("li")[-1])
    page_num = page_num_unextract.split(">")
    page_num = page_num[2].split("<")[0]
    return int(page_num)

def main():
    start_page = 1
    end_page = get_end_page('https://digital.wpi.edu/collections/hi?locale=en')
    valid_content_links = []
    for page in range(start_page, end_page + 1):
        links = fetch_links(page)
        for link in links:
            #print(link)
            if LINK_PATTERN.match(link):
                if link not in valid_content_links:
                    valid_content_links.append(link)
    print(valid_content_links)
    with open('content.txt', 'w') as f:
        for line in valid_content_links:
            f.write(f"{line}\n")
if __name__ == "__main__":
    main()
