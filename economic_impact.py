import pandas as pd
from climate_datasets import get_cleaned_data, 

def clean_disaster_summaries(filepath):
    '''
    Clean the Public Assistance Funded Project Summaries raw CSV file.
    Raw file downloaded from FEMA 
    
    Output (pandas df) data frame with the total FEMA public assistance federal 
    obligations by year and state.    
    '''

    project_summaries = pd.read_csv(filepath)
    
    # Limit dataset to the subsetted disasters (see assumptions in climate_datasets.py)
    disaster_list = list_of_disaster_numbers(get_cleaned_data(raw_data_path))

    # Clean raw data
    project_summaries = project_summaries.drop(columns=['disasterNumber', 
        'numberOfProjects', 'educationApplicant'])
    project_summaries["year"] = project_summaries["declarationDate"].str[:4]
   
    # Merge with state name to state code lookup file
    state_code_lookup_raw = pd.read_csv("Census_State_codes.txt",sep='|')
    state_code_lookup_raw = state_code_lookup_raw.drop(columns=['STATE', 
        'STATENS'])
    state_code_lookup_raw = state_code_lookup_raw.rename(
        columns={"STATE_NAME": "state", "STUSAB": "state_code"})
    project_summaries = pd.merge(
        project_summaries, state_code_lookup_raw, how='left', on = 'state')

    # Aggregate federal oblications by state year, and disaster type
    collapsed_summaries = project_summaries.groupby(['state_code', 
        'incidentType', "year"], as_index=False).sum('federalObligatedAmount')

    return collapsed_summaries