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
    # Multiselect dropdown for selecting years
    dcc.Dropdown(
        id='year-dropdown-function',
        options=[{'label': str(year), 'value': year} for year in df['year'].unique()],
        value=[2007],  # Default value
        multi=True
    ),
    
    html.H1("GDP vs Life Expectancy of Different countries (1952-2007)"),
    
    # Pie chart
    dcc.Graph(id='scatter-plot-two-inputs')
])

# Callback function that updates the pie chart (Output) based on selected countries (Input)
@app.callback(
    Output('scatter-plot-two-inputs', 'figure'),
    [Input('country-dropdown-function', 'value'),
     Input('year-dropdown-function', 'value')]
)

def updation_of_scatter_plot(chosen_countries, chosen_years):

    # Another if condition for the chosen countries if nothing is chosen
    if chosen_countries is None or len(chosen_countries) == 0:
     return {}
    
    else:

     # Filtered data of the chosen countries
     filtered_df = df[df['country'].isin(chosen_countries) & (df['year'].isin(chosen_years))]
    
     # Aggregated data to get the latest GDP per capita stat for every selected country (latest year)
     newest_gdp_df = filtered_df.loc[filtered_df.groupby('country')['year'].idxmax()][['country', 'gdpPercap']]

     # Creating a pie chart based on the provided values
    fig = px.scatter(
               filtered_df,
               x='gdpPercap',
               y='lifeExp',
               color='country',
               title=f'Life Expectancy vs GDP per Capita ({", ".join(map(str, chosen_years))})',
               labels={'gdpPercap': 'GDP per Capita', 'lifeExp': 'Life Expectancy'},
               hover_name='country'

        )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
