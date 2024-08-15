import sys
import os
from collections import deque
from functools import lru_cache

sys.setrecursionlimit(100000)

def bfs(graph_alist, start):
    """Perform BFS to find distances from the start node."""
    visited = [False] * len(graph_alist)
    distances = [0] * len(graph_alist)
    queue = deque([(start, 0)])
    
    while queue:
        vertex, depth = queue.popleft()
        if not visited[vertex]:
            visited[vertex] = True
            distances[vertex] = depth
            for neighbor in graph_alist[vertex]:
                if not visited[neighbor]:
                    queue.append((neighbor, depth + 1))
    
    return distances

def dist_list1(graph_alist):
    """Create a list of distances from each node to all other nodes."""
    return tuple(tuple(bfs(graph_alist, i)) for i in range(len(graph_alist)))

# Memoization cache
recur_calls = 0

@lru_cache(maxsize=None)
def recur(state, dist_list):
    global recur_calls
    recur_calls += 1

    weights, visited = state
    weights = list(weights)
    visited = list(visited)
    
    for i in range(len(weights)):
        if weights[i] == len(weights):
            visited[i] = 1
            return tuple(visited)
    
    for i in range(len(weights)):
        if weights[i] > 0:
            for j in range(len(weights)):
                if weights[j] > 0 and dist_list[i][j] == weights[j]:
                    original_weights = weights[:]
                    
                    # Transfer weights
                    weights[i] += weights[j]
                    weights[j] = 0
                    
                    # Set visited if it's a final state
                    if weights[i] == len(weights):
                        visited[i] = 1
                        return tuple(visited)
                    
                    # Recur to propagate the state
                    result = recur((tuple(weights), tuple(visited)), dist_list)
                    
                    if result is not None and sum(result) > sum(visited):
                        visited = list(result)
                    
                    # Restore weights if no valid state found
                    weights = original_weights
    
    return tuple(visited)

def brute(graph_alist):
    """Apply brute force approach to solve the problem."""
    weights = tuple([1] * len(graph_alist))
    dist_list = dist_list1(graph_alist)
    visited = tuple([0] * len(graph_alist))
    return recur((weights, visited), dist_list)



def read_graph_from_file(filename):
    """Read graph from a file and create an adjacency list."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    first_line = lines[0].strip().split()
    num_vertices = int(first_line[0])
    num_edges = int(first_line[1])
    
    graph_alist = [[] for _ in range(num_vertices)]
    for line in lines[1:]:
        u, v = map(int, line.strip().split())
        graph_alist[u].append(v)
        graph_alist[v].append(u)
    
    return graph_alist


def main(input_file):
    # Read the graph from the input file
    graph_alist = read_graph_from_file(input_file)
    print("ADJ LIST", graph_alist)

    # Calculate final visited state without loading any previous state
    visited_state = brute(graph_alist)
    print("Final visited:", visited_state)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python new_prog.py <.txt file>")
    else:
        main(sys.argv[1])
