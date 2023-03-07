'''
CAPP 30122
Team: Snow Laughing Matter
Author: Jennifer Yeaton

Code for querying the U.S. Census' API, cleaning U.S. Census data, and 
    combining three queries into one usable dataset.

https://www.census.gov/data/developers/data-sets/acs-5year.html
'''

import pathlib
import pandas as pd
import requests
import os

def api_query():
    '''
    Assemble API query for U.S. Census data, request data, clean data, then 
    return a dataframe of cleaned and combined data.

    Inputs:
        None.
    
    Returns
        full_census_df (pandas dataframe): Cleaned and merged US census data at 
            the county, state, and country-level for use for visualizations.
    '''
    #Assemble components of this query by following these steps:
    #1. Start query with the host name:
    host_name = "https://api.census.gov/data"

    #2. Add the data year to the query:
    #https://api.census.gov/data/2021
    data_year = "/2021"

    #3. Add the dataset name acronym:
    #https://api.census.gov/data/2021/acs/acs5
    dataset_name_acronym = "/acs/acs5/profile"

    #4. Add ?get= to the query:
    #https://api.census.gov/data/2021/acs/acs5/profile?get=
    get = "?get="

    #5. Add variables:
    list_of_vars_county = "NAME,DP02_0001E,DP03_0009PE,DP03_0062E,DP03_0099PE,DP02_0068PE,DP05_0037PE,DP05_0038PE,DP05_0039PE,DP05_0044PE,DP05_0052PE,DP05_0057PE,DP05_0058PE"
    list_of_vars_state = "NAME,DP02_0001E,DP03_0009PE,DP03_0062E,DP03_0099PE,DP02_0068PE"
    list_of_vars_us = "NAME,DP02_0001E,DP03_0009PE,DP03_0062E,DP03_0099PE,DP02_0068PE"

    '''
    See below for descriptions of each variable:
    #NAME = name of location

    #DP02_0001E = total households

    #DP03_0009PE = Percent Estimate!!EMPLOYMENT STATUS!!Civilian labor force!!Unemployment Rate
    #DP03_0062E = Estimate!!INCOME AND BENEFITS (IN 2021 INFLATION-ADJUSTED DOLLARS)!!Total households!!Median household income (dollars)
    #DP03_0099PE = Percent Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!No health insurance coverage

    #DP02_0068PE = Percent Estimate!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Bachelor's degree or higher

    #DP05_0037PE = Percent Estimate!!RACE!!Total population!!One race!!White
    #DP05_0038PE = Percent Estimate!!RACE!!Total population!!One race!!Black or African American
    #DP05_0039PE = Percent Estimate!!RACE!!Total population!!One race!!American Indian and Alaska Native
    #DP05_0044PE = Percent Estimate!!RACE!!Total population!!One race!!Asian
    #DP05_0052PE = Percent Estimate!!RACE!!Total population!!One race!!Native Hawaiian and Other Pacific Islander	
    #DP05_0057PE = Percent Estimate!!RACE!!Total population!!One race!!Some other race
    #DP05_0058PE = 	Percent Estimate!!RACE!!Total population!!Two or more races

    https://api.census.gov/data/2021/acs/acs5/profile/variables.html
    '''

    #6. Add geography for county, state, and country:
    geo_county = "&for=county:*"
    geo_state = "&for=state:*"
    geo_us = "&for=us:*"

    #7. Add census API key for this project:
    census_api_key = "&key=" + os.environ["CENSUS_API_KEY"]

    #8. Create f strings
    query_url_county = f"{host_name}{data_year}{dataset_name_acronym}{get}{list_of_vars_county}{geo_county}{census_api_key}"
    query_url_state = f"{host_name}{data_year}{dataset_name_acronym}{get}{list_of_vars_state}{geo_state}{census_api_key}"
    query_url_us = f"{host_name}{data_year}{dataset_name_acronym}{get}{list_of_vars_us}{geo_us}{census_api_key}"
    
    #REMOVE THESE CHECKS
    print("query_url_state: ", query_url_state)
    print("query_url_county: ", query_url_county)
    print("query_url_us: ", query_url_us)

    #9. Request data using the full query url:
    response_county = requests.get(query_url_county)
    response_state = requests.get(query_url_state)
    response_us = requests.get(query_url_us)
    census_json_county = response_county.json()
    census_json_state = response_state.json()
    census_json_us = response_us.json()

    #Create cleaned and merged pandas dataframe from the three above json files:
    full_census_df = sep_jsons_to_merged_cleaned_dataframes(census_json_county, 
        census_json_state, census_json_us)

    #Return census dataframe
    return full_census_df


