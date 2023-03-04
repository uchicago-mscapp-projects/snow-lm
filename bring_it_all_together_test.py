from economic_impact import clean_disaster_summaries
from voting_record import scrape_voting_behavior
from climate_datasets import *

def get_climate_econ_data(only_2000_onwards):
    '''
    Asks whether the user wants only data from 2000 onwards or the entire time
        period 1980-2022 and returns a dataframe with total number of disaster
        events in each year by disaster type and the federal amount of money
        given for the same.
    
    Inputs:
        only_2000_onwards(Boolean): True/False for whether to choose data from 
            2000-2022 or 1980-2022.
    
    Returns:
        climate_econ_data: A pandas dataframe that provided climate and economic
            data.
    '''
    FEMA_obli_by_yr_state_disastertype = clean_disaster_summaries(
    "PublicAssistanceFundedProjectsSummaries.csv", "disaster_declarations.csv")

    if only_2000_onwards:
        disaster_events_by_state = number_of_disaster_events_by_state(
            get_cleaned_data("disaster_declarations.csv", True))
    else:
        disaster_events_by_state = number_of_disaster_events_by_state(
            get_cleaned_data("disaster_declarations.csv", False))
    
    climate_econ_data = disaster_events_by_state.merge(
        FEMA_obli_by_yr_state_disastertype, how='left', 
        on = ['state', 'year','disaster_type'])
    
    climate_econ_data = climate_econ_data.sort_values(by='year',ascending=True)

    return climate_econ_data

def get_climate_econ_pop_data():
    '''
    Adds the population of the state at the time of the disaster. Note: 
        Population only available between 2000-2023.
    
    Inputs: None

    Returns:
        climate_econ_pop:A pandas dataframe that provided climate, economic and
            population data. 
    '''
    climate_econ_pop = get_climate_econ_data(only_2000_onwards=True)

    all_population = get_all_pop()
    climate_econ_pop["state_pop"] = None

    for index, row in climate_econ_pop.iterrows():
        state_name = str(row['state_name'])
        year = str(row['year'])
        pop_of_state_over_years = all_population.loc[all_population['state_name']
                                                      == state_name]
        pop_of_state_for_that_year = 0

        if not pop_of_state_over_years.empty:
            pop_of_state_for_that_year= pop_of_state_over_years[year].iloc[0]
        climate_econ_pop.at[index,'state_pop'] = pop_of_state_for_that_year
    
    return climate_econ_pop

def get_voting_data():
    return scrape_voting_behavior()