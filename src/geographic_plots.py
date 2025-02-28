# Filtering operations on our dataframes
import pandas as pd
import geopandas as gpd

# For the Choropleth
import json

# Bokeh shenanigans (try avoiding show if possible to test things, just use save with test.html)
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, Tabs, TabPanel, Tooltip

# HTML manipulation and visuals
from bokeh.io import curdoc
from bokeh.models import ColorBar, LinearColorMapper, Legend, Select, Select, CustomJS
from bokeh.layouts import column
from bokeh.palettes import RdPu9, Turbo256

FONT = 'DM Sans'


# This is the function from https://dmnfarrell.github.io/bioinformatics/bokeh-maps
def get_geodatasource(gdf: gpd.GeoDataFrame):
    """Get getjsondatasource from geopandas object"""
    json_data = json.dumps(json.loads(gdf.to_json()))
    return GeoJSONDataSource(geojson = json_data)

# This is the main function to make the two country related plots I will clean the code and add some comments if I find the time
def geographical_over_time(monthly_dfs, gdf: gpd.GeoDataFrame):
    # DATA PREPROCESSING

    curdoc().theme = 'dark_minimal'
    
    month_names = ['June', 'July', 'August', 'September', 'October', 'November', 'December']

    sales_per_currency_per_month = []
    for idx, month in enumerate(monthly_dfs):
        # Filter out the countries we initially had data for
        currencies_with_sales = month[month['_merge'] == 'both']
        currencies_with_sales = set(currencies_with_sales['Country Code of Buyer'])

        # Get and array of tuples (Country Code, Sales)
        sales_per_currency = [(country_code, len(month[month['Country Code of Buyer'] == country_code])) for country_code in currencies_with_sales]
        sales_per_currency = pd.DataFrame(sales_per_currency, columns=['Country Code of Buyer','Sales'])

        sales_per_currency['Sales'] = sales_per_currency['Sales'].astype(float)

        current_month = month_names[idx]
        # Initialize the column
        if idx == 0:
            sales_per_currency[f'Total Sales for {current_month}'] = sales_per_currency['Sales']
        # Intialize or add to total depending on if we have a previous entry
        else:
            previous_month = sales_per_currency_per_month[idx-1]
            previous_month_name = month_names[idx-1]
            countries_previous_month = set(previous_month['Country Code of Buyer'])
            countries_this_month = set(sales_per_currency['Country Code of Buyer'])
            countries_no_update = countries_previous_month - countries_this_month


            # I have to do it like this because addition is done on index
            for cc in countries_this_month:
                monthly_sales = sales_per_currency.loc[sales_per_currency['Country Code of Buyer'] == cc, 'Sales']
                # If we have a previous entry
                if cc in countries_previous_month:
                    past_sales = previous_month.loc[previous_month['Country Code of Buyer'] == cc, f'Total Sales for {previous_month_name}'].item()
                    sales_per_currency.loc[sales_per_currency['Country Code of Buyer']==cc, f'Total Sales for {current_month}'] = monthly_sales + past_sales
                else:
                    sales_per_currency.loc[sales_per_currency['Country Code of Buyer']==cc, f'Total Sales for {current_month}'] = monthly_sales
            
            # To reset index so we know that the next index is len(df)
            sales_per_currency.reset_index()
            
            # We have to make new rows for the countries not in the current month
            for idx, cc in enumerate(countries_no_update):
                past_sales = previous_month.loc[previous_month['Country Code of Buyer'] == cc, f'Total Sales for {previous_month_name}'].item()
                new_row = [cc, 0, past_sales]
                sales_per_currency.loc[len(sales_per_currency)+idx] = new_row
            

        sales_per_currency_per_month.append(sales_per_currency)

    merged_data = sales_per_currency_per_month[0]
    merged_data = merged_data.drop('Sales', axis=1)

    for month in sales_per_currency_per_month[1:]:
        month = month.drop('Sales', axis=1)
        merged_data = merged_data.merge(
            right=month,
            left_on='Country Code of Buyer',
            right_on='Country Code of Buyer',
            how='outer'
        )

    # Fill empty entries (which is before that currency gets a sale)
    merged_data = merged_data.fillna(0)

    cols = merged_data.columns.tolist()[1:]

    # DATA VISUALIZING 

    # CHOROPLETHS
    palette = RdPu9[:-2]
    palette = palette[::-1]

    cmap = LinearColorMapper(
        palette=palette,
        low=1,
        high=115,
    )

    cbar = ColorBar(
        color_mapper=cmap,
        label_standoff=9,
        width=500,
        height=20,
        location=(625,0),
        orientation='horizontal',
        major_label_text_font='DM Sans'
    )

    tabs = []
    # This amalgamation of code is creating the multiple choropleths and placing them in TabPanels
    for col in cols:
        month = col.split(' ')[-1]
        monthly_data = merged_data[['Country Code of Buyer', col]]

        gdf_monthly = gdf.merge(
            right=monthly_data,
            left_on='Country Code of Buyer',
            right_on='Country Code of Buyer',
            how='outer'
        )

        # Empty data means that we have no sales, we need these entries so we can plot the entire world
        gdf_monthly = gdf_monthly.fillna(0)

        # Separation for clearer coloring between no sale and at least one sale
        gdf_monthly_sales = gdf_monthly[gdf_monthly[col]!=0]
        gdf_monthly_no_sales = gdf_monthly[gdf_monthly[col]==0]

        geosource = get_geodatasource(gdf_monthly_sales)
        geosource_no_sales = get_geodatasource(gdf_monthly_no_sales)

        # Format the tooltips because of funky spacing
        tooltip_1 = '{Country of Buyer}'
        tooltip_2 = '{' + col + '}'

        choropleth = figure(
            title='Sales per country',
            toolbar_location='right',
            tools='hover,box_zoom,reset',
            tooltips=f'@{tooltip_1}: @{tooltip_2}',
            x_axis_location=None,
            y_axis_location=None,
            width=1750,
            height=900
        )

        choropleth.grid.grid_line_color = None

        choropleth.patches(
            xs='xs',
            ys='ys',
            source=geosource,
            fill_alpha=.7,
            line_width=.5,
            line_color='black',
            fill_color={
                'field': col,
                'transform': cmap,
            }
        )

        choropleth.patches(
            xs='xs',
            ys='ys',
            source=geosource_no_sales,
            fill_alpha=.7,
            line_width=.5,
            line_color='black',
            fill_color=RdPu9[-1]
        )

        choropleth.add_layout(
            cbar,
            'below'
        )

        choropleth.title.text_font = FONT

        tab = TabPanel(
            child=choropleth,
            title=col,
            tooltip=Tooltip(content=f'This is the accumulated sales for {month}', position='bottom_center')
        )

        tabs.append(tab)

    tabs = Tabs(
        tabs=tabs,
        styles={'font-family': 'DM Sans'},
        align='center'
    )

    # MULTILINE PLOT

    # Get rid of column labels
    total_sales = []
    countries = []
    for index, row in merged_data.iterrows():
        total_sales.append(row[1:].values.tolist())
        countries.append(row.iloc[0])

    multi_line_fig = figure(
        title='Total Sales over time',
        height=350,
        width=900,
        x_axis_label='Month of 2021',
        y_axis_label='Amount of Sales',
        x_range=month_names,
        toolbar_location='left',
        tools='pan,wheel_zoom,box_zoom',
    )
    legend_moment = []
    # Create a line for each country
    for idx, sales in enumerate(total_sales):
        current_country = countries[idx]

        data = {
            'Total Sales': sales,
            'Months': month_names,
        }

        buh = multi_line_fig.line(
            source=data,
            x='Months',
            y='Total Sales',
            color=Turbo256[idx*6],
            muted_color=Turbo256[idx*6],
            muted_alpha=.2
        )

        legend_moment.append((current_country, [buh]))

    legend_moment = Legend(items=legend_moment, ncols=3, styles={'font-family': 'DM Sans'})
    legend_moment.click_policy = 'mute'

    multi_line_fig.add_layout(legend_moment, 'right')
    multi_line_fig.y_range.start = 0
    multi_line_fig.y_range.end = 1400

    multi_line_fig.legend.title_text_font = FONT
    multi_line_fig.legend.label_text_font = FONT
    multi_line_fig.title.text_font = FONT
    multi_line_fig.axis.major_label_text_font = FONT
    multi_line_fig.axis.axis_label_text_font = FONT

    return tabs

