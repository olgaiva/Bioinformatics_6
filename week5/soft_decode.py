import sys
import math
import itertools

o = open("output.txt", 'w')
sys.stdout = o
        

filename = sys.argv[1]
with open(filename) as f:
    # Observed path
    obs_path = f.readline().strip()
    f.readline()
    obs_state_list = f.readline().split()
    f.readline()
    # Hidden states
    hid_state_list = f.readline().split()
    f.readline()
    # Skipping this line too, because the states
    # should be in the same order in the matrix
    f.readline()
    ## TRANSITIONS BETWEEN HIDDEN STATES
    transition_dict = {}
    curr_line = f.readline().split()
    while len(curr_line) != 1:
        curr_char = curr_line[0]
        transition_dict[curr_char] = list(map(float, curr_line[1:]))
        curr_line = f.readline().split()
    
    # Skipping this line too, because the states
    # should be in the same order in the matrix
    f.readline()
    ## EMISSION PROBABILITIES, GIVEN STATE
    cond_dict = {}
    curr_line = f.readline().split()
    while len(curr_line) != 0:
        curr_char = curr_line[0]
        cond_dict[curr_char] = list(map(float, curr_line[1:]))
        curr_line = f.readline().split()

    ## Cartesian product to give all possible paths
    all_paths = itertools.product(*[hid_state_list for x in obs_path])
    path_values = list()
    sum_path_values = 0
    path_probs = dict((hid_state, [0 for x in obs_path]) for hid_state in hid_state_list) 

    ## Calculate values for all possible paths
    for path in all_paths:
        value = 1
        for i in range(len(path)):
            curr_state = path[i]
            letter = obs_path[i]
            letter_index = obs_state_list.index(letter)
            emission_prob = cond_dict[curr_state][letter_index]
            value *= emission_prob
            if i < len(path) - 1:
                next_state = path[i+1]
                state_index = hid_state_list.index(next_state)
                trans_prob = transition_dict[curr_state][state_index]
                value *= trans_prob
        for i in range(len(path)):
            curr_state = path[i]
            path_probs[curr_state][i] += value
        path_values.append(value)
        sum_path_values += value

    
    ## Print
    for hid_state in hid_state_list:
        print(hid_state + '\t', end = '')
    print('\n', end = '')
    for i in range(len(obs_path)):
        for hid_state in hid_state_list:
            prob = path_probs[hid_state][i]/sum_path_values
            print(str(format(prob, '.4f')), end = '\t')
        print('\n', end = '')
        
    
        
    
