import random
import pandas as pd

from main import basic_election_prediction
from getData import getPollData
from us_electoral import ec_result, state_raw2win
from state_data_2020 import electoral_college, nomineePartyMap

data_source_1 = 'https://www.270towin.com/2020-polls-biden-trump/'
data_source_2 = 'http://www.electproject.org/2020g'
data_source_3 = 'https://www.nbcnews.com/politics/2020-election?icid=election_nav'

def simulation():
    voter_turnout_data = pd.read_csv("2020 November General Election - Turnout Rates.csv")
    raw_state_data = getPollData()
    simulation_results = {}
    state_number = 1
    for state in raw_state_data.keys():
        temporary_state_dictionary = raw_state_data[state]
    
        party_list = []
        party_thresholds = {'DEM': 0, 'REP': 0, 'LIB': 0, 'GRE': 0, 'IND': 0, 'CON': 0, 'OTH': 0, 'PSL': 0, 'SWP': 0}
        party_sim_tally = {'DEM': 0, 'REP': 0, 'LIB': 0, 'GRE': 1, 'IND': 0, 'CON': 0, 'OTH': 0, 'PSL': 0, 'SWP': 0}
        for party in temporary_state_dictionary.keys():
            party_list.append(party)
            for sum_party in party_list:
                old = party_thresholds[party]
                add = temporary_state_dictionary[sum_party]
                party_thresholds[party] = old + add
                sum_percents = party_thresholds[party]
    
        voting_population_of_state = voter_turnout_data.at[state_number,'Estimated_Vote']
        voting_population_of_state = int(voting_population_of_state)
    
        for i in range(voting_population_of_state):
            random_number = random.uniform(0, sum_percents)
            for party_sim in party_thresholds:
                if party_thresholds[party_sim] > random_number:
                    party_sim_tally[party_sim] += 1
        party_list1 = []
        new_party_sim_tally = party_sim_tally
        for party in temporary_state_dictionary.keys():
            for minus_party in party_list1:
                new_party_sim_tally[party] = party_sim_tally[party] - party_sim_tally[minus_party]
            party_list1.append(party)
        simulation_results[state] = new_party_sim_tally
        state_number += 1
        print(state + " simulation is done!")

    print("*"*30)
    print(basic_election_prediction(simulation_results))
    print("*"*30)

    simulation_results = pd.DataFrame(simulation_results)
    simulation_results.to_csv("simulation_results.csv")
    
simulation()