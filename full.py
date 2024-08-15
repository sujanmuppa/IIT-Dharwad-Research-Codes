
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





def generate_cycle_graph(num_vertices):
    """Generate an adjacency list for an undirected cycle graph."""
    if num_vertices < 3:
        raise ValueError("Number of vertices in a cycle graph must be at least 3.")
    
    graph_alist = [[] for _ in range(num_vertices)]
    for i in range(num_vertices):
        graph_alist[i].append((i + 1) % num_vertices)
        graph_alist[i].append((i - 1) % num_vertices)
    
    return graph_alist

def recur1(adj_list, num_vertices, memo):
    """Recursively find all possible edge combinations inside the cycle graph"""
    # print("Called recur with adj_list:", adj_list, "and memo:", memo)
    adj_tuple = tuple(tuple(neighbors) for neighbors in adj_list)  # Convert adjacency list to tuple of tuples
    if adj_tuple in memo:
        return memo
    
    memo.add(adj_tuple)
    
    for i in range(num_vertices):
        for j in range(num_vertices):
            if i != j and j not in adj_list[i] and i not in adj_list[j]:
                adj_list[i].append(j)
                adj_list[j].append(i)
                # print("Adjacency List:", adj_list)
                visited = brute(adj_list)
                for i in visited:
                    if i == 0:
                        print("NO")
                memo = recur1(adj_list, num_vertices, memo)
                adj_list[i].remove(j)
                adj_list[j].remove(i)
    
    return memo

def possibilities(adj_list, num_vertices):
    """Find all possible edge combinations inside the cycle graph"""
    memo = set()
    memo = recur1(adj_list, num_vertices, memo)
    return memo

num_vertices = 7
adj_list = generate_cycle_graph(num_vertices)
# print("Generated Adjacency List:", adj_list)

combinations = possibilities(adj_list, num_vertices)
# print("Possible Combinations:", combinations)