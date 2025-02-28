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

    print('Getting Crash data')
    crashdf = get_data_from_csv_cleaner('stats_crashes')
    
    print('Getting Rating data')
    ratingdf = get_data_from_csv_cleaner('stats_ratings_country')

    print('Cleaning country ratings')
    ratingdf = clean_country_ratings(ratingdf)
    # Visualizing data
    print('Making the html file')
    final_html(final_df, geodf, crashdf, ratingdf, df_no_geographical)
    
if __name__ == "__main__":
    main()