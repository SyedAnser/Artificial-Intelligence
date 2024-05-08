import heapq

class Node:
    def __init__(self, decision, profit, weight):
        self.decision = decision  
        self.profit = profit 
        self.weight = weight  

    def __lt__(self, other):
        return self.profit < other.profit

def knapsack(items, capacity):
    n = len(items)
    current_best_profit = float('-inf')
    current_best_solution = [0] * n

    def is_valid(node):
        return node.weight <= capacity

    def is_leaf(node):
        return -1 not in node.decision

    def heuristic(cap, items, start):
        total_value = 0
        remaining_capacity = cap
        for i in range(start, len(items)):
            if items[i][1] <= remaining_capacity:
                total_value += items[i][0]
                remaining_capacity -= items[i][1]
            else:
                total_value += items[i][0] * (remaining_capacity / items[i][1])
                break
        return total_value

    open_list = []
    closed_set = set()

    def search():
        nonlocal current_best_profit
        nonlocal current_best_solution

        root = Node([-1] * n, 0, 0)
        heapq.heappush(open_list, (root.profit + heuristic(capacity - root.weight, [(items[i][0], items[i][1]) for i in range(len(items)) if root.decision[i] == -1], 0), root))
        evaluations = 0
        while open_list:
            
            current_node = heapq.heappop(open_list)[1]

            if tuple(current_node.decision) not in closed_set:
                closed_set.add(tuple(current_node.decision))
                evaluations+=1

            if is_leaf(current_node):
                if current_node.profit > current_best_profit:
                    current_best_profit = current_node.profit
                    current_best_solution = current_node.decision.copy()
            else:
                for i in range(n):
                    if current_node.decision[i] == -1:
                        new_decision = current_node.decision.copy()
                        new_decision[i] = 1
                        new_profit = current_node.profit + items[i][0]
                        new_weight = current_node.weight + items[i][1]
                        if is_valid(Node(new_decision, new_profit, new_weight)):
                            if tuple(new_decision) not in closed_set:
                                heapq.heappush(open_list, (new_profit + heuristic(capacity - new_weight, [(items[j][0], items[j][1]) for j in range(len(items)) if new_decision[j] == -1], i+1), Node(new_decision, new_profit, new_weight)))

                        new_decision = current_node.decision.copy()
                        new_decision[i] = 0 
                        if tuple(new_decision) not in closed_set:
                            heapq.heappush(open_list, (current_node.profit + heuristic(capacity - current_node.weight, [(items[j][0], items[j][1]) for j in range(len(items)) if new_decision[j] == -1], i+1), Node(new_decision, current_node.profit, current_node.weight)))
        print("Number of evals:", evaluations)
    search() 

    return current_best_solution, current_best_profit, closed_set

# Example usage:
items = [(60, 5), (100, 10), (130, 10), (200, 15), (400, 30), (70, 5)]
capacity = 60
solution, max_profit,closed_set = knapsack(items, capacity)
print("Optimal solution:", solution)
print("Max profit:", max_profit)
