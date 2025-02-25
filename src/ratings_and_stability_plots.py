# Filtering operations on our dataframes
import pandas as pd
import geopandas as gpd

# Bokeh shenanigans (try avoiding show if possible to test things, just use save with test.html)
from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter, ColumnDataSource, CDSView, GroupFilter

# HTML manipulation and visuals
from bokeh.models import TabPanel, Tabs, Tooltip, Div
from bokeh.palettes import Bokeh8

FONT = 'DM Sans'

def ratings_and_stability(crashdf: pd.DataFrame, ratingdf: pd.DataFrame):
    # TODO: Key performance indicators to understand stability related to ratings, This is Lars task now.
    
    #works with panda's dataframe. grab total average rating (for that month) and sum daily crashes and ANR. Lineplot with crashes on x-axis, and ratings on the y axis
    #TODO: Later, the visuals. First make this function in a basic way.
    
    #filtered_df = df[df['column_name'] == 'row_data']
    # let's try absolute scaling
    #crashdf['Daily Crashes'] = crashdf['Daily Crashes']  /crashdf['Daily Crashes'].abs().max() #works well enough
    #crashdf['Daily ANRs'] = crashdf['Daily ANRs']  /crashdf['Daily ANRs'].abs().max() #will this work?
    #ratingdf['Total Average Rating'] = ratingdf['Total Average Rating'] /ratingdf['Total Average Rating'].abs().max() 
    # Get monthly entries
    df_june      = crashdf[(crashdf['Date'] >= '2021-06-01') & (crashdf['Date'] < '2021-07-01')]
    df_july      = crashdf[(crashdf['Date'] >= '2021-07-01') & (crashdf['Date'] < '2021-08-01')]
    df_august    = crashdf[(crashdf['Date'] >= '2021-08-01') & (crashdf['Date'] < '2021-09-01')]
    df_september = crashdf[(crashdf['Date'] >= '2021-09-01') & (crashdf['Date'] < '2021-10-01')]
    df_october   = crashdf[(crashdf['Date'] >= '2021-10-01') & (crashdf['Date'] < '2021-11-01')]
    df_november  = crashdf[(crashdf['Date'] >= '2021-11-01') & (crashdf['Date'] < '2021-12-01')]
    df_december  = crashdf[(crashdf['Date'] >= '2021-12-01') & (crashdf['Date'] < '2022-01-01')]

    # Get monthly entries, but for ratings now
    df_june_rating      = ratingdf[(ratingdf['Date'] >= '2021-06-01') & (ratingdf['Date'] < '2021-07-01')]
    df_july_rating      = ratingdf[(ratingdf['Date'] >= '2021-07-01') & (ratingdf['Date'] < '2021-08-01')]
    df_august_rating    = ratingdf[(ratingdf['Date'] >= '2021-08-01') & (ratingdf['Date'] < '2021-09-01')]
    df_september_rating = ratingdf[(ratingdf['Date'] >= '2021-09-01') & (ratingdf['Date'] < '2021-10-01')]
    df_october_rating   = ratingdf[(ratingdf['Date'] >= '2021-10-01') & (ratingdf['Date'] < '2021-11-01')]
    df_november_rating  = ratingdf[(ratingdf['Date'] >= '2021-11-01') & (ratingdf['Date'] < '2021-12-01')]
    df_december_rating  = ratingdf[(ratingdf['Date'] >= '2021-12-01') & (ratingdf['Date'] < '2022-01-01')]  

    monthly_dfs = [df_june, df_july, df_august, df_september, df_october, df_november, df_december]
    monthly_dfs_ratings = [df_june_rating, df_july_rating, df_august_rating, df_september_rating, df_october_rating, df_november_rating, df_december_rating]
    monthly_crashes = []
    monthly_ARNs = []
    monthly_average_ratings = []

    for month in monthly_dfs:
        # grab the crashes and ARNs
        crashes = month['Daily Crashes'] 
        ANR = month['Daily ANRs']
        # Add the monthly sums to a list
        monthly_crashes.append(crashes.sum()/200)#do note the division, as it does 'change' the data
        monthly_ARNs.append(ANR.sum()/5)#do note the division, as it does 'change' the data
    for month in monthly_dfs_ratings:
        notNAperMonth = 0
        totalMonth = 0
        betterMonth = month[~month['Daily Average Rating'].isna()]
        for value in betterMonth['Daily Average Rating']:
            notNAperMonth += 1
            totalMonth += value
        monthly_average_rating = totalMonth/notNAperMonth
        monthly_average_ratings.append((monthly_average_rating))

    
    months = ['June', 'July', 'August', 'September', 'October', 'November', 'December']

    data = {'months' : months, #now play around with plotting what where
            'ratings':  monthly_average_ratings,
            'crashes': monthly_crashes,
            'ANRs': monthly_ARNs}
    
    crashes_fig = figure(
	    title="Ratings compared to Stability",
        width= 650,
        height=500,
        x_axis_label='Month of 2021',
        y_axis_label='Average number of Xs that month',
        x_range=months,#other things like tooltip stuff might be nice
        toolbar_location=None,
        tools='hover',
        tooltips='@months: rating @ratings: crashes/200 @crashes: ANRs/5 @ANRs'
    )
    crashes_fig.line(
        x='months',
        y='ratings',
        color='blue',
        legend_label="ratings", 
        line_width=2,
        source = data
    )
    crashes_fig.line(
        x='months',
        y='crashes',
        color='red',
        legend_label="crashes /200", 
        line_width=2,
        source = data
    )
    crashes_fig.line(
        x='months',
        y='ANRs',
        color='yellow',
        legend_label="ANRs /5", 
        line_width=2,
        source = data
    )

    # Nicer looking font idk how else to set it for everything
    crashes_fig.legend.title_text_font = FONT
    crashes_fig.legend.label_text_font = FONT
    crashes_fig.title.text_font = FONT
    crashes_fig.axis.major_label_text_font = FONT
    crashes_fig.axis.axis_label_text_font = FONT

    return crashes_fig