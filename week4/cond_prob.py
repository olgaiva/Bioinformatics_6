import sys

o = open("output.txt", 'w')
#sys.stdout = o

filename = sys.argv[1]
with open(filename) as f:
    # Observed path
    obs_path = f.readline().strip()
    f.readline()
    obs_state_list = f.readline().split()
    print(obs_state_list)
    f.readline()
    # Hidden path
    hid_path = f.readline().strip()
    f.readline()
    hid_state_list = f.readline().split()
    f.readline()
    # Skipping this line too, because the states
    # should be in the same order in the matrix
    f.readline()
    cond_dict = {}
    curr_line = f.readline().split()
    while len(curr_line) != 0:
        curr_char = curr_line[0]
        cond_dict[curr_char] = list(map(float, curr_line[1:]))
        curr_line = f.readline().split()
    print(cond_dict)
    
    # Vector that stores transition probabilities
    total_prob = 1
    for i in range(len(hid_path)):
        curr_state = hid_path[i]
        obs_state = obs_state_list.index(obs_path[i])
        curr_prob = cond_dict[curr_state][obs_state]
        total_prob *= curr_prob
    print(str(total_prob))
