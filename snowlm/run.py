from snowlm.scrape_api.voting_record import scrape_voting_behavior

# this should just be in a main file with a bunch of run functions. 
# moved the getting of the climate and econ datasets to climate_datasets.py

def get_voting_data():
    return scrape_voting_behavior()
