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
def final_html(df:pd.DataFrame, geodf: gpd.GeoDataFrame):
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

    final_layout = column(
        children=[top_div, sales_tabs, choropleth],
        align='center'
    )

    save(
        obj=final_layout,
        filename='main.html',
        title='DnD5 Data Visualisation',
        resources=resources
    )    

def ratings_and_stability(df: pd.DataFrame):
    # TODO: Key performance indicators to understand stability related to ratings, This is Lars task now.
    ratings_cds = ColumnDataSource(df)
    
    daily_crashes_view = CDSView(source=ratings_cds, filters=[GroupFilter(column_name='Daily Crashes', group='IDK')])#TODO: probebly want to preselect some of the data for this. Usefull columns are the date, daily & total average rating, perhaps per country?, and daily crashes and ANRs
    daily_ratings_view = CDSView(source=ratings_cds, filters=[])
    plot = figure(
	title="ratings and stability TEST",
	
    )
    pass
