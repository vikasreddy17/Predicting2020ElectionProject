import pandas as pd

from main import basic_election_prediction
from getData import getPollData
from us_electoral import ec_result, state_raw2win
from state_data_2020 import electoral_college, nomineePartyMap


def results_to_data_table():
    simulation_results = pd.read_csv("simulation_results.csv")
    actual_voting_data = pd.read_csv("Actual Election Results - NBC - Sheet1.csv")
    raw_state_data = getPollData()
    state_number = 0

    results_dictionary = {'State': [], 'Abbreviation': [], 'Pred_Dem_Votes': [], 'Act_Dem_Votes': [],'Dem_Percent_Error': [], 'Pred_Rep_Votes': [], 'Act_Rep_Votes': [], 'Rep_Percent_Error': [], 'Predicted_Winner': [], 'Correct': []}

    stat_abb_list = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", 
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "ME-1", "ME-2", "MD", 
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NE-1", "NE-2", "NV", "NH", "NJ", 
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    for state_abb in stat_abb_list:
        results_dictionary['Abbreviation'].append(state_abb)


    for state in raw_state_data.keys():
        sim_dem_prediction = int(simulation_results.at[0, state])
        sim_rep_prediction = int(simulation_results.at[1, state])
        actual_dem = actual_voting_data.at[state_number, 'Biden']
        actual_rep = actual_voting_data.at[state_number, 'Trump']
    
        if (sim_dem_prediction > sim_rep_prediction):
            winner = 'Biden'
        else:
            winner = 'Trump'
    
        DEM_Percent_Error = abs((sim_dem_prediction - actual_dem)/actual_dem)*100
        REP_Percent_Error = abs((sim_rep_prediction - actual_rep)/actual_rep)*100
    
        results_dictionary['State'].append(state)
        results_dictionary['Pred_Dem_Votes'].append(sim_dem_prediction)
        results_dictionary['Act_Dem_Votes'].append(actual_dem)
        results_dictionary['Pred_Rep_Votes'].append(sim_rep_prediction)
        results_dictionary['Act_Rep_Votes'].append(actual_rep)
        results_dictionary['Predicted_Winner'].append(winner)
    
        results_dictionary['Dem_Percent_Error'].append(DEM_Percent_Error)
        results_dictionary['Rep_Percent_Error'].append(REP_Percent_Error)
        if (sim_dem_prediction > sim_rep_prediction) and (actual_dem > actual_rep):
            results_dictionary['Correct'].append(True)
        elif (sim_rep_prediction > sim_dem_prediction) and (actual_rep > actual_dem):
            results_dictionary['Correct'].append(True)
        else:
            results_dictionary['Correct'].append(False)
        state_number += 1
    
    results_dictionary = pd.DataFrame(results_dictionary)
    results_dictionary.to_csv("simulation_analysis.csv")
    return pd.DataFrame(results_dictionary)

results_to_data_table()
