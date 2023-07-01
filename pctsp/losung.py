import sys
from typing import Tuple, List
class Node(object):
    def __init__(self, ind, prize, penalty):
        self.ind = ind
        self.prize = prize 
        self.penalty = penalty 
        self.visited = False

    def __iter__(self):
        return iter(self)

    def __str__(self):
        return "Node index: %s \n Node prize: %s \n Node penalty: %s \n Node visted: %s \n" % (self.ind, self.prize, self.penalty, self.visited)
    
    def __repr__(self):
        return "Node index: %s \n Node prize: %s \n Node penalty: %s \n Node visted: %s \n" % (self.ind, self.prize, self.penalty, self.visited)

    def __len__(self):
        return self.length

    def getPrize(self):
        return self.prize

    def getPenalty(self):
        return self.penalty
    
    def isVisted(self):
        return self.visited
    
    def node_visited(self):
        self.visited = True


# parsing input file
# reads vertex prices and penalties and edge cost for a complete graph
def read_graph(filename: str) -> Tuple[List[int], List[int], List[List[int]]]:
    mode = "searching"
    cost = list()
    file = open(filename)
    for line in file.read().splitlines():
        if mode == "searching" and line.startswith("NODE PRIZES"):
            mode = "prize"
        elif mode == "prize":
            prizes = list(map(int, line.split()))
            mode = "searching"
        elif mode == "searching" and line.startswith("NODE PENALTIES"):
            mode = "penalty"
        elif mode == "penalty":
            penalties = list(map(int, line.split()))
            mode = "searching"
        elif mode == "searching" and line.startswith("TRAVEL COST MATRIX"):
            mode = "cost"
        elif mode == "cost":
            if len(line) > 1:
                cost.append(list(map(int, line.split())))
    file.close()
    return prizes, penalties, cost


prizes, penalties, cost = read_graph("v10.txt")

# create nodes instances
node_instances = []
for ind, prize in enumerate(prizes):
    node_instances.append(Node(ind, prize, penalties[ind]))

# create round trip
start_node = 0
current_node = -1
trip_cost = 0
visited_node_ind = []
visited_node_ind.append(start_node)
while start_node != current_node:
    if current_node == -1:
        current_node = 0
    optimal_path = -1000000000
    for ind, node_instance in enumerate(node_instances):
        if not node_instance.isVisted() and current_node != ind:
            if optimal_path < node_instance.getPrize() - cost[current_node][ind] - node_instance.getPenalty():
                optimal_path = node_instance.getPrize(
                ) - cost[current_node][ind] - node_instance.getPenalty()
                current_node = ind
    trip_cost += optimal_path
    visited_node_ind.append(current_node)
    node_instances[current_node].node_visited()

# calculate penalty
for ind, node_instance in enumerate(node_instances):
    if node_instance.isVisted():
        trip_cost += node_instance.getPenalty() 

print(trip_cost)
print(visited_node_ind)
