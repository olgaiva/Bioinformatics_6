class pattern_trie:
    def __init__(self):
        self.count = 1
        self.nodes = list()
        self.nodes.append(list())
        
    def insert(self, num, pattern):
        # pop off the first letter
        if not pattern:
            return
        letter = pattern.pop()
        for edge in self.nodes[num]:
            if letter == edge[0]:
                self.insert(edge[1], pattern)
                return
        # if no edge was found
        new_edge = [letter, self.count]
        self.nodes[num].append(new_edge)
        self.nodes.append(list())
        self.count += 1
        self.insert(new_edge[1], pattern)
        return

    # returns y/n if string at first position exists
    def match(self, num, text):
        if len(self.nodes[num]) == 0:
            return True
        elif not text:
            return False
        # If last char of pattern was reached
        letter = text[0]
        for edge in self.nodes[num]:
            if letter == edge[0]:
                return self.match(edge[1], text[1:])
        # If no matching chars were found
        return False

