# For the pie chart
from math import pi

# Filtering operations on our dataframes
import pandas as pd

# Bokeh shenanigans (try avoiding show if possible to test things, just use save with test.html)
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.models import Range1d, Label

FONT = 'DM Sans'

def donut_plot(df: pd.DataFrame):
    unlockcharacter = df[df['SKU ID'] == 'unlockcharactermanager']
    premium = df[df['SKU ID'] == 'premium']

    unlockcharacter_total = unlockcharacter['Amount (Merchant Currency)'].sum()
    premium_total = premium['Amount (Merchant Currency)'].sum()

    total = unlockcharacter_total + premium_total
    premium_percentage = premium_total/total*100
    unlockcharacter_percentage = unlockcharacter_total/total*100

    premium_string = '{:.2f}%'.format(premium_percentage)
    unlockcharacter_string = '{:.2f}%'.format(unlockcharacter_percentage)

    data = {
        'UnlockCharacterManager': unlockcharacter_total,
        'Premium': premium_total,
    }

    data = pd.Series(data).reset_index(name='value').rename(columns={'index': 'Product'})
    data['angle'] = data['value']/data['value'].sum()*2*pi
    data['color'] = ['#0236a5', '#fe0369']

    donut_fig = figure(
        height=350,
        width=350,
        title='Total revenue by Product',
        toolbar_location=None,
        x_range=Range1d(start=-2, end=2),
        y_range=Range1d(start=-2, end=2),
        tools='hover',
        tooltips='@Product: @value{0,0.00}€'
    )

    donut_fig.annular_wedge(
        source=data,
        x=0,
        y=0,
        inner_radius=.9,
        outer_radius=1.8,
        start_angle=cumsum('angle', include_zero=True),
        end_angle=cumsum('angle'),
        line_color='black',
        fill_color='color',
        legend_field='Product'
    )

    premium_label = Label(
        x=1.3,
        y=-1.7,
        text=premium_string,
        text_color='#fe0369',
        text_font='DM Sans'
    )

    unlockcharacter_label = Label(
        x=-1.9,
        y=1.6,
        text=unlockcharacter_string,
        text_color='#0236a5',
        text_font='DM Sans'
    )

    donut_fig.add_layout(premium_label)
    donut_fig.add_layout(unlockcharacter_label)

    # Stylizing the pie
    donut_fig.axis.axis_label = None
    donut_fig.axis.visible = False
    donut_fig.grid.grid_line_color = None

    donut_fig.legend.label_text_font = FONT
    donut_fig.title.text_font= FONT

    return donut_fig