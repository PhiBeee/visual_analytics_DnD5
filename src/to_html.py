# For the pie chart
from math import pi

# Filtering operations on our dataframes
import pandas as pd
import geopandas as gpd

# For the Choropleth
import json

# Bokeh shenanigans (try avoiding show if possible to test things, just use save with test.html)
from bokeh.plotting import figure, save
from bokeh.models import DatetimeTickFormatter, ColumnDataSource, CDSView, GroupFilter, GeoJSONDataSource
from bokeh.transform import cumsum
from bokeh.resources import Resources

# HTML manipulation and visuals
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import TabPanel, Tabs, Tooltip, Div, ColorBar, LinearColorMapper
from bokeh.palettes import Bokeh8, OrRd9, Viridis256, BuPu9, Oranges9, Magma11, RdPu9
from bokeh.transform import linear_cmap

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


def sales_volume(df: pd.DataFrame):
    # FIRST FIGURE

    # Get monthly entries
    df_june      = df[(df['Transaction Date'] >= '2021-06-01') & (df['Transaction Date'] < '2021-07-01')]
    df_july      = df[(df['Transaction Date'] >= '2021-07-01') & (df['Transaction Date'] < '2021-08-01')]
    df_august    = df[(df['Transaction Date'] >= '2021-08-01') & (df['Transaction Date'] < '2021-09-01')]
    df_september = df[(df['Transaction Date'] >= '2021-09-01') & (df['Transaction Date'] < '2021-10-01')]
    df_october   = df[(df['Transaction Date'] >= '2021-10-01') & (df['Transaction Date'] < '2021-11-01')]
    df_november  = df[(df['Transaction Date'] >= '2021-11-01') & (df['Transaction Date'] < '2021-12-01')]
    df_december  = df[(df['Transaction Date'] >= '2021-12-01') & (df['Transaction Date'] < '2022-01-01')] 

    monthly_dfs = [df_june, df_july, df_august, df_september, df_october, df_november, df_december]
    monthly_character = []
    monthly_premium = []

    for month in monthly_dfs:
        # Filter by specific purchase
        unlockcharacter = month[month['SKU ID'] == 'unlockcharactermanager']
        premium = month[month['SKU ID'] == 'premium']
        # Add the monthly sums to a list
        monthly_character.append(unlockcharacter['Amount (Merchant Currency)'].sum())
        monthly_premium.append(premium['Amount (Merchant Currency)'].sum())
    
    months = ['June', 'July', 'August', 'September', 'October', 'November', 'December']
    product_types = ['Premium', 'Unlock Character Manager']
    colors = ['#0236a5', '#fe0369']

    data = {'months' : months,
            'Premium':  monthly_premium,
            'Unlock Character Manager': monthly_character}

    # Change main theme (I don't like burning my eyes)
    curdoc().theme = 'dark_minimal'
    
    euro_fig = figure(
        title='Sales over time',
        width=750,
        height=500,
        x_axis_label='Month of 2021',
        y_axis_label='Revenue in EUR',
        x_range=months,
        toolbar_location=None,
        tools='hover',
        tooltips='$name @months: @$name'
    )

    euro_fig.vbar_stack(
        product_types,
        x='months',
        width=0.9,
        color=colors,
        source=data,
        muted_color=colors,
        muted_alpha=.2,
        legend_label=product_types
    )

    euro_fig.y_range.start = 0
    euro_fig.y_range.end = 1500
    euro_fig.x_range.range_padding = 0.1
    euro_fig.xgrid.grid_line_color = None
    euro_fig.axis.minor_tick_line_color = None
    euro_fig.outline_line_color = None
    euro_fig.legend.location = "top_left"
    euro_fig.legend.orientation = "horizontal"
    euro_fig.legend.click_policy = 'mute'

    euro_fig.min_border_bottom=0
    euro_fig.min_border_left=0

    # Nicer looking font idk how else to set it for everything
    euro_fig.legend.title_text_font = FONT
    euro_fig.legend.label_text_font = FONT
    euro_fig.title.text_font = FONT
    euro_fig.axis.major_label_text_font = FONT
    euro_fig.axis.axis_label_text_font = FONT

    # SECOND FIGURE 

    # Get individual currencies
    currencies = [str(currency) for currency in set(df['Currency of Sale'])]
    # Get amount of sales for main currencies >= 10 sales
    main_currencies = [currency for currency in currencies if len(df[df['Currency of Sale'] == currency]) >= 10]
    sales_per_main_currency = [len(df[df['Currency of Sale'] == currency]) for currency in main_currencies]
    # Get amount of sales for less popular currencies < 10 sales
    small_currencies = [currency for currency in currencies if len(df[df['Currency of Sale'] == currency]) < 10]
    sales_for_small_currencies = sum([len(df[df['Currency of Sale'] == currency]) for currency in small_currencies])

    sales_per_currency = sales_per_main_currency + [sales_for_small_currencies]
    used_currencies = main_currencies + ['Others']

    # dict to make it easier to turn into a df
    currency_data = {
        'Currency': used_currencies,
        'Sales'   : sales_per_currency,
    }
    
    # Turn our data back into a df to then calculate angles for our pie
    data = pd.DataFrame(currency_data)
    data['angle'] = data['Sales']/data['Sales'].sum() * 2*pi
    data['color'] = Bokeh8

    pie_fig = figure(
        title='Sales per currency',
        height=500,
        width=750,
        toolbar_location=None,
        tools='hover',
        tooltips='@Currency: @Sales',
        x_range=(-.5, 1.0)
    )

    pie_fig.wedge(
        x=.25,
        y=1,
        radius=.4,
        start_angle=cumsum('angle', include_zero=True),
        end_angle=cumsum('angle'),
        line_color='black',
        fill_color='color',
        legend_field='Currency',
        source=data
    )
    
    # Stylizing the pie
    pie_fig.axis.axis_label = None
    pie_fig.axis.visible = False
    pie_fig.grid.grid_line_color = None

    pie_fig.legend.label_text_font = FONT
    pie_fig.title.text_font= FONT

    tabs = Tabs(tabs=[
        TabPanel(child=euro_fig, title='EUR', tooltip=Tooltip(content='Sales in Euro', position='bottom_center')),
        TabPanel(child=pie_fig, title='Currencies Pie', tooltip=Tooltip(content='Amount of Sales per Currency but in a pie chart', position='bottom_center')),
        ],
        styles={'font-family': 'DM Sans', 'font-size': '1rem'},
        align='center'
    )

    return tabs, monthly_dfs
    
    

