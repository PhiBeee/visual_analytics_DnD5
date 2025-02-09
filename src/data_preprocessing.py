import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

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

# Reduces the data to what we need 
def clean_data(dataframe):
    pass