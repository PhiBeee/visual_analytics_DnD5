from data_preprocessing import *

def main():
    df = get_data_from_csv_cleaner("sales")
    df = clean_sales(df)
    print(df['Currency Conversion Rate'])
    
    
if __name__ == "__main__":
    main()