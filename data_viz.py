import dash
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
import geopandas as gpd
import shapely
#import pyshp
import pandas as pd
import numpy as np
import json
from dash import Dash, html, dcc

# def create_state_map(): 

    # data = pd.read_csv('climate_disasters_2000_2023_clean.csv')

    # # USA Map aggregated by Incident Type
    # fig = px.choropleth(data, locations='state',
    #                     locationmode="USA-states", color='disaster_type', scope="usa")
    
    # fig.show()

from economic_impact import *

df = clean_disaster_summaries()
df_t = df.groupby(["state_code", "year"], as_index=False)["federalObligatedAmount"].sum()

col_names = df_t.columns.tolist()
fig = px.choropleth(df_t, locations='state_code',
                        locationmode="USA-states", color='federalObligatedAmount', scope="usa",
                        color_continuous_scale=px.colors.sequential.OrRd,
                        hover_name = ('state_code'),
                        animation_frame = 'year'
)

fig.show()

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
