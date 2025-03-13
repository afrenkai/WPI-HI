# pyright: reportMissingImports=false
from datasets import Dataset, DatasetDict, Features, Value, Image
import os
import pandas as pd

def create_ds():
    metadata_files = [os.path.join('Data/Metadata', file) for file in os.listdir('Data/Metadata') if file.endswith('.csv')]
    print('metadata files made')
    image_files = sorted([os.path.join('Data/Image', file) for file in os.listdir('Data/Image') if file.endswith('.jpg')])
    print('img files made')

    all_metadata = []
    print('blank md list made')
    for mdfile in metadata_files:
        sample_df = pd.read_csv(mdfile)
        sample_df.reset_index(drop = True, inplace = True)
        all_metadata.append(sample_df)
        print(f'added {mdfile} to metadata df')
    if not all_metadata:
        raise ValueError('404 md not found lol')

    metadata_df = pd.concat(all_metadata, ignore_index=True).astype(str) #temp fix for pitch, need to fix later 
    print('metadata df made')
    ds = {'image': image_files  }

    for col in metadata_df.columns:
        ds[col] = metadata_df[col].tolist()

    
    features = Features({
        'image': Image(), 
        **{col: Value('string') for col in metadata_df.columns} 
    })
  
    dataset = Dataset.from_dict(ds, features=features) 
    dataset_dict = DatasetDict({'train': dataset})

    dataset_dict.push_to_hub('afrenkai/WPI-Historical-Image-Collection')

    return dataset_dict

if __name__ == "__main__":
    dataset_dict = create_ds()
    print(dataset_dict)

