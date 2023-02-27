import pandas as pd
#Func 1: get_cleaned_data(raw_data_path): converts the raw data into a 
# dataframe that can be used for screen 1 and screen 2

# func 2: climate_events_per_year(cleaned_data): Takes cleaned data dataframe
# and converts it to only the things needed for screen 1, returns that

# func 3: climate disasters in the state- for each state- what disasters took 
# place- takes the cleaned dataframe from 1 and computes

# func 4: Length of time in disaster state: Takes from one and computes lenght
# of time and returns the dataframe.

#importing dataset
#"disaster_declarations.csv"
def get_cleaned_data(raw_data_path):

    disasters_raw = pd.read_csv(raw_data_path)

    #keeping only required columns
    disasters = disasters_raw[['disasterNumber', 'state','fipsStateCode',
    'fipsCountyCode','declarationDate','incidentType','paProgramDeclared',
    'incidentBeginDate','incidentEndDate']]

    #renaming columns
    disasters.columns = ['disaster_number', 'state', 'state_code',
                          'county_code','dec_date',
                        'disaster_type', 'pa_program',
                        'begin_date', 'end_date']
    
    #keeping only climate related disasterrs
    disaster_type_list = disasters.disaster_type.unique().tolist()
    #non-climate related disasterrs
    unwanted_disasters = ['Biological','Toxic Substances','Chemical',
                          'Terrorist','Human Cause','Fishing Losses']
    climate_disasters_list = [ele for ele in disaster_type_list 
                              if ele not in unwanted_disasters]
    climate_disasters = disasters.loc[disasters['disaster_type']
                                      .isin(climate_disasters_list)]

    #subsetting into last 23 years (2000-2023)
    climate_disasters["dec_date"] = pd.to_datetime(climate_disasters["dec_date"])
    climate_disasters['year'] = climate_disasters['dec_date'].dt.strftime('%Y')
    climate_last_23 = climate_disasters.loc[(climate_disasters['year'] >= '2000')
                     & (climate_disasters['year'] <= '2023')]
    return climate_last_23

def list_of_disaster_numbers(climate_last_23):
    '''
    Inputs a pandas dataframe and returns a list of all disasters
    '''
    return climate_last_23.disaster_number.unique().tolist()