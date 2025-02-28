# Filtering operations on our dataframes
import pandas as pd
import geopandas as gpd

# Bokeh shenanigans (try avoiding show if possible to test things, just use save with test.html)
from bokeh.plotting import figure

# HTML manipulation and visuals
from bokeh.models import Label, Range1d, LabelSet, ColumnDataSource, Band
from bokeh.palettes import Bokeh8
from bokeh.core.properties import value as vl

FONT = 'DM Sans'

def ratings_and_stability(crashdf: pd.DataFrame, ratingdf: pd.DataFrame, monthly_sales_df: pd.DataFrame):
    # TODO: Key performance indicators to understand stability related to ratings, This is Lars task now.
    
    #works with panda's dataframe. grab total average rating (for that month) and sum daily crashes and ANR. Lineplot with crashes on x-axis, and ratings on the y axis
    #TODO: Later, the visuals. First make this function in a basic way.
    
    #filtered_df = df[df['column_name'] == 'row_data']
    # let's try absolute scaling
    #crashdf['Daily Crashes'] = crashdf['Daily Crashes']  /crashdf['Daily Crashes'].abs().max() #works well enough
    #crashdf['Daily ANRs'] = crashdf['Daily ANRs']  /crashdf['Daily ANRs'].abs().max() #will this work?
    #ratingdf['Total Average Rating'] = ratingdf['Total Average Rating'] /ratingdf['Total Average Rating'].abs().max() 
    # Get monthly entries
    df_june      = crashdf[(crashdf['Date'] >= '2021-06-01') & (crashdf['Date'] < '2021-07-01')]
    df_july      = crashdf[(crashdf['Date'] >= '2021-07-01') & (crashdf['Date'] < '2021-08-01')]
    df_august    = crashdf[(crashdf['Date'] >= '2021-08-01') & (crashdf['Date'] < '2021-09-01')]
    df_september = crashdf[(crashdf['Date'] >= '2021-09-01') & (crashdf['Date'] < '2021-10-01')]
    df_october   = crashdf[(crashdf['Date'] >= '2021-10-01') & (crashdf['Date'] < '2021-11-01')]
    df_november  = crashdf[(crashdf['Date'] >= '2021-11-01') & (crashdf['Date'] < '2021-12-01')]
    df_december  = crashdf[(crashdf['Date'] >= '2021-12-01') & (crashdf['Date'] < '2022-01-01')]

    # Get monthly entries, but for ratings now
    df_june_rating      = ratingdf[(ratingdf['Date'] >= '2021-06-01') & (ratingdf['Date'] < '2021-07-01')]
    df_july_rating      = ratingdf[(ratingdf['Date'] >= '2021-07-01') & (ratingdf['Date'] < '2021-08-01')]
    df_august_rating    = ratingdf[(ratingdf['Date'] >= '2021-08-01') & (ratingdf['Date'] < '2021-09-01')]
    df_september_rating = ratingdf[(ratingdf['Date'] >= '2021-09-01') & (ratingdf['Date'] < '2021-10-01')]
    df_october_rating   = ratingdf[(ratingdf['Date'] >= '2021-10-01') & (ratingdf['Date'] < '2021-11-01')]
    df_november_rating  = ratingdf[(ratingdf['Date'] >= '2021-11-01') & (ratingdf['Date'] < '2021-12-01')]
    df_december_rating  = ratingdf[(ratingdf['Date'] >= '2021-12-01') & (ratingdf['Date'] < '2022-01-01')]  

    monthly_dfs = [df_june, df_july, df_august, df_september, df_october, df_november, df_december]
    monthly_dfs_ratings = [df_june_rating, df_july_rating, df_august_rating, df_september_rating, df_october_rating, df_november_rating, df_december_rating]
    monthly_crashes = []
    monthly_crashes_not_divided = []
    monthly_ARNs = []
    monthly_ARNs_not_divided = []
    monthly_average_ratings = []

    cum_sales = []
    sales_over_time = []

    for idx, month in enumerate(monthly_sales_df):
        monthly_sales = len(month)
        sales_over_time.append(monthly_sales)
        if idx == 0:
            cum_sales.append(monthly_sales)
        else:
            accum = cum_sales[idx-1] + monthly_sales
            cum_sales.append(accum)

    for month in monthly_dfs:
        # grab the crashes and ARNs
        crashes = month['Daily Crashes'] 
        ANR = month['Daily ANRs']
        # Add the monthly sums to a list
        monthly_crashes_not_divided.append(sum(crashes))
        monthly_crashes.append(crashes.sum()/200)#do note the division, as it does 'change' the data

        monthly_ARNs_not_divided.append(sum(ANR))
        monthly_ARNs.append(ANR.sum()/5)#do note the division, as it does 'change' the data

    for month in monthly_dfs_ratings:
        notNAperMonth = 0
        totalMonth = 0
        betterMonth = month[~month['Daily Average Rating'].isna()]
        for value in betterMonth['Daily Average Rating']:
            notNAperMonth += 1
            totalMonth += value
        monthly_average_rating = totalMonth/notNAperMonth
        monthly_average_ratings.append((monthly_average_rating))

    
    months = ['June', 'July', 'August', 'September', 'October', 'November', 'December']
    categories =  ['Ratings', 'ANRs', 'Crashes']

    data = {'months' : months, #now play around with plotting what where
            'Ratings':  monthly_average_ratings,
            'Crashes': monthly_crashes,
            'ANRs': monthly_ARNs,
            'Ratings Rounded': [round(x, 2) for x in monthly_average_ratings]
        }
    
    crashes_fig = figure(
	    title="Ratings compared to Stability",
        width= 650,
        height=500,
        x_axis_label='Month of 2021',
        y_axis_label='Average number of Xs that month',
        x_range=months,#other things like tooltip stuff might be nice
        toolbar_location=None,
        tools='hover',
        tooltips='@months'
    )

    crashes_fig.line(
        x='months',
        y='Ratings',
        color='blue',
        legend_label="Ratings", 
        line_width=2,
        source = data
    )
    crashes_fig.line(
        x='months',
        y='Crashes',
        color='red',
        legend_label="Crashes /200", 
        line_width=2,
        source = data
    )

    crashes_fig.line(
        x='months',
        y='ANRs',
        color='yellow',
        legend_label="ANRs /5", 
        source = data
    )

    crashes_fig.scatter(
        x='months',
        y='Ratings',
        color='blue',
        legend_label="Ratings", 
        source = data
    )

    crashes_fig.scatter(
        x='months',
        y='Crashes',
        color='red',
        legend_label="Crashes /200", 
        source = data
    )

    crashes_fig.scatter(
        x='months',
        y='ANRs',
        color='yellow',
        legend_label="ANRs /5", 
        source = data
    )

    label_data = ColumnDataSource(data)

    ratings_label_set = LabelSet(
        source=label_data,
        x='months',
        y='Ratings Rounded',
        text='Ratings Rounded',
        level='glyph',
        text_font=vl('DM Sans'),
        text_color='white',
        text_align='center',
        y_offset=5,
        x_offset=0,
    )

    crashes_label_set = LabelSet(
        source=label_data,
        x='months',
        y='Crashes',
        text='Crashes',
        level='glyph',
        text_font=vl('DM Sans'),
        text_color='white',
        text_align='center',
        y_offset=-15,
        x_offset=0,
    )

    anr_label_set = LabelSet(
        source=label_data,
        x='months',
        y='ANRs',
        text='ANRs',
        level='glyph',
        text_font=vl('DM Sans'),
        text_color='white',
        text_align='center',
        y_offset=-15,
        x_offset=0,
    )

    crashes_fig.add_layout(ratings_label_set)
    crashes_fig.add_layout(crashes_label_set)
    crashes_fig.add_layout(anr_label_set)    

    # Nicer looking font idk how else to set it for everything
    crashes_fig.legend.title_text_font = FONT
    crashes_fig.legend.label_text_font = FONT
    crashes_fig.title.text_font = FONT
    crashes_fig.axis.major_label_text_font = FONT
    crashes_fig.axis.axis_label_text_font = FONT

    text_fig = crashes_and_ratings_stats(monthly_crashes_not_divided, monthly_average_ratings, monthly_ARNs_not_divided)

    cumulative_data={
        'months' : months,
        'cumulative_sales': cum_sales,
        'Sales over Time': sales_over_time
    }

    cumulative_data = ColumnDataSource(cumulative_data)
    
    cumulative_fig = figure(
	    title="Cumulative Sales",
        width= 650,
        height=500,
        x_axis_label='Month of 2021',
        y_axis_label='Cumulative Sales over time',
        x_range=months,#other things like tooltip stuff might be nice
        toolbar_location=None,
        tools='hover',
        tooltips='Sales in @months: @cumulative_sales'
    )

    cumulative_fig.line(
        x="months", 
        y="cumulative_sales", 
        color='#fe0369',
        source=cumulative_data
    )

    cumulative_fig.varea(
        source=cumulative_data,
        x='months',
        y1=0,
        y2='cumulative_sales',
        alpha=.2,
        fill_color='#fe0369',
    )

    # Nicer looking font idk how else to set it for everything
    cumulative_fig.title.text_font = FONT
    cumulative_fig.axis.major_label_text_font = FONT
    cumulative_fig.axis.axis_label_text_font = FONT
    cumulative_fig.xgrid.grid_line_color = None

    over_time_fig = figure(
	    title="Sales over Time",
        width= 650,
        height=500,
        x_axis_label='Month of 2021',
        y_axis_label='Sales over Time',
        x_range=months,
        toolbar_location=None,
        tools='hover',
        tooltips='Sales in @months: @{Sales over Time}'
    )

    over_time_fig.line(
        x="months", 
        y="Sales over Time", 
        color='#fe0369',
        source=cumulative_data
    )

    over_time_fig.varea(
        source=cumulative_data,
        x='months',
        y1=0,
        y2='Sales over Time',
        alpha=.2,
        fill_color='#fe0369',
    )

    over_time_fig.title.text_font = FONT
    over_time_fig.axis.major_label_text_font = FONT
    over_time_fig.axis.axis_label_text_font = FONT
    over_time_fig.xgrid.grid_line_color = None
    
    return crashes_fig, cumulative_fig, text_fig, over_time_fig

