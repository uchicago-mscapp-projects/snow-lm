import dash
# import dash_html_components as html
# import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.figure_factory as ff

data = pd.read_csv('disaster_declarations.csv')

# USA Map aggregated by Incident Type
fig = px.choropleth(data, locations='state',
                    locationmode="USA-states", color='incidentType', scope="usa")
 
fig.show()


# County Level Map for California
def create_county_level_map(data):

    df = data[data['state'] == 'CA']

    values = df['incidentType'].tolist()
    fips = df['fipsCountyCode'].tolist()

    colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
    "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
    "#08519c", "#0b4083", "#08306b"]

    





