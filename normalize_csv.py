import csv
import os

def norm():
    metadata_files = [os.path.join('Data/Metadata', file) for file in os.listdir('Data/Metadata') if file.endswith('.csv')]          
    for file in metadata_files:
        with open(file, newline='', encoding='utf-8') as f:
            c = csv.reader(f)
            normed = list(c)
        
        headers = [header.strip() for header in normed[0]]
        normed[0] = headers
        with open(file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(normed)

        print(f'updated headers in {file}: {headers}')
        




if __name__ == "__main__":
    norm()




