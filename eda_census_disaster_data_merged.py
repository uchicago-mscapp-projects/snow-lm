'''
CAPP 30122
Team: Snow Laughing Matter
Primary Author: Jennifer Yeaton

Purpose: Exploratory data analysis of county list with disaster data and census data.
    Merging list of counties with disaster data into census dataset.
'''

import pandas as pd
import pprint
from .census_api_query import api_query
from .climate_datasets import get_cleaned_data, counties_affected_by_disasters


def merge_data_census_disaster():
    '''
    Exploratory data analysis of county list with disaster data and census data.
    Merging list of counties with disaster data into census dataset.

    Inputs: none

    Returns: 
        Pandas dataframe with census and disaster data merged together.
    '''

    full_census_df = api_query()
    cleaned_data_df = get_cleaned_data("disaster_declarations.csv")

    counties_with_disaster_list = counties_affected_by_disasters(get_cleaned_data("disaster_declarations.csv", only_2000_onwards = True))
    column_name = ["state_and_county_code"]
    counties_with_disaster_df = pd.DataFrame(columns = column_name, data = counties_with_disaster_list)

    #Check data types for county_code. Do they match?
    print(full_census_df.dtypes)
    print(counties_with_disaster_df.dtypes)

    #Look at head of each dataset
    print(full_census_df.head)
    print(counties_with_disaster_df.head)

    #Add binary variable for whether disaster data exists
    counties_with_disaster_df["county_has_disaster_data"] = 1

    #return counties_with_disaster_df, full_census_df

    census_data_w_disaster_counties_df = full_census_df.merge(counties_with_disaster_df, how = "left", on = "state_and_county_code")

    return census_data_w_disaster_counties_df