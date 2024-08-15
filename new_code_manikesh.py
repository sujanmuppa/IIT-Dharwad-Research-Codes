from collections import deque
from functools import lru_cache
import networkx as nx

# Existing Functions
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


def bfs_new(graph_alist, start):
    """Perform BFS to find distances from the start node."""
    visited = [(False, 0) for _ in range(len(graph_alist))]
    queue = deque([(start, 0)])
    
    while queue:
        vertex, depth = queue.popleft()
        if not visited[vertex][0]:
            visited[vertex] = (True, depth)
            for neighbor in graph_alist[vertex]:
                if not visited[neighbor][0]:
                    queue.append((neighbor, depth + 1))
    
    return visited

def dist_list1_new(graph_alist):
    """Create a list of distances from each node to all other nodes."""
    dist_list = {}
    for i in range(len(graph_alist)):
        visited = bfs_new(graph_alist, i)
        dist_list[i] = [(j, visited[j][1]) for j in range(len(visited)) if visited[j][0]]
    return dist_list



def dfs(adj_list, visited, node, parent=None):
    visited.add(node)
    for neighbor in adj_list[node]:
        if neighbor not in visited:
            if dfs(adj_list, visited, neighbor, node) == False:
                return False
        elif neighbor != parent:
            return False
    return True


