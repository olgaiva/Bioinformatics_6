import sys

# I/O stuff
o = open('output.txt','w')
sys.stdout = o

graph = {}

filename = sys.argv[1]
with open(filename) as f:
    lines = f.readlines()
    for line in lines:
        line_list = line.split(" -> ")
        node = int(line_list[0])
        connected_nodes = line_list[1].split(',')
        connected_nodes = list(map(int, connected_nodes))
        graph[node] = connected_nodes

n1_to_1 = list() # list of nodes that are not 1-to-1
is1_to_1 = list()
end_nodes = list()

for key in graph.keys():
    # If there is not exactly 1 outgoing connection
    if len(graph[key]) != 1:
        n1_to_1.append(key)

    else:
        found_key = 0
        for value in graph.values():
            if key in value:
                found_key += 1
        if found_key != 1:
            n1_to_1.append(key)
        else:
            is1_to_1.append(key)

# find end nodes
for value in graph.values():
    for node in value:
        if (not(node in n1_to_1)) & (not(node in is1_to_1)):
            end_nodes.append(node)

# Helper function to find non-branching paths
def non_branching_path(graph, is1_to_1, used1_to_1, node, paths, curr_path):
    for child_node in graph[node]:
        new_ext = list(curr_path)
        if not(node in new_ext):
            new_ext.append(node)
        new_ext.append(child_node)
        if child_node in is1_to_1:
            used1_to_1.append(child_node)
            non_branching_path(graph, is1_to_1, used1_to_1, child_node, paths, new_ext)
        else:
            paths.append(new_ext)

def isolated_cycle(graph, is1_to_1, node, paths, curr_path):
    for child_node in graph[node]:
        new_ext = list(curr_path)
        if not(node in new_ext):
            new_ext.append(node)
        new_ext.append(child_node)
        if child_node == new_ext[0]:
            paths.append(new_ext)
        elif (child_node in is1_to_1):
            isolated_cycle(graph, is1_to_1, child_node, paths, new_ext)

# Now, time to start algorithm
paths = list()
used1_to_1 = list()

for node in n1_to_1:
    non_branching_path(graph, is1_to_1, used1_to_1, node, paths, [])

unused1_to_1 = list(set(is1_to_1) - set(used1_to_1))
if len(unused1_to_1) > 0:
    unused1_to_1.sort()
    for node in unused1_to_1:
        isolated_cycle(graph, unused1_to_1, node, paths, [])
        unused1_to_1 = list(set(unused1_to_1) - set(paths[-1]))


# print paths
for path in paths:
    path_string = ""
    for i in range(len(path) - 1):
        path_string += str(path[i]) + " -> "
    path_string += str(path[-1])
    print(path_string)
            
        

    
    
    
