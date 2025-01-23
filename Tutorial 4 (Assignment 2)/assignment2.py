import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Loading the dataset
df = pd.read_csv('gapminderDataFiveYear.csv')

# Initializing Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Gapminder Visualization Assignment to implement Slider,Dropdown and Radio Function"),
    
    # Dropdown for year selection
    html.Label('Dropdown option'),
    dcc.Dropdown(
        id='dropdown-year-option',
        options=[{'label': year, 'value': year} for year in df['year'].unique()],
        value=2007,  # Default
        clearable=False
    ),
    html.Br(),

    # Radio items for selecting a specific city
    html.Label('Radio items for cities'),
    dcc.RadioItems(
        id='country-radio-function',
        options=[{'label': country, 'value': country} for country in df['country'].unique()],
        value='Afghanistan',  # Default
        labelStyle={'display': 'inline-block'}
    ),
    
    html.Br(),
    html.Label('Slider'),
    dcc.Slider(
        id='slider-function',
        min=0,
        max=25,
        step=1,
        marks={i: str(i) for i in range(0, 26)},
        value=1,
    ),
    html.Br(),

    html.Label('Text Input'),
    html.Br(),
    dcc.Input(
        id='input-text-box',
        type='text',  
        placeholder='Input text' 
    ),
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
