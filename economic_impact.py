import pandas as pd

def clean_disaster_summaries():
    project_summaries = pd.read_csv("PublicAssistanceFundedProjectsSummaries.csv")
    project_summaries.head()
    list(project_summaries.columns)
    
    ##MERGE With disaster IDS from Harsh Here on disasterNumber
    
    project_summaries = project_summaries.drop(columns=['disasterNumber', 'numberOfProjects','educationApplicant' ])
    project_summaries["year"] = project_summaries["declarationDate"].str[:4]
   
    #can add county here 

    state_code_lookup_raw = pd.read_csv("Census_State_codes.txt",sep='|')
    state_code_lookup_raw = state_code_lookup_raw.drop(columns=['STATE', 'STATENS'])
    state_code_lookup_raw = state_code_lookup_raw.rename(columns={"STATE_NAME": "state", "STUSAB": "state_code"})

    project_summaries = pd.merge(project_summaries, state_code_lookup_raw, how='left', on = 'state')

    collapsed_summaries = project_summaries.groupby(['state_code','incidentType',"year"], as_index=False).sum('federalObligatedAmount')
    #print(collapsed_summaries)
    
    #pivoted = collapsed_summaries.pivot(index="state", columns="incidentType", values="federalObligatedAmount")
    #pivoted.sum(axis='columns') #returns total by state

    #return pivoted
    return collapsed_summaries