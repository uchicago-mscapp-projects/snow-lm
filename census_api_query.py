'''
CAPP 30122
Team: Snow Laughing Matter
Primary Author: Jennifer Yeaton
Code for querying the U.S. Census' API

https://www.census.gov/data/developers/data-sets/acs-5year.html
'''

import re
import pathlib
import pandas as pd
import requests

#Assemble components of this query by following these steps:
#1. Start query with the host name:
host_name = "https://api.census.gov/data"
query_url = host_name

#2. Add the data year to the query:
#https://api.census.gov/data/2021
data_year = "/2021"
query_url += data_year

#3. Add the dataset name acronym:
#https://api.census.gov/data/2019/acs/acs5
dataset_name_acronym = "/acs/acs5/profile"
query_url += dataset_name_acronym

#4. Add ?get= to the query:
#https://api.census.gov/data/2021/acs/acs5/profile?get=
get = "?get="
query_url += get

#5. Add variables:
list_of_vars = "NAME,DP02_0001E,DP02PR_0001E,DP03_0009PE,DP03_0062E,DP03_0096PE,DP03_0099PE,DP02_0067PE,DP05_0037PE,DP05_0038PE,DP05_0039PE,DP05_0044PE,DP05_0052PE,DP05_0057PE,DP05_0058PE"
query_url += list_of_vars

'''
See below for descriptions of each variable:
#NAME = name of location
#DP02_0001E = total households
#DP02PR_0001E = total households in puerto rico
#DP03_0009PE = Percent Estimate!!EMPLOYMENT STATUS!!Civilian labor force!!Unemployment Rate

#DP03_0062E = Estimate!!INCOME AND BENEFITS (IN 2018 INFLATION-ADJUSTED DOLLARS)!!Total households!!Median household income (dollars)
#DP03_0096PE = Percent Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!With health insurance coverage
#DP03_0099PE = Percent Estimate!!HEALTH INSURANCE COVERAGE!!Civilian noninstitutionalized population!!No health insurance coverage
#DP02_0067PE = Percent Estimate!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!Bachelor's degree or higher

#DP05_0037PE = Percent Estimate!!RACE!!Total population!!One race!!White
#DP05_0038PE = Percent Estimate!!RACE!!Total population!!One race!!Black or African American
#DP05_0039PE = Percent Estimate!!RACE!!Total population!!One race!!American Indian and Alaska Native
#DP05_0044PE = Percent Estimate!!RACE!!Total population!!One race!!Asian
#DP05_0052PE = Percent Estimate!!RACE!!Total population!!One race!!Native Hawaiian and Other Pacific Islander	
#DP05_0057PE = Percent Estimate!!RACE!!Total population!!One race!!Some other race
#DP05_0058PE = 	Percent Estimate!!RACE!!Total population!!Two or more races
'''

#6. Add geographies:
geo = "&for=county:*"
query_url += geo

#7. Add census API key for this project:
census_api_key = "&key=dbaf6b8c0aa053d4df5ae844bba98940952fc50b"
query_url += census_api_key

#Request data using the full query url:
response = requests.get(query_url)
census_json = response.json()

#print(census_json)

#Save census data to a pandas dataframe:
#helpful youtube video:
#https://www.youtube.com/watch?v=l47HptzM7ao

column_names = ["name", "total_households", "total_households_pr", "percent_unemployed", "median_household_income",
    "with_healthcare_coverage", "without_healthcare_coverage", "bach_or_higher", "percent_white", "percent_blackORaa", 
    "percent_ai_and_an", "percent_asian", "percent_nh_and_pi", "percent_race_other", "percent_race_two_more", "state", "county"]
census_df = pd.DataFrame(columns = column_names, data = census_json[1:])
#print(census_df)

#Checking variable types and making any revisions necessary:
census_df["total_households"] = census_df["total_households"].astype(float)
census_df["total_households_pr"] = census_df["total_households_pr"].astype(float)
census_df["percent_unemployed"] = census_df["percent_unemployed"].astype(float)
census_df["median_household_income"] = census_df["median_household_income"].astype(float)
census_df["with_healthcare_coverage"] = census_df["with_healthcare_coverage"].astype(float)
census_df["without_healthcare_coverage"] = census_df["without_healthcare_coverage"].astype(float)
census_df["bach_or_higher"] = census_df["bach_or_higher"].astype(float)
census_df["percent_white"] = census_df["percent_white"].astype(float)
census_df["percent_blackORaa"] = census_df["percent_blackORaa"].astype(float)
census_df["percent_ai_and_an"] = census_df["percent_ai_and_an"].astype(float)
census_df["percent_asian"] = census_df["percent_asian"].astype(float)
census_df["percent_nh_and_pi"] = census_df["percent_nh_and_pi"].astype(float)
census_df["percent_race_other"] = census_df["percent_race_other"].astype(float)
census_df["percent_race_two_more"] = census_df["percent_race_two_more"].astype(float)


#Add a variable that is a concatenation of the state code and the county code
census_df["state_and_county_code"] = census_df["state"] + census_df["county"]

print(census_df)
result = census_df.dtypes
print(result) #--> note: every variable was initially an "object" data type

#Save df to CSV:
census_df.to_csv("census_demographic_data.csv", index = False)