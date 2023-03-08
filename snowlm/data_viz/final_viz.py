"""
CAPP 30122
Team: Snow Laughing Matter
Author: Shwetha Srinivasan

Code for developing visualizations and final dashboard after data cleaning.

Sources: 
https://medium.com/codex/charting-with-plotly-dash-1bc9e25cbd5b
https://towardsdatascience.com/dash-for-beginners-create-interactive-python-dashboards-338bfcb6ffa4
https://towardsdatascience.com/creating-an-interactive-dashboard-with-dash-plotly-using-crime-data-a217da841df3

The above mentioned sources have been generally useful as a guide to develop the interactive
dashboard and visualizations for this project. 
"""
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Importing cleaned datasets from other files
from snowlm.data_analysis.climate import (
    get_cleaned_data,
    number_of_disaster_events_by_state,
    number_of_days_in_dec_disaster,
    type_of_disasters_by_state,
)
from snowlm.data_analysis.economic_impact import (
    clean_disaster_summaries,
    top_5_by_public_assistance,
)
from snowlm.data_analysis.climate_econ_pop import (
    get_climate_econ_pop_data,
    get_climate_econ_data,
)
from snowlm.scrape_api.census_api_query import api_query
from snowlm.scrape_api.voting_record import scrape_voting_behavior


