import re
import os
import requests
from bs4 import BeautifulSoup
import shutil
if not os.path.exists('Data/Image'):
    os.makedirs('Data/Image')


IMG_PATTERN = re.compile(r'/downloads/[A-Za-z0-9]+\?file=thumbnail$')


def fetch_img(link):
    response = requests.get(link)
    if response.status_code == 200:
        filename = os.path.join('Data/Image', os.path.basename(link).split('?')[0])
        filename += '.jpg'
        soup = BeautifulSoup(response.text, 'html.parser')
        imgs = soup.findAll('img')
        for img in imgs:
            if IMG_PATTERN.match(img['src']):
                img_link = f"https://digital.wpi.edu{img['src']}"
                img_response = requests.get(img_link, stream=True)
                if img_response.status_code == 200:
                    with open(filename, 'wb') as file:
                        shutil.copyfileobj(img_response.raw, file)
                    print(f"Saved image to: {filename}")
                else:
                    print(f"Failed to fetch image from {img_link} (Status code: {img_response.status_code})")
                