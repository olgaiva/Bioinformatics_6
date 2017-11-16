import sys

class suffix_trie:
    def __init__(self, text):
        self.count = 1
        self.nodes = list()
        self.nodes.append(list())
        self.text = text
        self.edges = list()
        self.longest_edge = ""
        
    def insert(self, num, t_ind):
        # Insert suffix as the final node
        # To save space, suffix might be an index to the original string?
        if t_ind < len(self.text):
            # "pop off" the first letter
            letter = self.text[t_ind]
            found = False
            for edge in self.nodes[num]:
                if letter == self.text[edge[0]]:
                    self.insert(edge[1], t_ind + 1)
                    found = True
            # if no edge was found
            if found == False:
                new_edge = [t_ind, self.count] 
                self.nodes[num].append(new_edge)
                self.nodes.append(list())
                self.count += 1
                self.insert(new_edge[1], t_ind + 1)


    def print_edges(self, num, curr_edge): # curr_edge has what is already on edge
        if not(self.nodes[num]):
            print(curr_edge)
            return
        if len(self.nodes[num]) == 1:
            # Will be part of same edge
            curr_edge += self.text[self.nodes[num][0][0]]
            self.print_edges(self.nodes[num][0][1], curr_edge)
        else:
            # Build string to print current edge
            print(curr_edge)
            for node in self.nodes[num]:
                self.print_edges(node[1], self.text[node[0]])

# I/O stuff
o = open('output.txt','w')
sys.stdout = o

sys.setrecursionlimit(1500)
                
filename = sys.argv[1]
with open(filename) as f:
    text = f.readline().strip()
    s_tree = suffix_trie(text)
    for i in range(len(text)):
        s_tree.insert(0, i)
    s_tree.print_edges(0, "")
            
            
            
                
        
