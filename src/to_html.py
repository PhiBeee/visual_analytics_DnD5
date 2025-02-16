from math import pi
import pandas as pd
from bokeh.plotting import figure, show, save
from bokeh.io import curdoc
from bokeh.models import DatetimeTickFormatter, ColumnDataSource, CDSView, GroupFilter, TabPanel, Tabs, Tooltip, Div
from bokeh.palettes import Bokeh8
from bokeh.transform import cumsum
from bokeh.layouts import column

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

# This function will bring together every other function to rener the final html (well as much as we can with bokeh I'd rather just be writing proper html atp)
def final_html(df: pd.DataFrame):
    top_div = Div(
        text='''Data Visualisation''',
        styles={'font-family': 'DM Sans', 'font-size': '5rem'},
        height=100,
        width=500,
        width_policy='fit',
        align='center'
    )

    # Get the Sales Volume plots
    sales_tabs = sales_volume(df)

    final_layout = column(
        children=[top_div, sales_tabs],
        align='center'
    )

    save(
        obj=final_layout,
        filename='main.html',
        title='DnD5 Data Visualisation'
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
        styles={'font-family': 'DM Sans', 'font-size': '1rem'}
    )

    return tabs
    
    

def ratings_and_stability(df: pd.DataFrame):
    # TODO: Key performance indicators to understand stability related to ratings, This is Lars task now.
    ratings_cds = ColumnDataSource(df)
    
    daily_crashes_view = CDSView(source=ratings_cds, filters=[GroupFilter(column_name='Daily Crashes', group='IDK')])#TODO: probebly want to preselect some of the data for this. Usefull columns are the date, daily & total average rating, perhaps per country?, and daily crashes and ANRs
    daily_ratings_view = CDSView(source=ratings_cds, filters=[])
    plot = figure(
	title="ratings and stability TEST",
	
    )
    pass

def geographical_view(df: pd.DataFrame):
    # TODO: Map of Sales volume and rating per coutnry (might want to separate both)
    # This stuff is just me playing around because the sales_volume has grown quite large
    plot = figure(width=300, height=300)
    plot.vbar(x=[1, 2, 3], width=0.5, bottom=0, top=[1,2,3], color="#CAB2D6")

    show(plot)