def climate_viz():
    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    )
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB, dbc_css])

    ########### Screen 1: National Figures ################
    climate_df = get_cleaned_data(
        "snowlm/data/disaster_declarations.csv", only_2000_onwards=False
    )
    climate_summary = number_of_disaster_events_by_state(climate_df)

    df_climate_summary = (
        climate_summary.groupby(["year", "disaster_type"])["total_number_of_events"]
        .sum()
        .reset_index()
    )
    fig1 = px.bar(
        data_frame=df_climate_summary,
        x="total_number_of_events",
        y="year",
        color="disaster_type",
        title="Total Number of Disaster Events from 1980 by State",
    )
    fig1.update_yaxes(title_text="Year", categoryorder="category descending")
    fig1.update_xaxes(title_text="Total Number of Disaster Events")
    fig1.update_layout(legend_title="Disaster Types", title_x=0.5)

    ########### Screen 2: State Maps ###################

    df = get_climate_econ_data(only_2000_onwards=True)
    df1 = (
        df.groupby(["year", "state", "state_name"])["total_number_of_events"]
        .sum()
        .reset_index()
    )
    df2 = df.groupby(["year", "state", "state_name"])["fed_amount"].sum().reset_index()

    # Dropdown Menu for Map

    dropdown_options = [
        {"label": "Total Number of Disaster Events", "value": "map1"},
        {"label": "Total FEMA Public Assistance Funding", "value": "map2"},
    ]
    dropdown = html.Div(
        [
            dbc.Label("Select a variable"),
            dcc.Dropdown(
                id="dropdown",
                options=dropdown_options,
                value="map1",
            ),
        ],
        className="mb-4",
    )

    # Displays and updates map based on the variable selected from the dropdown menu

    @app.callback(
        Output("choropleth-map", "figure"),
        Input("dropdown", "value"),
    )
    def update_choropleth_map(selected_map):
        if selected_map == "map1":
            fig2 = px.choropleth(
                df1,
                locations="state",
                color="total_number_of_events",
                scope="usa",
                locationmode="USA-states",
                animation_frame="year",
                color_continuous_scale=px.colors.sequential.OrRd,
                height=650,
                title="Map with Number of Disasters from 2000-2022",
            )
            fig2.update_layout(
                coloraxis_colorbar_title="Number of Disasters", title_x=0.5
            )
        else:
            fig2 = px.choropleth(
                df2,
                locations="state",
                color="fed_amount",
                scope="usa",
                locationmode="USA-states",
                animation_frame="year",
                color_continuous_scale=px.colors.sequential.matter,
                height=650,
                title="Map with FEMA Public Assistance from 2000-2022",
            )
            fig2.update_layout(coloraxis_colorbar_title="FEMA Funding", title_x=0.5)

        return fig2

    ########## Screen 2: Bubble Graph (Scatterplot) ##########

    df_pop = get_climate_econ_pop_data()

    data = (
        df_pop.groupby(["state", "year", "state_pop"])
        .agg({"total_number_of_events": "sum", "fed_amount": "sum"})
        .reset_index()
    )
    data = data.sort_values("year", ascending=True)

    fig3 = px.scatter(
        data,
        x="total_number_of_events",
        y="fed_amount",
        size="state_pop",
        animation_frame="year",
        color="state",
        hover_name="state",
        title="Relationship between Disasters and Funding Received by Size of State Over Time",
    )
    fig3.update_layout(title_x=0.5)
    fig3.update_xaxes(title_text="Number of Disasters")
    fig3.update_yaxes(title_text="FEMA Funding")

    ########### Screen 3: State and Census Level Information ###########

    # ########### Tables for Top 5 disaster types per state #############

    # Top 5 Disasters Table
    disaster_events = type_of_disasters_by_state(climate_summary)
    top_disasters = disaster_events.sort_values(by='total_number_of_events', ascending=False).head(5)
    table = dash_table.DataTable(
                    id='table',
                    columns=[{'name': col, 'id': col} for col in top_disasters.columns],
                    data=top_disasters.to_dict('records'),)

    # Top 5 Federal Assistance Table
    df_econ_impact = clean_disaster_summaries(
        "snowlm/data/PublicAssistanceFundedProjectsSummaries.csv", 
        "snowlm/data/disaster_declarations.csv")
    top_funding = top_5_by_public_assistance(df_econ_impact)
    top_funding = top_funding.drop(['disasterNumber'], axis=1)
    top_funding['fed_amount'] = top_funding['fed_amount'].astype(int)
    top_5_funding = top_funding.sort_values(by='fed_amount', ascending=False).head(5)

    funding_table = dash_table.DataTable(
                            id='funding-table',
                            columns=[{'name': col, 'id': col} for col in top_5_funding.columns],
                            data=top_5_funding.to_dict('records'),)


    # Function for calculating top 10 worst counties for an indicator

    def get_top_10_counties(df, state, col_name, col_name_state, col_name_us, bool_val):
        """
        Returns the top 10 worst counties for a specific census indicator
        Inputs:
            df (DataFrame): a census dataset
            state (str): state selected when interacting with the map
            col_name (str): column corresponding to county value for
                chosen indicator
            col_name_state (str): column corresponding to state value for chosen indicator
            col_name_us (str): column corresponding to national value for chosen indicator
            bool_val (boolean): True or False depending on whether the column
                should be sorted ascending
        Returns (DataFrame): The top 10 worst counties for chosen indicator
        """
        top_10 = df.sort_values(by=col_name, ascending=bool_val).head(10)
        top10_df = top_10[["name_county", col_name]]
        state_data = {
            "name_county": f"{state}",
            col_name: top_10[col_name_state].iloc[0],
        }
        national_data = {
            "name_county": "United States",
            col_name: top_10[col_name_us].iloc[0],
        }
        final_df = top10_df.append([state_data, national_data], ignore_index=True)

        return final_df

    ######## Voting Card #############
    def voting_card(state):
        """
        Calculates the number for senators that voted yes or no
        for the IRA (Climate Bill) legistation

        Inputs
            state (str): state selected when interacting with the map

        Returns (tuple): Number of yes and no votes for the bill for the state
        """
        voting_data = scrape_voting_behavior()
        voting_data["state"] = voting_data.index

        df_voting = voting_data[voting_data["state"] == state]
        yes_vote = df_voting["overal_yea"].iloc[0]
        no_vote = df_voting["overall_nay"].iloc[0]

        return yes_vote, no_vote

    ############### Callbacks ####################
    # Displays all the visuals created below based on the state selected on the choropleth map

    @app.callback(
        [
            Output("bar-chart", "figure"),
            Output("table", "data"),
            Output("funding-table", "data"),
            Output("unemployed-bar", "figure"),
            Output("insurance-bar", "figure"),
            Output("income-bar", "figure"),
            Output("education-bar", "figure"),
            Output("voting", "figure"),
        ],
        [Input("choropleth-map", "clickData")],
    )
    def generate_graphs(clickData):
        if clickData is not None:
            state = clickData["points"][0]["location"]

            # Create a bar graph
            df_climate = get_cleaned_data(
                "snowlm/data/disaster_declarations.csv", only_2000_onwards=True
            )

            num_days_in_disaster = {
                "states": number_of_days_in_dec_disaster(df_climate).keys(),
                "values": number_of_days_in_dec_disaster(df_climate).values(),
            }
            disaster_days = pd.DataFrame.from_dict(num_days_in_disaster)

            fig4 = px.bar(
                disaster_days,
                x="states",
                y="values",
                title="Average Number of Days Yearly in a Disaster Scenario",
            )
            highlight_values = [f"{state}", "National Average"]
            highlight_color = "red"
            fig4.update_traces(
                marker=dict(
                    color=[
                        highlight_color if x in highlight_values else "blue"
                        for x in disaster_days["states"]
                    ]
                )
            )
            fig4.update_yaxes(title_text="Average Number of Days")
            fig4.update_layout(title_x=0.5)
            
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
            df_census = df_census.loc[df_census["state_and_county_code"] != "48301"]
            click_data = df_census[df_census["state_code_alpha"] == state]
            state_name = click_data["name_state"].iloc[0]

            top10_unemployed = get_top_10_counties(
                click_data,
                state_name,
                "percent_unemployed",
                "percent_unemployed_state",
                "percent_unemployed_us",
                False,
            )
            fig5 = px.bar(
                data_frame=top10_unemployed,
                x="name_county",
                y="percent_unemployed",
                color_discrete_sequence=["#FF6B35"],
            )
            fig5.update_layout(
                title=f"Comparison of Unemployment Rate in Counties to {state_name} and National Average"
            )
            fig5.update_xaxes(title_text="Geographic Region")
            fig5.update_yaxes(title_text="Unemployment Rate")

            top10_income = get_top_10_counties(
                click_data,
                state_name,
                "median_household_income",
                "median_household_income_state",
                "median_household_income_us",
                True,
            )
            fig6 = px.bar(
                data_frame=top10_income,
                x="name_county",
                y="median_household_income",
                color_discrete_sequence=["#5603AD"],
            )
            fig6.update_layout(
                title=f"Comparison of Median Household Income in Counties to {state_name} & National Avg."
            )
            fig6.update_xaxes(title_text="Geographic Region")
            fig6.update_yaxes(title_text="Median Household Income")

            top10_noinsurance = get_top_10_counties(
                click_data,
                state_name,
                "without_healthcare_coverage",
                "without_healthcare_coverage_state",
                "without_healthcare_coverage_us",
                False,
            )
            fig7 = px.bar(
                data_frame=top10_noinsurance,
                x="name_county",
                y="without_healthcare_coverage",
                color_discrete_sequence=["#006D77"],
            )
            fig7.update_layout(
                title="Comparison of Percent of Population Without Health Insurance Coverage"
            )
            fig7.update_xaxes(title_text="Geographic Region")
            fig7.update_yaxes(title_text="% of Population with No Health Insurance")

            top10_education = get_top_10_counties(
                click_data,
                state_name,
                "bach_or_higher",
                "bach_or_higher_state",
                "bach_or_higher_us",
                True,
            )
            fig8 = px.bar(
                data_frame=top10_education,
                x="name_county",
                y="bach_or_higher",
                color_discrete_sequence=["#4CC9F0"],
            )
            fig8.update_layout(
                title=f"Comparison of Education Levels in Counties to {state_name} and National Average"
            )
            fig8.update_xaxes(title_text="Geographic Region")
            fig8.update_yaxes(title_text="Bachelor or Higher Education Completion Rate")

            # # Political Voting
            color_map = {"Yes": "blue", "No": "green"}
            fig9 = px.bar(
                x=["Yes", "No"],
                y=[voting_card(state)[0], voting_card(state)[1]],
                color_discrete_map=color_map,
                title=f"Senators Voting for the Climate Bill in {state_name}",
            )
            fig9.update_xaxes(title_text="Voting Record")
            fig9.update_yaxes(title_text="Number of Votes")
            fig9.update_layout(title_x=0.5)
            return (
                fig4,
                top_5_table,
                top_5_assistance_table,
                fig5,
                fig6,
                fig7,
                fig8,
                fig9,
            )
        return {}

    #################### Layout ######################

    # Text Content for the Page
    header = html.H4(
        "Investigating Patterns of Climate-related Natural Disasters in the United States",
        className="bg-primary text-white p-3 mb-2 text-center",
    )

    subheader = html.H5(
        "Jackie Glasheen, Jen Yeaton, Harsh Vardhan Pachisia, Shwetha Srinivasan",
        className="p-2 mb-2 text-center",
        style={"font-size": "20px"},
    )

    date = html.H5(
        "March 2023", className="p-2 mb-2 text-center", style={"font-size": "12px"}
    )

    intro_text = html.Div(
        [
            html.P(
                [
                    html.Strong("42.63%"),
                    " of natural "
                    "disasters in the United States since 1980"
                    " have taken place over the last 12 years. It is evident that climate "
                    "change and global warming are causing extreme weather disasters to "
                    "occur with more frequency. The increase in natural disaster declarations "
                    "over the past several decades has led to the federal government spending "
                    "more money on disaster relief.  Due to the increase in frequency and cost "
                    "of such disasters, a Congressional Research Service ",
                    html.A("paper", href="https://sgp.fas.org/crs/homesec/R45484.pdf"),
                    " from January "
                    "2022 suggests that Congress may consider limiting federal disaster relief "
                    "spending.",
                ]
            ),
            html.P(
                [
                    "Disasters impact different geographic regions, affecting specific states "
                    "and communities disproportionately. Through this dashboard, we hope to "
                    "shed light on the increase in disaster frequency and cost nationwide. "
                    "We highlight the specific situation in each state, where its political "
                    "stance is on climate, and showcase the top 10 counties that are at most "
                    "risk based on current socio-economic factors and require long-term "
                    "policy actions to tackle disasters."
                ]
            ),
            html.P(
                [
                    "This dashboard was built using Python and Dash, using ",
                    html.A(
                        "climate disaster",
                        href="https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2",
                    ),
                    " and ",
                    html.A(
                        "public assistance",
                        href="https://www.fema.gov/openfema-data-page/public-assistance-funded-project-summaries-v1",
                    ),
                    " data from the Federal Emergency Management Agency, "
                    "scraped data of the voting patterns on the Climate IRA bill, and the "
                    "US Census API for county, state and national-level socio-economic breakdown.",
                ]
            ),
        ],
        className="my-4",
        style={"color": "black", "font-family": "Garamond", "font-size": "20px"},
    )
    bar_text = html.Div(
        [
            html.P(
                [
                    "The number of disaster events is steadily increasing over time. "
                    "2011 stands out as the ",
                    html.A(
                        "“Year of Natural Disasters”",
                        href="https://www.livescience.com/17769-2011-record-natural-disasters-infographic.html#:~:text=The%20United%20States%20was%20hit,climate%20change%20is%20a%20contributor.",
                    ),
                    " breaking the record for costly, weather-related disasters, including "
                    "drought, wildfire, tornados, flooding, a blizzard, and a hurricane, "
                    "all as a result of climate change.",
                ]
            ),
        ],
        className="my-4",
        style={"color": "black", "font-family": "Garamond", "font-size": "20px"},
    )

    maps_text = html.Div(
        [
            html.P(
                [
                    "Choose between the number of disaster events or the public "
                    "assistance provided for disaster management to see how their patterns "
                    "have changed between 2000-2022. While there is certainly "
                    "year to year variation, in general, we see that California, "
                    "Texas, and Florida face the most amount of disasters (not normalized "
                    "by landmass). ",
                    html.Strong(
                        "Click on a state"
                        " to get granular state and county-level information!"
                    ),
                ],
            ),
        ],
        className="my-4",
        style={"color": "black", "font-family": "Garamond", "font-size": "20px"},
    )

    bubble_map_text = html.Div(
        [
            html.P(
                "Press play to see the relationship between the number of disaster "
                "events, and the amount of public assistance provided, relative to the "
                "size of the state’s population. Certain states even with smaller populations "
                "and fewer disasters get a lot more funding as compared to others."
            ),
        ],
        className="my-4",
        style={"color": "black", "font-family": "Garamond", "font-size": "20px"},
    )

    state_text = html.Div(
        [
            html.P(
                [
                    "See how your state compares to others in being in a declared disaster "
                    "scenario. On average, a state is in a situation where a disaster has been "
                    "declared 15 days a year between 2000-2022.  The Federated States of Micronesia "
                    "(FM) stands out as an outlier since it is located in the Pacific Ring "
                    "of Fire and is prone to ",
                    html.A(
                        "disasters.",
                        href="https://www.undrr.org/media/81878/download#:~:text=FSM%20is%20located%20in%20the,claim%20people's%20lives%20and%20livestock.",
                    ),
                ]
            ),
            html.P(
                [
                    "The Inflation Reduction Act of 2022 calls for investment in "
                    "domestic clean energy production and aims to substantially reduce carbon "
                    "emissions. However, we found that senators who voted for the bill were "
                    "not necessarily disproportionately impacted by disasters, but rather "
                    "the vote was along party lines."
                ]
            ),
        ],
        className="my-4",
        style={"color": "black", "font-family": "Garamond", "font-size": "20px"},
    )

    table_text = html.Div(
        [
            html.P(
                [
                    "The table to the left lists the top 5 disasters, and the type "
                    "of disaster, over the time period 2000-2022.",
                ]
            ),
            html.P(
                [
                    "The table to the right lists the top 5 disasters based on public "
                    "assistance funding received from FEMA, and the type "
                    "of disaster, over the time period 2000-2022."
                ]
            ),
        ],
        className="my-4",
        style={"color": "black", "font-family": "Garamond", "font-size": "20px"},
    )

    census_text = html.Div(
        [
            html.P(
                " At the county level, we can see in greater detail some information"
                "about the populations in each state and their"
                " socioeconomic circumstances. We’ve highlighted some circumstances"
                " (such as lack of health insurance and unemployment) that would make"
                " dealing with weather-related disasters especially challenging for "
                " these populations. In the bar charts below, clockwise, we show the"
                " the ten counties with the highest rates of unemployment, the ten counties"
                " with the lowest household income levels, and the ten counties with the"
                " greatest percent of the population without health insurance and the "
                "ten counties with the lowest rates of higher education."
            ),
        ],
        className="my-4",
        style={"color": "black", "font-family": "Garamond", "font-size": "20px"},
    )

    conclusion_text = html.Div(
        [
            html.P(
                "This dashboard highlights the overall increase in climate disasters "
                "by showing their trend, breaking down that trend by geography, disaster "
                "type, and FEMA spending, and further listing the top 5 events by state. "
                "In addition, we presented this data alongside information about how the "
                "senators in a state voted on the recent federal climate legislation and "
                "relevant demographic information for the various states and counties. "
                "To build upon this work, further analytical connections between climate "
                "disasters and other data sources should be considered. For example, are "
                "racial minorities disproportionately affected by climate disasters?  "
                "Moreover, some adjustments to the data may be necessary. For instance, "
                "the FEMA money granted as a result of climate disasters should be "
                "inflation-adjusted. Finally, more investigation is required to understand "
                "the relationship between some of the disaster types used in the FEMA data "
                "and global warming, and whether certain disaster types have been used "
                "consistently over time in the data."
            ),
        ],
        className="my-4",
        style={"color": "black", "font-family": "Garamond", "font-size": "20px"},
    )

    # Section Header Text

    intro1_text = html.Div(
        [
            html.H2([html.Strong("Introduction:")]),
        ],
        className="my-4",
        style={"color": "black", "font-family": "Garamond", "font-size": "15px"},
    )

    section1_text = html.Div(
        [
            html.H2([html.Strong("Section 1: National Trends")]),
        ],
        className="my-4",
        style={"color": "black", "font-family": "Garamond", "font-size": "15px"},
    )

    section2_text = html.Div(
        [
            html.H2([html.Strong("Section 2: State-Level Trends")]),
        ],
        className="my-4",
        style={"color": "black", "font-family": "Garamond", "font-size": "15px"},
    )

    section3_text = html.Div(
        [
            html.H2([html.Strong("Section 3: County-Level Trends")]),
        ],
        className="my-4",
        style={"color": "black", "font-family": "Garamond", "font-size": "15px"},
    )

    ################ Final App Layout ###################

    app.layout = dbc.Container(
        [
            header,
            subheader,
            date,
            intro1_text,
            intro_text,
            section1_text,
            bar_text,
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(
                                id="stacked-bar-chart",
                                figure=fig1,
                                style={"height": "600px"},
                            ),
                        ],
                        width={"size": 12, "offset": 0, "order": 1},
                    ),
                ]
            ),
            section2_text,
            maps_text,
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dropdown,
                            dcc.Graph(id="choropleth-map", style={"height": "600px"}),
                        ],
                        width={"size": 12, "offset": 0, "order": 2},
                    ),
                ]
            ),
            bubble_map_text,
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(
                                id="scatter-bubble",
                                figure=fig3,
                                style={"height": "600px"},
                            )
                        ],
                        width={"size": 12, "offset": 0, "order": 1},
                    ),
                ]
            ),
            state_text,
            dbc.Row(
                [
                    dbc.Col(
                        [dcc.Graph(id="bar-chart")],
                        width={"size": 8, "offset": 0, "order": 1},
                    ),
                    dbc.Col(
                        [dcc.Graph(id="voting")],
                        width={"size": 4, "offset": 0, "order": 2},
                    ),
                ]
            ),
            table_text,
            dbc.Row(
                [
                    dbc.Col([dbc.Label("Top 5 Disaster Events"), table], md=6),
                    dbc.Col(
                        [
                            dbc.Label(
                                "Top 5 Disaster Events by FEMA Public Assistance"
                            ),
                            funding_table,
                        ],
                        md=6,
                    ),
                ]
            ),
            section3_text,
            census_text,
            dbc.Row(
                [
                    dbc.Col(
                        [dcc.Graph(id="unemployed-bar")],
                        width={"size": 6, "offset": 0, "order": 1},
                    ),
                    dbc.Col(
                        [dcc.Graph(id="insurance-bar")],
                        width={"size": 6, "offset": 0, "order": 2},
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [dcc.Graph(id="income-bar")],
                        width={"size": 6, "offset": 0, "order": 1},
                    ),
                    dbc.Col(
                        [dcc.Graph(id="education-bar")],
                        width={"size": 6, "offset": 0, "order": 2},
                    ),
                ]
            ),
            conclusion_text,
        ],
        fluid=True,
        className="dbc",
    )

    app.run_server(host="127.0.0.1", port=8055, debug=False)