def geographic_ratings(salesdf: pd.DataFrame ,ratings_df: pd.DataFrame, gdf: gpd.GeoDataFrame):

    for country in set(ratings_df['Country']):
        # Rating DF

        countrydf = ratings_df[ratings_df['Country'] == country]
        rating_sum = sum(countrydf['Total Average Rating'])
        rating_avg = rating_sum/len(countrydf)
        
        gdf.loc[gdf['Country Code of Buyer']==country, 'Rating Average'] = rating_avg

        # Sales DF

        countrydf = salesdf[salesdf['Country Code of Buyer'] == country]
        revenue_sum = sum(countrydf['Amount (Merchant Currency)'])

        gdf.loc[gdf['Country Code of Buyer']==country, 'Total Revenue'] = revenue_sum

    gdf = gdf.fillna(0)

    countries_with_ratings = gdf[gdf['Rating Average'] != 0]
    countries_with_no_ratings = gdf[gdf['Rating Average'] == 0]

    geosource_ratings = get_geodatasource(countries_with_ratings)
    geosource_no_ratings = get_geodatasource(countries_with_no_ratings)

    countries_with_sales = gdf[gdf['Total Revenue'] != 0]
    countries_with_no_sales = gdf[gdf['Total Revenue'] == 0]

    geosource_sales = get_geodatasource(countries_with_sales)
    geosource_no_sales = get_geodatasource(countries_with_no_sales)

    # DATA VISUALIZATION

    palette = RdPu9[:-2]
    palette = palette[::-1]

    cmap = LinearColorMapper(
        palette=palette,
        low=0.01,
        high=5,
    )

    cbar = ColorBar(
        color_mapper=cmap,
        label_standoff=9,
        width=500,
        height=20,
        location=(625,0),
        orientation='horizontal',
        major_label_text_font='DM Sans'
    )

    rating_choro = figure(
        title='Total average rating per country',
        toolbar_location='right',
        tools='hover,box_zoom,reset',
        tooltips='@{Country of Buyer}: @{Rating Average}{0.00} ',
        x_axis_location=None,
        y_axis_location=None,
        width=1750,
        height=900
    )

    rating_choro.grid.grid_line_color = None

    rating_choro.patches(
        xs='xs',
        ys='ys',
        source=geosource_ratings,
        fill_alpha=.7,
        line_width=.5,
        line_color='black',
        fill_color={
            'field':'Rating Average',
            'transform': cmap,
        }
    )

    rating_choro.patches(
        xs='xs',
        ys='ys',
        source=geosource_no_ratings,
        fill_alpha=.7,
        line_width=.5,
        line_color='black',
        fill_color=RdPu9[-1]
    )

    rating_choro.add_layout(
        cbar,
        'below'
    )

    rating_choro.title.text_font = FONT

    cmap = LinearColorMapper(
        palette=palette,
        low=10,
        high=400,
    )

    cbar = ColorBar(
        color_mapper=cmap,
        label_standoff=9,
        width=500,
        height=20,
        location=(625,0),
        orientation='horizontal',
        major_label_text_font='DM Sans'
    )

    sales_choro = figure(
        title='Total average rating per country',
        toolbar_location='right',
        tools='hover,box_zoom,reset',
        tooltips='@{Country of Buyer}: @{Total Revenue}{0.00} €',
        x_axis_location=None,
        y_axis_location=None,
        width=1750,
        height=900,
        visible=False,
    )

    sales_choro.grid.grid_line_color = None

    sales_choro.patches(
        xs='xs',
        ys='ys',
        source=geosource_sales,
        fill_alpha=.7,
        line_width=.5,
        line_color='black',
        fill_color={
            'field':'Total Revenue',
            'transform': cmap,
        }
    )

    sales_choro.patches(
        xs='xs',
        ys='ys',
        source=geosource_no_sales,
        fill_alpha=.7,
        line_width=.5,
        line_color='black',
        fill_color=RdPu9[-1]
    )

    sales_choro.add_layout(
        cbar,
        'below'
    )

    sales_choro.title.text_font = FONT

    return rating_choro, sales_choro
