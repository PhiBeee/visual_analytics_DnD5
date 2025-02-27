# Splitting up the code because the fie was getting long
from geographic_plots import *
from sales_volume_plots import *
from ratings_and_stability_plots import *
from time_plots import *
from donut_plot import *

# Filtering operations on our dataframes
import pandas as pd
import geopandas as gpd

# Bokeh shenanigans (try avoiding show if possible to test things, just use save with test.html)
from bokeh.plotting import figure, save
from bokeh.models import DatetimeTickFormatter, ColumnDataSource, CDSView, GroupFilter
from bokeh.resources import Resources

# HTML manipulation and visuals
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Div, GlobalInlineStyleSheet

FONT = 'DM Sans'

"""
These need to be added to the final html head to get the right font and look, otherwise it's boring
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&display=swap" rel="stylesheet">
# navigation bar to be added to each html file, because bokeh does funky stuff
    <div class="topnav">
      <a class='active' href="/main.html">Home</a>
      <a href="/chropleth.html">Geographic Data</a>
      <img src="https://complete-reference.com/img/logo2.png" width=60 height=60>
    </div>
"""

# This function will bring together every other function to render the final html (well as much as we can with bokeh I'd rather just be writing proper html atp)
def final_html(df:pd.DataFrame, geodf: gpd.GeoDataFrame, crashdf: pd.DataFrame, ratingdf: pd.DataFrame):
    # DATA AND PLOTTING

    # Get the Sales Volume plots
    sales_bar, sales_fig, currency_pie, monthly_dfs = sales_volume(df)

    # old choropleth func
    # choropleth = geographical_view(df, geodf)

    multi_line, monthly_choro = geographical_over_time(monthly_dfs, geodf)

    hourly_figure = hourly_sales_fig(df)

    donut, text = donut_plot(df, monthly_dfs)

    # Get the new ratings and stability thing, hopefully
    stability_plot = ratings_and_stability(crashdf,ratingdf) #nothing returned right now

    # LAYOUT AND STYLING
    resources =  Resources(
        mode='cdn',
    )

    styles = GlobalInlineStyleSheet(
        css='''
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

        .topnav{
            background-color: #0c0d0f;
            overflow: hidden;
        }

        .topnav a{
            float: left;
            color: white;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
            font-size: 2em;
            font-family: DM Sans;
        }

        .topnav img{
            float: right;
        }

        .topnav a:hover {
            background-color: #38761d;
            color: white:
        }

        .topnav a.active {
            background-color: green;
            color: white;
        }
        '''
    )

    top_row = row(
        children=[sales_bar, sales_fig],
        align='center'
    )

    bottom_row = row(
        children=[hourly_figure],
        align='center'
    )

    right_col = column(
        children=[text, donut, currency_pie],
        align='center'
    )
    
    top_column = column(
        children=[top_row, bottom_row],
        align='center'
    )

    chungus = row(
        children=[top_column, right_col],
        stylesheets=[styles]
    )

    final_layout = column(
        children=[chungus],
        align='center'
    )

    save(
        obj=final_layout,
        filename='main.html',
        title='DnD5 Data Visualisation',
        resources=resources
    )    

    choro_style = styles.clone()
    choro_ressources = resources.clone()
    choro_page = column(
        children=[monthly_choro],
        stylesheets=[choro_style],
        align='center'
    )

    save(
        obj=choro_page,
        filename='choropleths.html',
        title='DnD5 Data Visualisation',
        resources=choro_ressources
    )