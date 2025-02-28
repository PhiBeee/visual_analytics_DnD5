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
from bokeh.models import DatetimeTickFormatter, ColumnDataSource, CDSView, GroupFilter, CustomJS, Select
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
      <a class='active' href="https://liacs.leidenuniv.nl/~s3555380/main.html">Home</a>
      <a href="https://liacs.leidenuniv.nl/~s3555380/choropleth.html">Geographic Data</a>
      <a href="https://liacs.leidenuniv.nl/~s3555380/crashes.html">Crashes and Ratings</a>
      <img src="https://complete-reference.com/img/logo2.png" width=65 height=65>
    </div>
"""

# This function will bring together every other function to render the final html (well as much as we can with bokeh I'd rather just be writing proper html atp)
def final_html(df:pd.DataFrame, geodf: gpd.GeoDataFrame, crashdf: pd.DataFrame, ratingdf: pd.DataFrame):
    # DATA AND PLOTTING

    # Get the Sales Volume plots
    sales_bar, sales_fig, currency_pie, monthly_dfs = sales_volume(df)

    # old choropleth func
    # choropleth = geographical_view(df, geodf)

    monthly_choro = geographical_over_time(monthly_dfs, geodf)
    monthly_choro_2 = geographical_over_time(monthly_dfs, geodf)

    hourly_figure = hourly_sales_fig(df)

    donut, text = donut_plot(df, monthly_dfs)

    rating_choro, sales_choro = geographic_ratings(df, ratingdf, geodf)
    rating_choro_2, sales_choro_2 = geographic_ratings(df, ratingdf, geodf)

    # Get the new ratings and stability thing, hopefully
    stability_plot = ratings_and_stability(crashdf,ratingdf) #nothing returned right now

    # Cool select for geograhic data
    rating_choro_2.visible = False
    monthly_choro.visible = False

    select = Select(title="Metric to show:", value="Ratings", options=["Ratings", "Revenue", 'Monthly Sales'])
    select.js_on_change("value", CustomJS(args=dict(sales_choro=sales_choro, rating_choro=rating_choro, monthly_choro=monthly_choro), code="""

    sales_choro.visible = true
    rating_choro.visible = true
    monthly_choro.visible = true

    if (this.value === "Ratings") {
        sales_choro.visible = false 
        monthly_choro.visible = false
    } else if (this.value === "Revenue") {
        rating_choro.visible = false
        monthly_choro.visible = false
    } else {
        sales_choro.visible = false
        rating_choro.visible = false
    }
        
    """))

    select_2 = Select(title="Metric to show:", value="Monthly Sales", options=["Ratings", "Revenue", 'Monthly Sales'])
    select_2.js_on_change("value", CustomJS(args=dict(sales_choro_2=sales_choro_2, rating_choro_2=rating_choro_2, monthly_choro_2=monthly_choro_2), code="""

    sales_choro_2.visible = true
    rating_choro_2.visible = true
    monthly_choro_2.visible = true

    if (this.value === "Ratings") {
        sales_choro_2.visible = false 
        monthly_choro_2.visible = false
    } else if (this.value === "Revenue") {
        rating_choro_2.visible = false
        monthly_choro_2.visible = false
    } else {
        sales_choro_2.visible = false
        rating_choro_2.visible = false
    }
        
    """))

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
            vertical-align: top;
        }

        .topnav{
            background-color: #080808;
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

    # Sales Data

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

    # Geographic Data  

    choro_style = styles.clone()
    choro_ressources = resources.clone()
    choro_page = column(
        children=[select_2, monthly_choro_2, rating_choro_2, sales_choro_2],
        stylesheets=[choro_style],
        align='center'
    )

    choro_page_2 = column(
        children=[select, monthly_choro, rating_choro, sales_choro],
        align='center'
    )

    buh = column(
        children=[choro_page, choro_page_2],
        align='center'
    )

    save(
        obj=buh,
        filename='choropleths.html',
        title='DnD5 Data Visualisation',
        resources=choro_ressources
    )

    # Crashes and Ratings

    crashes_style = styles.clone()
    crashes_resources = resources.clone()

    crashes_page = column(
        children=[stability_plot],
        stylesheets=[crashes_style],
        align='center'
    )

    save(
        obj=crashes_page,
        filename='crashes.html',
        title='DnD5 Data Visualisation',
        resources=crashes_resources
    )