def sep_jsons_to_merged_cleaned_dataframes(census_json_county, census_json_state, census_json_us):
    '''
    Create a cleaned and merged pandas dataframe from the json files returned by 
        quering to the U.S. Census' API.

    Inputs:
        census_json_county (JSON): JSON file returned by API query for county-level
            U.S. Census data.
        census_json_state (JSON): JSON file returned by API query for state-level
            U.S. Census data.
        census_json_us (JSON): JSON file returned by API query for U.S.-level
            U.S. Census data.

    Returns:
        full_census_df (pandas dataframe): Full merged and cleaned dataframe with
            the U.S. Census data we queried. 
    '''

    #Create lists for each dataset's variable names:
    column_names_county = ["name_county", "total_households", "percent_unemployed", "median_household_income",
        "without_healthcare_coverage", "bach_or_higher", "percent_white", "percent_blackORaa", 
        "percent_ai_and_an", "percent_asian", "percent_nh_and_pi", "percent_race_other", "percent_race_two_more", "state_code", "county_code"]

    column_names_state = ["name_state", "total_households_state", "percent_unemployed_state", "median_household_income_state",
        "without_healthcare_coverage_state", "bach_or_higher_state", "state_code"]

    column_names_us = ["name_country", "total_households_us", "percent_unemployed_us", "median_household_income_us",
        "without_healthcare_coverage_us", "bach_or_higher_us", "country_code"]

    #Save each file as a dataframe:
    census_df_county = pd.DataFrame(columns = column_names_county, data = census_json_county[1:])
    census_df_state = pd.DataFrame(columns = column_names_state, data = census_json_state[1:])
    census_df_us = pd.DataFrame(columns = column_names_us, data = census_json_us[1:])

    #Checking variable types and making any revisions necessary to census_df_county:
    clean_census_df_county = clean_county_level_census_data(census_df_county)

    #Checking variable types and making any revisions necessary to census_df_state:
    clean_census_df_state = clean_state_level_census_data(census_df_state)

    #Checking variable types and making any revisions necessary to census_df_us:
    clean_census_df_us = clean_us_level_census_data(census_df_us)

    #Citation for loading in data and changing its types: https://www.youtube.com/watch?v=l47HptzM7ao

    #Combine census_df_county, census_df_state, and census_df_us into full_census_df
    census_df_stateANDus = clean_census_df_state.merge(clean_census_df_us, how = "outer", on = "country_code")
    full_census_df = clean_census_df_county.merge(census_df_stateANDus, how = "outer", on = "state_code")

    #return census_df_county, census_df_state, census_df_us
    return full_census_df