def ratings_and_stability(df: pd.DataFrame):
    # TODO: Key performance indicators to understand stability related to ratings, This is Lars task now.
    ratings_cds = ColumnDataSource(df)
    
    daily_crashes_view = CDSView(source=ratings_cds, filters=[GroupFilter(column_name='Daily Crashes', group='IDK')])#TODO: probebly want to preselect some of the data for this. Usefull columns are the date, daily & total average rating, perhaps per country?, and daily crashes and ANRs
    daily_ratings_view = CDSView(source=ratings_cds, filters=[])
    plot = figure(
	title="ratings and stability TEST",
	
    )
    pass

# This is the function from https://dmnfarrell.github.io/bioinformatics/bokeh-maps
def get_geodatasource(gdf: gpd.GeoDataFrame):
    """Get getjsondatasource from geopandas object"""
    json_data = json.dumps(json.loads(gdf.to_json()))
    return GeoJSONDataSource(geojson = json_data)

# Needs some visual and interactive improvements but I'll do that later
def geographical_view(df: pd.DataFrame, gdf: gpd.GeoDataFrame):
    curdoc().theme = 'dark_minimal'
    # Fun fact: Puerto Rico and Argentina use USD, which is why the choropleth has less sales in the USA than the pie in USD
    
    # Filter out the countries we initially had data for
    currencies_with_sales = df[df['_merge'] == 'both']
    currencies_with_sales = set(currencies_with_sales['Country Code of Buyer'])

    # Get and array of tuples (Country Code, Sales)
    sales_per_currency = [(country_code, len(df[df['Country Code of Buyer'] == country_code])) for country_code in set(df['Country Code of Buyer'])]
    sales_per_currency = pd.DataFrame(sales_per_currency, columns=['Country Code of Buyer','Sales'])
    
    # Adjust for the fact that the countries with no sales now have a row because of our outer merge
    meow = sales_per_currency[~sales_per_currency['Country Code of Buyer'].isin(currencies_with_sales)]
    # It suddenly started not liking this but is behaving properly so whatever
    meow['Sales'] = meow['Sales']-1
    sales_per_currency[~sales_per_currency['Country Code of Buyer'].isin(currencies_with_sales)] = meow

    # 38 countries with sales
    gdf = gdf.merge(
        right=sales_per_currency,
        left_on='Country Code of Buyer',
        right_on='Country Code of Buyer',
    )

    # Separating for better colouring
    gdf_no_sales = gdf[gdf['Sales']==0]
    gdf_sales = gdf[gdf['Sales']!=0]

    geosource_sales = get_geodatasource(gdf_sales)
    geosource_no_sales = get_geodatasource(gdf_no_sales)

    # Visualizing part
    palette = RdPu9[:-2]
    palette = palette[::-1]

    cmap = LinearColorMapper(
        palette=palette,
        low=1,
        high=115,
    )

    cbar = ColorBar(
        color_mapper=cmap,
        label_standoff=9,
        width=500,
        height=20,
        location=(550,0),
        orientation='horizontal'
    )

    choropleth = figure(
        title='Sales per country',
        toolbar_location=None,
        tools='hover',
        tooltips='@{Country of Buyer}: @Sales',
        x_axis_location=None,
        y_axis_location=None,
        width=1600,
        height=900
    )

    choropleth.grid.grid_line_color = None

    choropleth.patches(
        xs='xs',
        ys='ys',
        source=geosource_sales,
        fill_alpha=.7,
        line_width=.5,
        line_color='black',
        fill_color={
            'field': 'Sales',
            'transform': cmap,
        }
    )

    choropleth.add_layout(
        cbar,
        'below'
    )

    choropleth.patches(
        xs='xs',
        ys='ys',
        source=geosource_no_sales,
        fill_alpha=.7,
        line_width=.5,
        line_color='black',
        fill_color=RdPu9[-1]
    )

    choropleth.title.text_font = FONT

    return choropleth

def geographical_over_time(monthly_dfs, gdf: gpd.GeoDataFrame):
    curdoc().theme = 'dark_minimal'

    sales_per_currency_per_month = []
    for month in monthly_dfs:
        # Filter out the countries we initially had data for
        currencies_with_sales = month[month['_merge'] == 'both']
        currencies_with_sales = set(currencies_with_sales['Country Code of Buyer'])

        # Get and array of tuples (Country Code, Sales)
        sales_per_currency = [(country_code, len(month[month['Country Code of Buyer'] == country_code])) for country_code in currencies_with_sales]
        sales_per_currency = pd.DataFrame(sales_per_currency, columns=['Country Code of Buyer','Sales'])

        sales_per_currency_per_month.append(sales_per_currency)

    print(sale)
    for month in sales_per_currency:
        print(month)
