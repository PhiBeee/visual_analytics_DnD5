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
    # Makes merging columns work 
    # df = df.fillna('')
    for column in df.columns:
        if df.dtypes[column] != "object":
            df[column] = df[column].fillna(0)
        else:
            df[column] = df[column].fillna('')
    
    merge_from = ['Hardware'    , 'Sku Id', 'Description' , 'Order Charged Date', 'Product id', 'Buyer State'   , 'Buyer Country'   , 'Buyer Postal Code'   , 'Financial Status', 'Buyer Currency'  , 'Amount (Buyer Currency)']
    merge_to   = ['Device Model', 'SKU ID', 'Order Number', 'Transaction Date'  , 'Product ID', 'State of Buyer', 'Country of Buyer', 'Postal Code of Buyer', 'Transaction Type', 'Currency of Sale', 'Charged Amount'         ]
    
    for to_idx, merge_from_col in enumerate(merge_from):
        merge_to_col = merge_to[to_idx]
        print(f"{merge_from_col}:{merge_to_col}")
        df[merge_to_col] += df[merge_from_col]
        # Get rid of redundant column
        df = df.drop(merge_from_col, axis=1)
        match merge_to_col:
            case 'Product ID':
                # Filter to only the app we want
                df = df[df[merge_to_col] == product_id]
                continue
            case 'Transaction Type':
                # Filter out anything that's not a Charge
                df = df[df[merge_to_col] == "Charge"]
                continue
    
    
    # Hardware = Device Model
    # Sku Id = SKU ID
    # Order Number = Description
    # Transaction Date = Order Charged Date
    # Product id = Product ID
    # Product Type (0 = paidapp, 1 = inapp)
    # State of Buyer = Buyer State
    # Country of Buyer = Buyer Country
    # Postal Code of Buyer = Buyer Postal Code
    # Transaction Type = Financial Status (Charged = Charge)
    # Currency of Sale = Buyer Currency
    # Charged Amount = Amount (Buyer Currency)
    return df