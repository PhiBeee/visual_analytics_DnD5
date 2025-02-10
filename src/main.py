from data_preprocessing import *

def main():
    df = get_data_from_csv_cleaner("sales")
    print(df['Device Model'])
    df = clean_sales(df)
    print(df['Device Model'])

if __name__ == "__main__":
    main()