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
from dash.dependencies import Input, Output

# def create_state_map(): 

    # data = pd.read_csv('climate_disasters_2000_2023_clean.csv')

    # # USA Map aggregated by Incident Type
    # fig = px.choropleth(data, locations='state',
    #                     locationmode="USA-states", color='disaster_type', scope="usa")
    
    # fig.show()

# from economic_impact import *

# df = clean_disaster_summaries()
# df_t = df.groupby(["state_code", "year"], as_index=False)["federalObligatedAmount"].sum()

# col_names = df_t.columns.tolist()
# fig = px.choropleth(df_t, locations='state_code',
#                         locationmode="USA-states", color='federalObligatedAmount', scope="usa",
#                         color_continuous_scale=px.colors.sequential.OrRd,
#                         hover_name = ('state_code'),
#                         animation_frame = 'year'
# )

# fig.show()


from climate_datasets import *

df = get_cleaned_data("disaster_declarations.csv")
data = number_of_disaster_events_by_state(df)

grouped_data = data.groupby(["state", "year"], as_index=False)["total_number_of_events"].sum()

fig1 = px.choropleth(grouped_data, locations='state',
                        locationmode="USA-states", color='total_number_of_events', scope="usa",
                        color_continuous_scale=px.colors.sequential.OrRd,
                        animation_frame = 'year',
                        # range_color = (0, 60)
)

fig1.show()