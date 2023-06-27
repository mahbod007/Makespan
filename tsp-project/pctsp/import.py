from typing import Tuple, List


# reads vertex prices and penalties and edge cost for a complete graph
def read_graph(filename: str) -> Tuple[List[int], List[int], List[List[int]]]:
    mode = "searching"
    cost = list()
    file = open(filename)
    for line in file.read().splitlines():
        if mode == "searching" and line.startswith("NODE PRIZES"):
            mode = "prize"
        elif mode == "prize":
            prices = list(map(int, line.split()))
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
    return prices, penalties, cost

prices, penalties, cost = read_graph("v10.txt")
print("prices", prices)
print("penalties", penalties)
print("cost", cost)
