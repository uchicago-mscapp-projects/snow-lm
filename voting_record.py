import requests
import lxml.html


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
        # print(i, table.text_content())

        # Removing the state name that is brought in as every third observation
        if i % 3 == 0:
            continue

        vote = row.text_content()[-4:-1]
        #print(vote)
        state = row.text_content()[-9:-7]
        #print(state)

        if state in senator_voting_by_state:
            if vote == "Yea":
                senator_voting_by_state[state] = senator_voting_by_state[state] + 1
        else:
            senator_voting_by_state[state] = 0
            if vote == "Yea":
                senator_voting_by_state[state] = 1

    print(senator_voting_by_state)

    return senator_voting_by_state