import pandas as pd
from snowlm.data_analysis.climate import (get_cleaned_data,
                                                       list_of_disaster_numbers)

def clean_disaster_summaries(filepath_public_assistance, filepath_disasters):
    '''
    Clean the Public Assistance Funded Project Summaries raw CSV file.
    Raw file downloaded from FEMA 
    
    Inputs:
        filepath_public_assistance (str): filepath to raw public assistance data
        filepath_disasters (str): filepath to raw disaster data
    Output (pandas df) data frame with the total FEMA public assistance federal 
    obligations by year and state.    
    '''

    project_summaries = pd.read_csv(filepath_public_assistance)

    # Limit dataset to the subsetted disasters (see assumptions in climate_datasets.py)
    disaster_list = list_of_disaster_numbers(get_cleaned_data(filepath_disasters, True))
    project_summaries = project_summaries[project_summaries.isin({"disasterNumber":
        disaster_list}).any(axis=1)]
    
    # Clean raw data
    project_summaries = project_summaries.drop(columns=['disasterNumber',
       'numberOfProjects', 'educationApplicant'])

    # Make a year variable
    project_summaries["year"] = project_summaries["declarationDate"].str[:4]

    # Merge with state name to state code lookup file
    state_code_lookup_raw = pd.read_csv("snowlm/data/Census_State_codes.txt",
                                        sep='|')
    state_code_lookup_raw = state_code_lookup_raw.drop(columns=['STATE',
        'STATENS'])
    state_code_lookup_raw = state_code_lookup_raw.rename(
        columns={"STATE_NAME": "state", "STUSAB": "state_code"})
    project_summaries = pd.merge(
        project_summaries, state_code_lookup_raw, how='left', on = 'state')

    project_summaries = project_summaries.drop(columns=['state'])

    # Aggregate federal oblications by state year, and disaster type
    project_summaries = project_summaries.groupby(['state_code',
        'incidentType', "year"], as_index=False).sum('federalObligatedAmount')
    project_summaries.rename(columns = {"state_code": "state", 
        "federalObligatedAmount": "fed_amount", "incidentType": "disaster_type"}, 
                           inplace = True)
                           
    return project_summaries

def aggregate_public_assistance(public_assistance_df_file):    
    """
    """
    project_summaries = public_assistance_df_file.drop(columns=['disasterNumber',
        'numberOfProjects', 'educationApplicant'])

    # Aggregate federal oblications by state year, and disaster type
    collapsed_summaries = project_summaries.groupby(['state',
        'disaster_type', "year"], as_index=False).sum('fed_amount')

    return collapsed_summaries

def top_5_by_public_assistance(public_assistance_df_file):   
    """
    """
    project_summaries = public_assistance_df_file.drop(columns = ['numberOfProjects',
     'educationApplicant'])
    collapsed_summaries = project_summaries.groupby(['disasterNumber','state', 
        'disaster_type', "year"], as_index = False).sum('fed_amount')

    collapsed_summaries = public_assistance_df_file.sort_values(['state','fed_amount'], 
        ascending = [True, False]).groupby('state').head(5)

    return collapsed_summaries