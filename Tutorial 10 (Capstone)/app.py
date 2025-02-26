import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd
import plotly.express as px
from flask import redirect, url_for, request, session, flash
from geopy.geocoders import Nominatim  # For reverse geocoding
import dash.dash_table as dt
import pages.output
from pages.login import app

if __name__ == '__main__':
    app.run_server(debug=True)