import os
import requests

if not os.path.exists('Data/Metadata'):
    os.makedirs('Data/Metadata')

def fetch_csv(link):
    print(f"Fetching CSV from: {link}")
    response = requests.get(link)
    if response.status_code == 200:
        filename = os.path.join('Data/Metadata', os.path.basename(link).split('?')[0])
        temp = response.content
        temp = temp.decode('utf-8')
        temp = temp.strip()
        temp = temp.replace('|', ',')
        temp = '\n'.join([line.strip() for line in temp.split('\n')])
        with open(filename, 'wb') as file:
            file.write(temp.encode('utf-8'))
        print(f"Saved CSV to: {filename}")
    else:
        print(f"Failed to fetch CSV from {link} (Status code: {response.status_code})")


