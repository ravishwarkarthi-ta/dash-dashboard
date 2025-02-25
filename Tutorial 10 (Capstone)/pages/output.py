import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd
import plotly.express as px
from flask import redirect, url_for, request, session, flash
from geopy.geocoders import Nominatim  # For reverse geocoding
import dash.dash_table as dt
from pages.login import dbc, gapminder_df
from pages.about import about_layout
from pages.Input_page import input_layout


# Output Layout

output_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("User Provided Fields"),
                dbc.CardBody([
                    html.Div([
                        html.Strong("Latitude: "),
                        html.Span(id='display-lat')
                    ], className="mb-2"),
                    html.Div([
                        html.Strong("Longitude: "),
                        html.Span(id='display-lon')
                    ], className="mb-2"),
                    html.Div([
                        html.Strong("Dataset: "),
                        html.Span(id='display-dataset')
                    ], className="mb-2"),
                    html.Div([
                        html.Strong("Country: "),
                        html.Span(id='display-country')
                    ], className="mb-2"),
                ])
            ])
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Location Map"),
                dbc.CardBody([
                    html.Div(id='map-container')  # We'll fill this in via callback
                ])
            ])
        ], md=9)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Country Data"),
                dbc.CardBody([
                    html.Div([
                        html.Strong("Total GDP: "),
                        html.Span(id="country-total-gdp")
                    ], className="mb-2"),
                    html.Div([
                        html.Strong("Total Population: "),
                        html.Span(id="country-total-pop")
                    ], className="mb-2"),
                    html.Div([
                        html.Strong("Average Life Expectancy: "),
                        html.Span(id="country-avg-lifeexp")
                    ], className="mb-2"),
                ])
            ])
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Visualizations"),
                dbc.CardBody([
                    html.Div(id='graph-container')
                ])
            ])
        ], md=9)
    ], className="mb-4"),
    dbc.Row([
        dbc.Col([
            html.Div(className="mt-4 text-center", children=[
                dbc.Button("Back to Input", href="/input", color="primary", className="mr-2"),
                dbc.Button("New Analysis", href="/", color="secondary"),
                html.A("Logout", href="/logout", className="btn btn-danger ml-2")
            ])
        ], width=12)
    ])
], className="mt-5")

def update_output(data):
    """
    Updates the Output page fields and visualizations
    based on the stored user data (lat, lon, dataset, country).
    """
    if not data:
        # If no data is submitted yet, show placeholders
        return [
            '', '', '', '',
            dbc.Alert("No data submitted!", color="danger"),
            dbc.Alert("No data submitted!", color="danger"),
            "", "", ""
        ]

    lat = data.get('lat', 'N/A')
    lon = data.get('lon', 'N/A')
    dataset = data.get('dataset', '').title()
    country = data.get('country', 'N/A')

    # Create a map figure
    try:
        lat_val = float(lat)
        lon_val = float(lon)
        map_fig = px.scatter_mapbox(
            lat=[lat_val],
            lon=[lon_val],
            zoom=5,
            height=300
        )
        map_fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r":0,"t":0,"l":0,"b":0}
        )
        map_div = dcc.Graph(figure=map_fig)
    except:
        map_div = dbc.Alert("Invalid coordinates for map", color="danger")

    # Prepare visualizations
    graphs = []
    total_gdp = "N/A"
    total_pop = "N/A"
    avg_life = "N/A"

    if data['dataset'] == 'gapminder':
        country_data = gapminder_df[gapminder_df['country'] == country]
        if country_data.empty:
            graphs = dbc.Alert("Country not found in GapMinder dataset!", color="warning")
        else:
            # Build bar charts for population, lifeExp, and gdpPercap
            metrics = {
                'pop': 'Population',
                'lifeExp': 'Life Expectancy',
                'gdpPercap': 'GDP per Capita'
            }
            all_graphs = []
            for col in metrics:
                fig = px.bar(
                    country_data,
                    x='year',
                    y=col,
                    labels={col: metrics[col], 'year': 'Year'},
                    template='plotly_white',
                    text_auto=True,
                    color_discrete_sequence=['#636EFA']
                )
                fig.update_layout(xaxis={'type': 'category'}, showlegend=False)
                all_graphs.append(
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{metrics[col]} Trend", className="card-title"),
                            dcc.Graph(figure=fig)
                        ])
                    ], className="mb-4")
                )
            graphs = all_graphs

            # Calculate total GDP, total population, average life expectancy
            country_data['totalGDP'] = country_data['pop'] * country_data['gdpPercap']
            total_gdp = f"{country_data['totalGDP'].sum():,.2f}"
            total_pop = f"{country_data['pop'].sum():,.0f}"
            avg_life = f"{country_data['lifeExp'].mean():,.2f}"

    elif data['dataset'] == 'iris':
        # Show a scatter plot for the iris dataset
        fig = px.scatter(
            iris_df,
            x='sepal_length',
            y='petal_length',
            color='species',
            labels={'sepal_length': 'Sepal Length', 'petal_length': 'Petal Length'},
            template='plotly_white'
        )
        graphs = [dcc.Graph(figure=fig)]

    return [
        lat,
        lon,
        dataset,
        country,
        map_div,
        graphs,
        total_gdp,
        total_pop,
        avg_life
    ]

