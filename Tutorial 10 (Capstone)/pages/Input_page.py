import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd
import plotly.express as px
from flask import redirect, url_for, request, session, flash
from geopy.geocoders import Nominatim  # For reverse geocoding
import dash.dash_table as dt
from pages.about import dbc


# Input Layout 

input_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Input Parameters", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Geographical Coordinates", className="card-title"),
                    dbc.Form([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Latitude:", html_for="lat-input"),
                                dbc.Input(type="number", id="lat-input", value=39.0)
                            ], md=6),
                            dbc.Col([
                                dbc.Label("Longitude:", html_for="lon-input"),
                                dbc.Input(type="number", id="lon-input", value=-79.0)
                            ], md=6)
                        ]),
                        html.Div("Country will be auto-detected based on Latitude and Longitude.", className="mt-3"),
                        html.Hr(),
                        dbc.Label("Dataset Selection:", className="mt-2"),
                        dbc.Select(
                            id='dataset-select',
                            options=[
                                {'label': 'GapMinder', 'value': 'gapminder'},
                                {'label': 'Iris Dataset', 'value': 'iris'}
                            ],
                            value='gapminder'
                        ),
                        dbc.Button("Submit", id='submit-button', color="primary", className="mt-4 w-100")
                    ])
                ])
            ])
        ], width=8, className="mx-auto")
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(className="mt-4 text-center", children=[
                dbc.Button("Back to About", href="/", color="light", className="mr-2"),
                dbc.Button("View Results", href="/output", color="success")
            ])
        ], width=12)
    ])
], className="mt-5")

