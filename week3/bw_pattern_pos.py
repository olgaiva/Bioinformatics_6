import sys

o = open("output.txt", 'w')
#sys.stdout = o

## To provide to sorted function
def sorting(char):
    suffix = char[1:]
    compar_key = char[0] + str(len(suffix)) + str(suffix)
    return compar_key

## Function which returns 0 if pattern not found,
## 1 if found
## start_pos gives position of first char in pattern
def find_pattern(col1, transform, start_pos, pattern_list):
    while len(pattern_list) > 1:
        #print(len(pattern_list))
        next_char = col1[start_pos]
        #print(next_char[0] + " " + pattern_list[0])
        if next_char[0] != pattern_list[0]:
            return 0
        else:
            start_pos = transform[next_char]
            del pattern_list[0]
    next_char = col1[start_pos]
    if next_char[0] != pattern_list[0]:
        return 0
    return 1

filename = sys.argv[1]
with open(filename) as f:
    ## TEXT STUFF
    # Create BW Transform
    text = f.readline().strip() + '$'
    # Stores number of each char in string
    numbered_text = list(text)
    text_chars = {}
    # Hash of original text
    orig_text = {}
    for i in range(len(numbered_text)):
        if numbered_text[i] in text_chars:
            text_chars[numbered_text[i]] += 1
            numbered_text[i] = numbered_text[i] + str(text_chars[numbered_text[i]])
        else:
            text_chars[numbered_text[i]] = 1
            numbered_text[i] = numbered_text[i] + str(1)
        orig_text[numbered_text[i]] = i

    # Create list of adjacent pairs
    adj_pairs = [[numbered_text[i+1], numbered_text[i]] for i in range(len(numbered_text)-1)]
    adj_pairs.append([numbered_text[0], numbered_text[-1]])
    # This sorting should create the partial matrix
    adj_pairs.sort(key = lambda x: sorting(x[0]))
    BW_col1 = list(map(lambda x: x[0], adj_pairs))
    BW_transform_list = list(map(lambda x: x[1], adj_pairs))
    print(BW_transform_list)
    
    # Stores indeces IN BW_TRANSFORM for each letter
    index_dict = {}
    BW_transform = {}
    for i in range(len(BW_transform_list)):
        char = BW_transform_list[i][0]
        if char in index_dict:
            index_dict[char].append(i)
        else:
            index_dict[char] = [i]
        BW_transform[BW_transform_list[i]] = i

    ## MANIPULATION THAT OPTIMIZES PATTERN SEARCH
    char_list = [[k, 0, v] for k,v in text_chars.items()]
    char_list.sort(key = lambda x: x[0])
    for i in range(1,len(char_list)):
        char_list[i][1] = char_list[i-1][2]
        char_list[i][2] += char_list[i-1][2]
    char_dict = {}
    for i in range(len(char_list)):
        char_dict[char_list[i][0]] = [char_list[i][1], char_list[i][2]]

    ## PATTERN STUFF
    # Stores indeces of each found pattern
    pattern_indeces = list()
    patterns = f.read().split('\n')
    #print(patterns)
    while len(patterns) > 0:
        #print(len(patterns))
        #print(pattern_indeces)
        curr_pattern_list = list(patterns[0])
        curr_count = 0

        curr_char = curr_pattern_list[0]
        next_char = curr_pattern_list[1]
        next_char2 = curr_pattern_list[2]
        lo_index = char_dict[next_char][0]
        hi_index = char_dict[next_char][1]
        
        if curr_char in index_dict:
            # Use list comprehension to cut down the indeces
            reduced_indeces = [x for x in index_dict[curr_char] if x in range(lo_index, hi_index)]
            #print(reduced_indeces)
            for x in reduced_indeces:
                if find_pattern(BW_col1, BW_transform, x, curr_pattern_list[1:]) > 0:
                    pattern_indeces.append(orig_text[BW_transform_list[x]])
        del patterns[0]

    # pattern_counts printing stuff
    print_str = ''
    for i in range(len(pattern_indeces) - 1):
        print_str += str(pattern_indeces[i]) + ' '
    print_str += str(pattern_indeces[-1])
    print(print_str)
        
        






