import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

utf16_encoded_files = ["reviews", "stats_crashes", "stats_ratings_country", "stats_ratings_overview"]
utf8_encoded_files = ["sales"]

product_id = "com.vansteinengroentjes.apps.ddfive"

# Should return a pandas dataframe with the data from the csv files in that dir
def get_data_from_csv(data_type: str):
    path_to_data = "data/"
    # These are currently all separate just in case one of the files needs special pre-processing but will probably combine them later down the line
    match data_type:
        case "reviews":
            # Add the specific folder
            path_to_data += data_type
            # Grab all files from the specified dir and turn them into pandas DataFrames (there should only be csv files in the directory else this blows up)
            data_frames = [pd.read_csv(join(path_to_data,file), encoding='utf-16', header=0) for file in listdir(path_to_data) if isfile(join(path_to_data, file))]
            final_df = pd.concat(data_frames, ignore_index=True)
            return final_df 
        case "sales":
            # Add the specific folder
            path_to_data += data_type
            # THESE FILES FOR SOME GODFORSAKEN REASON HAVE A DIFFERENT ENCODING
            data_frames = [pd.read_csv(join(path_to_data,file), encoding='utf-8', header=0) for file in listdir(path_to_data) if isfile(join(path_to_data, file))]
            final_df = pd.concat(data_frames, ignore_index=True)
            return final_df 
        case "stats_crashes":
            # Add the specific folder
            path_to_data += data_type
            # Grab all files from the specified dir and turn them into pandas DataFrames (there should only be csv files in the directory else this blows up)
            data_frames = [pd.read_csv(join(path_to_data,file), encoding='utf-16', header=0) for file in listdir(path_to_data) if isfile(join(path_to_data, file))]
            final_df = pd.concat(data_frames, ignore_index=True)
            return final_df 
        case "stats_ratings_country":
            # Add the specific folder
            path_to_data += data_type
            # Grab all files from the specified dir and turn them into pandas DataFrames (there should only be csv files in the directory else this blows up)
            data_frames = [pd.read_csv(join(path_to_data,file), encoding='utf-16', header=0) for file in listdir(path_to_data) if isfile(join(path_to_data, file))]
            final_df = pd.concat(data_frames, ignore_index=True)
            return final_df 
        case "stats_ratings_overview":
            # Add the specific folder
            path_to_data += data_type
            # Grab all files from the specified dir and turn them into pandas DataFrames (there should only be csv files in the directory else this blows up)
            data_frames = [pd.read_csv(join(path_to_data,file), encoding='utf-16', header=0) for file in listdir(path_to_data) if isfile(join(path_to_data, file))]
            final_df = pd.concat(data_frames, ignore_index=True)
            return final_df 

def get_data_from_csv_cleaner(data_type: str) -> pd.DataFrame:
    path_to_data = "data/"
    if data_type in utf16_encoded_files:
        # Add the specific folder to the path
        path_to_data += data_type
        
        # Grab all files from the specified dir and turn them into pandas DataFrames (there should only be csv files in the directory else this blows up)
        data_frames = [pd.read_csv(join(path_to_data,file), encoding='utf-16', header=0) for file in listdir(path_to_data) if isfile(join(path_to_data, file))]
        final_df = pd.concat(data_frames, ignore_index=True)
        
        return final_df 
    elif data_type in utf8_encoded_files:
        # Add the specific folder to the path
        path_to_data += data_type
        
        # THESE FILES FOR SOME GODFORSAKEN REASON HAVE A DIFFERENT ENCODING
        data_frames = [pd.read_csv(join(path_to_data,file), encoding='utf-8', header=0) for file in listdir(path_to_data) if isfile(join(path_to_data, file))]
        final_df = pd.concat(data_frames, ignore_index=True)
        
        return final_df 
    
def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
                
    merge_from = ['Hardware'    , 'Sku Id', 'Description' , 'Order Charged Date', 'Product id', 'Buyer State'   , 'Buyer Country'   , 'Buyer Postal Code'   , 'Financial Status', 'Buyer Currency'  , 'Amount (Buyer Currency)']
    merge_to   = ['Device Model', 'SKU ID', 'Order Number', 'Transaction Date'  , 'Product ID', 'State of Buyer', 'Country of Buyer', 'Postal Code of Buyer', 'Transaction Type', 'Currency of Sale', 'Charged Amount'         ]
    
    # Deal with columns that need to get merged
    for to_idx, merge_from_col in enumerate(merge_from):
        merge_to_col = merge_to[to_idx]
                
        # Check if both columns are of the same type and turn into float if either of them is float
        if df[merge_to_col].dtype != df[merge_from_col].dtype:
            if df[merge_to_col].dtype != "object":
                # Format Currency Strings
                df[merge_from_col] = df[merge_from_col].replace('[$€£,]', '', regex=True).astype(float)
                # Change column type to appropriate type
                df[merge_from_col] = df[merge_from_col].astype(float)
            elif df[merge_from_col].dtype != "object":
                df[merge_to_col] = df[merge_to_col].replace('[$€£,]', '', regex=True).astype(float)
                df[merge_to_col] = df[merge_to_col].astype(float)
            else:
                df[merge_from_col] = df[merge_from_col].astype(object)
            
        # Fill in the NaN with the appropriate values depending on dtype
        if df[merge_to_col].dtype != "object":
            df[[merge_from_col, merge_to_col]] = df[[merge_from_col, merge_to_col]].fillna(0)
        else:
            df[[merge_from_col, merge_to_col]] = df[[merge_from_col, merge_to_col]].fillna('')
        
        
        # Merge columns
        df[merge_to_col] += df[merge_from_col]
        # Get rid of redundant column
        df = df.drop(merge_from_col, axis=1)
        
        # Get rid of unnecessary rows early
        match merge_to_col:
            case 'Product ID':
                # Filter to only the app we want
                df = df[df[merge_to_col] == product_id]
                continue
            case 'Transaction Type':
                # Filter out anything that's not a Charge
                df = df[df[merge_to_col].isin(['Charge', 'Charged'])]
                continue
        
    # Product Type (0 = paidapp, 1 = inapp)
    return df