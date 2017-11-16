import sys

o = open("output.txt", 'w')
sys.stdout = o

# Returns a rotated string
def cyclic_rotation(index, text):
# Will take chars in positions 0-index,
# and and append them to the end of the string
    new_suff = text[:index]
    new_pref = text[index:]
    rotated_str = new_pref + new_suff
    return(rotated_str)
    

filename = sys.argv[1]
with open(filename) as f:
    BW_matrix = list()
    text = f.readline().strip()
    
    for i in range(len(text)):
        BW_matrix.append([cyclic_rotation(i, text), i])
    BW_matrix.sort(key = lambda x: x[0])

    

    # This is printing stuff
    print_str = ""
    for i in range(len(BW_matrix)):
        print_str += str(BW_matrix[i][1]) + ' '
    print(print_str)
        
