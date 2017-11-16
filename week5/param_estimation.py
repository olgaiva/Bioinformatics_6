import sys
import math

o = open("output.txt", 'w')
sys.stdout = o

filename = sys.argv[1]
with open(filename) as f:
    obs_path = f.readline().strip()
    f.readline()
    alphabet = f.readline().split()
    f.readline()
    hid_path = f.readline().strip()
    f.readline()
    hid_states = f.readline().split()

    ## COUNT TRANSITIONS
    tot_transitions = [0 for x in hid_states]
    transitions = [dict.fromkeys(hid_states, 0) for x in hid_states]
    prev_state = ''
    for state in hid_path:
        if prev_state:
            prev_state_index = hid_states.index(prev_state)
            tot_transitions[prev_state_index] += 1
            transitions[prev_state_index][state] += 1
        prev_state = state

    ## SET UP TRANSITION MATRIX
    transition_matrix = list()
    for i in range(len(hid_states)):
        state = hid_states[i]
        prob_list = [0 for x in hid_states]
        # Check if a state has no transitions
        if set(transitions[i].values()) == {0}:
            prob = 1/len(hid_states)
            prob_list = [prob for x in hid_states]
        else:
            for key in transitions[i]:
                key_index = hid_states.index(key)
                prob = transitions[i][key]/tot_transitions[i]
                prob_list[key_index] += prob
        transition_matrix.append([state, prob_list])

    ## PRINT TRANSITION MATRIX
    for state in hid_states:
        print('\t' + state, end = '')
    print('\n', end = '')
    for state in transition_matrix:
        print(state[0], end = '')
        for prob in state[1]:
            print('\t' + str(format(prob, '.3f')), end = '')
        print('\n', end = '')              
    print("--------")

     ## COUNT EMISSIONS
    tot_emissions = [0 for x in hid_states]
    emissions = [dict.fromkeys(alphabet, 0) for x in hid_states]
    for i in range(len(hid_path)):
        state = hid_path[i]
        state_index = hid_states.index(state)
        tot_emissions[state_index] += 1
        emissions[state_index][obs_path[i]] += 1

    ## SET UP EMISSION MATRIX
    emission_matrix = list()
    for i in range(len(hid_states)):
        state = hid_states[i]
        prob_list = [0 for x in alphabet]
        # Check if a state has no emissions
        if set(emissions[i].values()) == {0}:
            prob = 1/len(alphabet)
            prob_list = [prob for x in alphabet]
        else:
            for key in emissions[i]:
                key_index = alphabet.index(key)
                prob = emissions[i][key]/tot_emissions[i]
                prob_list[key_index] += prob
        emission_matrix.append([state, prob_list])

    ## PRINT EMISSION MATRIX
    for state in alphabet:
        print('\t' + state, end = '')
    print('\n', end = '')
    for state in emission_matrix:
        print(state[0], end = '')
        for prob in state[1]:
            print('\t' + str(format(prob, '.3f')), end = '')
        print('\n', end = '')              

        

    
            
        
    
            
        
    
