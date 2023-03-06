import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Importing cleaned datasets from other files
from snowlm.data_analysis.climate import *
from snowlm.data_analysis.economic_impact import *
from snowlm.data_analysis.climate_econ_pop import *
from snowlm.scrape_api.census_api_query import *
from snowlm.scrape_api.voting_record import *


def climate_viz():
    dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB, dbc_css])

    app.css.append_css({
    'external_url': 'https://fonts.googleapis.com/css?family=Roboto',
    'font-size': '16px',
    'color': '#333333',
    'font-family': 'Roboto, sans-serif'
    })

    ########### Screen 1 Figures ################
    climate_df = get_cleaned_data("snowlm/data/disaster_declarations.csv", only_2000_onwards = False)
    climate_summary = number_of_disaster_events_by_state(climate_df)
    change_in_frequency(climate_summary)
    number_of_disasters_stat = number_of_disasters_over_last_decade(climate_summary)


    df_climate_summary = climate_summary.groupby(["year", "disaster_type"])["total_number_of_events"].sum().reset_index()
    fig1 = px.bar(data_frame=df_climate_summary, x='total_number_of_events', y='year', color = "disaster_type")
    fig1.update_yaxes(title_text = 'Year', categoryorder='category descending')
    fig1.update_xaxes(title_text='Total Number of Disaster Events')
    # fig1.update_traces(name='Disaster Types')

    ########### Screen 2: Maps ###################

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
            fig2.update_traces(name='Total Number of Disaster Events')
        else:
            fig2 = px.choropleth(df2, locations='state', color='fed_amount', 
                                scope='usa', locationmode='USA-states', 
                                animation_frame = 'year',
                                color_continuous_scale=px.colors.sequential.matter,
                                height = 650)
            fig2.update_traces(name='Total FEMA Public Assistance Funding (in millions)')

        return fig2


    ########## Screen 2: Bubble Graph ##########

    df_pop = get_climate_econ_pop_data()

    data = df_pop.groupby(["state", 'year', 'state_pop']).agg({"total_number_of_events": "sum", "fed_amount":"sum"}).reset_index()
    data = data.sort_values('year', ascending=True)

    fig3 = px.scatter(data, x="total_number_of_events", y="fed_amount", size="state_pop", 
                    animation_frame="year", color = "state", hover_name = "state")


    ########### Screen 3: State and Census Level Information ###########


    ########### Tables for Top 5 disaster types per state #############

    # Top 5 Disasters Table
    disaster_events = type_of_disasters_by_state(climate_summary)
    top_disasters = disaster_events.sort_values(by='total_number_of_events', ascending=False).head(5)
    table = dash_table.DataTable(
                    id='table',
                    columns=[{'name': col, 'id': col} for col in top_disasters.columns],
                    data=top_disasters.to_dict('records'),)

    # Top 5 Federal Assistance Table
    df_econ_impact = clean_disaster_summaries("snowlm/data/PublicAssistanceFundedProjectsSummaries.csv", "snowlm/data/disaster_declarations.csv" )
    top_funding = top_5_by_public_assistance(df_econ_impact)
    top_5_funding = top_funding.sort_values(by='fed_amount', ascending=False).head(5)

    funding_table = dash_table.DataTable(
                            id='funding-table',
                            columns=[{'name': col, 'id': col} for col in top_5_funding.columns],
                            data=top_5_funding.to_dict('records'),)

    # Function for calculating top 10 worst counties for an indicator

    def get_top_10_counties(df, state, col_name, col_name_state, col_name_us, bool_val):
        top_10 = df.sort_values(by=col_name, ascending=bool_val).head(10)
        top10_df = top_10[['name_county', col_name]]
        state_data = {'name_county': f'{state}', col_name : top_10[col_name_state].iloc[0]}
        national_data = {'name_county': 'United States', col_name : top_10[col_name_us].iloc[0]}
        final_df = top10_df.append([state_data, national_data], ignore_index=True)

        return final_df

    ######## Voting Card #############
    def voting_card(state):
        voting_data = scrape_voting_behavior()
        voting_data['state'] = voting_data.index

        df_voting = voting_data[voting_data['state'] == state]
        yes_vote = df_voting['overal_yea'].iloc[0]
        no_vote = df_voting['overall_nay'].iloc[0]

        return yes_vote, no_vote

    #     vote_yes = dbc.Card(
    #     [
    #         dbc.CardImg(src="https://cdn-icons-png.flaticon.com/512/7444/7444409.png", top=True),
    #         dbc.CardBody(
    #             [
    #                 html.H4("Vote Yes", className="card-title"),
    #                 html.P(str(yes_vote),
    #                     className="card-text",
    #                 ),
    #             ]
    #         ),
    #     ],
    #     id='vote-yes',
    #     style={"width": "18rem"},
    #     )

    #     vote_no = dbc.Card(
    #         [
    #             dbc.CardImg(src="https://cdn-icons-png.flaticon.com/512/7444/7444427.png", top=True),
    #             dbc.CardBody(
    #                 [
    #                     html.H4("Vote No", className="card-title"),
    #                     html.P(str(voting_behavior()[1]),
    #                         className="card-text",
    #                     ),
    #                 ]
    #             ),
    #         ],
    #         id='vote-no',
    #         style={"width": "18rem"},
    #         )
        
    #     return vote_yes, vote_no

    ############### Callbacks ####################
    @app.callback(
        [Output('bar-chart', 'figure'), Output('table', 'data'), 
        Output('funding-table', 'data'), Output('unemployed-bar', 'figure'),
        Output('insurance-bar', 'figure'), Output('income-bar', 'figure'),
        Output('education-bar', 'figure'), Output('voting', 'figure')],
        [Input('choropleth-map', 'clickData')]
    )

    def generate_graphs(clickData):
        if clickData is not None:
            state = clickData['points'][0]['location']
        
            # Create a bar graph 
            df_climate = get_cleaned_data ("snowlm/data/disaster_declarations.csv", only_2000_onwards = True)

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
            top5_funding = top_funding[top_funding['state'] == state]
            top_5_assistance = top5_funding.sort_values(by='fed_amount', ascending=False).head(5)

            top_5_assistance_table = top_5_assistance.to_dict('records')

            # Create visuals for county level information from each state
            df_census = api_query()
            click_data = df_census[df_census['state_code_alpha'] == state]
            state_name = click_data['name_state'].iloc[0]

            top10_unemployed = get_top_10_counties(click_data, state_name, 'percent_unemployed', 'percent_unemployed_state', 'percent_unemployed_us', False)
            fig5 = px.bar(data_frame=top10_unemployed, x = 'name_county', y = 'percent_unemployed',
                            color_discrete_sequence = ['#FF6B35'])
            fig5.update_layout(title= f"Comparison of Unemployment Rate in Counties to {state_name} and National Average")
    


            top10_income = get_top_10_counties(click_data, state_name, 'median_household_income', 'median_household_income_state', 'median_household_income_us', True)
            fig6 = px.bar(data_frame=top10_income, x = 'name_county', y = 'median_household_income',
                            color_discrete_sequence = ['#5603AD'])
            fig6.update_layout(title= f"Comparison of Median Household Income in Counties to {state_name} and National Average")

            top10_noinsurance = get_top_10_counties(click_data, state_name, 'without_healthcare_coverage', 'without_healthcare_coverage_state', 'without_healthcare_coverage_us', False)
            fig7 = px.bar(data_frame=top10_noinsurance, x = 'name_county', y = 'without_healthcare_coverage',
                            color_discrete_sequence = ['#006D77'])
            fig7.update_layout(title = "Comparison of Percent of Population Without Health Insurance Coverage")

            top10_education = get_top_10_counties(click_data, state_name, 'bach_or_higher', 'bach_or_higher_state', 'bach_or_higher_us', True)
            fig8 = px.bar(data_frame=top10_education, x = 'name_county', y = 'bach_or_higher', 
                            color_discrete_sequence = ['#4CC9F0'])
            fig8.update_layout(title = f"Comparison of Education Levels in Counties to {state_name} and National Average")

            # # Political Voting
            
            fig9 = px.bar(x=['Yes', 'No'], y = [voting_card(state)[0], voting_card(state)[1]],
                    color_discrete_map={'Yes':'blue',  'No': 'red'},
                    title= f"Voting Record for IRA Climate Bill in {state_name}")

            return fig4, top_5_table, top_5_assistance_table, fig5, fig6, fig7, fig8, fig9 #vote_yes, vote_no
        else:
            return {}


    #################### Layout ######################

    # Text
    header = html.H4("Analysis of Weather-related Disasters in the United States",
                className="bg-primary text-white p-3 mb-2 text-center")

    # intro_text = 

    # maps_text = 

    # bubble_map_text = 
    
    census_text = html.Div(
        [
        html.P(" At the county level, we can see in greater detail some information"
            "about the populations being affected by climate disasters and their" 
            "socioeconomic circumstances. We’ve highlighted some circumstances"
            " (such as lack of health insurance and unemployment) that would make"
            " dealing with weather-related disasters especially challenging for "
            " these populations. In the bar charts below, clockwise, we show the"
            " racial breakdown of each state compared to the United States as a whole,"
            " the ten counties with the highest rates of unemployment, the ten counties"
            " with the lowest household income levels, and the ten counties with the"
            " greatest percent of the population without health insurance."),
        ],
    className="my-4",
    )


    # https://cdn.5280.com/2022/10/00-Denver-Voting-Guide.jpg
    # https://cdn-icons-png.flaticon.com/512/7444/7444409.png
    # https://cdn-icons-png.flaticon.com/512/7444/7444427.png

    # first_card = dbc.Card(
    #     dbc.CardBody(
    #         [
    #             html.H5("42.63%", className="card-title"),
    #             html.P("Disasters are increasing, over 42.63% of them took place since "
    #                     "2010 (when looking at a dataset from 1980-2022)"),
    #             # dbc.Button("Go somewhere", color="primary"),
    #         ]
    #     )
    # )



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
                    dcc.Graph(id='stacked-bar-chart', figure=fig1, style={"height":"500px"}),
                ], width={'size': 12, 'offset': 0, 'order': 1}),
                # dbc.Col(first_card, width={'size': 4, 'offset': 0, 'order': 1}),
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='choropleth-map')
                ], width={'size': 9, 'offset': 0, 'order': 1}),
                dbc.Col([selec_input], width=3)
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='scatter-bubble', figure=fig3, style={"height":"500px"})
                ], width={'size': 12, 'offset': 0, 'order': 1}),
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='bar-chart')
                ], width={'size': 6, 'offset': 0, 'order': 1}),
                dbc.Col([
                    dcc.Graph(id='voting')
                ], width={'size': 6, 'offset': 0, 'order': 2}),
                # dbc.Col(vote_yes, width={'size': 3, 'offset': 0, 'order': 2}),
                # dbc.Col(vote_no, width={'size': 3, 'offset': 0, 'order': 3})
            ]),
            dbc.Row([
                dbc.Col(table, md=6),
                dbc.Col(funding_table, md=6),
            ]),
            census_text,
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='unemployed-bar')
                ], width={'size': 6, 'offset': 0, 'order': 1}),
                dbc.Col([
                    dcc.Graph(id='insurance-bar')
                ], width={'size': 6, 'offset': 0, 'order': 2}),
            ]), 
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='income-bar')
                ], width={'size': 6, 'offset': 0, 'order': 1}),
                dbc.Col([
                    dcc.Graph(id='education-bar')
                ], width={'size': 6, 'offset': 0, 'order': 2}),
            ])
        ],
        fluid = True,
        className = "dbc",)

    app.run_server(host = "127.0.0.1", port =8055, debug=False)
# if __name__ == '__main__':
#     app.run_server(debug=False, port=8055)




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

# Jumbotron
# jumbotron = dbc.Col(html.Div(
#         [html.H4("42.63%", className="display-6"),
#          html.Hr(className="my-2"),
#          html.P(
#               "Disasters are increasing, over 42.63% of them took place since "
#               "2010 (when looking at a dataset from 1980-2010) "),],
#            className = "h-100 p-5 text-white bg-dark rounded-3",), 
#          md=12,)