from  bring_it_all_together_test import *
import dash
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import numpy as np

# data = get_climate_econ_data()

# # data = df.groupby(["state", "year"], as_index=False) #["fed_amount"].sum().reset_index()

# # Create a Sankey trace
# fig = go.Figure(data=[go.Sankey(
#     node=dict(
#         pad=15,
#         thickness=20,
#         line=dict(color="black", width=0.5),
#         label=data['state'].unique().tolist() + data['disaster_type'].unique().tolist()
#     ),
#     link=dict(
#         source=data['year'].apply(lambda x: int(x) - 2000),
#         target=data['state'].apply(lambda x: data['state'].unique().tolist().index(x)),
#         value=data['fed_amount'],
#         label=data['disaster_type']

#     ))])
# # print(data)
# # Create the layout
# fig.update_layout(
#     title="State and Amount of FEMA Public Assistance money disbursed over Time",
#     font=dict(size=12),
#     height=500,
#     width=800,
#     xaxis=dict(title="Year"),
#     yaxis=dict(title="State/Disaster Type")
# )

# # # Plot the Sankey map
# fig.show()

# data = pd.DataFrame({
#     'state': ['California', 'New York', 'Texas', 'Florida', 'California', 'New York', 'Texas', 'Florida'],
#     'year': [2015, 2015, 2015, 2015, 2016, 2016, 2016, 2016],
#     'amount': [100, 50, 75, 200, 150, 75, 100, 250]
# })

# # Create a Sankey trace
# fig = go.Figure(data=[go.Sankey(
#     node=dict(
#         pad=15,
#         thickness=20,
#         line=dict(color="black", width=0.5),
#         label=data['state'].unique()
#     ),
#     link=dict(
#         source=data['year'].apply(lambda x: x - 2015),
#         target=data['state'].apply(lambda x: np.where(data['state'].unique() == x)[0][0]),
#         value=data['amount']
#     ))])

# # Create the layout
# fig.update_layout(
#     title="Amount of Money Disbursed to States over Years",
#     font=dict(size=12),
#     height=500,
#     width=800,
#     xaxis=dict(title="Year"),
#     yaxis=dict(title="State")
# )

# # Plot the Sankey diagram
# fig.show()


#################################