def clean_county_level_census_data(census_df_county):
    '''
    Cleans county-level US Census data.

    Input:
        census_df_county (pandas dataframe): Raw data from api pull at county level
    
    Returns:
        census_df_county (pandas dataframe): Clean county-level U.S. Census data.
    '''

    #Revise variable types:
    census_df_county["total_households"] = census_df_county["total_households"].astype(float)
    census_df_county["percent_unemployed"] = census_df_county["percent_unemployed"].astype(float)
    census_df_county["median_household_income"] = census_df_county["median_household_income"].astype(float)
    census_df_county["without_healthcare_coverage"] = census_df_county["without_healthcare_coverage"].astype(float)
    census_df_county["bach_or_higher"] = census_df_county["bach_or_higher"].astype(float)
    census_df_county["percent_white"] = census_df_county["percent_white"].astype(float)
    census_df_county["percent_blackORaa"] = census_df_county["percent_blackORaa"].astype(float)
    census_df_county["percent_ai_and_an"] = census_df_county["percent_ai_and_an"].astype(float)
    census_df_county["percent_asian"] = census_df_county["percent_asian"].astype(float)
    census_df_county["percent_nh_and_pi"] = census_df_county["percent_nh_and_pi"].astype(float)
    census_df_county["percent_race_other"] = census_df_county["percent_race_other"].astype(float)
    census_df_county["percent_race_two_more"] = census_df_county["percent_race_two_more"].astype(float)

    #Add a variable to census_df_county that is a concatenation of the state code and the county code:
    census_df_county["state_and_county_code"] = census_df_county["state_code"] + census_df_county["county_code"]

    #Add a variable to census_df_county that is an alphabetic code for states (e.g., IL, NJ, WI)
    #(The code in the next 4 lines is a revised version of code written by Jackie Glasheen 
    #for another dataset in this project)
    file_path = "snowlm/data/Census_State_codes.txt"
    state_code_alpha_and_numeric = pd.read_csv(file_path, sep='|')
    state_code_alpha_and_numeric = state_code_alpha_and_numeric.drop(columns
        =['STATE_NAME','STATENS'])
    state_code_alpha_and_numeric = state_code_alpha_and_numeric.rename(columns
        ={"STATE": "state_code", "STUSAB": "state_code_alpha"})
    census_df_county["state_code"] = census_df_county["state_code"].astype(int)
    census_df_county_w_statecodes = pd.merge(census_df_county, 
        state_code_alpha_and_numeric, how = "left", on = "state_code")

    return census_df_county_w_statecodes



def clean_state_level_census_data(census_df_state):
    '''
    Cleans state-level U.S. Census data.

    Input:
        census_df_state (pandas dataframe): Raw data from api pull at state level
    
    Returns:
        census_df_state (pandas dataframe): Clean state-level U.S. Census data.
    '''

    #Revise variable types:
    census_df_state["total_households_state"] = census_df_state["total_households_state"].astype(float)
    census_df_state["percent_unemployed_state"] = census_df_state["percent_unemployed_state"].astype(float)
    census_df_state["median_household_income_state"] = census_df_state["median_household_income_state"].astype(float)
    census_df_state["without_healthcare_coverage_state"] = census_df_state["without_healthcare_coverage_state"].astype(float)
    census_df_state["bach_or_higher_state"] = census_df_state["bach_or_higher_state"].astype(float)
    census_df_state["country_code"] = 1
    census_df_state["state_code"] = census_df_state["state_code"].astype(int)

    return census_df_state


def clean_us_level_census_data(census_df_us):
    '''
    Cleans country-level US Census data.

    Input:
        census_df_us (pandas dataframe): Raw data from U.S. Census API pull at 
            the country level.
    
    Returns:
        census_df_us (pandas dataframe): Clean country-level U.S. Census data.
    '''

    #Revise variable types:
    census_df_us["total_households_us"] = census_df_us["total_households_us"].astype(float)
    census_df_us["percent_unemployed_us"] = census_df_us["percent_unemployed_us"].astype(float)
    census_df_us["median_household_income_us"] = census_df_us["median_household_income_us"].astype(float)
    census_df_us["without_healthcare_coverage_us"] = census_df_us["without_healthcare_coverage_us"].astype(float)
    census_df_us["bach_or_higher_us"] = census_df_us["bach_or_higher_us"].astype(float)
    census_df_us["country_code"] = census_df_us["country_code"].astype(int)

    return census_df_us


def clean_census_data_to_csv(full_census_df):
    '''
    Print cleaned and merged U.S. Census dataset to a csv.

    Input:
        full_census_df (pandas dataframe): Cleaned and merged census dataset as
            a pandas dataframe.

    Returns:
        None. Creates a csv file.
    '''

    full_census_df.to_csv("census_demographic_data.csv", index = False)