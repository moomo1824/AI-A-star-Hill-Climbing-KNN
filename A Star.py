import heapq
import math
import time

class Graph:
    def __init__(self):
        self.vertices = set()
        self.edges = {}

    def add_vertex(self, value):
        self.vertices.add(value)
        self.edges[value] = []

    def add_edge(self, from_vertex, to_vertex, weight):
        self.edges[from_vertex].append((to_vertex, weight))
        self.edges[to_vertex].append((from_vertex, weight))

def dijkstra(graph, start, goal):
    start_time = time.time_ns()

    visited = set()
    distances = {vertex: math.inf for vertex in graph.vertices}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_vertex in visited:
            continue

        visited.add(current_vertex)

        for neighbor, weight in graph.edges[current_vertex]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    path = []
    current_vertex = goal

    while current_vertex != start:
        path.insert(0, current_vertex)
        current_vertex = min(
            graph.edges[current_vertex], key=lambda x: distances[x[0]] + x[1]
        )[0]

    path.insert(0, start)

    end_time = time.time_ns()
    elapsed_time = (end_time - start_time)   # Convert to milliseconds

    return path, distances[goal], elapsed_time

def euclidean_distance(coord1, coord2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(coord1, coord2)))

def astar(graph, start, goal, coordinates):
    start_time = time.time()*1000


    visited = set()
    distances = {vertex: math.inf for vertex in graph.vertices}
    distances[start] = 0
    priority_queue = [(0 + euclidean_distance(coordinates[start], coordinates[goal]), 0, start)]

    while priority_queue:
        _, current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_vertex in visited:
            continue

        visited.add(current_vertex)

        for neighbor, weight in graph.edges[current_vertex]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(
                    priority_queue,
                    (distance + euclidean_distance(coordinates[neighbor], coordinates[goal]), distance, neighbor),
                )

    path = []
    current_vertex = goal

    while current_vertex != start:
        path.insert(0, current_vertex)
        current_vertex = min(
            graph.edges[current_vertex], key=lambda x: distances[x[0]] + x[1]
        )[0]

    path.insert(0, start)

    end_time = time.time()*1000
    elapsed_time = (end_time - start_time)   # Convert to milliseconds

    return path, distances[goal], elapsed_time

def read_coordinates(filename):
    coordinates = {}
    with open(filename, "r") as file:
        next(file)  # skip header
        for line in file:
            star, x, y, z = line.strip().split(",")
            coordinates[star] = (float(x), float(y), float(z))
    return coordinates

def read_distances(filename):
    graph = Graph()
    with open(filename, "r") as file:
        for line in file:
            source, destination, distance = line.strip().split(",")
            distance = float(distance)
            if source not in graph.vertices:
                graph.add_vertex(source)
            if destination not in graph.vertices:
                graph.add_vertex(destination)
            graph.add_edge(source, destination, distance)
    return graph

if __name__ == "__main__":
    coordinates = read_coordinates("Coordinates.csv")
    graph = read_distances("distances.csv")

    start = "TRAPPIST-1"
    goal_upsilon = "55 Cancri"

    print("\nDijkstra Algorithm:")
    path_dijkstra, cost_dijkstra, time_dijkstra = dijkstra(graph, start, goal_upsilon)
    print("Path:", " -> ".join(path_dijkstra))
    print("Cost:", cost_dijkstra)
    print(f"Time: {time_dijkstra:.6f} milliseconds")

    print("A* Algorithm:")
    path_astar, cost_astar, time_astar = astar(graph, start, goal_upsilon, coordinates)
    print("Path:", " -> ".join(path_astar))
    print("Cost:", cost_astar)
    print(f"Time: {time_astar:.6f} milliseconds")
