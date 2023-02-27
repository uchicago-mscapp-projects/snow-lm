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
    pass


#keeping only required columns
disasters = disasters_raw[['disasterNumber', 'state','fipsStateCode','fipsCountyCode','placeCode','declarationDate','fyDeclared','incidentType',
    'ihProgramDeclared','iaProgramDeclared','paProgramDeclared','hmProgramDeclared',
    'incidentBeginDate','incidentEndDate','designatedArea']]

# only keeping climate related disasters
unwanted_disasters = ['Fire', 'Biological','Toxic Substances','Chemical','Terrorist','Human Cause','Fishing Losses']
climate_disasters_list = [ele for ele in disaster_type_list if ele not in unwanted_disasters]
climate_disasters = disasters.loc[disasters['incidentType'].isin(climate_disasters_list)]

# adding a year column
climate_disasters["declarationDate"] = pd.to_datetime(climate_disasters["declarationDate"])
climate_disasters['Year'] = climate_disasters['declarationDate'].dt.strftime('%Y')

#subsetting the data into the last 23 years (2000-2023)
climate_last_23 = climate_disasters.loc[(climate_disasters['Year'] >= '2000')
                     & (climate_disasters['Year'] <= '2023')]

#renaming columns
climate_last_23.columns = ['record_id', 'disaster_number', 'state', 'state_code',
                          'county_code','place_code','dec_date', 'fiscal_year',
                        'disaster_type','ih_program','ia_program', 'pa_program',
                        'hm_progam','begin_date', 'end_date', 'area_name','year']