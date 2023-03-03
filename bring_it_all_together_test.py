from economic_impact import clean_disaster_summaries
from voting_record import scrape_voting_behavior
from climate_datasets import *

def get_climate_econ_data(only_2000_onwards):
    '''
    Asks whether the user wants only data from 2000 onwards or the entire time
    period 1980-2022 and returns a dataframe with total number of disaster events
    in each year by disaster type and the federal amount of money given for the
    same. 
    '''
    FEMA_obli_by_yr_state_disastertype = clean_disaster_summaries(
    "PublicAssistanceFundedProjectsSummaries.csv", "disaster_declarations.csv")

    #renaming the state_code column- move this to other file. 
    FEMA_obli_by_yr_state_disastertype.rename(columns = {"state_code": "state"}, 
                           inplace = True)
    FEMA_obli_by_yr_state_disastertype.rename(
        columns = {"federalObligatedAmount": "fed_amount"}, inplace = True)
    FEMA_obli_by_yr_state_disastertype.rename(
        columns = {"incidentType": "disaster_type"}, inplace = True)

    if only_2000_onwards:
        disaster_events_by_state = number_of_disaster_events_by_state(
            get_cleaned_data("disaster_declarations.csv", True))
    else:
        disaster_events_by_state = number_of_disaster_events_by_state(
            get_cleaned_data("disaster_declarations.csv", False))
    
    screen_1_data = disaster_events_by_state.merge(
        FEMA_obli_by_yr_state_disastertype, how='left', 
        on = ['state', 'year','disaster_type'])
    
    screen_1_data = screen_1_data.sort_values(by='year', ascending=True)

    return screen_1_data

def get_climate_econ_pop_data():
    '''
    Adds the population of the state at the time of the disaster.
    Population only available between 2000-2023, hence, only takes
    2000 onwards values.
    '''
    screen_1_data = get_climate_econ_data(only_2000_onwards=True)

    all_population = get_all_pop()
    screen_1_data["state_pop"] = None

    for index, row in screen_1_data.iterrows():
        state_name = str(row['state_name'])
        year = str(row['year'])
        pop_of_state_over_years = all_population.loc[all_population['state_name']
                                                      == state_name]
        pop_of_state_for_that_year = 0

        # remove if only taking 2000 onwards. 
        if year >= '2000' and not pop_of_state_over_years.empty:
            pop_of_state_for_that_year= pop_of_state_over_years[year].iloc[0]
        screen_1_data.at[index,'state_pop'] = pop_of_state_for_that_year
    
    return screen_1_data

def get_voting_data():
    return scrape_voting_behavior()
