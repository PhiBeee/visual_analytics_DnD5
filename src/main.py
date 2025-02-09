from data_preprocessing import *

def main():
    df = get_data_from_csv_cleaner("reviews")
    print(df)
    df = get_data_from_csv("sales")
    print(df)
    df = get_data_from_csv("stats_crashes")
    print(df)
    df = get_data_from_csv("stats_ratings_country")
    print(df)
    df = get_data_from_csv("stats_ratings_overview")
    print(df)

if __name__ == "__main__":
    main()