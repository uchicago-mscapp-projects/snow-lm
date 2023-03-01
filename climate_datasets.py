import pandas as pd
pd.options.mode.chained_assignment = None
#importing dataset
#"disaster_declarations.csv"

#get the state name added to the file- so that it can be used to hover. 
# add the graphics in jupyter- make that clean
# make the file for 

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
                          'Terrorist','Human Cause','Fishing Losses',
                            'Severe Storm(s)']
    climate_disasters_list = [ele for ele in disaster_type_list 
                              if ele not in unwanted_disasters]
    climate_disasters = disasters.loc[disasters['disaster_type']
                                      .isin(climate_disasters_list)]

    #subsetting into last 22 years (2000-2022), excluding 2023. 
    climate_disasters["dec_date"] = pd.to_datetime(climate_disasters["dec_date"])
    climate_disasters['year'] = climate_disasters['dec_date'].dt.strftime('%Y')
    climate_last_23 = climate_disasters.loc[(climate_disasters['year'] >= '2000')
                     & (climate_disasters['year'] < '2023')]
    
    #remove records that have 0's in the county code- they are ones that are 
    # state-wide disasters and are already covered by other rows. 
    climate_last_23.drop(climate_last_23[climate_last_23['county_code'] == 0].index,
                          inplace = True)
    
    # add state name
    state_names = get_state_names("Census_State_codes.txt")
    climate_data = climate_last_23.merge(state_names, how='left', 
                                         on = ['state'])
    
    return climate_data

# Census_State_codes.txt
def get_state_names(raw_file_path):
    '''
    Inputs a raw file of state codes and outputs a pandas dataframe with
    the 2 letter state codes and the state name.
    '''
    state_code_lookup_raw = pd.read_csv(raw_file_path,sep='|')
    state_code_lookup_raw.drop(columns=['STATE',
        'STATENS'], inplace=True)
    state_names =  state_code_lookup_raw.rename(
        columns={"STATE_NAME": "state_name", "STUSAB": "state"})
    
    return state_names

def list_of_disaster_numbers(climate_df):
    '''
    Inputs a cleaned climate pandas dataframe and returns a list of all disasters
    '''
    return climate_df.disaster_number.unique().tolist()

def counties_affected_by_disasters(climate_df):
    '''
    Inputs a pandas dataframe (the output of running 
        get_cleaned_data(raw_data_path)) and returns a list of cleaned county 
        codes that are affected by climate related disasters over 
        the last 23 years. 
    '''
    # adding leading 0's to each state code

    #climate_last_23['state_code'] = list(map(lambda x: x.zfill(1), 
    # climate_last_23['state_code']))
    climate_df["state_code"] = climate_df.state_code.map("{:02}".format)

    # ensuring each county code has 3 digits and a leading zero where needed
    climate_df["county_code"] = climate_df.county_code.map("{:03}".format)
    #climate_last_23['county_code'] = list(map(lambda x: x.zfill(2), 
    # climate_last_23['county_code']))

    # merging it into a full county code
    climate_df['full_county_code'] = climate_df['state_code'] + climate_df[
        'county_code']
    
    return climate_df.full_county_code.unique().tolist()

def number_of_disaster_events_by_state(climate_df):
    '''
    Inputs a pandas dataframe(the output of running 
        get_cleaned_data(raw_data_path)) and provides a dataframe of the number
        of disaster events by state.
    '''
    # removing unneccessary columns
    climate_summary = climate_df.drop(columns=['state_code','county_code',
                                               'dec_date','pa_program',
                                                 'begin_date', 'end_date'])

    #only keep one county row per disaster- since we just need to find the total
    # number of events
    climate_summary = climate_summary.drop_duplicates(subset ='disaster_number',
                                                       keep = "first")

    #reordering the columns
    climate_summary = climate_summary[['year','state','state_name','disaster_type']]

    # getting the total number of events in each state by incident type- just 
    # the duplicate rows
    climate_summary = climate_summary.groupby(climate_summary.columns.tolist(),
                                              as_index=False).size()

    #renaming the size column. 
    climate_summary.rename(columns = {"size": "total_number_of_events"}, 
                           inplace = True)
    
    return climate_summary

def number_of_days_in_dec_disaster(climate_df):
    '''
    Takes in a cleaned pandas dataframe and returns a dictonary that maps the
    average number of days per year that a state has been in a disaster 
    scenario.
    '''
    # removing unneccessary columns
    climate_state = climate_df.drop(columns=['state_code','county_code',
                                               'dec_date','pa_program'])
    
    # checking len of begin_date and end_date
    len(climate_state.begin_date.value_counts())
    len(climate_state.end_date.value_counts())

    # remove all disasters that did not have either a begin date or end date
    climate_state_no_na=climate_state.dropna(subset=['begin_date','end_date'])
    # converting both end date and begin date to 
    climate_state_no_na['end_date']= pd.to_datetime(
        climate_state_no_na['end_date'])
    climate_state_no_na['begin_date']= pd.to_datetime(
        climate_state_no_na['begin_date'])
    climate_state_no_na['length_of_disaster'] = (
        climate_state_no_na['end_date'] - 
        climate_state_no_na['begin_date']).dt.days

    #only keep one county row per disaster- since we just need to find the total
    # number of events
    climate_state_no_na = climate_state_no_na.drop_duplicates(
        subset ='disaster_number',keep = "first")
   
    climate_grouped_by_state = climate_state_no_na.groupby(
        ['state', 'year'], as_index = False)['length_of_disaster'].mean()
    climate_grouped_by_state = climate_grouped_by_state.groupby(
        ['state'], as_index = False)['length_of_disaster'].mean()
    
    # a dict with states as keys and values as the average length of the disaster
    climate_dict= dict(zip(climate_grouped_by_state.state,
                            climate_grouped_by_state.length_of_disaster))

    return climate_dict