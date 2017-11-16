import sys
import math

o = open("output.txt", 'w')
#sys.stdout = o

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


    ## VITERBI ALGORITHM
    ## PSEUDOCODE (FOR NOW)
    # Have values for each hidden state: (A,B,C)
    # These values will be the SCORES for each state
    max_vals = [cond_dict[x][obs_state_list.index(obs_path[0])] for x in hid_state_list]
    max_paths = [[x] for x in hid_state_list]
    for i in range(1,len(obs_path)):
        curr_obs_ind = obs_state_list.index(obs_path[i])
        new_max_paths = [[],[]]
        new_max_vals = [0, 0]
        for state in hid_state_list:
            copy_max_paths = [x for x in max_paths]
            emission_prob = cond_dict[state][curr_obs_ind]
            trans_probs = list(map(lambda u: transition_dict[u[-1]][hid_state_list.index(state)], max_paths))
            all_vals = list(map(lambda u, v, w: u*v*w, max_vals, trans_probs, [emission_prob for x in range(len(max_vals))]))
            best_val = max(all_vals)
            best_choice = all_vals.index(best_val)
            best_path = [x for x in copy_max_paths[best_choice]]
            best_path.append(state)
            new_max_paths[hid_state_list.index(state)] = best_path
            new_max_vals[hid_state_list.index(state)] = best_val
        max_paths = new_max_paths
        max_vals = new_max_vals
        #print(max_vals)
        #print(max_paths)
    viterbi_val = max(max_vals)
    viterbi_path = max_paths[max_vals.index(viterbi_val)]
    print_str = ''
    for i in viterbi_path:
        print_str += i
    print(print_str)
            
            
            
            
            
            
            
        
        
