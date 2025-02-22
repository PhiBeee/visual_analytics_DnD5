from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
import pandas as pd
from bokeh.models import DatetimeTickFormatter

# Sample data
dates = pd.date_range('2024-01-01', periods=10)
values = [5, 6, 7, 8, 7, 5, 4, 6, 8, 9]

# Create a ColumnDataSource
source = ColumnDataSource(data=dict(date=dates, value=values))


# Create a new plot with a datetime x-axis
p = figure(x_axis_type='datetime', title="Datetime Axis Example")

# Customize the x-axis tick format
p.xaxis.formatter = DatetimeTickFormatter(
    days="%d %b %Y",
    months="%b %Y",
    years="%Y"
)

print(source.data)

# Add a line renderer
p.line('date', 'value', source=source, line_width=2)