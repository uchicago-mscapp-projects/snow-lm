import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from dash import dash_table
from dash_bootstrap_templates import load_figure_template


# Importing cleaned datasets from other files
from snowlm.data_analysis.climate import *
from snowlm.data_analysis.economic_impact import *
from snowlm.data_analysis.climate_econ_pop import *
from snowlm.scrape_api.census_api_query import *

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB, dbc_css])
# load_figure_template("spacelab")

########## Screen 1 Figures
climate_df = get_cleaned_data ("disaster_declarations.csv", only_2000_onwards = False)
climate_summary = number_of_disaster_events_by_state (climate_df)
change_in_frequency(climate_summary)
number_of_disasters_stat = number_of_disasters_over_last_decade(climate_summary)


df_climate_summary = climate_summary.groupby(["year", "disaster_type"])["total_number_of_events"].sum().reset_index()
fig1 = px.bar(data_frame=df_climate_summary, x='total_number_of_events', y='year', color = "disaster_type")
fig1.update_yaxes(categoryorder='category descending')

########### Screen 2: Maps

df = get_climate_econ_data(only_2000_onwards = True)
df1 = df.groupby(["year", "state", "state_name"])["total_number_of_events"].sum().reset_index()
df2 = df.groupby(["year", "state", "state_name"])["fed_amount"].sum().reset_index()
disaster_types = list(df.disaster_type.unique())

@app.callback(
    Output('choropleth-map', 'figure'), 
    Input('dropdown', 'value'),
)

def update_choropleth_map(selected_map):


    if selected_map == 'map1':
        fig2 = px.choropleth(df1, locations='state', color='total_number_of_events', 
                            scope='usa', locationmode='USA-states', 
                            animation_frame = 'year',
                            color_continuous_scale=px.colors.sequential.OrRd,
                            height = 650)
    else:
        fig2 = px.choropleth(df2, locations='state', color='fed_amount', 
                            scope='usa', locationmode='USA-states', 
                            animation_frame = 'year',
                            color_continuous_scale=px.colors.sequential.OrRd,
                            height = 650)

    return fig2


###########Screen 2: Bubble Maps

df_pop = get_climate_econ_pop_data()

data = df_pop.groupby(["state", 'year', 'state_pop']).agg({"total_number_of_events": "sum", "fed_amount":"sum"}).reset_index()
data = data.sort_values('year', ascending=True)

fig3 = px.scatter(data, x="total_number_of_events", y="fed_amount", size="state_pop", 
                animation_frame="year", color = "state", hover_name = "state")


########### Screen 3: Census


####### Tables

# Top 5 Disasters Table
disaster_events = type_of_disasters_by_state(climate_summary)
top_disasters = disaster_events.sort_values(by='total_number_of_events', ascending=False).head(5)
table = dash_table.DataTable(
                id='table',
                columns=[{'name': col, 'id': col} for col in top_disasters.columns],
                data=top_disasters.to_dict('records'),)

# Top 5 Federal Assistance Table



@app.callback(
    Output('bar-chart', 'figure'),
    Output('table', 'data'),
    Input('choropleth-map', 'clickData')
)

def generate_graphs(clickData):
    if clickData is not None:
        state = clickData['points'][0]['location']
       
        # Create a bar graph 
        df_climate = get_cleaned_data ("disaster_declarations.csv", only_2000_onwards = True)

        num_days_in_disaster = {"states": number_of_days_in_dec_disaster(df_climate).keys(),
        "values": number_of_days_in_dec_disaster(df_climate).values()}
        disaster_days = pd.DataFrame.from_dict(num_days_in_disaster)

        fig4 = px.bar(disaster_days, x = "states", y = "values")
        highlight_values = [f"{state}", 'National Average']
        highlight_color = 'red'
        fig4.update_traces(marker=dict(color=[highlight_color if x in highlight_values else 'blue' for x in disaster_days["states"]]))

        #Create data table for top five disaster events for each state
        top5_disasters = disaster_events[disaster_events['state'] == state]
        top_5 = top5_disasters.sort_values(by='total_number_of_events', ascending=False).head(5)

        top_5_table = top_5.to_dict('records')

        #Create data table for top five states receiving federal funding


        # Create visuals for county level information from each state
        census_data = clean_census_data_to_csv(data)
        df_census = pd.read_csv("census_demographic_data.csv")

        # click_data = df_census[df_census['name_state'] == state]
    

        # fig5 = px.bar(data_frame=click_data, x= ['name_county', 'name_state', 'name_country'], 
        #                 y=['percent_unemployed', 'percent_unemployed_state', 'percent_unemployed_country'])

        return fig4, top_5_table

    else:
        return {}

# fig_list = [fig4]

########## Layout

# Header
header = html.H4("Analysis of Weather-related Disasters in the United States",
             className="bg-primary text-white p-3 mb-2 text-center")

# Jumbotron
jumbotron = dbc.Col(html.Div(
        [html.H4("42.63%", className="display-6"),
         html.Hr(className="my-2"),
         html.P(
              "Disasters are increasing, over 42.63% of them took place since "
              "2010 (when looking at a dataset from 1980-2010) "),],
           className = "h-100 p-5 text-white bg-dark rounded-3",), 
         md=12,)

