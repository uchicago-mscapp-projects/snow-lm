import pandas as pd

################################################################################
### Exploration of FEMA public assistance federal obligation data  ###
project_summaries = pd.read_csv("PublicAssistanceFundedProjectsSummaries.csv")

# Initial Exploratory 
project_summaries.head()
list(project_summaries.columns)

# Code for reshaping the data to be wide by disaster type rather than long
pivoted = collapsed_summaries.pivot(index="state", columns="incidentType", values="federalObligatedAmount")
pivoted.sum(axis='columns') #returns total by state
print(pivoted)


################################################################################
