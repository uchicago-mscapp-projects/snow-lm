#capp 122
#snow laughing matter
#census api query

import re
import pathlib
import pandas as pd
import requests
#anything else we need to import?

census_api_key = dbaf6b8c0aa053d4df5ae844bba98940952fc50b #will need to put &key= this key at end of url

#https://api.census.gov/data/2018/acs/acs5/profile/variables.html
#https://www.census.gov/data/developers/data-sets/acs-5year.html

#Assemble components of this query by following these steps:
#1. Start your query with the host name:
host_name = "https://api.census.gov/data"

# 2. Add the data year to the query:
#https://api.census.gov/data/2021
data_year = "/2021"

#3. Add the dataset name acronym:
#https://api.census.gov/data/2019/acs/acs5
dataset_name_acronym = "/acs/acs5"

#This is the base URL for this dataset. You can find dataset names by browsing the
#discovery tool: https://api.census.gov/data.html

#4. Add ?get= to the query:
#https://api.census.gov/data/2021/acs/acs5?get=

#5. Add your variables:
list_of_vars = "NAME,DP02_0001E,DP02PR_0001E,DP03_0001E,DP03_0051E,DP03_0095E,DP02_0058E,DP05_0033E" #note that this list isn't complete

#NAME
# = total population

#DP02_0001E = total households
#DP02PR_0001E = total households in puerto rico
#DP03_0001E = employment (employment rate); Estimate!!EMPLOYMENT STATUS!!Population 16 years and over
#DP03_0051E = income and poverty (median household income); Estimate!!INCOME AND BENEFITS (IN 2018 INFLATION-ADJUSTED DOLLARS)!!Total households
#DP03_0095E = health (without health care coverage); Estimate!!HEALTH INSURANCE 
#DP02_0058E = education (bachelor's degree or higher); Estimate!!EDUCATIONAL ATTAINMENT!!Population 25 years and over
#DP05_0033E = Estimate!!RACE!!Total population


#6. Add your geographies:
#https://api.census.gov/data/2021/acs/acs5/profile/examples.html
#geo = "&for=state*"
geo = "&for=county:*&in=state:*"

#query_url = f"{host}{year}{dataset_acronym}{g}{variables}{location}{usr_key}" #fix these variables
response = requests.get(query_url)
census_json = response.json()

#save to a data frame
#census_df = 

#some light cleaning of the variables in the dataframe (e.g., it would be nice if the variables had descriptive variable names)

#save df to csv


#manually constructed link
https://api.census.gov/data/2021/acs/acs5?get=DP02_0001E,DP02PR_0001E,DP03_0001E,DP03_0051E,DP03_0095E,DP02_0058E,DP05_0033E&for=county:*&in=state:*&key=dbaf6b8c0aa053d4df5ae844bba98940952fc50b
#^error: error: unknown variable 'DP02_0001E'

#attempt 2, after deleting above variable
https://api.census.gov/data/2021/acs/acs5?get=DP02PR_0001E,DP03_0001E,DP03_0051E,DP03_0095E,DP02_0058E,DP05_0033E&for=county:*&in=state:*&key=dbaf6b8c0aa053d4df5ae844bba98940952fc50b
#^error: error: unknown variable 'DP02PR_0001E'

#additional attempts: adding NAME to list of vars, deleting state from geo, acs1