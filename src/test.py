
from math import pi
from data_preprocessing import *

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
import pandas as pd
import geopandas as gpd
from bokeh.models import DatetimeTickFormatter, Range1d, Label
import datetime
from bokeh.transform import cumsum

df = get_data_from_csv_cleaner('sales')

df = clean_sales(df)

df, geodf = better_geographical_data(df)

ratingdf = get_data_from_csv_cleaner('stats_ratings_country')

ratingdf = clean_country_ratings(ratingdf)

def geographic_ratings(ratings_df: pd.DataFrame, gdf: gpd.GeoDataFrame):
    for country in set(ratings_df['Country']):
        countrydf = ratings_df[ratings_df['Country'] == country]
        rating_sum = sum(countrydf['Total Average Rating'])
        rating_avg = rating_sum/len(countrydf)
        
        gdf.loc[gdf['Country Code of Buyer']==country, 'Rating Average'] = rating_avg

    gdf = gdf.fillna(0)

    countries_with_ratings = gdf[gdf['Rating Average'] != 0]
    countries_with_no_ratings = gdf[gdf['Rating Average'] == 0]
    print(gdf)
geographic_ratings(ratingdf, geodf)
        