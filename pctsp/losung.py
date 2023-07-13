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

    def getIndex(self):
        return self.ind
    
    def getPrize(self):
        return self.prize

    def getPenalty(self):
        return self.penalty
    
    def isVisted(self):
        return self.visited
    
    def node_visited(self):
        self.visited = True
    
    def node_not_visited(self):
        self.visited = False


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
    optimal_path = -sys.maxsize
    temp_current_node = 0
    for ind, node_instance in enumerate(node_instances):
        if not node_instance.isVisted() and current_node != ind:
            if optimal_path < node_instance.getPrize() - cost[current_node][ind] - node_instance.getPenalty():
                optimal_path = node_instance.getPrize(
                ) - cost[current_node][ind]
                temp_current_node = ind
    current_node = temp_current_node
    trip_cost += optimal_path 
    visited_node_ind.append(current_node)
    node_instances[current_node].node_visited()

# calculate penalty
for ind, node_instance in enumerate(node_instances):
    if not node_instance.isVisted():
        trip_cost -= node_instance.getPenalty()

print("First Round Trip without Nodes:")
print(trip_cost)
print(visited_node_ind)

# add node to round trip when it worth it
node_can_be_added = True
while (node_can_be_added):
    node_can_be_added = False
    for node_instance in node_instances:
        if not node_instance.isVisted():
            cost_of_candidate_node_to_add = node_instance.getPrize() + node_instance.getPenalty() - cost[visited_node_ind[len(visited_node_ind) - 2]][node_instance.getIndex()]
            if cost_of_candidate_node_to_add > 0:
                node_instance.node_visited()
                node_can_be_added = True
                trip_cost += node_instance.getPrize()
                trip_cost += node_instance.getPenalty()
                trip_cost -= cost[visited_node_ind[len(
                    visited_node_ind) - 2]][node_instance.getIndex()]
                visited_node_ind.insert(len(
                    visited_node_ind) - 2, node_instance.getIndex())



print("First Round Trip with Adding Nodes:")
print(trip_cost)
print(visited_node_ind)

temp_visted_node_ind = visited_node_ind
temp_trip_cost = trip_cost

for ind in range(1, len(visited_node_ind) - 2):
    temp_trip_cost += cost[visited_node_ind[ind - 1]][visited_node_ind[ind]]
    temp_trip_cost += cost[visited_node_ind[ind]][visited_node_ind[ind + 1]]
    temp_trip_cost += cost[visited_node_ind[ind + 1]][visited_node_ind[ind + 2]]

    temp_trip_cost -= cost[visited_node_ind[ind - 1]][visited_node_ind[ind + 1]]
    temp_trip_cost -= cost[visited_node_ind[ind + 1]][visited_node_ind[ind]]
    temp_trip_cost -= cost[visited_node_ind[ind]][visited_node_ind[ind + 2]]

    if temp_trip_cost > trip_cost:
        trip_cost = temp_trip_cost
        temp_swap = temp_visted_node_ind[ind]
        temp_visted_node_ind[ind] = temp_visted_node_ind[ind + 1]
        temp_visted_node_ind[ind + 1] = temp_swap
        visited_node_ind = temp_visted_node_ind
    else:
        temp_trip_cost = trip_cost

print("Optimazation on First Round Trip (Local Search):")
print(trip_cost)
print(visited_node_ind)    


# create nodes instances
node_instances = []
for ind, prize in enumerate(prizes):
    node_instances.append(Node(ind, prize, penalties[ind]))

# create round trip from all nodes
main_trip_cost = -sys.maxsize
for main_ind, node_to_strat_with in enumerate(node_instances):
    for item in node_instances:
        item.node_not_visited()
    start_node = main_ind
    current_node = -1
    trip_cost = 0
    visited_node_ind = []
    visited_node_ind.append(start_node)
    while start_node != current_node:
        if current_node == -1:
            current_node = main_ind
        optimal_path = -sys.maxsize
        temp_current_node = 0
        for ind, node_instance in enumerate(node_instances):
            if not node_instance.isVisted() and current_node != ind:
                if optimal_path < node_instance.getPrize() - cost[current_node][ind] - node_instance.getPenalty():
                    optimal_path = node_instance.getPrize(
                    ) - cost[current_node][ind]
                    temp_current_node = ind
        current_node = temp_current_node
        trip_cost += optimal_path
        visited_node_ind.append(current_node)
        node_instances[current_node].node_visited()

    # calculate penalty
    for ind, node_instance in enumerate(node_instances):
        if not node_instance.isVisted():
            trip_cost -= node_instance.getPenalty()

    print("Round Trip on without adding node node " + str(current_node))
    print(visited_node_ind)

    # add node to round trip when it worth it
    node_can_be_added = True
    while (node_can_be_added):
        node_can_be_added = False
        for node_instance in node_instances:
            if not node_instance.isVisted():
                cost_of_candidate_node_to_add = node_instance.getPrize() + node_instance.getPenalty() - \
                    cost[visited_node_ind[len(
                        visited_node_ind) - 2]][node_instance.getIndex()]
                if cost_of_candidate_node_to_add > 0:
                    node_instance.node_visited()
                    node_can_be_added = True
                    trip_cost += node_instance.getPrize()
                    trip_cost += node_instance.getPenalty()
                    trip_cost -= cost[visited_node_ind[len(
                        visited_node_ind) - 2]][node_instance.getIndex()]
                    visited_node_ind.insert(len(
                        visited_node_ind) - 2, node_instance.getIndex())



    temp_visted_node_ind = visited_node_ind
    temp_trip_cost = trip_cost

    print("Round Trip on with adding node node " + str(current_node))
    print(visited_node_ind)

    for ind in range(1, len(visited_node_ind) - 2):
        temp_trip_cost += cost[visited_node_ind[ind - 1]][visited_node_ind[ind]]
        temp_trip_cost += cost[visited_node_ind[ind]][visited_node_ind[ind + 1]]
        temp_trip_cost += cost[visited_node_ind[ind + 1]
                            ][visited_node_ind[ind + 2]]

        temp_trip_cost -= cost[visited_node_ind[ind - 1]
                            ][visited_node_ind[ind + 1]]
        temp_trip_cost -= cost[visited_node_ind[ind + 1]][visited_node_ind[ind]]
        temp_trip_cost -= cost[visited_node_ind[ind]][visited_node_ind[ind + 2]]

        if temp_trip_cost > trip_cost:
            trip_cost = temp_trip_cost
            temp_swap = temp_visted_node_ind[ind]
            temp_visted_node_ind[ind] = temp_visted_node_ind[ind + 1]
            temp_visted_node_ind[ind + 1] = temp_swap
            visited_node_ind = temp_visted_node_ind
        else:
            temp_trip_cost = trip_cost

    print("Optimized Round Trip on node " + str(current_node))
    print(visited_node_ind)
    
    if trip_cost > main_trip_cost:
        main_trip_cost = trip_cost

print("Overall Optimization on all Nodes:")
print(main_trip_cost)
print(visited_node_ind)
