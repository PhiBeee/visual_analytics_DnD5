from data_preprocessing import *
from to_html import *

def main():
    # Data pre-processing
    print('Getting the data from csv file')
    df = get_data_from_csv_cleaner("sales")

    print('Cleaning sales data')
    df_no_geographical = clean_sales(df)

    print('Getting geographical data')
    final_df, geodf = better_geographical_data(df_no_geographical)

    crashdf = get_data_from_csv_cleaner('stats_crashes')
    
    ratingdf = get_data_from_csv_cleaner('stats_ratings_country')
    # Visualizing data
    print('Making the html file')
    final_html(final_df, geodf, crashdf, ratingdf)
    
if __name__ == "__main__":
    main()