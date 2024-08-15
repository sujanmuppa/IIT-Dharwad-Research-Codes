import sys
import os
from collections import deque
from functools import lru_cache
import networkx as nx

sys.setrecursionlimit(100000)

SAVE_FILE = "visited_state3.txt"

def graph6_to_adjacency_list(graph6_string):
    G = nx.from_graph6_bytes(graph6_string.encode('utf-8'))
    adjacency_list = nx.to_dict_of_lists(G)
    adjacency_list = [adjacency_list[node] for node in range(len(adjacency_list))]
    return adjacency_list

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
                    weights[i] += weights[j]
                    weights[j] = 0
                    if weights[i] == len(weights):
                        visited[i] = 1
                    result = recur((tuple(weights), tuple(visited)), dist_list)
                    if result is not None and sum(result) > sum(visited):
                        visited = list(result)
                    weights = original_weights
    return tuple(visited)

def brute(graph_alist):
    """Apply brute force approach to solve the problem."""
    weights = tuple([1] * len(graph_alist))
    dist_list = dist_list1(graph_alist)
    visited = tuple([0] * len(graph_alist))
    return recur((weights, visited), dist_list)