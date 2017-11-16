import sys

class color_tree:
    def __init__(self, num): # num is number of nodes
        self.nodes = [["gray", list()] for i in range(num)]
        self.uncolored = num
        
    def connect(self, node, connected): # no need to insert
        # Only nodes that have connections will be passed here
        self.nodes[node][1] = connected
            
    def color_leaf(self, node, color):
        self.nodes[node][0] = color
        self.uncolored -= 1

    def color(self):
        while self.uncolored > 0:
            # Look for "ripe" nodes
            for node in self.nodes:
                if node[0] == "gray":
                    child_colors = self.check_color(node[1])
                    if child_colors and len(child_colors) == 1:
                        node[0] = child_colors[0]
                        self.uncolored -= 1
                    elif child_colors and len(child_colors) > 1:
                        node[0] = "purple"
                        self.uncolored -= 1
        
                
    def check_color(self, node_list):
        # Given list of nodes, return list of colors if "ripe"
        color_list = list()
        for node in node_list:
            child_color = self.nodes[node][0]
            if child_color == "gray":
                return(list())
            else:
                if not(child_color in color_list):
                    color_list.append(child_color)
        return color_list


# I/O stuff
o = open('output.txt','w')
sys.stdout = o



filename = sys.argv[1]
with open(filename) as f:
    # First read list of connected nodes
    connected_nodes = list()
    line = f.readline().strip()
    while line[0] != '-':
        line_list = line.split("->")
        node = int(line_list[0])
        connected = line_list[1].strip().split(",")
        if connected[0] == "{}":
            connected = list()
        else:
            connected = list(map(int, connected))
        node_list = [node, connected]
        connected_nodes.append(node_list)
        line = f.readline().strip()

    ctree = color_tree(len(connected_nodes))
    for node in connected_nodes:
        ctree.connect(node[0], node[1])

    # Now, color the leaves
    leaf_nodes = list()
    line = f.readline().strip()
    while line:
        line_list = line.split(':')
        node = int(line_list[0])
        line_list[1] = line_list[1].strip()
        ctree.color_leaf(node, line_list[1])
        line = f.readline().strip()

ctree.color()
for i in range(len(ctree.nodes)):
    print(str(i) + ': ' + ctree.nodes[i][0]) 
        
        
        
        
        
        
        
    
    


            
