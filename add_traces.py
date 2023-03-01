from  bring_it_all_together_test import *
import dash
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output


# traces = []

# trace1 = go.Choropleth(locations=df_trace1['state'],
#                         locationmode="USA-states", z=df_trace1['total_number_of_events'],
#                         colorscale=px.colors.sequential.OrRd,
# )

# traces.append(trace1)

# trace2 = go.Choropleth(locations=df_trace2['state'],
#                         locationmode="USA-states", z=df_trace2['fed_amount'],
#                         colorscale=px.colors.sequential.OrRd,
# )

# # Create the layout for the map
# map_layout = go.Layout(
#     title='Climate Didasters in the US',
#     geo_scope='usa'
# )


# traces.append(trace2)

# # initial_trace = traces[0]

# fig = go.Figure(data=traces, layout=map_layout)

# fig.update_layout(updatemenus=[dict(type='dropdown', buttons=list([
#     dict(label='Total Number of Disaster Events', method='update', args=[{'visible': [True, False]}]),
#     dict(label='Total FEMA Public Assistance Funding', method='update', args=[{'visible': [False, True]}]),
# ])),
# ])

# app = dash.Dash(__name__)

# app.layout = html.Div([
#     html.H1('Choropleth Map with Year Slider'),
#     dcc.Graph(id='choropleth-map', figure=fig),
#     dcc.Slider(
#         id='year-slider',
#         min=df['year'].min(),
#         max=df['year'].max(),
#         value=df['year'].min(),
#         marks={str(year): str(year) for year in df['year'].unique()},
#         step=None
#     )
# ])

# # Define the callback to update the choropleth map
# @app.callback(
#     dash.dependencies.Output('choropleth-map', 'figure'),
#     [dash.dependencies.Input('year-slider', 'value')]
# )
# def update_choropleth_map(selected_year):
#     # Filter the data for the selected year
#     filtered_df = df[df['year'] == selected_year]

#     # Update the z values for the choropleth map trace
#     fig.update_traces(
#         z=[filtered_df['value']],
#         locationmode='USA-states'
#     )

#     return fig

# # Run the app
# if __name__ == '__main__':
#     app.run_server()
# # Show the figure



###########################################################
# df = get_climate_econ_data()

# df1 = df.groupby(["state", "year"])["total_number_of_events"].sum().reset_index()
# df2 = df.groupby(["state", "year"])["fed_amount"].sum().reset_index()

# # Create the app
# app = dash.Dash(__name__)

# # Define the layout
# app.layout = html.Div([
#     dcc.Dropdown(
#         id='map-dropdown',
#         options=[
#             {'label': 'Map 1', 'value': 'map1'},
#             {'label': 'Map 2', 'value': 'map2'}
#         ],
#         value='map1'
#     ),
#     dcc.Graph(
#         id='map-graph'
#     ),
#     dcc.Slider(
#         id='year-slider',
#         min=df['year'].min(),
#         max=df['year'].max(),
#         value=df['year'].min(),
#         marks={str(year): str(year) for year in df['year'].unique()},
#         step=None
#     )
# ])

# # Define the callback function
# @app.callback(
#     Output('map-graph', 'figure'),
#     Input('map-dropdown', 'value')
# )
# def update_map(selected_map):
#     # Update the data based on the selected map
#     if selected_map == 'map1':
#         locations = df1['state']
#         z = df1['total_number_of_events']
#         # text = df1['name']
#         colorscale = 'Reds'
#         # zmin = 0
#         # zmax = 1000
#     elif selected_map == 'map2':
#         locations = df2['state']
#         z = df2['fed_amount']
#         # text = df2['name']
#         colorscale = 'YlOrRd'
#         # zmin = 0
#         # zmax = 2000

#     # Create the choropleth map figure
#     fig = go.Figure(
#         go.Choropleth(
#             locations=locations,
#             z=z,
#             # text=text,
#             colorscale=colorscale,
#             # zmin=zmin,
#             # zmax=zmax
#         )
#     )

#     # Set the layout
#     fig.update_layout(
#         title=selected_map.capitalize(),
#         geo_scope='usa'
#     )

#     return fig

# # Run the app
# if __name__ == '__main__':
#     app.run_server()

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
        style={'width': '100vw', 'height': '90vh'}
    ),
    # autosize=True,
    # margin=dict(t=0, b=0, l=0, r=0)
]) #style={'width': '100%', 'height': '500px'})

@app.callback(
    Output('choropleth-map', 'figure'),
    Input('dropdown', 'value')
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

if __name__ == '__main__':
    app.run_server(debug=False)