import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import curdoc
from bokeh.models import DatetimeTickFormatter

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
    # TODO: Key performance indicators to understand stability related to ratings
    pass

def geographical_view(df: pd.DataFrame):
    # TODO: Map of Sales volume and rating per coutnry (might want to separate both)
    pass