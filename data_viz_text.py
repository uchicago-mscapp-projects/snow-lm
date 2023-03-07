"""
CAPP 30122
Team: Snow Laughing Matter
Author: Shwetha Srinivasan

Code for developing the text for our final visualization output. 
"""
from dash import html

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

# Section Heading

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