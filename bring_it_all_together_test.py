from economic_impact import clean_disaster_summaries
import voting_record
from climate_datasets import *

def get_climate_econ_data():
    FEMA_obli_by_yr_state_disastertype = clean_disaster_summaries(
    "PublicAssistanceFundedProjectsSummaries.csv", "disaster_declarations.csv")

    #renaming the state_code column- move this to other file. 
    FEMA_obli_by_yr_state_disastertype.rename(columns = {"state_code": "state"}, 
                           inplace = True)
    FEMA_obli_by_yr_state_disastertype.rename(
        columns = {"federalObligatedAmount": "fed_amount"}, inplace = True)
    FEMA_obli_by_yr_state_disastertype.rename(
        columns = {"incidentType": "disaster_type"}, inplace = True)

    disaster_events_by_state = number_of_disaster_events_by_state(
    get_cleaned_data("disaster_declarations.csv", False))
    
    screen_1_data = disaster_events_by_state.merge(
        FEMA_obli_by_yr_state_disastertype, how='left', 
        on = ['state', 'year','disaster_type'])
    
    screen_1_data = screen_1_data.sort_values(by='year', ascending=True)
    
    return screen_1_data

