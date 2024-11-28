from datasets import load_dataset, Dataset, DatasetDict
import os
import pandas as pd

def create_ds():
    metadata_files = [os.path.join('Data/Metadata', file) for file in os.listdir('Data/Metadata') if file.endswith('.csv')]
    image_files = [os.path.join('Data/Image', file) for file in os.listdir('Data/Image') if file.endswith('.jpg')]
    
    ds = {'image': []}
    
    sample_df = pd.read_csv(metadata_files[0])
    for col in sample_df.columns:
        ds[col.strip()] = []
    
    print(ds.keys())

    for image_file in image_files:
        ds['image'].append(image_file)
    

    for metadata_file in metadata_files:
        temp_df = pd.read_csv(metadata_file)
        
        keyword_columns = [col for col in temp_df.columns if "keyword" in col]
        temp_df['keyword_combined'] = temp_df[keyword_columns].apply(
            lambda row: '; '.join(filter(None, row.astype(str).str.strip())), axis=1
        )
        temp_df = temp_df.drop(columns=keyword_columns)
        
        for col in temp_df.columns:
            if col not in ds:
                ds[col] = [] 
            ds[col].extend(temp_df[col].tolist())
    
    dataset = Dataset.from_dict(ds)
    dataset_dict = DatasetDict({'train': dataset})

    

    return dataset_dict
if __name__ == "__main__":
    create_ds()