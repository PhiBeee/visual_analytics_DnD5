
from math import pi
from data_preprocessing import *

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
import pandas as pd
from bokeh.models import DatetimeTickFormatter, Range1d, Label
import datetime
from bokeh.transform import cumsum

df = get_data_from_csv_cleaner('sales')

df = clean_sales(df)