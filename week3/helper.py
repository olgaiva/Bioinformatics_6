import sys

o = open("input.txt", 'w')
#sys.stdout = o

filename = sys.argv[1]
with open(filename) as f:
    ## TEXT STUFF
    text = f.readline()
    print(text)
    len_chunk = 2
    substrings = dict()
    while len_chunk < len(text):
        for i in range(len(text)):
            if i + len_chunk < len(text):
                text_chunk = text[i:i+len_chunk]
                print(text_chunk)
                if not(text_chunk in substrings):
                    substrings[text_chunk] = 1
                else:
                    substrings[text_chunk] += 1
            else:
                break
        len_chunk += 1

    max_len = 0
    max_string = ''
    for substring in substrings:
        if substrings[substring] > 1:
            if len(substring) > max_len:
                max_len = len(substring)
                max_string = substring
    print(max_string)
