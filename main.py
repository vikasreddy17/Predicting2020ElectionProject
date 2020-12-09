"""
This python script will use various functions to provide predictive information about 2020 Presedential Winners
"""

from pprint import pprint

from getData import getPollData
from us_electoral import ec_result, state_raw2win


def basic_election_prediction(pollData):
    # Convert raw results to a winner by state
    state_results = state_raw2win(pollData)
    # Return the winner (First entry) from the ordered dict from the ec_result function
    winner2020 = next(iter(ec_result(state_results)))
    return(winner2020)
    
if __name__ == "__main__":
    basic_election_prediction()
    

