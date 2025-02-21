# Filtering operations on our dataframes
import pandas as pd
import geopandas as gpd

# For the Choropleth
import json

# Bokeh shenanigans (try avoiding show if possible to test things, just use save with test.html)
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource

# HTML manipulation and visuals
from bokeh.io import curdoc
from bokeh.models import ColorBar, LinearColorMapper
from bokeh.palettes import RdPu9

FONT = 'DM Sans'


# This is the function from https://dmnfarrell.github.io/bioinformatics/bokeh-maps
def get_geodatasource(gdf: gpd.GeoDataFrame):
    """Get getjsondatasource from geopandas object"""
    json_data = json.dumps(json.loads(gdf.to_json()))
    return GeoJSONDataSource(geojson = json_data)

# Needs some visual and interactive improvements but I'll do that later
def geographical_view(df: pd.DataFrame, gdf: gpd.GeoDataFrame):
    curdoc().theme = 'dark_minimal'
    # Fun fact: Puerto Rico and Argentina use USD, which is why the choropleth has less sales in the USA than the pie in USD
    
    # Filter out the countries we initially had data for
    currencies_with_sales = df[df['_merge'] == 'both']
    currencies_with_sales = set(currencies_with_sales['Country Code of Buyer'])

    # Get and array of tuples (Country Code, Sales)
    sales_per_currency = [(country_code, len(df[df['Country Code of Buyer'] == country_code])) for country_code in set(df['Country Code of Buyer'])]
    sales_per_currency = pd.DataFrame(sales_per_currency, columns=['Country Code of Buyer','Sales'])
    
    # Adjust for the fact that the countries with no sales now have a row because of our outer merge
    meow = sales_per_currency[~sales_per_currency['Country Code of Buyer'].isin(currencies_with_sales)]
    # It suddenly started not liking this but is behaving properly so whatever
    meow['Sales'] = meow['Sales']-1
    sales_per_currency[~sales_per_currency['Country Code of Buyer'].isin(currencies_with_sales)] = meow

    # 38 countries with sales
    gdf = gdf.merge(
        right=sales_per_currency,
        left_on='Country Code of Buyer',
        right_on='Country Code of Buyer',
    )

    # Separating for better colouring
    gdf_no_sales = gdf[gdf['Sales']==0]
    gdf_sales = gdf[gdf['Sales']!=0]

    geosource_sales = get_geodatasource(gdf_sales)
    geosource_no_sales = get_geodatasource(gdf_no_sales)

    # Visualizing part
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
        location=(550,0),
        orientation='horizontal'
    )

    choropleth = figure(
        title='Sales per country',
        toolbar_location=None,
        tools='hover',
        tooltips='@{Country of Buyer}: @Sales',
        x_axis_location=None,
        y_axis_location=None,
        width=1600,
        height=900
    )

    choropleth.grid.grid_line_color = None

    choropleth.patches(
        xs='xs',
        ys='ys',
        source=geosource_sales,
        fill_alpha=.7,
        line_width=.5,
        line_color='black',
        fill_color={
            'field': 'Sales',
            'transform': cmap,
        }
    )

    choropleth.add_layout(
        cbar,
        'below'
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

    choropleth.title.text_font = FONT

    return choropleth

def geographical_over_time(monthly_dfs, gdf: gpd.GeoDataFrame):
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

    total_sales = []
    countries = []
    for index, row in merged_data.iterrows():
        total_sales.append(row[1:].values.tolist())
        countries.append(row[0])

    multi_line_fig = figure(
        title='Total Sales over time',
        width=750,
        height=500,
        x_axis_label='Month of 2021',
        y_axis_label='Amount of Sales',
        x_range=month_names,
        toolbar_location=None,
        tools='hover',
    )

    for idx, sales in enumerate(total_sales):
        country =  countries[idx]
        multi_line_fig.line(
            x=month_names
        )

    return multi_line_fig

