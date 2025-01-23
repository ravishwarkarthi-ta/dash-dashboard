import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

# Loading data from gapminder csv file
df = pd.read_csv('gapminderDataFiveYear.csv')

# Creating a Dash application
app = dash.Dash(__name__)

app.layout = html.Div([
    
    
    # Multiselect dropdown for selecting countries
    dcc.Dropdown(
        id='country-dropdown-function',
        options=[{'label': country, 'value': country} for country in df['country'].unique()],
        multi=True,
        placeholder="Please Select from the list of countries"
    ),
    
    html.H1("GDP of Different countries (1952-2007)"),

    html.Button('Submit', id='submit-button', n_clicks=0),
    
    # Pie chart
    dcc.Graph(id='gdp-pie-chart-function')
])

# Callback function that updates the pie chart (Output) based on selected countries (Input)
@app.callback(
    Output('gdp-pie-chart-function', 'figure'),
    Input('submit-button', 'n_clicks'),
    State('country-dropdown-function', 'value')
)

def dynamic_updation_of_pie_chart(n_clicks,chosen_countries):
# An if condition for the number of clicks being above 0
 if n_clicks > 0: 
    # Another if condition for the chosen countries if nothing is chosen
    if chosen_countries is None or len(chosen_countries) == 0:
     return {}
    
    else:

     # Filtered data of the chosen countries
     filtered_df = df[df['country'].isin(chosen_countries)]
    
     # Aggregated data to get the latest GDP per capita stat for every selected country (latest year)
     newest_gdp_df = filtered_df.loc[filtered_df.groupby('country')['year'].idxmax()][['country', 'gdpPercap']]

     # Creating a pie chart based on the provided values
     fig = px.pie(newest_gdp_df, values='gdpPercap', names='country', title='GDP per Capita (Chosen Countries)')
    
     return fig
 else:
    return {}

if __name__ == '__main__':
    app.run_server(debug=True)
