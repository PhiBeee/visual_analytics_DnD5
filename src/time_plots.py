from bokeh.plotting import figure

import pandas as pd
import datetime

FONT = 'DM Sans'

def convert(buh: str):
    format = '%H:%M:%S'
    datetime_str = datetime.datetime.strptime(buh, format)

    return datetime_str

def hourly_sales_fig(df: pd.DataFrame):
    # DATA HANDLING

    hourly_dfs = []
    times = []
    sales = []

    for i in range(24):
        current_hour = str(i)+':00:00'
        next_hour = str(i+1)+':00:00'

        if i < 9:
            current_hour = '0'+str(i)+':00:00'
            next_hour = '0'+str(i+1)+':00:00'
        elif i == 9:
            current_hour = '0'+str(i)+':00:00'
        elif i == 23:
            next_hour = '23:59:59'

        if i < 10:
            times.append(current_hour[1:-3])
        else:
            times.append(current_hour[:-3])

        # Convert to datetime.time so we can actually compare (it doesnt like strings :( )
        current_hour = convert(current_hour).time()
        next_hour = convert(next_hour).time()

        # Make our filter here to avoid having a stupidly long line of code
        filter = (df['Transaction Time'] >= current_hour) & (df['Transaction Time'] < next_hour)

        hourly_df = df[filter]

        hourly_dfs.append(hourly_df)
        sales.append(len(hourly_df))
    
    data = {
        'Time': times,
        'Sales': sales
    }

    # DATA VISUALIZING

    hourly_fig = figure(
        title='Hourly Sales',
        width=1400,
        height=550,
        x_axis_label='Hour of the day',
        y_axis_label='Sales',
        x_range=times,
        toolbar_location=None,
        tools='hover',
        tooltips='Sales at @Time: @Sales'
    )

    hourly_fig.vbar(
        source=data,
        x='Time',
        top='Sales',
        width=.95,
        color='#407ee8'
    )

    hourly_fig.line(
        source=data,
        x='Time',
        y='Sales',
        color='#fe0369',
        line_width=2
    )
    
    hourly_fig.xgrid.grid_line_color = None
    hourly_fig.y_range.start = 0

    hourly_fig.title.text_font = FONT
    hourly_fig.axis.major_label_text_font = FONT
    hourly_fig.axis.axis_label_text_font = FONT

    return hourly_fig
