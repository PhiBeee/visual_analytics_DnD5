# For the pie chart
from math import pi

# Filtering operations on our dataframes
import pandas as pd

# Bokeh shenanigans (try avoiding show if possible to test things, just use save with test.html)
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.models import Range1d, Label

FONT = 'DM Sans'

def donut_plot(df: pd.DataFrame, monthly_dfs):
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
    data['color'] = ['#407ee8', '#fe0369']

    donut_fig = figure(
        height=350,
        width=350,
        title='Total revenue by Product',
        toolbar_location=None,
        x_range=Range1d(start=-2, end=2),
        y_range=Range1d(start=-2, end=2),
        tools='hover',
        tooltips='@Product: @value{0,0.00} €'
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
        text_font='DM Sans',
    )

    unlockcharacter_label = Label(
        x=-1.9,
        y=1.6,
        text=unlockcharacter_string,
        text_color='#407ee8',
        text_font='DM Sans',
    )

    donut_fig.add_layout(premium_label)
    donut_fig.add_layout(unlockcharacter_label)

    # Stylizing the pie
    donut_fig.axis.axis_label = None
    donut_fig.axis.visible = False
    donut_fig.grid.grid_line_color = None
    donut_fig.background_fill_color= (21, 25, 28)
    donut_fig.outline_line_color = '#15191c'

    donut_fig.legend.label_text_font = FONT
    donut_fig.title.text_font= FONT
    donut_fig.title.align = 'center'

    # TEXT FIGURE NO PLOTTING REALLY JUST TEXT

    text_fig = figure(
        height=350,
        width=350,
        toolbar_location=None,
        tools='',
        x_range=Range1d(start=-2, end=2),
        y_range=Range1d(start=-2, end=2),
    )

    total_string = '▲ {:.2f} €'.format(total)

    total_label = Label(
        x=0,
        y=1,
        text=total_string,
        text_color='#0be200',
        text_font='DM Sans',
        text_font_style='bold',
        text_align='center',
        text_font_size='2.5em'
    )

    inbetween_label = Label(
        x=0,
        y=.5,
        text='Performance relative to last month:',
        text_color='white',
        text_font='DM Sans',
        text_font_style='bold',
        text_align='center',
        text_font_size='1.5em'
    )

    # ▼
    last_df = monthly_dfs[-1]
    penultimate_df = monthly_dfs[-2]

    sales_last_month = len(last_df)
    sales_penultimate_month = len(penultimate_df)

    difference = sales_last_month - sales_penultimate_month
    difference_percentage = difference/sales_penultimate_month*100

    sales_relative_to_penultimate_month_string = '▼ {:.2f} %  ▼ {:.0f}'.format(difference_percentage, difference)

    sales_relative_to_penultimate_month = Label(
        x=0,
        y=-.5,
        text=sales_relative_to_penultimate_month_string,
        text_color='red',
        text_font='DM Sans',
        text_font_style='bold',
        text_align='center',
        text_font_size='1.5em'
    )

    revenue_last_month = last_df['Amount (Merchant Currency)'].sum()
    revenues_penultimate_month = penultimate_df['Amount (Merchant Currency)'].sum()

    difference = revenue_last_month - revenues_penultimate_month
    difference_percentage = difference/revenues_penultimate_month*100

    revenues_relative_to_penultimate_month_string = '▼ {:.2f} %  ▼ {:.2f} €'.format(difference_percentage, difference)

    revenues_relative_to_penultimate_month = Label(
        x=0,
        y=-1.5,
        text=revenues_relative_to_penultimate_month_string,
        text_color='red',
        text_font='DM Sans',
        text_font_style='bold',
        text_align='center',
        text_font_size='1.5em'
    )

    first_between = Label(
        x=0,
        y=0,
        text='Amount of sales: ',
        text_color='white',
        text_font='DM Sans',
        text_font_style='bold',
        text_align='center',
        text_font_size='1.5em'
    )

    second_between = Label(
        x=0,
        y=-1,
        text='Monthly revenue: ',
        text_color='white',
        text_font='DM Sans',
        text_font_style='bold',
        text_align='center',
        text_font_size='1.5em'
    )

    text_fig.add_layout(total_label)
    text_fig.add_layout(inbetween_label)
    text_fig.add_layout(sales_relative_to_penultimate_month)
    text_fig.add_layout(revenues_relative_to_penultimate_month)
    text_fig.add_layout(first_between)
    text_fig.add_layout(second_between)

    # Stylizing the pie
    text_fig.axis.axis_label = None
    text_fig.axis.visible = False
    text_fig.grid.grid_line_color = None
    text_fig.background_fill_color= (21, 25, 28)
    text_fig.outline_line_color = '#15191c'

    return donut_fig, text_fig