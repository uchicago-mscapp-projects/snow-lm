'''
CAPP 30122
@Team: Snow Laughing Matter
@Author: Harsh Vardhan Pachisia

Code for cleaning and analyzing the climate datasets from FEMA and
writing functions to obtain final datasets for each visual. 
'''
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np

def get_cleaned_data(raw_data_path,only_2000_onwards):
    '''
    Takes in raw data filepath and a boolean to choose only last 20 years of 
        data or data since 1980 and outputs the clean climate related disasters
        betweeen 2000-2022 or between 1980-2000.
    
    Inputs:
        raw_data_path(string): File path to CSV File of climate data.
        only_2000_onwards(Boolean): True/False for whether to choose data from 
            2000-2022 or 1980-2022.
        
    Returns:
        A pandas dataframe of cleaned data containing climate related disasters
            for the specified time period. 
    '''
    disasters_raw = pd.read_csv(raw_data_path)

    #keeping only required columns
    disasters = disasters_raw[['disasterNumber', 'state','fipsStateCode',
    'fipsCountyCode','declarationDate','incidentType','paProgramDeclared',
    'incidentBeginDate','incidentEndDate']]

    disasters.columns = ['disaster_number', 'state', 'state_code',
                          'county_code','dec_date',
                        'disaster_type', 'pa_program',
                        'begin_date', 'end_date']
    
    disaster_type_list = disasters.disaster_type.unique().tolist()

    #removing non-climate related disasters or climate disasters that are 
    #repeated (check climate_eda.py for further details)
    unwanted_disasters = ['Biological','Toxic Substances','Chemical',
                          'Terrorist','Human Cause','Fishing Losses',
                            'Severe Storm(s)']
    climate_disasters_list = [ele for ele in disaster_type_list 
                              if ele not in unwanted_disasters]
    climate_disasters = disasters.loc[disasters['disaster_type']
                                      .isin(climate_disasters_list)]

    #subsetting data based on time period
    climate_disasters["dec_date"] = pd.to_datetime(
        climate_disasters["dec_date"])
    climate_disasters['year'] = climate_disasters['dec_date'].dt.strftime('%Y')

    if only_2000_onwards:
        #subsetting into last 22 years (2000-2022), excluding 2023. 
        climate_cleaned = climate_disasters.loc[(
            climate_disasters['year'] >= '2000')
                     & (climate_disasters['year'] < '2023')]
    else:
        climate_cleaned = climate_disasters.loc[(
            climate_disasters['year'] >= '1980') & (
            climate_disasters['year'] < '2023')]
    
    #remove records that have 0's in the county code- they are ones that are 
    # state-wide disasters and are already covered by other rows. 
    climate_cleaned.drop(climate_cleaned[
        climate_cleaned['county_code'] == 0].index,inplace=True)
    
    # add state name for readability
    state_names = get_state_names("snowlm/data/Census_State_codes.txt")
    climate_data = climate_cleaned.merge(state_names,how='left',on=['state'])
    
    return climate_data

def get_state_names(raw_file_path):
    '''
    Inputs a raw file of state codes ("snowlm/data/Census_State_codes.txt")
    and outputs a pandas dataframe with the 2 letter state codes and state name.

    Inputs:
        raw_data_path(string): File path to CSV File of state codes data.
    
    Returns:
        state_names: A pandas dataframe of state codes and state names. 
    '''
    state_code_lookup_raw = pd.read_csv(raw_file_path,sep='|')
    state_code_lookup_raw.drop(columns=['STATE','STATENS'],inplace=True)
    state_names =  state_code_lookup_raw.rename(
        columns={"STATE_NAME": "state_name", "STUSAB": "state"})
    
    return state_names

def list_of_disaster_numbers(climate_df):
    '''
    Inputs a cleaned climate pandas dataframe and returns list of all disasters.
    
    Inputs:
        climate_df (pandas dataframe): Cleaned climate disasters data.
    
    Returns:
        List of disasters (based by their unique disaster numbers) that have
            occurred in that time period. 
    '''
    return climate_df.disaster_number.unique().tolist()

