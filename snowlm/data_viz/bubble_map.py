import dash
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

########################################################

# df = get_climate_econ_pop_data()
# df['state_pop'] = df['state_pop'].str.replace(',','')
# df["state_pop"]= pd.to_numeric(df["state_pop"])


# data = df.groupby(["state", 'year', 'state_pop']).agg({"total_number_of_events": "sum", "fed_amount":"sum"}).reset_index()
# data = data.sort_values('year', ascending=True)

# fig = px.scatter(data, x="total_number_of_events", y="fed_amount", size="state_pop", 
#                 animation_frame="year", color = "state", hover_name = "state")

# fig.show()

# from climate_datasets import *
# from economic_impact import *
# from bring_it_all_together_test import *
# from census_api_query import *

# climate_df = get_cleaned_data ("disaster_declarations.csv", only_2000_onwards = False)
# climate_summary = number_of_disaster_events_by_state (climate_df)
# change_in_frequency(climate_summary)
# number_of_disasters_stat = number_of_disasters_over_last_decade(climate_summary)

# df_climate_summary = climate_summary.groupby(["year", "disaster_type"])["total_number_of_events"].sum().reset_index()

# fig = px.bar(data_frame=df_climate_summary, x='total_number_of_events', y='year', color = "disaster_type")
# fig.update_yaxes(categoryorder='category descending')

# fig.show()

from snowlm.data_analysis.climate import *
from snowlm.data_analysis.economic_impact import *
from snowlm.data_analysis.climate_econ_pop import *
from snowlm.scrape_api.census_api_query import *


climate_df = get_cleaned_data ("snowlm/data/disaster_declarations.csv", only_2000_onwards = False)

# states = number_of_days_in_dec_disaster(climate_df).keys()
# values = number_of_days_in_dec_disaster(climate_df).values()

# fig1 = px.bar(x = states, y = values)
# fig1.show()

num_days_in_disaster = {"states": number_of_days_in_dec_disaster(climate_df).keys(),
    "values": number_of_days_in_dec_disaster(climate_df).values()}
disaster_days = pd.DataFrame.from_dict(num_days_in_disaster)

fig4 = px.bar(disaster_days, x = "states", y = "values")
highlight_values = ["TX", 'National Average']
highlight_color = ['green']
fig4.update_traces(marker=dict(color=[highlight_color if x in highlight_values else 'blue' for x in disaster_days["states"]]))


fig4.show()
