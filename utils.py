import requests
from bs4 import BeautifulSoup



if __name__ == "__main__":
    html = requests.get('https://digital.wpi.edu/collections/hi?locale=en')
    html = html.content

    end_page = get_end_page(html)
    print(end_page)