"""
Function for determining the 2020 US Election
"""

from state_data_2020 import electoral_college, nomineePartyMap  # Pull in Electoral College Data
from collections import OrderedDict

def ec_result(state_results):
    """Calculate Winner.

    Given per state determination, provide the election result
    Args:
        state_results (dict): Results for each state, by state name.
    Returns:
        Total Electoral Votes for each candidate
    """
    ec = electoral_college
    results = {}
    for state in state_results.keys():
        winner = state_results[state]
        if winner in results.keys():
            results[winner] += ec[state]
        else:
            results[winner] = ec[state]
    # Now we could sort it
    results = OrderedDict(sorted(results.items(), key=lambda t: -t[1]))
    return results

def state_raw2win(pollData):
    """Convert Raw State Data to Winner for each state/district"""
    state_results = {}
    for state, sdata in pollData.items():
        winparty = max(sdata, key=sdata.get)
        state_results[state] = nomineePartyMap[winparty]
    return state_results

if __name__ == "__main__":
    candidates_2020 = ["Biden, Joe", "Hawkins, Howie", "Jorgensen, Jo", "Trump, Donald"]
    state_results = {}
    print("For each state, enter the first letter of the candidate last name.\n Or a full name for a write-in.")
    for state in electoral_college:
        # Here I loop through each state in the electoral college.
        redo = True
        # We're going to loop if bad import is provided.
        while redo:
            # The state key also is used for the results dictionary
            state_results[state] = str(input("Provide result for " + state + ": "))
            # Store the candidates to match the input.
            lowercandidates = [str(x[:len(state_results[state])]).lower() for x in candidates_2020]
            if state_results[state].lower() not in lowercandidates:
                print("Your entry is not in the 2020 Candidate List.")
                print(candidates_2020)
                c = str(input("Your entry is not in the 2020 Candidate List.  Would you like to re-enter? (Y/N)"))
                if c[0].lower() == "n":
                    # If the user wanted to add a candidate, we can add it to the list.
                    candidates_2020.append(state_results[state])
                    lowercandidates = [str(x[:len(state_results[state])]).lower() for x in candidates_2020]
                else:
                    # Else, we continue to loop again.
                    continue
            # Make sure we store the state's candidate in the correct format.
            state_results[state] = candidates_2020[lowercandidates.index(state_results[state].lower())]
            redo = False  # Break the loop if we like the input.

    results = ec_result(state_results)
    r = iter(results)
    if results[next(r)] == results[next(r)]:
        print("Uh Oh, we have a tie.")
    else:
        print("It looks like next year's US President will be {}.".format(next(iter(results))))
    print(results)

