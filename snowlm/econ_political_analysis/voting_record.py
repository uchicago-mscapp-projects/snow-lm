import requests
import lxml.html
import pandas as pd


def scrape_voting_behavior():
    """
    Scrapes the Senator voting behavior on the Inflation Reduction Act

    Returns: dictionary mapping states to the number of senator "Yay" votes for the bill
    """
    
    response = requests.get("https://www.senate.gov/legislative/LIS/roll_call_votes/vote1172/vote_117_2_00325.htm")

    #print(response.text)

    root = lxml.html.fromstring(response.content)
    root.cssselect("b")[0].text_content()
    c = root.cssselect("b")[0].text_content()
    c = root.cssselect("div.contenttext")[30:180]
     
    senator_voting_by_state = {}
    for i, row in enumerate(c):
        #print(i, row.text_content())
        value_list = ()

        # Removing the state name that is brought in as every third observation
        if i % 3 == 0:
            continue

        vote = row.text_content()[-4:-1]
        #print(vote)
        state = row.text_content()[-9:-7]
        #print(state)
        party = row.text_content()[-11:-10]
        #print(party)

        if state in senator_voting_by_state:
            overal_yea, D_yea, D_nay, R_yea, R_nay = senator_voting_by_state[state]
            if vote == "Yea":
                overal_yea += 1
                if (party == "D" or party == "I"):
                    D_yea += 1
                if party == "R":
                    R_yea += 1
            if vote == "Nay":  
                if (party == "D" or party == "I"):
                    D_nay += 1
                if party == "R":
                    R_nay += 1

        else:
            senator_voting_by_state[state] = (0,0,0,0,0)
            overal_yea, D_yea, D_nay, R_yea, R_nay = senator_voting_by_state[state]
            if vote == "Yea":
                overal_yea += 1
                if (party == "D" or party == "I"):
                    D_yea += 1
                if party == "R":
                    R_yea += 1
            if vote == "Nay":  
                if (party == "D" or party == "I"):
                    D_nay += 1
                if party == "R":
                    R_nay += 1

        senator_voting_by_state[state] = (overal_yea, D_yea, D_nay, R_yea, R_nay)

    dataframe = pd.DataFrame.from_dict(senator_voting_by_state, orient='index', 
        columns=['overal_yea', 'D_yea', 'D_nay', 'R_yea', 'R_nay'])
    #print(dataframe)
    #print(senator_voting_by_state)
    return dataframe
