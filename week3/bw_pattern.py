import sys

o = open("output.txt", 'w')
sys.stdout = o

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
    text = f.readline().strip()
    BW_transform_list = list(text)

    # Stores number of each char in string
    text_chars = {}
    # Stores indeces for each letter
    index_dict = {}
    for char in BW_transform_list:
        if char in text_chars:
            text_chars[char] += 1
        else:
            text_chars[char] = 1
        if char in index_dict:
            index_dict[char].append(BW_transform_list.index(char))
        else:
            index_dict[char] = [BW_transform_list.index(char)]
        BW_transform_list[BW_transform_list.index(char)] = str(char) + str(text_chars[char])
    BW_col1 = sorted(BW_transform_list, key = sorting)
    BW_transform = {}
    for i in range(len(BW_transform_list)):
        BW_transform[BW_transform_list[i]] = i

    ## Manipulation that might optimize pattern search
    char_list = [[k, 0, v] for k,v in text_chars.items()]
    char_list.sort(key = lambda x: x[0])
    for i in range(1,len(char_list)):
        char_list[i][1] = char_list[i-1][2]
        char_list[i][2] += char_list[i-1][2]
    char_dict = {}
    for i in range(len(char_list)):
        char_dict[char_list[i][0]] = [char_list[i][1], char_list[i][2]]

    ## PATTERN STUFF
    # Stores number of occurrences of each pattern
    pattern_counts = list()
    patterns = f.read().split()
    #print(patterns)
    while len(patterns) > 0:
        #print(len(patterns))
        #print(pattern_counts)
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
            curr_count += sum([find_pattern(BW_col1, BW_transform, x, curr_pattern_list[1:]) for x in reduced_indeces])
            #print(curr_count)
        pattern_counts.append(curr_count)
        del patterns[0]

    # pattern_counts printing stuff
    print_str = ''
    for i in range(len(pattern_counts) - 1):
        print_str += str(pattern_counts[i]) + ' '
    print_str += str(pattern_counts[-1])
    print(print_str)
        
        






