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

def create_state_map(): 
    data = pd.read_csv('climate_disasters_2000_2023_clean.csv')

    # USA Map aggregated by Incident Type
    fig = px.choropleth(data, locations='state',
                        locationmode="USA-states", color='disaster_type', scope="usa")
    
    fig.show()


# County Level Map for California
def create_county_level_map():

    data = pd.read_csv('climate_disasters_2000_2023_clean.csv')

    df = data[data['state'] == 'CA']

    values = df['incidentType'].tolist()
    fips = df['fipsCountyCode'].tolist()

    fig = ff.create_choropleth(fips=fips, values=values)
    fig.layout.template = None

    fig.show()

# d = data.loc[:, ['state', 'incidentType', 'fipsStateCode', 'fipsCountyCode']]
# d.incidentType.value_counts()
# d.groupby(['state', 'incidentType']).count()
 
# from urllib.request import urlopen
# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)

# fig = px.choropleth(perCountry, geojson=counties, locations='FIPS', 
#                     color='Cases',
#                     color_continuous_scale=px.colors.sequential.OrRd,
#                     color_continuous_midpoint=2,
#                     range_color=(1, 20),
#                     scope="usa",
#                     labels={'Cases':'Confirmed'}, 
#                     hover_name = 'Province_State'
#                     )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()