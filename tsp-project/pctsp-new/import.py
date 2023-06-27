from typing import Tuple, List
from gurobipy import *
from time import time


# reads vertex prizes, prize target and penalties and edge cost for a complete graph
def read_graph(filename: str) -> Tuple[List[int], int, List[int], List[List[int]]]:
    mode = "searching"
    cost = list()
    file = open(filename)
    for line in file.read().splitlines():
        if mode == "searching" and line.startswith("NODE PRIZES"):
            mode = "prize"
        elif mode == "prize":
            prizes = list(map(int, line.split()))
            mode = "searching"
        elif mode == "searching" and line.startswith("PRIZE TARGET"):
            mode = "target"
        elif mode == "target":
            target = int(line)
            mode = "searching"
        elif mode == "searching" and line.startswith("NODE PENALTIES"):
            mode = "penalty"
        elif mode == "penalty":
            penalties = list(map(int, line.split()))
            for i in range(1, len(penalties)):
                penalties[i] = round(0.25*penalties[i])
            mode = "searching"
        elif mode == "searching" and line.startswith("TRAVEL COST MATRIX"):
            mode = "cost"
        elif mode == "cost":
            if len(line) > 1:
                cost.append(list(map(int, line.split())))
    file.close()
    return prizes, target, penalties, cost

prizes, target, penalties, cost = read_graph("v10.txt")
print("prizes", prizes)
print("target", target)
print("penalties", penalties)
print("cost", cost)


