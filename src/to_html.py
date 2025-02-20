# Splitting up the code because the fie was getting long
from geographic_plots import *
from sales_volume_plots import *

# For the pie chart
from math import pi

# Filtering operations on our dataframes
import pandas as pd
import geopandas as gpd

# Bokeh shenanigans (try avoiding show if possible to test things, just use save with test.html)
from bokeh.plotting import figure, save
from bokeh.models import DatetimeTickFormatter, ColumnDataSource, CDSView, GroupFilter
from bokeh.transform import cumsum
from bokeh.resources import Resources

# HTML manipulation and visuals
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import TabPanel, Tabs, Tooltip, Div
from bokeh.palettes import Bokeh8

FONT = 'DM Sans'

"""
These need to be added to the final html head to get the right font and look, otherwise it's boring
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&display=swap" rel="stylesheet">
    <style>
      html, body {
        box-sizing: border-box;
        padding: 0;
        background-color: #15191c;
        color: white;
        align-items: center;
      }

      html{
        display: table;
        margin: auto;
      }

      body{
        display: table-cell;
        vertical-align: middle;
      }
      
    </style>
"""

# This function will bring together every other function to render the final html (well as much as we can with bokeh I'd rather just be writing proper html atp)
def final_html(df:pd.DataFrame, geodf: gpd.GeoDataFrame, crashdf: pd.DataFrame, ratingdf: pd.DataFrame):
    resources =  Resources(
        mode='cdn',
    )

    title_div = Div(
        text='''Dashboard for ''',
        styles={'font-family': 'DM Sans', 'font-size': '4rem', 'text-align':'center'},
        height=100,
        width=500,
        width_policy='fit',
        align='center'
    )

    img_div = Div(
        text='<img src="https://complete-reference.com/img/logo2.png" width=100 height=100>',
        styles={'font-family': 'DM Sans', 'max-width':'50%', 'max-height':'50%', 'height': 'auto'},
        height=100,
        width=100,
        width_policy='fit',
        align='center'
    )

    top_div = row(
        children=[title_div, img_div],
        align='center'
    )

    # Get the Sales Volume plots
    sales_tabs, monthly_dfs = sales_volume(df)

    # Get our awesome choropleth
    choropleth = geographical_view(df, geodf)

    geographical_over_time(monthly_dfs, geodf)

    # Get the new ratings and stability thing, hopefully
    stability_plot = ratings_and_stability(crashdf,ratingdf) #nothing returned right now

    final_layout = column(
        children=[top_div, sales_tabs, choropleth, stability_plot],
        align='center'
    )

    save(
        obj=final_layout,
        filename='main.html',
        title='DnD5 Data Visualisation',
        resources=resources
    )    

def ratings_and_stability(crashdf: pd.DataFrame, ratingdf: pd.DataFrame):
    # TODO: Key performance indicators to understand stability related to ratings, This is Lars task now.
    
    #works with panda's dataframe. grab total average rating (for that month) and sum daily crashes and ANR. Lineplot with crashes on x-axis, and ratings on the y axis
    #TODO: Later, the visuals. First make this function in a basic way.
    
    #filtered_df = df[df['column_name'] == 'row_data']

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
        monthly_crashes.append(crashes.sum()/200)
        monthly_ARNs.append(ANR.sum()/5)
    for month in monthly_dfs_ratings:
        monthly_average_rating = month['Total Average Rating'].iloc[0] #will this work? let's find out
        monthly_average_ratings.append((monthly_average_rating-4.5)*100)

    
    months = ['June', 'July', 'August', 'September', 'October', 'November', 'December']

    data = {'months' : months, #now play around with plotting what where
            'ratings':  monthly_average_ratings,
            'crashes': monthly_crashes,
            'ANRs': monthly_ARNs}
    
    crashes_fig = figure(
	    title="ratings and stability TEST",
        width= 800,
        height=800,
        x_axis_label='Month of 2021',
        y_axis_label='Other data?',
        x_range=months,#other things like tooltip stuff might be nice
        toolbar_location=None,
        tools='hover',
        tooltips='@months: @data?'
    )
    crashes_fig.line(
        x='months',
        y='ratings',
        color='blue',
        legend_label="Temp.", 
        line_width=2,
        source = data
    )
    crashes_fig.line(
        x='months',
        y='crashes',
        color='red',
        legend_label="Temp.", 
        line_width=2,
        source = data
    )
    crashes_fig.line(
        x='months',
        y='ANRs',
        color='yellow',
        legend_label="Temp.", 
        line_width=2,
        source = data
    )
    return crashes_fig