def counties_affected_by_disasters(climate_df):
    '''
    Inputs a pandas dataframe (the output of running
        get_cleaned_data(raw_data_path)) and returns a list of cleaned county 
        codes that are affected by climate related disasters over last 23 years.
    
    Inputs:
        climate_df (pandas dataframe): Cleaned climate disasters data
    
    Returns:
        List of full county codes to be used for matching with Census data. 
    '''
    # adding leading 0's to each state code
    climate_df["state_code"] = climate_df.state_code.map("{:02}".format)

    # ensuring each county code has 3 digits and a leading zero where needed
    climate_df["county_code"] = climate_df.county_code.map("{:03}".format)

    # merging it into a full county code
    climate_df['full_county_code'] = climate_df['state_code'] + climate_df[
        'county_code']
    
    return climate_df.full_county_code.unique().tolist()

def number_of_disaster_events_by_state(climate_df):
    '''
    Inputs a pandas dataframe(the output of running 
        get_cleaned_data(raw_data_path)) and provides a dataframe of the number
        of disaster events by state.
    
    Inputs:
         climate_df (pandas dataframe): Cleaned climate disasters data
    
    Returns:
        climate_summary: A pandas dataframe of the number of disaster events in
            each state. 
    '''
    # removing unneccessary columns
    climate_summary = climate_df.drop(columns=['state_code','county_code',
                                               'dec_date','pa_program',
                                                 'begin_date', 'end_date'])

    #only keep one county row per disaster- since we just need to find the total
    #number of events
    climate_summary = climate_summary.drop_duplicates(subset ='disaster_number',
                                                       keep = "first")
    climate_summary = climate_summary[['year','state','state_name',
                                       'disaster_type']]

    # getting the total number of events in each state by incident type
    climate_summary = climate_summary.groupby(climate_summary.columns.tolist(),
                                              as_index=False).size()
    climate_summary.rename(columns = {"size": "total_number_of_events"}, 
                           inplace = True)

    return climate_summary

def type_of_disasters_by_state(climate_summary):
    '''
    Gets the type of disasters that take place in each state.

    Inputs:
        climate_summary (pandas dataframe): Number of disasters in each state.
    
    Returns:
        climate_top_5 (pandas dataframe): Sum of each disaster
            type by each state, limited to the top 5.  
    '''
    climate_grouped_by_disasters = climate_summary.groupby(
        ['state', 'disaster_type'], as_index = False)[
        'total_number_of_events'].sum()
    climate_top_5 = climate_grouped_by_disasters.sort_values([
        'state','total_number_of_events'], ascending = [
        True, False]).groupby('state').head(5)
    
    return climate_top_5

def change_in_frequency(climate_summary):
    '''
    Takes a pandas dataframe and returns the sum of each disaster taking place
    each year across the nation to compare across time.

    Inputs:
        climate_summary (pandas dataframe): Number of disasters in each state.
    
    Returns:
        climate_by_state: A pandas dataframe with the total number of each kind
            of climate disaster across the nation. 
    '''
    climate_by_state = climate_summary.groupby(
        ['state_name','disaster_type','year'], as_index = False)[
        'total_number_of_events'].sum()

    climate_by_state = climate_by_state.groupby(
        ['disaster_type','year'], as_index = False)[
        'total_number_of_events'].sum()
    
    return climate_by_state

def number_of_disasters_over_last_decade(climate_summary):
    '''
    Takes a pandas df and returns the percentage of disasters that have taken 
        place since 2010.
    
    Inputs:
        climate_summary (pandas dataframe): Number of disasters in each state.
    
    Returns:
        percent_of_disasters: A float value of the number of disasters that have
            taken place since 2010. 
    '''
    climate_last_dec = climate_summary.loc[(climate_summary['year'] >= '2010')
                     & (climate_summary['year'] <= '2022')]
    num_of_disasters_total = climate_summary['total_number_of_events'].sum()
    num_of_disasters_since2010 = climate_last_dec[
        'total_number_of_events'].sum()
    
    no_of_disasters = (num_of_disasters_since2010/num_of_disasters_total) * 100
    percent_of_disasters = np.round(no_of_disasters,decimals=2)

    return percent_of_disasters

