

import requests
import pandas as pd
from pprint import pprint  # Allows "Pretty Printing" of dictionaries

"""
Found this website that has national poll information
https://projects.fivethirtyeight.com/polls/president-general/

A csv file can be downloaded from this address
https://projects.fivethirtyeight.com/polls-page/president_polls.csv
"""
verify_ssl = False  # True to enable SSL Certificate Check

#%%
# -----------------------------------------------------------------------------
# Download and Save National Poll Information
# -----------------------------------------------------------------------------
# Set the download url
url = 'https://projects.fivethirtyeight.com/polls-page/president_polls.csv'


def getPollData(url=url):
    # Create a request object
    r = requests.get(url, allow_redirects=True, verify=verify_ssl)

    # Set the filename the data is to be saved to
    fileName = 'president_polls.csv'

    # Write the contents of r to filename in binary format
    # The method below is the preferred way because the this form will automatically
    # close the file, even if an error occurs during the writing process.
    with open(fileName, 'wb') as f:
        f.write(r.content)

    # NOTE The line below is the one-line version that I found online. This is not
    # a preferred method because there is no close() command. Perhaps a ".close()"
    # could be appended to the end of this line.
    # open(fileName, 'wb').write(r.content)


    #%%
    # -----------------------------------------------------------------------------
    # Import Poll Information using PANDAS
    # -----------------------------------------------------------------------------
    """
    Using PANDAS to load in the CSV file. These are two good links...
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
    # https://pandas.pydata.org/pandas-docs/stable/reference/frame.html
    
    """

    # Load csv file into a PANDAS dataframe
    pollData = pd.read_csv(fileName)


    #%%
    # -----------------------------------------------------------------------------
    # Distill Database information into a Python Dictionary
    # -----------------------------------------------------------------------------
    # Use .columns to get a list of all the column titles
    # I noticed that some "states" were inported as "nan" which is IEEE standard for "not
    # a number" and indicates that there is no information in the "state" column.
    # This could mean that the poll was for multiple states or a region rather than
    # an individual state. Either way, I want to remove these rows from the data.
    # See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html
    # for an exmplination of this line.
    # dropna removes rows with missing data
    # subset allows for only certian columns to be evaluated
    # inplace overwrites the object so I don't need to use
    # pollData=pollData.dropna(subset=['state'])
    pollData.dropna(subset=['state'], inplace=True)

    # Get all the states/localities
    localities = pollData["state"].unique()

    # sort the localities
    # sort() is a method of an numpy ndarray to sort in place
    localities.sort()

    # Get all the possible parties
    parties = pollData["candidate_party"].unique()

    # Initialize the storage dictionary
    pollDict = {}

    for eachLoc in localities:
        pollDict[eachLoc] = {}
        for eachParty in parties:
            pollDict[eachLoc][eachParty] = 0

    #%%
    # Average the results from each party in each state and store in pollDict
    for eachLoc in localities:
        for eachParty in parties:
            # print(eachLoc)
            # print(eachParty)
            partyValues = pollData[(pollData['state'] == eachLoc) & (pollData['candidate_party'] == eachParty)]
            if not partyValues.empty:
                pollDict[eachLoc][eachParty] = partyValues['pct'].mean()
                # I don't need an elif here because everything was initialized as zero
                # so if partyValues is empty it will just leave it as zero

    return pollDict


if __name__ == "__main__":
    results = getPollData(url=url)
    pprint(results)
