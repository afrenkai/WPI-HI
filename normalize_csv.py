import csv
import os
from tqdm import tqdm
def norm():
    metadata_files = [os.path.join('Data/Metadata', file) for file in os.listdir('Data/Metadata') if file.endswith('.csv')]          
    for file in tqdm(metadata_files):
        with open(file, newline='', encoding='utf-8') as f:
            c = csv.reader(f)
            normed = list(c)
        
        if len(normed) < 2:
            print (f' skipping {file} since theres only 1 row somehow')
            continue

        headers = [header.strip() for header in normed[0]]
        values = [value.strip() for value in normed[1]]

        normed[0] = headers
        normed[1] = values

        with open(file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(normed)

        # print(f'updated headers in {file}: {headers}')
        




if __name__ == "__main__":
    norm()




