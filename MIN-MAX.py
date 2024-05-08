import random
import matplotlib.pyplot as plt

class Node:
    def __init__(self, value=None):
        self.value = value
        self.children = []

def generate_tree(node, depth, max_children):
    if depth == 0:
        return
    num_children = random.randint(3, max_children)
    for _ in range(num_children):
        child = Node(random.randint(-5, 5))
        node.children.append(child)
        generate_tree(child, depth - 1, max_children)

def minmax(node, maximizing_player):
    minmax.visited_nodes += 1
    if not node.children:
        return node.value
    if maximizing_player:
        value = float('-inf')
        for child in node.children:
            value = max(value, minmax(child, False))
        return value
    else:
        value = float('inf')
        for child in node.children:
            value = min(value, minmax(child, True))
        return value

def alphabeta(node, alpha, beta, maximizing_player):
    alphabeta.visited_nodes += 1
    if not node.children:
        return node.value
    if maximizing_player:
        value = float('-inf')
        for child in node.children:
            value = max(value, alphabeta(child, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for child in node.children:
            value = min(value, alphabeta(child, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

def plot_tree(node, ax=None, pos=None, level=0, x=0, y=0, spacing=20):
    if ax is None:
        _, ax = plt.subplots()
    if pos is None:
        pos = {}
    
    if node not in pos:
        pos[node] = (x, y)
    else:
        return
    
    # Use MINMAX algorithm to assign values to nodes
    if node.children:
        if level % 2 == 0:  # MAX node
            node.value = max(child.value for child in node.children)
        else:  # MIN node
            node.value = min(child.value for child in node.children)
    
    value_str = 'None' if level == 0 else str(node.value)  # Display empty string for root node
    
    ax.text(x, y, f'{value_str}\n{("MAX" if level % 2 == 0 else "MIN")}', ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))
    
    if node.children:
        num_children = len(node.children)
        total_width = spacing * num_children
        for i, child in enumerate(node.children):
            child_x = x - total_width/2 + (i + 0.5) * spacing
            child_y = y - spacing
            plot_tree(child, ax, pos, level + 1, child_x, child_y, spacing/2.5)  # Adjust spacing
            ax.plot([x, child_x], [y, child_y], 'b-' if level % 2 == 0 else 'r-')

root = Node()
depth = 2  # Change the depth as needed
max_children = 3  # Change the max number of children as needed

generate_tree(root, depth, max_children)

# Initialize variables to count visited nodes
minmax.visited_nodes = 0
alphabeta.visited_nodes = 0


print("MINMAX Result:", minmax(root, True))
print("Number of Nodes Visited (MINMAX):", minmax.visited_nodes)
print()

print("Alpha-Beta Pruning Result:", alphabeta(root, float('-inf'), float('inf'), True))
print("Number of Nodes Visited (Alpha-Beta Pruning):", alphabeta.visited_nodes)
print()

plot_tree(root)
plt.title("Original Tree")
plt.show()
