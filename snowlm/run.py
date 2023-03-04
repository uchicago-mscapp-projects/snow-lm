from snowlm.scrape_api.voting_record import scrape_voting_behavior
from snowlm.data_analysis.climate import (
    clean_disaster_summaries)
# this should just be in a main file with a bunch of run functions. 
# moved the getting of the climate and econ datasets to climate_datasets.py

def get_voting_data():
    return scrape_voting_behavior()

## add neccessary function calls here. 