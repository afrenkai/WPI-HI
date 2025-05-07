# pyright: reportMissingImports=false
from datasets import Dataset, DatasetDict, Features, Value, Image
import os
import pandas as pd
from tqdm import tqdm
import re

def feat_type(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return Value("int32")
    elif pd.api.types.is_float_dtype(dtype):
        return Value("float32")
    elif pd.api.types.is_bool_dtype(dtype):
        return Value("bool")
    else:
        return Value("string")

def create_ds():
    metadata_files = [os.path.join('Data/Metadata', file) for file in os.listdir('Data/Metadata') if file.endswith('.csv')]
    # print('metadata files made')
    image_files = sorted([os.path.join('Data/Image', file) for file in os.listdir('Data/Image') if file.endswith('.jpg')])
    # print('img files made')

    all_metadata = []
    # print('blank md list made')
    for mdfile in tqdm(metadata_files):
        sample_df = pd.read_csv(mdfile)
        sample_df.reset_index(drop = True, inplace = True)
        all_metadata.append(sample_df)
        # print(f'added {mdfile} to metadata df')
    if not all_metadata:
        raise ValueError('404 md not found lol')
    # print('all md dfs made')
    metadata_df = pd.concat(tqdm(all_metadata), ignore_index=True) 
    #print(metadata_df.isnull().sum())
    # metadata_df = metadata_df.fillna('').astype(str)
    print('metadata df made')
    
    ds = {'image': image_files}
    good_col = []
    for col in tqdm(metadata_df.columns):
        print(col)
        col_comp = re.sub(r"(?=\.\d|d)(?:\.?\d*)", '', col )
        print(col_comp)
        if col_comp not in ds.keys():
            good_col.append(col)
            ds[col] = metadata_df[col].tolist() 
            print(f'added {col_comp}')


    

    features = Features({'image': Image(),
                **{col: feat_type(metadata_df[col]) for col in good_col}})

    dataset = Dataset.from_dict(ds, features = features)
    print(type(dataset['image']))

    dataset_dict = DatasetDict({'train': dataset})
    dataset_dict.push_to_hub('afrenkai/WPI-Historical-Image-Collection')

    return dataset_dict

if __name__ == "__main__":
    dataset_dict = create_ds()
    print(dataset_dict)