def number_of_days_in_dec_disaster(climate_df):
    '''
    Takes in cleaned pandas dataframe and returns a dictionary that maps the
        average number of days/year that a state has been in disaster scenario.
    
    Inputs:
        climate_df (pandas dataframe): Cleaned climate disasters data.
    
    Returns:
        climate_dict: A dictionary that maps each state and the avg number of
            days that it has been in a declared disaster scenario. 
    '''
    # removing unneccessary columns
    climate_state = climate_df.drop(columns=['state_code','county_code',
                                               'dec_date','pa_program',
                                               'state_name'])
    
    # remove all disasters that did not have either a begin date or end date
    climate_state_no_na = climate_state.dropna(subset=['begin_date','end_date'])
    
    # converting both end date and begin date to datetime
    climate_state_no_na['end_date']= pd.to_datetime(
        climate_state_no_na['end_date'])
    climate_state_no_na['begin_date']= pd.to_datetime(
        climate_state_no_na['begin_date'])
    climate_state_no_na['length_of_disaster'] = (
        climate_state_no_na['end_date'] - 
        climate_state_no_na['begin_date']).dt.days

    #only keep one county row per disaster- since we just need to find the total
    #number of events
    climate_state_no_na = climate_state_no_na.drop_duplicates(
        subset ='disaster_number',keep = "first")
    
    # getting the number of days
    climate_grouped_by_state = climate_state_no_na.groupby(
        ['state', 'year'], as_index = False)['length_of_disaster'].mean()
    climate_grouped_by_state = climate_grouped_by_state.groupby(
        ['state'], as_index = False)['length_of_disaster'].mean()
    climate_grouped_by_state['length_of_disaster'] = np.round(
        climate_grouped_by_state['length_of_disaster'], decimals = 1)
    
    # a dict with states as keys and values as the average length of disaster
    climate_dict = dict(zip(climate_grouped_by_state.state,
                            climate_grouped_by_state.length_of_disaster))
    
    # add the national average
    national_average = climate_grouped_by_state["length_of_disaster"].mean()
    climate_dict['National Average'] = np.round(national_average,decimals = 1)

    return climate_dict

def get_pop_across_years(raw_data_path,period_start,period_end):
    '''
    Inputs state level population numbers from either 2000-2009, 2010-2019 or
    2020-2022, a period_start and period_end year and outputs the population
    of each state in that period. 

    Inputs:
        raw_data_path(string): File path to CSV File of population data.
        period_start(int): Start of the period to get population data from.
        period_end(int): End of the period to get population data from.
    
    Returns:
        pop_period: A pandas dataframe that gives state population for period. 
    '''
    pop_period = pd.read_csv(raw_data_path)
    
    # dropping all NA values
    pop_period.dropna(axis=0,inplace= True)

    col_name_list = ['state_name'] + list(range(period_start,period_end +1))
    col_name_list = [str(i) for i in col_name_list]

    # file specific cleaning requirements based on exploration
    if period_start == 2000:
        pop_period.drop(columns=pop_period.columns[-2:],axis=1,inplace=True)
        pop_period.drop(columns=pop_period.columns[1],axis=1,inplace=True)
    elif period_start == 2010:
        pop_period.drop(columns=pop_period.columns[1:3],axis=1,inplace=True)
    elif period_start == 2020:
        pop_period.drop(columns=pop_period.columns[1],axis=1,inplace=True)
    else:
        raise Exception ("Out of bound time period")
    
    pop_period.columns = col_name_list
    
    #data cleaning
    pop_period['state_name'] = pop_period["state_name"
                                          ].str.replace(".","",regex= True)
    
    # get the state names and match
    state_names = get_state_names("snowlm/data/Census_State_codes.txt")
    state_name_list = state_names.state_name.values.tolist()
    pop_period = pop_period.loc[pop_period['state_name']
                                      .isin(state_name_list)]
    
    return pop_period

def get_all_pop():
    '''
    Gets all state population numbers from 2000-2022.

    Inputs: None

    Returns:
        all_pop: A pandas dataframe that gets population data from the period
            of 2000-2022. 
    '''
    pop_2000_2009 = get_pop_across_years("snowlm/data/state_pop_2000_2009.csv",
                                         2000,2009)
    pop_2010_2019 = get_pop_across_years("snowlm/data/state_pop_2010_2019.csv",
                                         2010,2019)
    pop_2020_2022 = get_pop_across_years("snowlm/data/state_pop_2020_2022.csv",
                                         2020,2022)

    #merging all periods together
    all_pop = pop_2000_2009.merge(pop_2010_2019,how='left',on='state_name')
    all_pop = all_pop.merge(pop_2020_2022,how='left',on='state_name')
    
    return all_pop