#Importing required packages
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd


#Load the data
df = pd.read_csv('https://raw.githubusercontent.com/ct0571/visualization/main/airbnb.csv')

# Attaching the theme from bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])


# Set up the layout
app.layout = dbc.Container([
    # Styling the title
    dbc.Row(
        dbc.Col(html.H1("Boston Airbnb Analysis",
                         className='text-center text-primary'),
                width=12)
    ),
    dbc.Row([
        
        dbc.Col(html.P("Count of ID: 1,154", className='font-weight-bold'), 
            width = 3
        ),
        dbc.Col(html.P("Average Host Identity: 55%", className='font-weight-bold'), 
            width = 3
        ),
        dbc.Col(html.P("Airbnb in Exact Location: 86.40%", className='font-weight-bold'), 
            width = 3
        ),
        dbc.Col(html.P("Average Host Identity: 55%", className='font-weight-bold'), 
            width = 3
        ),
    ], style={'margin-top': '2rem', 'margin-bottom': '2rem', 'padding': '1rem', 'font-size':'18px',
              'border-radius': '7px', 'border': '3px solid coral', 'background-color':'#15e676', 'font-weight':'bold'
            }),
   
   #Creating the graphs
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='dropdown1', multi=False, value='Loft',
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df['property_type'].unique())],
                         ),
            dcc.Graph(id='scatter-fig', figure={}),
        ], width=6, style={'margin-top': '2rem', 'margin-bottom': '2rem', 'padding': '1rem'}),

        dbc.Col([
            dcc.Dropdown(id='dropdown2', multi=True, value=['Loft', 'House'],
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df['property_type'].unique())],
                         ),
            dcc.Graph(id='line-fig', figure={})
        ], width=6, style={'margin-top': '2rem', 'margin-bottom': '2rem', 'padding': '1rem'}),
    ], style = {'border-radius': '7px', 'border': '3px solid coral'}),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='dropdown3', multi=True, value=['Loft', 'House'],
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df['property_type'].unique())],
                         ),
            dcc.Graph(id='sunburst-fig', figure={})
        ], width=12, style={'margin-top': '2rem', 'margin-bottom': '2rem', 'padding': '1rem', 
                            'border-radius': '7px', 'border': '3px solid coral'})
    ])
],style={'margin-top': '2rem', 'margin-bottom': '2rem', 'padding': '1rem'})

# Callback section: connecting the components
# Scatter plot
@app.callback(
    Output('scatter-fig', 'figure'),
    Input('dropdown1', 'value')
)
def update_graph(property_slctd):
    dff = df[df['property_type']==property_slctd]
    figln = px.scatter(dff, x='price', y='room_type', color='host_identity_verified', title = 'Scatter Plot of Room Type and Price')
    return figln

@app.callback(
    Output('line-fig', 'figure'),
    Input('dropdown2', 'value')
)
def update_graph(property_slctd):
    dff = df[df['property_type'].isin(property_slctd)]
    figln2 = px.line(dff, x='price', y='room_type', color='is_location_exact', title='Line Chart of Room Type and Price')
    return figln2


#sunburst chart
@app.callback(
    Output('sunburst-fig', 'figure'),
    Input('dropdown3', 'value')
)

# create the sunburst chart using Plotly Express
def update_graph(property_slctd):
    dff = df[df['property_type'].isin(property_slctd)]
    fig = px.sunburst(dff, path=['room_type', 'cancellation_policy', 'neighbourhood_cleansed'], 
                      values='number_of_reviews', color='room_type', 
                      title = 'Sunburst Chart of the Room Type, Cancellation Policy and the Clean Neighbourhood')
    fig.update_layout(
    width=800, 
    height=600, 
    )
    return fig


#Running the dash app
if __name__=='__main__':
    app.run_server(debug=True)

    
