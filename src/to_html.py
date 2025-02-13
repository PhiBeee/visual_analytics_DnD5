import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import curdoc
from bokeh.models import DatetimeTickFormatter, ColumnDataSource, CDSView, GroupFilter

def sales_volume(df: pd.DataFrame):
    # TODO: Should create a visual of sales over time in terms of at least two measures
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
    colors = ['blue', 'red']

    data = {'months' : months,
            'Premium':  monthly_premium,
            'Unlock Character Manager': monthly_character}
    
    plot = figure(
        title='Sales over time',
        width=500,
        height=500,
        x_axis_label='Month of 2021',
        # Still have to decide what I want here
        y_axis_label='Revenue in EUR',
        x_range=months,
        tools='hover',
        tooltips='$name @months: @$name'
    )

    plot.vbar_stack(product_types, x='months', width=0.9, color=colors, source=data, legend_label=product_types)

    plot.y_range.start = 0
    plot.y_range.end = 1500
    plot.x_range.range_padding = 0.1
    plot.xgrid.grid_line_color = None
    plot.axis.minor_tick_line_color = None
    plot.outline_line_color = None
    plot.legend.location = "top_left"
    plot.legend.orientation = "horizontal"

    curdoc().theme = 'caliber'

    show(plot)
    
    

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
    pass
