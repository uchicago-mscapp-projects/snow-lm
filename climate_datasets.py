import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
#importing dataset
#"disaster_declarations.csv"

def get_cleaned_data(raw_data_path, only_2000_onwards):
    '''
    Takes in raw data filepath and a boolean to choose only last 20 years of 
        data or data since 1980 and outputs the clean climate related disasters
        over the last 23 years or between 1980-2000. 
        For counties: Only take last 23 years
        For days in disaster: Take data from last 23 years. 
        For rest: Take data from 1980. 
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

    
    climate_disasters["dec_date"] = pd.to_datetime(climate_disasters["dec_date"])
    climate_disasters['year'] = climate_disasters['dec_date'].dt.strftime('%Y')

    if only_2000_onwards:
        #subsetting into last 22 years (2000-2022), excluding 2023. 
        climate_cleaned = climate_disasters.loc[(
            climate_disasters['year'] >= '2000')
                     & (climate_disasters['year'] < '2023')]
    else:
        # take from 1980-2022
        climate_cleaned = climate_disasters.loc[(
            climate_disasters['year'] >= '1980') & (
            climate_disasters['year'] < '2023')]
    
    #remove records that have 0's in the county code- they are ones that are 
    # state-wide disasters and are already covered by other rows. 
    climate_cleaned.drop(climate_cleaned[climate_cleaned['county_code'] == 0].index,
                          inplace = True)
    
    # add state name
    state_names = get_state_names("Census_State_codes.txt")
    climate_data = climate_cleaned.merge(state_names, how='left', 
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
    climate_summary = climate_summary[['year','state','state_name',
                                       'disaster_type']]

    # getting the total number of events in each state by incident type- just 
    # the duplicate rows
    climate_summary = climate_summary.groupby(climate_summary.columns.tolist(),
                                              as_index=False).size()
    #renaming the size column. 
    climate_summary.rename(columns = {"size": "total_number_of_events"}, 
                           inplace = True)
    #print(climate_summary)
    return climate_summary

def num_of_disasters(climate_summary):
    '''
    get the major disasters that take place in each state
    '''
    climate_grouped_by_disasters =  climate_summary.groupby(
        ['state_name', 'disaster_type'], as_index = False)[
        'total_number_of_events'].sum()
    
    return climate_grouped_by_disasters

def change_in_frequency(climate_summary):
    '''
    Takes a pandas dataframe and returns the sum of each disaster taking place
    each year across the nation to compare across time.
    '''
    climate_by_state = climate_summary.groupby(
        ['state_name','disaster_type','year'], as_index = False)[
        'total_number_of_events'].sum()

    climate_by_state = climate_by_state.groupby(
        ['disaster_type','year'], as_index = False)['total_number_of_events'].sum()

    return climate_by_state

def number_of_disasters_over_last_decade(climate_summary):
    '''
    Takes a pandas df and returns the % of disasters that have taken place since
    2010.
    '''
    climate_last_dec = climate_summary.loc[(climate_summary['year'] >= '2010')
                     & (climate_summary['year'] <= '2022')]
    num_of_disasters_total = climate_summary['total_number_of_events'].sum()
    num_of_disasters_since2010 = climate_last_dec['total_number_of_events'].sum()
    
    no_of_disasters = num_of_disasters_since2010/num_of_disasters_total * 100

    return np.round(no_of_disasters,decimals = 2)

def number_of_days_in_dec_disaster(climate_df):
    '''
    Takes in a cleaned pandas dataframe and returns a dictonary that maps the
    average number of days per year that a state has been in a disaster 
    scenario.
    '''
    # removing unneccessary columns
    climate_state = climate_df.drop(columns=['state_code','county_code',
                                               'dec_date','pa_program','state'])
    
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
        ['state_name', 'year'], as_index = False)['length_of_disaster'].mean()
    
    climate_grouped_by_state = climate_grouped_by_state.groupby(
        ['state_name'], as_index = False)['length_of_disaster'].mean()
    
    climate_grouped_by_state['length_of_disaster'] = np.round(
        climate_grouped_by_state['length_of_disaster'], decimals = 1)
    
    # a dict with states as keys and values as the average length of the disaster
    climate_dict= dict(zip(climate_grouped_by_state.state_name,
                            climate_grouped_by_state.length_of_disaster))
    
    # add the national average
    national_average = climate_grouped_by_state["length_of_disaster"].mean()
    climate_dict['National Average'] = np.round(national_average,decimals = 1)

    return climate_dict

def get_pop_across_years(raw_file,period_start, period_end):
    '''
    Inputs state level population numbers from either 2000-2009, 2010-2019 or
    2020-2022, a period_start and period_end year and outputs the population
    of each state in that period. 
    '''
    pop_period = pd.read_csv(raw_file)
    
    # dropping all NA values
    pop_period.dropna(axis=0,inplace= True)

    # getting the right columns needed for the period
    name_list = ['state_name'] + list(range(period_start,period_end +1))
    name_list = [str(i) for i in name_list]

    # file specific cleaning requirements based on exploration
    if period_start == 2000:
        pop_period.drop(columns=pop_period.columns[-2:], axis=1, inplace=True)
        pop_period.drop(columns=pop_period.columns[1], axis=1, inplace=True)
    elif period_start == 2010:
        pop_period.drop(columns=pop_period.columns[1:3], axis=1, inplace=True)
    elif period_start == 2020:
        pop_period.drop(columns=pop_period.columns[1], axis=1, inplace=True)
    else:
        raise Exception ("Out of bound time period")
    
    #renaming all columns for the period
    pop_period.columns = name_list
    
    #data cleaning
    pop_period['state_name'] = pop_period["state_name"].str.replace(".","",
                                                                     regex= True)

    # get the state names and matching
    state_names = get_state_names('Census_State_codes.txt')
    state_name_list = state_names.state_name.values.tolist()
    pop_period = pop_period.loc[pop_period['state_name']
                                      .isin(state_name_list)]
    
    return pop_period

def get_all_pop():
    '''
    gets all state population numbers from 2000-2022. 
    '''
    pop_2000_2009 = get_pop_across_years("state_pop_2000_2009.csv", 2000,2009)
    pop_2010_2019 = get_pop_across_years("state_pop_2010_2019.csv", 2010,2019)
    pop_2020_2022 = get_pop_across_years("state_pop_2020_2022.csv", 2020,2022)

    #merging all periods together
    all_pop= pop_2000_2009.merge(pop_2010_2019, how='left', on='state_name')
    all_pop = all_pop.merge(pop_2020_2022, how='left', on='state_name')
    
    return all_pop