import heapq

def astar(graph, start, goal, heuristic):
    open_set = []
    closed_set = set()
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, goal)

    heapq.heappush(open_set, (f_score[start], start))

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path

        closed_set.add(current)

        for neighbor in graph[current]:
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + graph[current][neighbor]

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

                if neighbor not in open_set:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return list(reversed(path))

# Example usage:

# Define a graph as an adjacency dictionary
graph = {
    'A': {'B': 1, 'C': 3},
    'B': {'A': 1, 'D': 2, 'E': 4},
    'C': {'A': 3, 'F': 2},
    'D': {'B': 2},
    'E': {'B': 4, 'F': 1},
    'F': {'C': 2, 'E': 1}
}

# Define a heuristic function (e.g., Euclidean distance)
def euclidean_distance(node, goal):
    # You need domain-specific knowledge to create the heuristic function.
    # In this example, you can define coordinates for nodes to calculate Euclidean distance.
    coordinates = {
        'A': (0, 0),
        'B': (1, 1),
        'C': (3, 0),
        'D': (2, 1),
        'E': (2, 2),
        'F': (4, 2)
    }
    x1, y1 = coordinates[node]
    x2, y2 = coordinates[goal]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

start_node = 'A'
goal_node = 'F'
path = astar(graph, start_node, goal_node, heuristic=euclidean_distance)

if path:
    print("A* Path:", path)
else:
    print("No path found.")