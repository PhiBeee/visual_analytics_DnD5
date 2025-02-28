
from math import pi
from data_preprocessing import *

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
import pandas as pd
import geopandas as gpd
from bokeh.models import DatetimeTickFormatter, Range1d, Label
import datetime
from bokeh.transform import cumsum


FONT = 'DM Sans'

df = get_data_from_csv_cleaner('sales')

df = clean_sales(df)

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

daily_sales = []
print(set(df['Day of Week']))
for day in set(df['Day of Week']):
    daydf = df[df['Day of Week'] == day]
    daily_sale = len(daydf)
    
    daily_sales.append(daily_sale)

data = {
    'days': days,
    'Daily Sales': daily_sales
}

day_fig = figure(
    title='Hourly Sales',
    width=1400,
    height=550,
    x_axis_label='Day of the Week',
    y_axis_label='Sales',
    x_range=days,
    toolbar_location=None,
    tools='hover',
    tooltips='Sales on @days: @{Daily Sales}'
)

day_fig.vbar(
    source=data,
    x='days',
    top='Daily Sales',
    width=.95,
    color='#407ee8'
)

day_fig.xgrid.grid_line_color = None
day_fig.y_range.start = 0

day_fig.title.text_font = FONT
day_fig.axis.major_label_text_font = FONT
day_fig.axis.axis_label_text_font = FONT

show(day_fig)

        