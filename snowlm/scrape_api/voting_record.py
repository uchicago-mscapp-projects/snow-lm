'''
CAPP 30122
Team: Snow Laughing Matter
Author: Jackie Glasheen

Code for scraping and processing senator voting on the Inflation Reduction Act

Source web page:
https://www.senate.gov/legislative/LIS/roll_call_votes/vote1172/vote_117_2_00325.htm
'''

import requests
import lxml.html
import pandas as pd


def scrape_voting_behavior():
    """
    Scrapes the Senator voting behavior on the Inflation Reduction Act.

    Returns (df) a pandas dataframe with the number of senators voting "Yay" and
        "Nay" votes for the bill, by state and political party.
    """

    response = requests.get(
    "https://www.senate.gov/legislative/LIS/roll_call_votes/vote1172/vote_117_2_00325.htm")

    root = lxml.html.fromstring(response.content)
    c = root.cssselect("div.contenttext")[30:180]

    senator_voting_by_state = {}
    for i, row in enumerate(c):

        # Removing the state name that is brought in as every third observation
        if i % 3 == 0:
            continue

        # Extracting key information
        vote = row.text_content()[-4:-1]
        state = row.text_content()[-9:-7]
        party = row.text_content()[-11:-10]

        if state in senator_voting_by_state:
            overal_yea, overall_nay, D_yea, D_nay, R_yea, R_nay = senator_voting_by_state[state]
        else:
            senator_voting_by_state[state] = (0,0,0,0,0,0)
            overal_yea, overall_nay, D_yea, D_nay, R_yea, R_nay = senator_voting_by_state[state]

        if vote == "Yea":
            overal_yea += 1
            if party in ("D","I"):
                D_yea += 1
            if party == "R":
                R_yea += 1
        if vote == "Nay":
            overall_nay += 1
            if party in ("D","I"):
                D_nay += 1
            if party == "R":
                R_nay += 1

        senator_voting_by_state[state] = (overal_yea, overall_nay, D_yea, D_nay,
            R_yea, R_nay)

    dataframe = pd.DataFrame.from_dict(senator_voting_by_state, orient='index',
        columns=['overal_yea', 'overall_nay', 'D_yea', 'D_nay', 'R_yea', 'R_nay'])

    return dataframe