# Card

first_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("42.63%", className="card-title"),
            html.P("Disasters are increasing, over 42.63% of them took place since "
                    "2010 (when looking at a dataset from 1980-2022)"),
            # dbc.Button("Go somewhere", color="primary"),
        ]
    )
)


#Dropdown
dropdown_options = [
    {'label': 'Total Number of Disaster Events', 'value': 'map1'},
    {'label': 'Total FEMA Public Assistance Funding', 'value': 'map2'}
]
dropdown = html.Div(
        [dbc.Label("Select a variable"),
         dcc.Dropdown(
           id = "dropdown",
           options=dropdown_options,
           value="map1",),],
         className="mb-4",)

# Checklist
checklist = html.Div(
        [dbc.Label("Select a disaster type"),
         dbc.Checklist(
           id = "checklist",
           options=[{"label": i, "value": i} for i in disaster_types],
           value = [],
           inline = True,),],
         className="mb-4",)

selec_input = dbc.Card([dropdown, checklist], body=True)

app.layout = dbc.Container(
       [
           header,
           dbc.Row([
                dbc.Col([
                    dcc.Graph(id='stacked-bar-chart', figure=fig1)
                ], width={'size': 6, 'offset': 0, 'order': 2}),
                dbc.Col(first_card, width={'size': 4, 'offset': 0, 'order': 1}),
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='choropleth-map')
                ], width={'size': 9, 'offset': 0, 'order': 1}),
                dbc.Col([selec_input], width=3)
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='scatter-bubble', figure=fig3)
                ], width={'size': 6, 'offset': 0, 'order': 2}),
                dbc.Col([
                    dcc.Graph(id='bar-chart')
                ], width={'size': 6, 'offset': 0, 'order': 2}),
            ]),
            dbc.Row([
                dbc.Col(table, md=6),
            ])
        ],
        fluid = True,
        className = "dbc",)


if __name__ == '__main__':
    app.run_server(debug=False, port=8055)




#     dbc.Row([
#         dbc.Col([
#             dcc.Graph(id='chart-1', figure=fig1
#         ], width={'size': 6, 'offset': 0, 'order': 2}),
#         dbc.Col((html.Div(
#         [html.H4("42.63%", className="display-6"),
#          html.Hr(className="my-2"),
#          html.P(
#               "Disasters are increasing, over 42.63% of them took place since "
#               "2010 (when looking at a dataset from 1980-2010) "),],
#            className = "h-100 p-5 text-white bg-dark rounded-3",), 
#          md=12,), width={'size': 6, 'offset': 0, 'order': 1})
#     ]),
#     dbc.Row([
#         dbc.Col([
#             dcc.Graph(id='chart-3', figure=fig2
#         ], width={'size': 6, 'offset': 0, 'order': 1}),
#     ])
# ])


# app.layout = dbc.Container(
#        [
#            header,
#            dbc.Row([
#                 dbc.Col([
#                     dcc.Graph(id='chart-1', figure=fig1
#                 ], width={'size': 6, 'offset': 0, 'order': 2}),
#                 dbc.Col((html.Div(
#                 [html.H4("42.63%", className="display-6"),
#                 html.Hr(className="my-2"),
#                 html.P(
#                     "Disasters are increasing, over 42.63% of them took place since "
#                     "2010 (when looking at a dataset from 1980-2010) "),],
#                 className = "h-100 p-5 text-white bg-dark rounded-3",), 
#                 md=12,), width={'size': 6, 'offset': 0, 'order': 1})
#             ]),
#              dbc.Row([
#                 dbc.Col([
#                     dcc.Graph(id='chart-2', figure=fig2
#                 ], width={'size': 6, 'offset': 0, 'order': 1}),
#                 dbc.Col([selec_input], width =4),
#             ])
#         ],
#         fluid = True,
#         className = "dbc",)

# app.layout = dbc.Container(
#        [
#            header,
#            dbc.Row(
#                [dbc.Col([selec_input], width =4),
#                 dbc.Col([charts],      width =8),],),
#         ],
#         fluid = True,
#         className = "dbc",)



# Slider

# years  = df.year.unique()
# years  = np.sort(years)

# slider = html.Div(
#         [dbc.Label("Select a year"),
#          dcc.RangeSlider(
#            id  = "years",
#            min = years[0],
#            max = years[-1],
#            tooltip={"placement": "bottom", "always_visible": True},
#            value=[years[0], years[-1]],),],
#          className="mb-4",)


# dbc.Col(html.Div(
#                     [html.H4("42.63%", className="display-6"),
#                     html.Hr(className="my-2"),
#                     html.P(
#                         "Disasters are increasing, over 42.63% of them took place since "
#                         "2010 (when looking at a dataset from 1980-2010) "),],
#                     className = "h-100 p-3 text-white bg-dark rounded-3",), width={'size': 6, 'offset': 0, 'order': 1}),