import sys

## Sorting function
## Not the best, but works for this purpose
def sorting(key):
    if key == 'S':
        # Anything is "greater" than 'S'
        return '0A'
    elif key == "I0":
        return '0B'
    elif key == 'E':
        return 'Z'
    else:
        suffix = key[1:]
        if key[0] == 'D':
            compar_key = str(len(suffix)) + str(suffix) + 'N'
            return compar_key
        elif key[0] == 'I':
            compar_key = str(len(suffix)) + str(suffix) + 'O'
            return compar_key
        compar_key = str(len(suffix)) + str(suffix) + key[0]
        return compar_key

o = open("output.txt", 'w')
sys.stdout = o

filename = sys.argv[1]
with open(filename) as f:
    # Max fraction of "insertions" per column
    theta = float(f.readline().strip())
    f.readline()
    alphabet = f.readline().split()
    f.readline()
    
    ## THIS SECTION: Convert alignment into
    ## rows/cols to make manipulations easier
    # Stores proteins
    row_list = list()
    curr_protein = f.readline().strip()
    col_num = 0
    row_num = 0
    cols_list = [list() for x in range(len(curr_protein))]
    while curr_protein:
        row_list.append(curr_protein)
        for i in range(len(curr_protein)):
            cols_list[col_num].append(curr_protein[col_num])
            col_num += 1
        col_num = 0
        row_num += 1
        curr_protein = f.readline().strip()

    # Make list of potential states
    potential_states = list()
    potential_states.append('S')
    potential_states.append('I0')
    for i in range(1, (len(cols_list)+1)):
        M_index = 'M' + str(i)
        D_index = 'D' + str(i)
        I_index = 'I' + str(i)
        potential_states.append(M_index)
        potential_states.append(D_index)
        potential_states.append(I_index)

    ## THIS SECTION: Convert each row in alignment into path
    # max_col will keep track of how many potential
    # states are actually used
    max_col = 'S'
    # Will optimize process by labeling cols as 'M' or 'I'
    # Keys will be the col indeces in cols_list
    col_dict = {}
    # Will help construct col_dict using first row
    curr_I_index = 0
    curr_M_index = 1
    # Variable to ensure that M indeces get increased correctly
    has_been_added = False
    for i in range(len(row_list[0])):
        curr_index = ''
        curr_col = cols_list[i]
        num_dashes = sum([1 for x in curr_col if x == '-'])
        col_ratio = float(num_dashes)/float(len(curr_col))
        if col_ratio > theta:
            # Column is an 'I'
            curr_index = 'I' + str(curr_I_index)
            col_dict[i] = curr_index
        else:
            has_been_added = False
            curr_index = 'M' + str(curr_M_index)
            col_dict[i] = curr_index
            # Update M and I indeces
            curr_I_index = curr_M_index
            curr_M_index += 1
        max_col = curr_index[1:]
    max_index = potential_states.index('I' + max_col) + 1
    del potential_states[max_index:]
    potential_states.append('E')

    # Stores each row as a path of states
    state_paths = list()
    # Dict will store all following edges from each state
    forward_edges = dict.fromkeys(potential_states)
    for row in row_list:
        state_paths.append(['S'])
        for i in range(len(row)):
            if row[i] != '-':
                curr_state = col_dict[i]
                if forward_edges[state_paths[-1][-1]] == None:
                    forward_edges[state_paths[-1][-1]] = [curr_state]
                else:
                    forward_edges[state_paths[-1][-1]].append(curr_state)
                state_paths[-1].append(curr_state)
            elif col_dict[i][0] == 'M':
                curr_state = 'D'+col_dict[i][1:]
                if forward_edges[state_paths[-1][-1]] == None:
                    forward_edges[state_paths[-1][-1]] = [curr_state]
                else:
                    forward_edges[state_paths[-1][-1]].append(curr_state)
                state_paths[-1].append(curr_state)
        if forward_edges[state_paths[-1][-1]] == None:
                forward_edges[state_paths[-1][-1]] = ['E']
        else:
                forward_edges[state_paths[-1][-1]].append('E')
        state_paths[-1].append('E')

    ## CONTRUCT TRANSITION MATRIX
    trans_matrix = list()
    for key in forward_edges:
        if forward_edges[key] == None:
            trans_matrix.append([key, [0 for x in range(len(potential_states))]])
        else:
            prob_list = list()
            for i in range(len(potential_states)):
                if potential_states[i] in forward_edges[key]:
                    prob_count = sum([1 for x in forward_edges[key] if x == potential_states[i]])
                    prob = prob_count/len(forward_edges[key])
                    prob_list.append(prob)
                else:
                    prob_list.append(0)
            trans_matrix.append([key, prob_list])
    trans_matrix.sort(key = lambda x: sorting(x[0]))
    
    ## PRINT TRANSITION MATRIX
    for state in potential_states:
        print('\t' + state, end = '')
    print('\n', end = '')
    for state in trans_matrix:
        print(state[0], end = '')
        for prob in state[1]:
            print('\t' + str(format(prob, '.3f')), end = '')
        print('\n', end = '')
                    
    print("--------")

    ## CONSTRUCT EMISSION MATRIX
    emission_matrix = list()
    # Create list of state that emit something
    emitting_states_dict = [list(item) for item in col_dict.items()]
    emitting_states_dict.sort(key = lambda x: x[0])
    emitting_states = [x[1] for x in emitting_states_dict]
    for state in potential_states:
        if not(state in emitting_states):
            emission_matrix.append([state, [0 for x in range(len(alphabet))]])
        elif emitting_states.count(state) == 1:
            prob_list = list()
            curr_index = emitting_states.index(state)
            curr_col = cols_list[curr_index]
            for letter in alphabet:
                if letter in curr_col:
                    letter_count = sum([1 for x in curr_col if x == letter])
                    tot_count = sum([1 for x in curr_col if x != '-'])
                    prob = letter_count/tot_count
                    prob_list.append(prob)
                else:
                    prob_list.append(0)
            emission_matrix.append([state, prob_list])
        else:
            state_count = emitting_states.count(state)
            prob_list = list()
            curr_indeces = [x for x in range(emitting_states.index(state), emitting_states.index(state)+state_count)]
            for letter in alphabet:
                letter_count = 0
                tot_count = 0
                for index in curr_indeces:
                    curr_col = cols_list[index]
                    tot_count += sum([1 for x in curr_col if x != '-'])
                    if letter in curr_col:
                        letter_count += sum([1 for x in curr_col if x == letter])
                prob = letter_count/tot_count
                prob_list.append(prob)
            emission_matrix.append([state, prob_list])
           
    emission_matrix.sort(key = lambda x: sorting(x[0]))

    ## PRINT EMISSION MATRIX
    for letter in alphabet:
        print('\t' + letter, end = '')
    print('\n', end = '')
    for state in emission_matrix:
        print(state[0], end = '')
        for prob in state[1]:
            print('\t' + str(format(prob, '.3f')), end = '')
        print('\n', end = '')
        
    
    
            
            

    
        
            
            
            
        
                
                
                
            
            
            
    
    

    
                
                
                
            
        
        
        

        
        
        
    
    
    
    
