from collections import deque

def bfs(graph, start, goal):
    visited = set()
    queue = deque([[start]])
    total_nodes_visited = 0

    while queue:
        total_nodes_in_queue = sum(len(path) for path in queue)
        print(queue, ", Total number of nodes:", total_nodes_in_queue)
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path
       
        if node not in visited:
            visited.add(node)
            total_nodes_visited += 1
            successors = successor(graph, node)
            for succ in successors:
                new_path = list(path)
                new_path.append(succ)
                queue.append(new_path)

def successor(graph, node):
    successors = []
    for i in range(len(graph[node])):
        if graph[node][i] > 0:
            successors.append(i)
    return successors

adjacency_matrix = [
    [0, 1, 1, 0, 0],
    [1, 0, 1, 1, 1],
    [1, 1, 0, 0, 1],
    [0, 1, 0, 0, 1],
    [0, 1, 1, 1, 0]
]

initial_node = int(input("Enter the initial node: "))
goal_node = int(input("Enter the goal node: "))

print("Optimal path:", bfs(adjacency_matrix, initial_node, goal_node))