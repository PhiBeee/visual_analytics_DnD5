# For the pie chart
from math import pi

# Filtering operations on our dataframes
import pandas as pd

# Bokeh shenanigans (try avoiding show if possible to test things, just use save with test.html)
from bokeh.plotting import figure
from bokeh.transform import cumsum

# HTML manipulation and visuals
from bokeh.io import curdoc
from bokeh.models import TabPanel, Tabs, Tooltip
from bokeh.palettes import Bokeh8

FONT = 'DM Sans'

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