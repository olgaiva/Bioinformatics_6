import sys

o = open("output.txt", 'w')
#sys.stdout = o

# To provide to sorted function
def sorting(char):
    suffix = char[1:]
    compar_key = char[0] + str(len(suffix)) + str(suffix)
    return compar_key

filename = sys.argv[1]
with open(filename) as f:
    text = f.read().strip()
    BW_transform = list(text)

    # Stores number of each char in string
    text_chars = {}
    for char in BW_transform:
        if char in text_chars:
            text_chars[char] += 1
        else:
            text_chars[char] = 1
        BW_transform[BW_transform.index(char)] = str(char) + str(text_chars[char])
    BW_col1 = sorted(BW_transform, key = sorting)

    # Place the two strings side-by-side
    curr_letter = "$1"
    # This will be the (formatted) original sequence
    orig_list = list()
    end = False
            
    while not end:
        #print(len(orig_list))
        #print(len(BW_col1))
        for i in range(len(BW_transform)):
            if BW_transform[i] == curr_letter:
                if BW_col1[i] == "$1":
                    end = True
                curr_letter = BW_col1[i]
                orig_list.append(curr_letter)
                break

    # List must now be reformatted as the original string
    orig_string = ''
    for char in orig_list:
        orig_string += str(char[0])
    print(orig_string)
          

##with open("sample_output.txt") as s_o:
##    sample_output = s_o.read().strip()
##
##    maxlen=len(sample_output) if len(orig_string)<len(sample_output) else len(orig_string)
##    for i in range(maxlen):
##        #use a slice rather than index in case one string longer than other
##        letter1=orig_string[i:i+1]
##        letter2=sample_output[i:i+1]
##        #create string with differences
##        if letter1 != letter2:
##            print("first index difference: " + str(i))
##            break
    

    
