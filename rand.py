import sys
import os
from collections import deque
from functools import lru_cache
import random

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

def generate_cycle_graph(num_vertices):
    """Generate an adjacency list for an undirected cycle graph."""
    if num_vertices < 3:
        raise ValueError("Number of vertices in a cycle graph must be at least 3.")
    
    graph_alist = [[] for _ in range(num_vertices)]
    for i in range(num_vertices):
        graph_alist[i].append((i + 1) % num_vertices)
        graph_alist[i].append((i - 1) % num_vertices)
    
    return graph_alist

def edges_not_present(adj_list):
    """The edges which are noot present in in the given graph"""
    return_list = {}
    for i in range(len(adj_list)):
        return_list[i] = []
        for j in range(num_vertices):
            if j not in adj_list[i]:
                return_list[i].append(j)
    return return_list

def randomize_cycle_graph(num_vertices):
    flg = 0
    """Randomly add edges that are not present in the cycle graph."""
    graph_alist = generate_cycle_graph(num_vertices)
    edges = edges_not_present(graph_alist)
    addable_edges = (num_vertices * (num_vertices - 1) // 2) - (num_vertices)
    while addable_edges:
        u = random.randint(0, num_vertices - 1)
        v = random.choice(edges[u])
        if u == v or v in graph_alist[u]:
            continue
        graph_alist[u].append(v)
        graph_alist[v].append(u)
        addable_edges -= 1
        # print(graph_alist)
        visited = brute(graph_alist)
        for i in visited:
            if i != 1:
                print("Not all nodes are visited")
                print(graph_alist)
                flg = 1
                break
            
        if flg == 1 or addable_edges == 0:
            break
            
num_vertices = 10
for i in range (5):
    randomize_cycle_graph(num_vertices)