# Callbacks

# Multipage callback
@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    """
    Determines which page layout to display based on the URL pathname.
    """
    if pathname == '/input':
        return input_layout
    elif pathname == '/output':
        return output_layout
    return about_layout

@callback(
    Output('store-data', 'data'),
    Input('submit-button', 'n_clicks'),
    State('lat-input', 'value'),
    State('lon-input', 'value'),
    State('dataset-select', 'value'),
    prevent_initial_call=True
)
def store_data(n_clicks, lat, lon, dataset):
    """
    Stores user inputs (lat, lon, dataset, and detected country) in dcc.Store.
    Uses geopy to reverse geocode the latitude/longitude if 'gapminder' is chosen.
    """
    detected_country = 'N/A'
    if dataset == 'gapminder':
        geolocator = Nominatim(user_agent="dash_app")
        try:
            location = geolocator.reverse((lat, lon), language='en')
            if location:
                address = location.raw.get('address', {})
                detected_country = address.get('country', 'N/A')
        except:
            detected_country = 'N/A'
    return {
        'lat': lat,
        'lon': lon,
        'dataset': dataset,
        'country': detected_country
    }

@callback(
    [
        Output('display-lat', 'children'),
        Output('display-lon', 'children'),
        Output('display-dataset', 'children'),
        Output('display-country', 'children'),
        Output('map-container', 'children'),
        Output('graph-container', 'children'),
        Output('country-total-gdp', 'children'),
        Output('country-total-pop', 'children'),
        Output('country-avg-lifeexp', 'children')
    ],
    Input('store-data', 'data')
)
def update_output(data):
    """
    Updates the Output page fields and visualizations
    based on the stored user data (lat, lon, dataset, country).
    """
    if not data:
        # If no data is submitted yet, show placeholders
        return [
            '', '', '', '',
            dbc.Alert("No data submitted!", color="danger"),
            dbc.Alert("No data submitted!", color="danger"),
            "", "", ""
        ]

    lat = data.get('lat', 'N/A')
    lon = data.get('lon', 'N/A')
    dataset = data.get('dataset', '').title()
    country = data.get('country', 'N/A')

    # Create a map figure
    try:
        lat_val = float(lat)
        lon_val = float(lon)
        map_fig = px.scatter_mapbox(
            lat=[lat_val],
            lon=[lon_val],
            zoom=5,
            height=300
        )
        map_fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r":0,"t":0,"l":0,"b":0}
        )
        map_div = dcc.Graph(figure=map_fig)
    except:
        map_div = dbc.Alert("Invalid coordinates for map", color="danger")

    # Prepare visualizations
    graphs = []
    total_gdp = "N/A"
    total_pop = "N/A"
    avg_life = "N/A"

    if data['dataset'] == 'gapminder':
        country_data = gapminder_df[gapminder_df['country'] == country]
        if country_data.empty:
            graphs = dbc.Alert("Country not found in GapMinder dataset!", color="warning")
        else:
            # Build bar charts for population, lifeExp, and gdpPercap
            metrics = {
                'pop': 'Population',
                'lifeExp': 'Life Expectancy',
                'gdpPercap': 'GDP per Capita'
            }
            all_graphs = []
            for col in metrics:
                fig = px.bar(
                    country_data,
                    x='year',
                    y=col,
                    labels={col: metrics[col], 'year': 'Year'},
                    template='plotly_white',
                    text_auto=True,
                    color_discrete_sequence=['#636EFA']
                )
                fig.update_layout(xaxis={'type': 'category'}, showlegend=False)
                all_graphs.append(
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{metrics[col]} Trend", className="card-title"),
                            dcc.Graph(figure=fig)
                        ])
                    ], className="mb-4")
                )
            graphs = all_graphs

            # Calculate total GDP, total population, average life expectancy
            country_data['totalGDP'] = country_data['pop'] * country_data['gdpPercap']
            total_gdp = f"{country_data['totalGDP'].sum():,.2f}"
            total_pop = f"{country_data['pop'].sum():,.0f}"
            avg_life = f"{country_data['lifeExp'].mean():,.2f}"

    elif data['dataset'] == 'iris':
        # Show a scatter plot for the iris dataset
        fig = px.scatter(
            iris_df,
            x='sepal_length',
            y='petal_length',
            color='species',
            labels={'sepal_length': 'Sepal Length', 'petal_length': 'Petal Length'},
            template='plotly_white'
        )
        graphs = [dcc.Graph(figure=fig)]

    return [
        lat,
        lon,
        dataset,
        country,
        map_div,
        graphs,
        total_gdp,
        total_pop,
        avg_life
    ]

