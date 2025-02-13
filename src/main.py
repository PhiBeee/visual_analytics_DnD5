from data_preprocessing import *
from to_html import *

def main():
    df = get_data_from_csv_cleaner("sales")
    df = clean_sales(df)
    print(df.dtypes)

# THIS IS A TEST
    
if __name__ == "__main__":
    main()