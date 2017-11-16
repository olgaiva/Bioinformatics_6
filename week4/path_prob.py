import sys

o = open("output.txt", 'w')
#sys.stdout = o

filename = sys.argv[1]
with open(filename) as f:
    path = f.readline().strip()
    f.readline()
    state_list = f.readline().split()
    print(state_list)
    f.readline()
    # Skipping this line too, because the states
    # should be in the same order in the matrix
    f.readline()
    transition_dict = {}
    curr_line = f.readline().split()
    while len(curr_line) != 0:
        curr_char = curr_line[0]
        transition_dict[curr_char] = list(map(float, curr_line[1:]))
        curr_line = f.readline().split()
    print(transition_dict)
    
    # Vector that stores transition probabilities
    total_prob = 0.5
    for i in range(len(path)-1):
        curr_state = path[i]
        next_state = state_list.index(path[i+1])
        curr_prob = transition_dict[curr_state][next_state]
        total_prob *= curr_prob
    print(str(total_prob))
    
        
        
    
