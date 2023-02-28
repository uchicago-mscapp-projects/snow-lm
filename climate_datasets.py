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
    '''
    Takes in raw data filepath and outputs the clean climate related disasters
    over the last 23 years. 
    '''

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
    # removing severe storm(s) since they are only 4 which are statewide emergencies 
    # that are already covered by severe storm, duplicates for our purposes.
    unwanted_disasters = ['Biological','Toxic Substances','Chemical',
                          'Terrorist','Human Cause','Fishing Losses', 'Severe Storm(s)']
    climate_disasters_list = [ele for ele in disaster_type_list 
                              if ele not in unwanted_disasters]
    climate_disasters = disasters.loc[disasters['disaster_type']
                                      .isin(climate_disasters_list)]

    #subsetting into last 23 years (2000-2023)
    climate_disasters["dec_date"] = pd.to_datetime(climate_disasters["dec_date"])
    climate_disasters['year'] = climate_disasters['dec_date'].dt.strftime('%Y')
    climate_last_23 = climate_disasters.loc[(climate_disasters['year'] >= '2000')
                     & (climate_disasters['year'] <= '2023')]
    
    #remove records that have 0's in the county code- they are ones that are state-wide
    climate_last_23.drop(climate_last_23[climate_last_23['county_code'] == 0].index, inplace = True)
    
    return climate_last_23

def list_of_disaster_numbers(climate_df):
    '''
    Inputs a cleaned climate pandas dataframe and returns a list of all disasters
    '''
    return climate_df.disaster_number.unique().tolist()

def counties_affected_by_disasters(climate_df):
    '''
    Inputs a pandas dataframe and returns a list of cleaned county codes that
    are affected by climate related disasters over the last 23 years. 
    '''
    # adding leading 0's to each state code

    #climate_last_23['state_code'] = list(map(lambda x: x.zfill(1), climate_last_23['state_code']))
    climate_df["state_code"] = climate_df.state_code.map("{:02}".format)
    #climate_last_23["state_code"] = climate_last_23.state_code.map("{:02}".format)
    #print(climate_last_23["state_code"])

    # ensuring each county code has 3 digits and a leading zero where needed
    climate_df["county_code"] = climate_df.county_code.map("{:03}".format)
    #climate_last_23['county_code'] = list(map(lambda x: x.zfill(2), climate_last_23['county_code']))
    # merging it into a full county code
    
    climate_df['full_county_code'] = climate_df['state_code'] + climate_df['county_code']
    
    return climate_df.full_county_code.unique().tolist()

def number_of_disaster_events_by_state(climate_df):
    '''
    Inputs a pandas dataframe and provides a dataframe of the number of disaster
    events by state.
    '''
    # removing unneccessary columns
    climate_summary = climate_df.drop(columns=['state_code','county_code','dec_date','pa_program', 'begin_date', 'end_date'])

    #only keep one county row per disaster- since we just need to find the total number of events
    climate_summary = climate_summary.drop_duplicates(subset ='disaster_number', keep = "first")

    #reordering the columns
    climate_summary = climate_summary[['year','state','disaster_type']]

    # getting the total number of events in each state by incident type- just the duplicate rows
    climate_summary = climate_summary.groupby(climate_summary.columns.tolist(),as_index=False).size()

    #renaming the size column. 
    climate_summary.rename(columns = {"size": "total_number_of_events"}, inplace = True)
    
    return climate_summary

