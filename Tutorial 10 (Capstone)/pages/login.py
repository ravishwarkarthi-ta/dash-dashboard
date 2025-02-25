import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd
import plotly.express as px
from flask import redirect, url_for, request, session, flash
from geopy.geocoders import Nominatim  # For reverse geocoding
import dash.dash_table as dt

# For CSV download (dcc.Download)
from dash import dcc  # ensures we have dcc.Download

# Load datasets
gapminder_df = px.data.gapminder()
iris_df = px.data.iris()

# Initialize the Dash app with Bootstrap
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
server.secret_key = 'your_secret_key_here'  # Needed for session management


# Flask routes for login/logout

@server.before_request
def require_login():
    """
    This function runs before every request.
    It checks if the user is logged in, except for the /login and /logout endpoints,
    static assets, or Dash assets (/_dash-*).
    If not logged in, it redirects to /login.
    """
    if request.path in ['/login', '/logout'] or request.path.startswith('/static') or request.path.startswith('/_dash-'):
        return None
    if not session.get('logged_in'):
        return redirect(url_for('login'))

@server.route('/login', methods=['GET', 'POST'])
def login():
    """
    A simple login route using hardcoded credentials (admin/password).
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # For demonstration, using hardcoded credentials:
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect('/')
        else:
            flash("Invalid credentials", "danger")
    # A simple login form using Bootstrap CSS
    return '''
    <html>
    <head>
      <title>Login</title>
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    </head>
    <body>
      <div class="container" style="max-width: 400px; margin-top: 100px;">
        <h2 class="text-center">Login</h2>
        <form method="post">
          <div class="form-group">
            <label>Username</label>
            <input type="text" name="username" class="form-control" placeholder="Enter username" required>
          </div>
          <div class="form-group">
            <label>Password</label>
            <input type="password" name="password" class="form-control" placeholder="Enter password" required>
          </div>
          <button type="submit" class="btn btn-primary btn-block">Login</button>
        </form>
      </div>
    </body>
    </html>
    '''

@server.route('/logout')
def logout():
    """
    Logout route. Pops the 'logged_in' session key and redirects to /login.
    """
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Define the multipage navigation bar

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("About", href="/")),
        dbc.NavItem(dbc.NavLink("Input", href="/input")),
        dbc.NavItem(dbc.NavLink("Output", href="/output")),
        # Logout link: using html.A ensures a full page refresh
        dbc.NavItem(html.A("Logout", href="/logout", className="nav-link"))
    ],
    brand="Tiger Analytics",
    brand_href="/",
    color="primary",
    dark=True,
    sticky="top"
)


# Dash app layout

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='store-data'),
    navbar,  # Multipage navigation bar at the top
    html.Div(id='page-content', style={"marginTop": "75px"})  # Add top margin to avoid navbar overlap
])



