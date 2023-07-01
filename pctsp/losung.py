class Node(object):
    def __init__(self, ind, prize, penalty):
        self.ind = ind
        self.prize = prize 
        self.penalty = penalty 
        self.visited = False

    def __iter__(self):
        return iter(self)

    def __str__(self):
        return "Node index: %s \n Node prize: %s \n Node penalty: %s \n Node visted %s \n" % (self.ind, self.prize, self.penalty, self.vistied)
    
    def __repr__(self):
        return "Node index: %s \n Node prize: %s \n Node penalty: %s \n Node visted %s \n" % (self.ind, self.prize, self.penalty, self.vistied)

    def __len__(self):
        return self.length

    def getPrize(self):
        return self.prize

    def getPenalty(self):
        return self.penalty
    
    def isVisted(self):
        return self.visited


class Edge(object):
    def __init__(self, ind, prize, penalty):
        self.ind = ind
        self.prize = prize 
        self.penalty = penalty 
        self.visited = False

    def __iter__(self):
        return iter(self)

    def __str__(self):
        return "Node index: %s \n Node prize: %s \n Node penalty: %s \n Node visted %s \n" % (self.ind, self.prize, self.penalty, self.vistied)
    
    def __repr__(self):
        return "Node index: %s \n Node prize: %s \n Node penalty: %s \n Node visted %s \n" % (self.ind, self.prize, self.penalty, self.vistied)

    def __len__(self):
        return self.length

    def __eq__(self, other):
        if self.number != other.number:
            return False
        else:
            return True

    def getPrize(self):
        return self.prize

    def getPenalty(self):
        return self.penalty
    
    def isVisted(self):
        return self.visited
