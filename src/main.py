from data_preprocessing import *
from to_html import *

def main():
    df = get_data_from_csv_cleaner("sales")
    df = clean_sales(df)

    sales_volume(df)
    # geographical_view(df)
    
if __name__ == "__main__":
    main()