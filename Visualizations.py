import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from main import basic_election_prediction
from getData import getPollData
from us_electoral import ec_result, state_raw2win
from state_data_2020 import electoral_college, nomineePartyMap

def create_percent_error_bar_chart():
    simulation_analysis = pd.read_csv("simulation_analysis.csv")

    simulation_analysis_trump = simulation_analysis[['Pred_Rep_Votes', 'Act_Rep_Votes', 'Rep_Percent_Error']]
    simulation_analysis_biden = simulation_analysis[['Pred_Dem_Votes', 'Act_Dem_Votes', 'Dem_Percent_Error']]

    labels = simulation_analysis['Abbreviation']
    percent_error_trump = simulation_analysis['Rep_Percent_Error']
    percent_error_biden = simulation_analysis['Dem_Percent_Error']

    x = np.arange(len(labels))
    width = 0.35
    empty_list = []
              
    fig = plt.figure(figsize=(30,10))
    ax = fig.add_subplot(111)
    ax.bar(x - width/2, percent_error_trump, width, label='Trump', tick_label=labels)
    ax.bar(x + width/2, percent_error_biden, width, label='Biden', tick_label=labels):
    plt.legend(loc='upper left')
    plt.title('Percent Error for Simulation Predicted Voted by Party', fontsize=30)
    plt.xlabel('State', fontsize=17)
    plt.ylabel('Percent Error (%)', fontsize=17)
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)

    plt.savefig('Percent_Error_Bar_Chart.png')


create_percent_error_bar_chart()