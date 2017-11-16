from pattern_trie import pattern_trie
import sys

# Create trie for patterns
ptrie = pattern_trie()

o = open('output.txt','w')
sys.stdout = o

filename = sys.argv[1]
with open(filename) as f:
    # Get text line
    lines = f.readlines()
    text_line = list(lines[0].strip())
    lines = lines[1:]
    # Create pattern trie
    for line in lines:
        line = line.strip()
        pattern = list(line)
        pattern.reverse()
        ptrie.insert(0, pattern)

# Now, do matching
matches = list()
for i in range(0, len(text_line)):
    found = ptrie.match(0, text_line)
    if found:
        matches.append(i)
    text_line = text_line[1:]

for n in matches:
    print(str(n) + " ")



        
