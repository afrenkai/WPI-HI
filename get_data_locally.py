from get_csvs import fetch_csv
from get_imgs import fetch_img
from fetch_content_links import fetch_links
import re

LINK_PATTERN = re.compile(r'^https://digital\.wpi\.edu/concern/generic_works/[A-Za-z0-9]+\?locale=en$')


def main():
    start_page = 1
    end_page = 1
    valid_content_links = []
    for page in range(start_page, end_page + 1):
        links = fetch_links(page)
        for link in links:
            print(link)
            if LINK_PATTERN.match(link):
                if link not in valid_content_links:
                    valid_content_links.append(link)
    print(valid_content_links)
    with open('content.txt', 'w') as f:
        for line in valid_content_links:
            f.write(f"{line}\n")    
    with open('content.txt', 'r') as f:
        content_links = f.readlines()
    for link in content_links:
        fetch_img(link.strip())
        link = link.replace('?locale=en', '.csv?locale=en')
        fetch_csv(link.strip())
if __name__ == "__main__":
    main()
