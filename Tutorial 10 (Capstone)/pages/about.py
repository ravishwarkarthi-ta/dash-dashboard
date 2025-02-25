import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd
import plotly.express as px
from flask import redirect, url_for, request, session, flash
from geopy.geocoders import Nominatim  # For reverse geocoding
import dash.dash_table as dt
import pages.login
from pages.login import gapminder_df
from pages.login import dbc

# About Page Layout 
about_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Introduction to GapMinder", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.P("This application visualizes socio-economic indicators from the GapMinder dataset.",
                   className="lead"),
            html.Hr(),
            dbc.Card([
                dbc.CardBody([
                    html.H4("Features:", className="card-title"),
                    html.Ul([
                        html.Li("Interactive data visualization"),
                        html.Li("Multi-year historical trends"),
                        html.Li("Country-specific metrics")
                    ])
                ])
            ]),
            html.Div(className="mt-4", children=[
                dbc.Button("Get Started", href="/input", color="primary", className="mr-2"),
                dbc.Button("View Output", href="/output", color="secondary")
            ])
        ], width=8, className="mx-auto")
    ]),

    # Filter Controls using Greater Than / Less Than Inputs
    dbc.Row([
        dbc.Col([
            html.H5("Filter Options", className="mb-3"),
            
            # Population Filter
            dbc.Label("Population Filter:"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Minimum Population:"),
                    dbc.Input(
                        id='pop-min-input', 
                        type='number', 
                        value=int(gapminder_df['pop'].min())
                    )
                ], md=6),
                dbc.Col([
                    dbc.Label("Maximum Population:"),
                    dbc.Input(
                        id='pop-max-input', 
                        type='number', 
                        value=int(gapminder_df['pop'].max())
                    )
                ], md=6)
            ]),
            html.Br(),

            # Life Expectancy Filter
            dbc.Label("Life Expectancy Filter:"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Minimum Life Expectancy:"),
                    dbc.Input(
                        id='lifeexp-min-input', 
                        type='number', 
                        value=gapminder_df['lifeExp'].min()
                    )
                ], md=6),
                dbc.Col([
                    dbc.Label("Maximum Life Expectancy:"),
                    dbc.Input(
                        id='lifeexp-max-input', 
                        type='number', 
                        value=gapminder_df['lifeExp'].max()
                    )
                ], md=6)
            ]),
            html.Br(),

            # Country dropdown (multi-select)
            dbc.Label("Country:"),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': c, 'value': c} for c in sorted(gapminder_df['country'].unique())],
                multi=True,
                placeholder="Select one or more countries"
            ),
            html.Br(),

            # Download button + Download component
            dbc.Button("Download Filtered CSV", id='download-btn', color="info"),
            dcc.Download(id='download-dataframe-csv'),
        ], width=12)
    ], className="mt-4"),

    # DataTable
    dbc.Row([
        dbc.Col([
            html.H3("Explore Countries", className="text-center mt-5 mb-3"),
            dt.DataTable(
                id='gapminder-table',
                columns=[
                    {'name': 'Country', 'id': 'country'},
                    {'name': 'Continent', 'id': 'continent'},
                    {'name': 'Year', 'id': 'year'},
                    {'name': 'Population', 'id': 'pop'},
                    {'name': 'Life Expectancy', 'id': 'lifeExp'},
                ],
                data=gapminder_df.to_dict('records'),
                filter_action='native',  # Built-in filter 
                sort_action='native',
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'}
            )
        ], width=12)
    ])
], className="mt-5")


