from  bring_it_all_together_test import *
import dash
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
# import dash_bootstrap_components as dbc

########################################################

df = get_climate_econ_data()

df1 = df.groupby(["state", "year"])["total_number_of_events"].sum().reset_index()
df2 = df.groupby(["state", "year"])["fed_amount"].sum().reset_index()

# Create the app
app = dash.Dash(__name__)

dropdown_options = [
    {'label': 'Total Number of Disaster Events', 'value': 'map1'},
    {'label': 'Total FEMA Public Assistance Funding', 'value': 'map2'}
]

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=dropdown_options,
        value='map1'
    ),
    dcc.Graph(
        id='choropleth-map',
        style={'width': '100vw', 'height': '90vh'},
    ),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='line-chart')  
]) 

@app.callback(
    Output('choropleth-map', 'figure'), #Output('output', 'children'),
    Input('dropdown', 'value') #Input('choropleth-map', 'clickData')
)
def update_choropleth_map(selected_map):
    if selected_map == 'map1':
        fig = px.choropleth(df1, locations='state', color='total_number_of_events', 
                            scope='usa', locationmode='USA-states', 
                            animation_frame = 'year',
                            color_continuous_scale=px.colors.sequential.OrRd)
    else:
        fig = px.choropleth(df2, locations='state', color='fed_amount', 
                            scope='usa', locationmode='USA-states', 
                            animation_frame = 'year',
                            color_continuous_scale=px.colors.sequential.OrRd)
    return fig


@app.callback(
    Output('bar-chart', 'figure'),
    Output('line-chart', 'figure'),
    Input('choropleth-map', 'clickData')
)

def generate_graphs(clickData):
    if clickData is None:
        return {}, {}
    
    state = clickData['points'][0]['location']
    click_data = df1[df1['state'] == state]

    fig1 = px.bar(data_frame=click_data, x='year', y='total_number_of_events')

    # create a line chart
    fig2 = px.line(data_frame=click_data, x='year', y='total_number_of_events')

    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=False)

############################################

#Add Graphs when you click on a state

# define the function that generates the graphs
# def generate_graphs(state):
#     # create a bar chart
#     data = df[df['state'] == state]
#     fig1 = px.bar(data_frame=df1, x='state', y='fed_amount')

#     # create a line chart
#     fig2 = px.line(data_frame=df1, x='year', y='total_number_of_events', color='disaster_type')

#     # display the graphs
#     fig1.show()
#     fig2.show()

# @app.callback(
#     Output('output', 'children'),
#     Input('choropleth-map', 'clickData')
# )

# # set up the on_click event handler
# fig.on_click(lambda trace, points, state_code: generate_graphs(state))