# Callbacks for Filtering & CSV

@callback(
    Output('gapminder-table', 'data'),
    Input('pop-min-input', 'value'),
    Input('pop-max-input', 'value'),
    Input('lifeexp-min-input', 'value'),
    Input('lifeexp-max-input', 'value'),
    Input('country-dropdown', 'value')
)
def update_gapminder_table(pop_min, pop_max, lifeexp_min, lifeexp_max, selected_countries):
    """
    Filter the gapminder_df based on the numeric filters for population and life expectancy,
    and update the DataTable.
    """
    filtered_df = gapminder_df.copy()

    # Filter by population
    filtered_df = filtered_df[
        (filtered_df['pop'] >= pop_min) &
        (filtered_df['pop'] <= pop_max)
    ]

    # Filter by life expectancy
    filtered_df = filtered_df[
        (filtered_df['lifeExp'] >= lifeexp_min) &
        (filtered_df['lifeExp'] <= lifeexp_max)
    ]

    # Filter by selected countries (if any)
    if selected_countries:
        filtered_df = filtered_df[filtered_df['country'].isin(selected_countries)]

    return filtered_df.to_dict('records')

@callback(
    Output('download-dataframe-csv', 'data'),
    Input('download-btn', 'n_clicks'),
    State('pop-min-input', 'value'),
    State('pop-max-input', 'value'),
    State('lifeexp-min-input', 'value'),
    State('lifeexp-max-input', 'value'),
    State('country-dropdown', 'value'),
    prevent_initial_call=True
)
def download_filtered_csv(n_clicks, pop_min, pop_max, lifeexp_min, lifeexp_max, selected_countries):
    """
    Applies the same numeric filters and returns a CSV for download.
    """
    filtered_df = gapminder_df.copy()

    # Filter by population
    filtered_df = filtered_df[
        (filtered_df['pop'] >= pop_min) &
        (filtered_df['pop'] <= pop_max)
    ]

    # Filter by life expectancy
    filtered_df = filtered_df[
        (filtered_df['lifeExp'] >= lifeexp_min) &
        (filtered_df['lifeExp'] <= lifeexp_max)
    ]

    # Filter by selected countries
    if selected_countries:
        filtered_df = filtered_df[filtered_df['country'].isin(selected_countries)]

    return dcc.send_data_frame(filtered_df.to_csv, "filtered_gapminder.csv")
