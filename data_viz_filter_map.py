import dash
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

from climate_datasets import *

df = get_cleaned_data("disaster_declarations.csv")
data = number_of_disaster_events_by_state(df)


dropdown_df = data.groupby(["state", "year", "disaster_type"]).agg({"total_number_of_events": "sum"}).reset_index()
fig = px.choropleth(
    data_frame=dropdown_df,
    locations='state',
    locationmode='USA-states',
    color='total_number_of_events',
    scope='usa',
    color_continuous_scale=px.colors.sequential.OrRd,
    animation_frame = 'year'
)

fig.show()
# dropdown_options = [{'label': row['distaster_type'], 'value': row['value']} for index, row in dropdown_df.iterrows()]

# app = dash.Dash(__name__)

# app.layout = html.Div([
#     html.H1('Weather-related disasters in USA'),
#     dcc.Dropdown(
#         id='my-dropdown',
#         options=dropdown_options,
#         value=dropdown_options[0]['value']
#     ),
#     dcc.Graph(id='my-graph')
# ])

# # Define the callback to update the graph
# @app.callback(
#     dash.dependencies.Output('my-graph', 'figure'),
#     [dash.dependencies.Input('my-dropdown', 'value')]
# )
# def update_graph(value):
#     # Filter the data based on the selected dropdown value
#     filtered_df = grouped_data[grouped_data['category'] == value]

    # Create the choropleth map
    # fig = px.choropleth(
    #     data_frame=filtered_df,
    #     locations='state_code',
    #     locationmode='USA-states',
    #     color='tota_number_of_events',
    #     scope='usa',
    #     color_continuous_scale='reds'
    # )

    # return fig

# Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)



# fig1.add_trace(px.choropleth(dropdown_data, locations='state',
#                         locationmode="USA-states", color='disaster_type', scope="usa",
#                         color_continuous_scale=px.colors.sequential.OrRd,
#                         animation_frame = 'year'
# ))

# fig1.update_layout(
#     updatemenus=[
#         dict(
#             buttons=list([
#                 dict(
#                     label='Total Number of Disaster Events',
#                     method='update',
#                     args=[{'visible': [True, False]}, {'title': 'Option 1'}, {"type":"total_number_of_events"}]
#                 ),
#                 dict(
#                     label='FEMA Distribution of Public Assistance Funds',
#                     method='update',
#                     args=[{'visible': [False, True]}, {'title': 'Option 2'}, {"type":"disaster_type"}]
#                 )
#             ]),
#             direction='down',
#             showactive=True,
#             active=0,
#             x=0.1,
#             y=1.1
#         )
#     ]
# )
# fig1.show()


# app = dash.Dash()

# app.layout = html.Div([
#     dcc.Dropdown(['incidentType'])
# ])

# fig  = go.Figure()

# fig.add_trace(px.choropleth(df_t, locations='state_code',
#                         locationmode="USA-states", color='federalObligatedAmount', scope="usa",
#                         color_continuous_scale=px.colors.sequential.OrRd,
#                         hover_name = ('state_code')
# ))

# fig.update_layout(
#     updatemenus=[
#         dict(
#             buttons=list([
#                 dict(
#                     args=["type", "surface"],
#                     label="3D Surface",
#                     method="restyle"
#                 ),
#                 dict(
#                     args=["type", "heatmap"],
#                     label="Heatmap",
#                     method="restyle"
#                 )
#             ]),
#             direction="down",
#             pad={"r": 10, "t": 10},
#             showactive=True,
#             x=0.1,
#             xanchor="left",
#             y=1.1,
#             yanchor="top"
#         ),
#     ]
# )

# steps = []


# Cleaning PA dataset - year, incident types, severe storms(s)
# Merged dataset for dropdowns