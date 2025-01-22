import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

df = px.data.tips()
# Initializing the Dash app
app = dash.Dash(__name__)

# Defining the layout of the app
app.layout = html.Div(
    children=[


         # Adding a container for the dropdowns with flex display
        html.Div(
            style={
                "display": "flex",           # Using flexbox to arrange items horizontally
            },
            children=[
        # Adding a dropdown below the bordered text
    dbc.Select(
    id="select",
    options=[
        {"label": "Smoker", "value": "1"},
        {"label": "Non Smoker", "value": "2"},
    ],
)

         ]
        ),
        # Adding a bar graph below the dropdown
        dcc.Graph(

            figure = px.bar(df, x="sex", y="total_bill", color='smoker')
        ),
    ]
)

# Running the app
if __name__ == "__main__":
    app.run_server(debug=True)

