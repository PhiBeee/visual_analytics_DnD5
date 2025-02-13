import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import curdoc
from bokeh.models import DatetimeTickFormatter, ColumnDataSource, CDSView, GroupFilter

def sales_volume(df: pd.DataFrame):
    # TODO: Should create a visual of sales over time in terms of at least two measures
    plot = figure(
        title='Sales over time',
        sizing_mode='scale_both',
        x_axis_label='Month and Year',
        # Still have to decide what I want here
        y_axis_label='The other Metric'
    )
    
    plot.scatter(
        x=df['Transaction Date'],
        y=df['Transaction Date']
    )
    
    plot.xaxis[0].formatter = DatetimeTickFormatter(months="%b %Y")

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