def crashes_and_ratings_stats(monthly_crashes, monthly_average_ratings, monthly_ANRs):
    # Crashes
    crashes_last_month = monthly_crashes[-1]
    crashes_penultimate_month = monthly_crashes[-2]

    crashes_diff = crashes_last_month - crashes_penultimate_month
    crashes_diff_percentage = crashes_diff/crashes_penultimate_month*100
    crashes_diff_percentage = round(crashes_diff_percentage, 2)

    # Ratings 
    ratings_last_month = monthly_average_ratings[-1]
    ratings_penultimate_month = monthly_average_ratings[-2]

    ratings_diff = ratings_last_month - ratings_penultimate_month
    ratings_diff_percentage = ratings_diff/ratings_penultimate_month*100
    ratings_diff_percentage = round(ratings_diff_percentage, 2)
    ratings_diff = round(ratings_diff, 2)

    # ANRs

    anrs_last_month = monthly_ANRs[-1]
    anrs_penultimate_month = monthly_ANRs[-2]

    anrs_diff = anrs_last_month - anrs_penultimate_month
    anrs_diff_percentage = anrs_diff/anrs_penultimate_month*100
    anrs_diff_percentage = round(anrs_diff_percentage, 2)

    # Text figure with metrics compared to previous month

    text_fig = figure(
        height=150,
        width=1300,
        toolbar_location=None,
        tools='',
        x_range=Range1d(start=-10, end=10),
        y_range=Range1d(start=-10, end=10),
    )

    title_label = Label(
        x=0,
        y=5,
        text='Performance relative to last month:',
        text_color='white',
        text_font='DM Sans',
        text_font_style='bold',
        text_align='center',
        text_font_size='2.5em'
    )

    crashes_string = f'▲ {crashes_diff_percentage} %   ▲ {crashes_diff}'

    crashes_label = Label(
        x=-7,
        y=-9,
        text=crashes_string,
        text_color='red',
        text_font='DM Sans',
        text_font_style='bold',
        text_align='center',
        text_font_size='2em'
    )

    crashes_title_label = Label(
        x=-7,
        y=-2,
        text='Crashes:',
        text_color='white',
        text_font='DM Sans',
        text_font_style='bold',
        text_align='center',
        text_font_size='2em'
    )

    ratings_string = f'▲ {ratings_diff_percentage} %   ▲ {ratings_diff} ⭐'

    ratings_label = Label(
        x=0,
        y=-9,
        text=ratings_string,
        text_color='green',
        text_font='DM Sans',
        text_font_style='bold',
        text_align='center',
        text_font_size='2em'
    )

    ratings_title_label = Label(
        x=0,
        y=-2,
        text='Ratings:',
        text_color='white',
        text_font='DM Sans',
        text_font_style='bold',
        text_align='center',
        text_font_size='2em'
    )

    anrs_sring =  f'▼ {anrs_diff_percentage} %   ▼ {anrs_diff}'

    anrs_label = Label(
        x=7,
        y=-9,
        text=anrs_sring,
        text_color='green',
        text_font='DM Sans',
        text_font_style='bold',
        text_align='center',
        text_font_size='2em'
    )

    anrs_title_label = Label(
        x=7,
        y=-2,
        text='App not Responding:',
        text_color='white',
        text_font='DM Sans',
        text_font_style='bold',
        text_align='center',
        text_font_size='2em'
    )

    text_fig.add_layout(title_label)
    text_fig.add_layout(crashes_label)
    text_fig.add_layout(ratings_label)
    text_fig.add_layout(anrs_label)
    text_fig.add_layout(crashes_title_label)
    text_fig.add_layout(ratings_title_label)
    text_fig.add_layout(anrs_title_label)

    # Stylizing the pie
    text_fig.axis.axis_label = None
    text_fig.axis.visible = False
    text_fig.grid.grid_line_color = None
    text_fig.background_fill_color = (21, 25, 28)
    text_fig.outline_line_color = '#15191c'

    return text_fig