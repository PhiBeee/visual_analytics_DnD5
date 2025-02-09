from data_preprocessing import *

def main():
    df = get_data_from_csv_cleaner("sales")
    print(df)
    df = clean_sales(df)
    print(df.columns)

if __name__ == "__main__":
    main()