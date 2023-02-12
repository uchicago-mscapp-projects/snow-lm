import requests
import lxml.html

#pip install lxml
## need lxml and requests in virtual environment!!

def scrape_voting_behavior():
"""
Scrapes the Senator voting behavior on the Inflation Reduction Act

Returns: dictionary mapping states to the number of senator "Yay" votes for the bill
"""
response = requests.get("https://www.senate.gov/legislative/LIS/roll_call_votes/vote1172/vote_117_2_00325.htm")

#print(response.text)

root = lxml.html.fromstring(response.content)
response.cssselect("b")[0].text_content()