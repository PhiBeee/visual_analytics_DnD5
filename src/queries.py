import pandas as pd
import geopandas as gpd
from math import pi

from bokeh.plotting import figure
from bokeh.palettes import TolRainbow18
from bokeh.transform import cumsum
from bokeh.models import LabelSet, ColumnDataSource
from bokeh.core.properties import value

FONT = 'DM Sans'

def rating_plots(ratingdf: pd.DataFrame):
    df_june_rating      = ratingdf[(ratingdf['Date'] >= '2021-06-01') & (ratingdf['Date'] < '2021-07-01')]
    df_july_rating      = ratingdf[(ratingdf['Date'] >= '2021-07-01') & (ratingdf['Date'] < '2021-08-01')]
    df_august_rating    = ratingdf[(ratingdf['Date'] >= '2021-08-01') & (ratingdf['Date'] < '2021-09-01')]
    df_september_rating = ratingdf[(ratingdf['Date'] >= '2021-09-01') & (ratingdf['Date'] < '2021-10-01')]
    df_october_rating   = ratingdf[(ratingdf['Date'] >= '2021-10-01') & (ratingdf['Date'] < '2021-11-01')]
    df_november_rating  = ratingdf[(ratingdf['Date'] >= '2021-11-01') & (ratingdf['Date'] < '2021-12-01')]
    df_december_rating  = ratingdf[(ratingdf['Date'] >= '2021-12-01') & (ratingdf['Date'] < '2022-01-01')]

    monthly_dfs_ratings = [df_june_rating, df_july_rating, df_august_rating, df_september_rating, df_october_rating, df_november_rating, df_december_rating]

    months = ['June', 'July', 'August', 'September', 'October', 'November', 'December']
    countries = set(ratingdf['Country'])

    monthly_dfs_with_daily_ratings = []

    data = {
        'USA': []
    }

    data_ratings_per_month = {
        'USA': []
    }

    for idx, month in enumerate(monthly_dfs_ratings):
        cur_month = months[idx]
        header_text = f'Countries with new ratings in {cur_month}'

        month = month[~month['Daily Average Rating'].isna()]

        for country in set(month['Country']):
            # Get the rows for that country
            country_entries = month[month['Country'] == country]
            # Turn into list so that we can add to our data dict
            country_entries = country_entries['Daily Average Rating'].values.tolist()
            if country in data.keys():
                data[country] += country_entries
                # Append the amount of ratings we have per month
                len_diff = idx - len(data_ratings_per_month[country])
                if len_diff == 0:
                    data_ratings_per_month[country].append(len(country_entries))
                # If there is no ratings between months add the needed 0 entries
                else:
                    data_ratings_per_month[country] += ([0]*len_diff)+[len(country_entries)]
            else:
                data[country] = country_entries
                # Append empty for months prior
                data_ratings_per_month[country] = [0]*idx
                data_ratings_per_month[country].append(len(country_entries))

    # Make sure that we have 7 entries for every country (the ones that had no entry for the last month need stuff added at the end)
    for key in data_ratings_per_month.keys():
        len_diff = 7 - len(data_ratings_per_month[key])
        if len_diff != 0:
            data_ratings_per_month[key] += ([0]*len_diff)

    # Add a list of countries for which we have ratings to our data
    countries_with_data = [c for c in data.keys()]

    data['months'] = months
    data_ratings_per_month['months'] = months

    amount_of_ratings_per_month = figure(
        title='Amount of Ratings per Country per Month',
        width=900,
        height=500,
        x_axis_label='Month of 2021',
        y_axis_label='Amount of Ratings',
        x_range=months,
        toolbar_location=None,
        tools='hover',
        tooltips='$name in @months: @$name',
    )

    amount_of_ratings_per_month.vbar_stack(
        countries_with_data,
        x='months',
        width=0.9,
        color=TolRainbow18,
        source=data_ratings_per_month,
        muted_color=TolRainbow18,
        muted_alpha=.2,
        legend_label=countries_with_data
    )

    amount_of_ratings_per_month.xgrid.grid_line_color = None
    amount_of_ratings_per_month.axis.minor_tick_line_color = None
    amount_of_ratings_per_month.outline_line_color = None

    amount_of_ratings_per_month.legend.ncols = 3
    amount_of_ratings_per_month.min_border_bottom = 0
    amount_of_ratings_per_month.min_border_left = 0

    # Nicer looking font idk how else to set it for everything
    amount_of_ratings_per_month.legend.title_text_font = FONT
    amount_of_ratings_per_month.legend.label_text_font = FONT
    amount_of_ratings_per_month.title.text_font = FONT
    amount_of_ratings_per_month.axis.major_label_text_font = FONT
    amount_of_ratings_per_month.axis.axis_label_text_font = FONT
    amount_of_ratings_per_month.axis.axis_label_text_align = 'left'

    # Convenience lists
    total_amount_of_ratings_per_currency = []
    average_per_country = []

    for country in countries_with_data:
        total_amount_of_ratings_per_currency.append(sum(data_ratings_per_month[country]))
        # Calculate the average per country
        average_per_country.append(round(sum(data[country])/len(data[country]), 2))

    # AVERAGE RATING BAR CHART

    data = {
        'Countries': countries_with_data,
        'Averages': average_per_country,
        'colour': TolRainbow18
    }

    average_rating_bar = figure(
        title='Average Rating per Country',
        width=900,
        height=500,
        x_axis_label='Country',
        y_axis_label='Average Rating',
        x_range=countries_with_data,
        toolbar_location=None,
    )

    average_rating_bar.vbar(
        source=data,
        x='Countries',
        top='Averages',
        width=.95,
        color='colour'
    )

    average_rating_bar.xgrid.grid_line_color = None
    average_rating_bar.y_range.start = 0

    average_rating_bar.title.text_font = FONT
    average_rating_bar.axis.major_label_text_font = FONT
    average_rating_bar.axis.axis_label_text_font = FONT

    label_data = ColumnDataSource(data)

    average_rating_labelset = LabelSet(
        source=label_data,
        x='Countries',
        y='Averages',
        text='Averages',
        level='glyph',
        text_font=value('DM Sans'),
        text_color='white',
        y_offset=5,
        x_offset=-10
    )

    average_rating_bar.add_layout(average_rating_labelset)

    # PIE CHART

    # dict to make it easier to turn into a df
    pie_data = {
        'Countries': countries_with_data,
        'RatingsAmount'   : total_amount_of_ratings_per_currency,
    }

    # Turn our data back into a df to then calculate angles for our pie
    data = pd.DataFrame(pie_data)
    data['angle'] = data['RatingsAmount']/data['RatingsAmount'].sum() * 2*pi
    data['color'] = TolRainbow18

    pie_fig = figure(
        title='Ratings Amount per Country',
        height=500,
        width=500,
        toolbar_location=None,
        tools='hover',
        tooltips='@Countries: @RatingsAmount',
        x_range=(-.5, 1.0),
    )

    pie_fig.wedge(
        x=.10,
        y=1,
        radius=.5,
        start_angle=cumsum('angle', include_zero=True),
        end_angle=cumsum('angle'),
        line_color='#15191c',
        fill_color='color',
        legend_field='Countries',
        source=data
    )

    # Stylizing the pie
    pie_fig.axis.axis_label = None
    pie_fig.axis.visible = False
    pie_fig.grid.grid_line_color = None
    pie_fig.background_fill_color= (21, 25, 28)
    pie_fig.outline_line_color = '#15191c'

    pie_fig.legend.label_text_font = FONT
    pie_fig.title.text_font = FONT
    pie_fig.title.align = 'center'
    pie_fig.legend.ncols = 2


    return amount_of_ratings_per_month, average_rating_bar, pie_fig