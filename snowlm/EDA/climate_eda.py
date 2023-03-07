'''
Severe Climate Events: Disaster Declaration for states and counties
Exploratory Data Analysis by @Harsh Vardhan Pachisia
'''
import pandas as pd
pd.options.mode.chained_assignment = None

disasters_raw = pd.read_csv("snowlm/data/disaster_declarations.csv")

##Understanding the raw data
disasters_raw.head()
disasters_raw.info()

# keeping only the possibly relevant columns
disasters = disasters_raw[[
    'id','disasterNumber', 'state','fipsStateCode','fipsCountyCode','placeCode',
    'declarationDate','fyDeclared','incidentType', 'ihProgramDeclared',
    'iaProgramDeclared','paProgramDeclared','hmProgramDeclared',
    'incidentBeginDate','incidentEndDate','designatedArea']]

#Understanding the type of disasters present
disasters.incidentType.describe()
disasters.incidentType.value_counts()

##Two points of note: 
#1. There are non-natural disasters in this data that need to be removed 
# including: 'Biological','Toxic Substances','Chemical','Terrorist',
# 'Human Cause','Fishing Losses'. 
#2. 'Severe Storms' and 'Severe Storm(s)' are repeated, needs to be checked.

disasters.loc[disasters["incidentType"] == "Severe Storms(s)"]
# only 3 severe storms(s) (based on disaster numbers). 
# check if they overlap with 'Severe Storm'.
disasters.loc[disasters["disasterNumber"] == 4670]
disasters.loc[disasters["disasterNumber"] == 4664]
disasters.loc[disasters["disasterNumber"] == 4672]
# each severe storms(s) overlaps with 'Severe Storm'
# can be removed from the dataset to avoid duplication. 

#Calculating the number of disasters by incident type and 
# removing the ones that are not climate disasters. 
disaster_type_list = disasters.incidentType.unique().tolist()
disaster_type_list
#removing severe storm(s) since they are only 3 which are 
# statewide emergencies that are already covered by severe storm- duplicates
unwanted_disasters = ['Biological','Toxic Substances','Chemical','Terrorist',
                      'Human Cause','Fishing Losses', 'Severe Storm(s)']
climate_disasters_list = [ele for ele in disaster_type_list 
                          if ele not in unwanted_disasters]
climate_disasters = disasters.loc[
    disasters['incidentType'].isin(climate_disasters_list)]

#Checking for state-wide disasters that can be removed
# if they are already covered by a county, to ensure that county codes of 0
# are not kept in the dataset. 
state_wide_disasters = disasters.loc[disasters["designatedArea"] == "Statewide"]

#### Subsetting the data to the last 23 years (2000-2022). 
climate_disasters["declarationDate"] = pd.to_datetime(
    climate_disasters["declarationDate"])
# adding a year column
climate_disasters['Year'] = climate_disasters[
    'declarationDate'].dt.strftime('%Y')

# subsetting the data
climate_last_23 = climate_disasters.loc[(climate_disasters['Year'] >= '2000')
                     & (climate_disasters['Year'] <= '2023')]
climate_last_23.head()

#If we take all years- we have 52,445 counties that have been affected
# by climate-related disasters.
# If we take from 2000 onwards (2000-2022 included),
# we get 36,340 counties that have been affected by climate-related disasters.
 
#Renaming climate columns
climate_last_23.columns = ['record_id', 'disaster_number', 'state', 'state_code',
                          'county_code','place_code','dec_date', 'fiscal_year',
                        'disaster_type','ih_program','ia_program', 'pa_program',
                        'hm_progam','begin_date', 'end_date', 'area_name',
                        'year']
climate_last_23.drop(columns=['record_id'], inplace= True)

### Deciding on economic assistance program to analyze. 
total_number_of_counties_affected = climate_last_23.shape[0]
climate_last_23.hm_progam.value_counts()/total_number_of_counties_affected
climate_last_23.ih_program.value_counts()/total_number_of_counties_affected
climate_last_23.ia_program.value_counts()/total_number_of_counties_affected
climate_last_23.pa_program.value_counts()/total_number_of_counties_affected

#Hazard Mitigation declared: 61.34%
#Individual and Households: 81.71%
#Individual Assistance: 86.46%
#Public Assistance: 94.13%

#Keeping only Public assistance column as it has the highest coverage
# in our dataset, is the largest program under FEMA, and hence, 
# has the largest economic impact. 

climate_last_23 = climate_last_23.drop(columns=[
    'ih_program','ia_program','hm_progam'])