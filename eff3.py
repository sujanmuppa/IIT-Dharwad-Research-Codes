import sys
from collections import deque

sys.setrecursionlimit(100000)

def bfs(graph_alist, start):
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

def dist_list1(graph_alist):
    """Create a list of distances from each node to all other nodes."""
    dist_list = {}
    for i in range(len(graph_alist)):
        visited = bfs(graph_alist, i)
        dist_list[i] = [(j, visited[j][1]) for j in range(len(visited)) if visited[j][0]]
    return dist_list

def recur(visited, weights, dist_list, memo):
    """Recursively process the graph to find the correct visited states."""
    state = (tuple(visited), tuple(weights))
    if state in memo:
        return memo[state]
    
    for i in range(len(weights)):
        if weights[i] == len(weights):
            visited[i] = 1
            memo[state] = visited[:]
            return visited
    
    for i in range(len(weights)):
        if weights[i] > 0:
            for neighbor, distance in dist_list[i]:
                if weights[neighbor] > 0 and weights[i] >= distance:
                    original_weights = weights[:]
                    
                    # Transfer weights
                    weights[i] += weights[neighbor]
                    weights[neighbor] = 0
                    
                    # Set visited if it's a final state
                    if weights[i] == len(weights):
                        visited[i] = 1
                        memo[state] = visited[:]
                        return visited
                    
                    # Recur to propagate the state
                    result = recur(visited, weights, dist_list, memo)
                    
                    if result is not None:
                        memo[state] = result
                        return result
                    
                    # Restore weights if no valid state found
                    weights = original_weights
    
    memo[state] = None
    return None

def brute(graph_alist):
    """Apply brute force approach to solve the problem."""
    weights = [1] * len(graph_alist)
    dist_list = dist_list1(graph_alist)
    visited = [0] * len(dist_list)
    memo = {}
    result = recur(visited, weights, dist_list, memo)
    return result if result is not None else visited

def neighbors(level):
    """Generate adjacency list for a perfect binary tree of given level."""
    no_of_nodes = 2 ** level - 1
    graph_alist = [[] for _ in range(no_of_nodes)]
    for i in range(no_of_nodes):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < no_of_nodes:
            graph_alist[i].append(left)
            graph_alist[left].append(i)
        if right < no_of_nodes:
            graph_alist[i].append(right)
            graph_alist[right].append(i)
    return graph_alist

# Example usage:
graph_alist = neighbors(4)
print(brute(graph_alist))
