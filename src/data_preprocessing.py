# Data handling modules
import pandas as pd
import geopandas as gpd

# Used for country code conversion
import country_converter as cc

# Used for getting the files with our data
from os import listdir
from os.path import isfile, join

utf16_encoded_files = ["reviews", "stats_crashes", "stats_ratings_country", "stats_ratings_overview"]
utf8_encoded_files = ["sales"]

product_id = "com.vansteinengroentjes.apps.ddfive"
shapefile = 'GeoBoundaries/geoBoundariesCGAZ_ADM0.shp'
puerto_rico_shapefile = 'GeoBoundaries/PRI_adm0.shp'
better_shapefile = 'betterGeoBoundaries/ne_110m_admin_0_countries.shp'

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
                
    merge_from = ['Hardware'    , 'Sku Id', 'Description' , 'Product id', 'Buyer State'   , 'Buyer Country'   , 'Buyer Postal Code'   , 'Financial Status', 'Buyer Currency'  , 'Amount (Buyer Currency)']
    merge_to   = ['Device Model', 'SKU ID', 'Order Number', 'Product ID', 'State of Buyer', 'Country of Buyer', 'Postal Code of Buyer', 'Transaction Type', 'Currency of Sale', 'Charged Amount'         ]
    
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
        
    # Product Type (0 = paidapp, 1 = inapp) Data changes midway through the csv's so we normalize
    df.loc[df['Product Type'] == 0, 'Product Type'] = 'paidapp'
    df.loc[df['Product Type'] == 1, 'Product Type'] = 'inapp'
    
    time_columns = ['Transaction Time', 'Order Charged Timestamp']
    date_columns = ['Transaction Date', 'Order Charged Date'     ]
    
    for date_idx, time_column in enumerate(time_columns):
        date_column = date_columns[date_idx]
        # Naive approach 
        if date_idx == 0:
            # Fill NaN so I can use replace without it screaming at me (Not needed)
            # df[[date_column, time_column]] = df[[date_column, time_column]].fillna('')
            
            # Change Timezone so it stops screaming at me (I gave up on timezone and I am hoping it doesn't matter)
            df[time_column] = df[time_column].str.replace(r'PDT', '', regex=True)
        
            df[date_column] = pd.to_datetime(df[date_column])
            # Format this one because there is no point in having the date twice
            df[time_column] = pd.to_datetime(df[time_column], format='mixed')
            # Also timezone thing 
            # df[time_column] = df[time_column].tz_convert(tz='CET')
            df[time_column] = df[time_column].dt.time
        else:
            # Convert to the datetime dtype
            df[[time_column, date_column]] = df[[time_column, date_column]].astype('datetime64[s]')
            df[time_column] = df[time_column].dt.time
    
    # Merge the Columns that mean the same thing
    list_of_lists = [time_columns, date_columns]
    for columns in list_of_lists:
        df[columns[0]] = df[columns[0]].fillna(df[columns[1]])
        # Get rid of duplicate data
        df = df.drop(columns[1], axis=1)
    
    # Conversion Rates taken from https://www.exchange-rates.org/exchange-rate-history/[cop, crc, nzd]-eur-2021
    currency_conversions_2021 = {'NZD': 0.598, 'CRC': 0.001361, 'COP': 0.0002260}   
    
    # Fill Conversion Rate column to have a rough Euro value for every sale         
    for currency in set(df['Currency of Sale']):
        # Remove entries without a conversion rate
        df_currency = df[~df['Currency Conversion Rate'].isna()]
        # Take current currency rows to check if we can sample to a conversion rate
        df_currency = df_currency[df_currency['Currency of Sale'] == currency]
        # No conversion rate
        if df_currency.empty:
            # Very long looking way of filling in the NaN for the currency rows in the Conversion Rate Column with a value from previously defined list
            df[df['Currency of Sale'] == currency] = df[df['Currency of Sale'] == currency].fillna(value={'Currency Conversion Rate':currency_conversions_2021[currency]})
        else:
            sample_conversion = df_currency['Currency Conversion Rate'].sample(1)
            #                                                                                                            This part over here gets upset without cast to float and iloc
            df[df['Currency of Sale'] == currency] = df[df['Currency of Sale'] == currency].fillna(value={'Currency Conversion Rate':float(sample_conversion.iloc[0])})
    
    # Fills the column of charged amount in Euro, recalculated entries but they're the same value, but more precise
    df['Amount (Merchant Currency)'] = df['Currency Conversion Rate'] * df['Charged Amount']

    # Convenience rename to be clearer
    df = df.rename(
        columns={
            'Country of Buyer': 'Country Code of Buyer'
        }
    )
    
    return df

def clean_country_ratings(df: pd.DataFrame):
    # This is here really just for being here sake, the data is already filtered
    # Filter to only the app we want
    df = df[df['Package Name'] == product_id]
    #Convert the country code to iso3 so we can use it with the shapefile
    iso3_cc = cc.convert(
        names=df['Country'],
        to='ISO3'
    )  

    df['Country'] = iso3_cc
    
    return df 

# This function adds geometry data to our df to make a choropleth
def better_geographical_data(df: pd.DataFrame) -> pd.DataFrame:
    iso3_cc = cc.convert(
        names=df['Country Code of Buyer'],
        to='ISO3'
    )

    # Replace old data
    df['Country Code of Buyer'] = iso3_cc

    geometry = gpd.read_file(better_shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    geometry = geometry.rename(
        columns={
            'ADMIN': 'Country of Buyer',
            'ADM0_A3': 'Country Code of Buyer'
        }
    )

    # Merge the two add geometry data to original db
    merged_df = df.merge(
        right=geometry,
        how='outer',
        left_on='Country Code of Buyer',
        right_on='Country Code of Buyer',
        indicator=True
    )

    return merged_df, geometry