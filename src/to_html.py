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
from bokeh.plotting import save
from bokeh.models import DatetimeTickFormatter, CustomJS, Select
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
      <a href="https://liacs.leidenuniv.nl/~s3555380/choropleths.html">Geographic Data</a>
      <a href="https://liacs.leidenuniv.nl/~s3555380/crashes.html">Crashes and Ratings</a>
      <img src="https://complete-reference.com/img/logo2.png" width=65 height=65>
    </div>
"""

# This function will bring together every other function to render the final html (well as much as we can with bokeh I'd rather just be writing proper html atp)
def final_html(df:pd.DataFrame, geodf: gpd.GeoDataFrame, crashdf: pd.DataFrame, ratingdf: pd.DataFrame, df_no_geographical: pd.DataFrame):
    # DATA AND PLOTTING

    # Get the Sales Volume plots
    sales_bar, sales_fig, currency_pie, monthly_dfs = sales_volume(df)

    # old choropleth func
    # choropleth = geographical_view(df, geodf)

    monthly_choro = geographical_over_time(monthly_dfs, geodf)
    monthly_choro_2 = geographical_over_time(monthly_dfs, geodf)

    hourly_figure = hourly_sales_fig(df)
    daily_figure = day_of_week_fig(df_no_geographical)

    donut, text = donut_plot(df, monthly_dfs)

    rating_choro, sales_choro = geographic_ratings(df, ratingdf, geodf)
    rating_choro_2, sales_choro_2 = geographic_ratings(df, ratingdf, geodf)

    # Get the new ratings and stability thing, hopefully
    stability_plot, cumulative_plot, stats_fig, over_time_fig = ratings_and_stability(crashdf,ratingdf, monthly_dfs) #nothing returned right now

    # Cool select for geograhic data
    rating_choro_2.visible = False
    monthly_choro.visible = False

    select_style = '''
    .bk-input {
        background-color: #15191c;
        color: white;
    }
    '''

    select = Select(title="Metric to show:", value="Ratings", options=["Ratings", "Revenue", 'Monthly Sales'], styles={'font-family': 'DM Sans'},stylesheets=[select_style])
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

    select_2 = Select(title="Metric to show:", value="Monthly Sales", options=["Ratings", "Revenue", 'Monthly Sales'], styles={'font-family': 'DM Sans'}, stylesheets=[select_style])
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

    select_time = Select(title="Metric to show:", value="Daily", options=["Daily", "Hourly"], styles={'font-family': 'DM Sans'}, stylesheets=[select_style])
    select_time.js_on_change("value", CustomJS(args=dict(daily_figure=daily_figure, hourly_figure=hourly_figure), code="""

    daily_figure.visible = true
    hourly_figure.visible = true

    if (this.value === "Daily") {
        hourly_figure.visible = false 
    } else {
        daily_figure.visible = false
    }
        
    """))

    select_buh = Select(title="Metric to show:", value="Cumulative", options=["Cumulative", "Monthly"], styles={'font-family': 'DM Sans'}, stylesheets=[select_style])
    select_buh.js_on_change("value", CustomJS(args=dict(cumulative_plot=cumulative_plot, over_time_fig=over_time_fig), code="""

    cumulative_plot.visible = true
    over_time_fig.visible = true

    if (this.value === "Cumulative") {
        over_time_fig.visible = false 
    } else {
        cumulative_plot.visible = false
    }
        
    """))

    # LAYOUT AND STYLING
    resources =  Resources(
        mode='cdn',
    )

    # Put the styles in their own file so that it doesn't clog up this
    css = open('style.css').read()
    styles = GlobalInlineStyleSheet(
        css=css
    )

    # Sales Data

    top_row = row(
        children=[sales_bar, sales_fig],
        align='center'
    )

    funky_select = column(
        children=[select_time, hourly_figure, daily_figure],
        align='center'
    )

    bottom_row = row(
        children=[funky_select],
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
    choro_page = row(
        children=[select_2, monthly_choro_2, rating_choro_2, sales_choro_2],
        stylesheets=[choro_style],
        align='center'
    )

    choro_page_2 = row(
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

    crashes_page = row(
        children=[stability_plot, select_buh, cumulative_plot, over_time_fig],
        stylesheets=[crashes_style],
        align='center'
    )

    over_time_fig.visible = False

    crashe_main = column(
        children=[stats_fig, crashes_page],
        align='center'
    )

    save(
        obj=crashe_main,
        filename='crashes.html',
        title='DnD5 Data Visualisation',
        resources=crashes_resources
    )