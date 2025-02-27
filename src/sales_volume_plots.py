# For the pie chart
from math import pi

# Filtering operations on our dataframes
import pandas as pd

# Bokeh shenanigans (try avoiding show if possible to test things, just use save with test.html)
from bokeh.plotting import figure
from bokeh.transform import cumsum

# HTML manipulation and visuals
from bokeh.io import curdoc
from bokeh.palettes import Spectral8
from bokeh.models import LabelSet, ColumnDataSource

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
    monthly_total_revenue = []
    monthly_character_amount = []
    monthly_premium_amount = []
    monthly_total_amount = []

    for month in monthly_dfs:
        # Filter by specific purchase
        unlockcharacter = month[month['SKU ID'] == 'unlockcharactermanager']
        premium = month[month['SKU ID'] == 'premium']

        unlockcharacter_rev = unlockcharacter['Amount (Merchant Currency)'].sum()
        premium_rev = premium['Amount (Merchant Currency)'].sum()

        rev_total = unlockcharacter_rev + premium_rev
        rev_total = round(rev_total, 2)

        unlockcharacter_sales = len(unlockcharacter)
        premium_sales = len(premium)
        total_sales = unlockcharacter_sales + premium_sales
        
        # Add the monthly sums to a list
        monthly_character.append(unlockcharacter_rev)
        monthly_premium.append(premium_rev)
        monthly_total_revenue.append(rev_total)
        # Add monthly sales to their lists
        monthly_character_amount.append(unlockcharacter_sales)
        monthly_premium_amount.append(premium_sales)
        monthly_total_amount.append(total_sales)
    
    months = ['June', 'July', 'August', 'September', 'October', 'November', 'December']
    product_types = ['Premium', 'Unlock Character Manager']
    product_counts = ['Unlock Character Manager Sales', 'Premium Sales']
    colors = ['#407ee8', '#fe0369']

    data = {'months' : months,
            'Premium':  monthly_premium,
            'Unlock Character Manager': monthly_character,
            'Unlock Character Manager Sales': monthly_character_amount,
            'Premium Sales': monthly_premium_amount,
            'Total Revenue': monthly_total_revenue,
            'Total Sales': monthly_total_amount}

    # Change main theme (I don't like burning my eyes)
    curdoc().theme = 'dark_minimal'
    
    euro_fig = figure(
        title='Revenue over time',
        width=750,
        height=500,
        x_axis_label='Month of 2021',
        y_axis_label='Revenue in EUR',
        x_range=months,
        toolbar_location=None,
        tools='hover',
        tooltips='$name in @months: @$name{0,0.00} €',
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

    label_data = ColumnDataSource(data)

    euro_labelset = LabelSet(
        source=label_data,
        x='months',
        y='Total Revenue',
        text='Total Revenue',
        level='glyph',
        text_font='DM Sans',
        text_color='white',
        y_offset=5,
        x_offset=-25
    )

    euro_fig.add_layout(euro_labelset)

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
    euro_fig.axis.axis_label_text_align = 'left'

    # SECOND FIGURE
    
    sales_fig = figure(
        title='Sales over time',
        width=750,
        height=500,
        x_axis_label='Month of 2021',
        y_axis_label='Sales',
        x_range=months,
        toolbar_location=None,
        tools='hover',
        tooltips='$name in @months: @$name',
    )

    sales_fig.vbar_stack(
        product_counts,
        x='months',
        width=0.9,
        color=colors,
        source=data,
        muted_color=colors,
        muted_alpha=.2,
        legend_label=product_counts
    )

    sales_labelset = LabelSet(
        source=label_data,
        x='months',
        y='Total Sales',
        text='Total Sales',
        level='glyph',
        text_font='DM Sans',
        text_color='white',
        y_offset=5,
        x_offset=-15
    )

    sales_fig.add_layout(sales_labelset)

    sales_fig.y_range.start = 0
    sales_fig.y_range.end = 400
    sales_fig.x_range.range_padding = 0.1
    sales_fig.xgrid.grid_line_color = None
    sales_fig.axis.minor_tick_line_color = None
    sales_fig.outline_line_color = None
    sales_fig.legend.location = "top_left"
    sales_fig.legend.orientation = "horizontal"
    sales_fig.legend.click_policy = 'mute'

    sales_fig.min_border_bottom=0
    sales_fig.min_border_left=0

    # Nicer looking font idk how else to set it for everything
    sales_fig.legend.title_text_font = FONT
    sales_fig.legend.label_text_font = FONT
    sales_fig.title.text_font = FONT
    sales_fig.axis.major_label_text_font = FONT
    sales_fig.axis.axis_label_text_font = FONT
    sales_fig.axis.axis_label_text_align = 'left'

    # THIRD FIGURE 

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
    data['color'] = Spectral8

    pie_fig = figure(
        title='Sales per currency',
        height=350,
        width=350,
        toolbar_location=None,
        tools='hover',
        tooltips='@Currency: @Sales',
        x_range=(-.5, 1.0),
    )

    pie_fig.wedge(
        x=.10,
        y=1,
        radius=.5,
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
    pie_fig.background_fill_color= (21, 25, 28)
    pie_fig.outline_line_color = '#15191c'

    pie_fig.legend.label_text_font = FONT
    pie_fig.title.text_font= FONT
    pie_fig.title.align = 'center'

    

    return euro_fig, sales_fig, pie_fig, monthly_dfs