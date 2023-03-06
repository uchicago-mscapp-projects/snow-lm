# Project Snow-Laughing-Matter

Final Project for CAPP122

### Team

Jackie Glasheen, Harsh Vardhan Pachisia, Shwetha Srinivasan, and Jennifer Yeaton

### Description

**42.63 %** of natural disasters in the United States since 1980 have taken place over the last 12 years. It is evident that climate change and global warming are causing extreme weather disasters to occur with more frequency. The increase in natural disaster declarations over the past several decades has led to the federal government spending more money on disaster relief.  Due to the increase in frequency and cost of such disasters,  a Congressional Research Service [paper](https://sgp.fas.org/crs/homesec/R45484.pdf) from January 2022 suggests that Congress may consider limiting federal disaster relief spending. 

Disasters impact different geographic regions, affecting specific states and communities disproportionately. Through this dashboard, we hope to shed light on the increase in disaster frequency and cost nationwide. We highlight the specific situation in each state, where its political stance is on climate, and showcase the top ten counties that are at most risk based on socio-economic factors and require long term policy action. 

This dashboard was built using Python and Dash, using [climate disaster](https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2) and [public assistance](https://www.fema.gov/openfema-data-page/public-assistance-funded-project-summaries-v1) data from the Federal Emergency Management Agency, scraped data of the voting patterns on the Climate IRA bill, and the [Census API](https://www.census.gov/data/developers/data-sets.html) for county-level socio-economic breakdown. 

### Runing the project

This project can be run using Poetry. The steps are outlined below.

1. Make a clone of the project repository

2. Go to the project directory: `cd 30122-project-snow-lm`

3. From the directory install virtual environment and dependencies: `poetry install`

4. Activate the virtual environment: `poetry shell`

5. Run the project: `python3 -m snowlm`

It will ask you to open the dash application in the browser to see the interactive dashboard. 

### Example Charts

![Trends in Number of Disaters](https://drive.google.com/file/d/14DmBf-ecgK25l1VxlRsWcoEnNA5sD4WN/view?usp=sharing)

![Disasters in states across years](https://drive.google.com/file/d/1b5LcTK_xHHWHlqe9LvI3PgQm-4jkCMeo/view?usp=sharing)