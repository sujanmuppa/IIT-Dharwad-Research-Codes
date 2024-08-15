import sys
from heapq import nlargest
sys.setrecursionlimit(100000)

def dfs(graph_alist, start):
    visited = [False] * len(graph_alist)
    distances = [0] * len(graph_alist)
    stack = [start]
    visited[start] = True
    
    while stack:
        vertex = stack.pop()
        for neighbor in graph_alist[vertex]:
            if not visited[neighbor]:
                stack.append(neighbor)
                visited[neighbor] = True
                distances[neighbor] = distances[vertex] + 1
    
    return distances

def recur(visited, weights, graph_alist, memo):
    state = tuple(weights)
    if state in memo:
        return memo[state]
    
    max_weights = nlargest(2, range(len(weights)), key=weights.__getitem__)
    i, j = max_weights[0], max_weights[1]
    if weights[i] == len(weights):
        visited[i] = 1
        memo[state] = visited[:]
        return visited
    
    dist = dfs(graph_alist, i)
    if dist[j] == weights[j] and weights[i] > 0:
        weights[i] += weights[j]
        weights[j] = 0
        result = recur(visited, weights, graph_alist, memo)
        if sum(result) > sum(visited):
            visited = result[:]
        weights[j] = dist[j]  # Restore weights
        weights[i] -= weights[j]  # Restore weights
    
    memo[state] = visited[:]
    return visited

def brute(graph_alist):
    weights = [1] * len(graph_alist)
    visited = [0] * len(graph_alist)
    memo = {}
    return recur(visited, weights, graph_alist, memo)

def neighbors(level):
    no_of_nodes = 2**level - 1
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

graph_alist = neighbors(5)
print("Final visited:", brute(graph_alist))