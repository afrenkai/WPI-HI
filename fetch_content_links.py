import requests
from bs4 import BeautifulSoup
import re
base_url = "https://digital.wpi.edu/collections/hi?locale=en&page="
link_pattern = re.compile(r'^https://digital\.wpi\.edu/concern/generic_works/[A-Za-z0-9]+\?locale=en$')
pattern = re.compile(r'https://digital\.wpi\.edu/concern/generic_works/[A-Za-z0-9]+\.csv\?locale=en')

def fetch_links(page_number):
    url = f"{base_url}{page_number}"
    print(f"Fetching page: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [
            a['href'] for a in soup.find_all('a', href=True)
            if '/concern/generic_works/' in a['href'] and a['href'].endswith('?locale=en')
        ]
        return [f"https://digital.wpi.edu{link}" for link in links]
    return []

def extract_content_details(link):
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        images = [img['src'] for img in soup.find_all('img', src=True)]
        csv_link = f"{link.split('?')[0]}.csv?locale=en"
        return {"images": images, "csv": csv_link}
    return {"images": [], "csv": None}

def sanitize_filename(filename):
    return filename.split('?')[0]  # Removes everything after '?' including '?locale=en' coz shitter behaviour 

def download_file(url, folder, filename):
    sanitized_filename = sanitize_filename(filename)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, sanitized_filename), 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

def download_content(content_mapping, output_folder="downloads"):
    for content_id, details in content_mapping.items():
        content_folder = os.path.join(output_folder, content_id)
        if details["csv"]:
            csv_name = details["csv"].split('/')[-1]
            download_file(details["csv"], content_folder, csv_name)
        for idx, img_url in enumerate(details["images"]):
            img_name = f"image_{idx + 1}.jpg"
            download_file(img_url, content_folder, img_name)

def main():
    base_url = "https://digital.wpi.edu/collections/hi?locale=en&page="
    start_page = 1
    end_page = 2
    valid_content_links = []
    for page in range(start_page, end_page + 1):
        links = fetch_links(base_url, page)
        for link in links:
            print(link)
            if link_pattern.match(link):
                if link not in valid_content_links:
                    valid_content_links.append(link)
    print(valid_content_links)
    with open('content.txt', 'w') as f:
        for line in valid_content_links:
            f.write(f"{line}\n")
if __name__ == "__main__":
    main()

    