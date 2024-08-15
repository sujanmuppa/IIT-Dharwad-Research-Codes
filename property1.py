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

def is_ecc3(dist_list):
    flg = True
    flg1 = False
    for (i,j) in dist_list:
        if j > 3:
            flg = False
            break
    for (i,j) in dist_list:
        if j == 3:
            flg1 = True
    return (flg,flg1)

def is_tree(adj_list):
    visited = set()
    flg = dfs(adj_list, visited, 0)
    return flg

def check_prop1(dist_lists, i, degrees):
    degree_1_at_dist_1 = 0
    degree_1_at_dist_2 = 0
    for j, k in dist_lists[i]:
        if k == 1:
            for (l, m) in dist_lists[j]:
                if m == 1 and degrees[l] == 1:
                    degree_1_at_dist_1 += 1
            
        if k == 2:
            for (l, m) in dist_lists[j]:
                if m == 1 and degrees[l] == 1:
                    degree_1_at_dist_2 += 1
    if degrees[i] == 1:
        if degree_1_at_dist_1 <= 2:
            if degree_1_at_dist_1 == 1 and degree_1_at_dist_2 <= 2:
                return True
            elif degree_1_at_dist_1 == 2 and degree_1_at_dist_2 <= 3:
                return True
    elif degrees[i] != 1:
        if degree_1_at_dist_1 <=  1:
            if degree_1_at_dist_1 == 0 and degree_1_at_dist_2 <= 2:
                return True
            if degree_1_at_dist_1 == 1 and degree_1_at_dist_2 <= 3:
                return True
    return False
def degrees(adj_list):
    degrees = [len(i) for i in adj_list]
    return degrees

def graph6_to_adjacency_list(graph6_string):
    """
    Convert a graph6 string to an adjacency list.

    Parameters:
    graph6_string (str): The graph6 representation of the graph.

    Returns:
    list: The adjacency list of the graph.
    """
    # Convert the graph6 string to a NetworkX graph
    G = nx.from_graph6_bytes(graph6_string.encode('utf-8'))

    # Convert the NetworkX graph to an adjacency list
    adjacency_list = nx.to_dict_of_lists(G)
    
    # Convert dict of lists to list of lists
    adjacency_list = [adjacency_list[node] for node in range(len(adjacency_list))]
    
    return adjacency_list

def prop1(adj_list):
    degrees1 = degrees(adj_list)
    dist_lists = dist_list1_new(adj_list)
    # check if the graph is a tree
    check1 = is_tree(adj_list)
    if check1 == False:
        print("Graph is not a tree")
        return False
    # check if the graph has eccentricity 3
    ecc3_vertices = []
    flg, flg1 = False, False
    for i in range(len(adj_list)):
        (flg, flg1) = is_ecc3(dist_lists[i])
        print("vertex", i, "flg", flg, "flg1", flg1)
        if flg and flg1:
            ecc3_vertices.append(i)
    print("ecc3",ecc3_vertices)
    # give output by above checks
    if len(ecc3_vertices) == 0:
        print("Graph does not have eccentricity 3")
        print("flg", flg, "flg1", flg1)
        return False
    prop1_satisfied_vertices = []
    for i in range(len(adj_list)):
        if i in ecc3_vertices:
            if check_prop1(dist_lists, i, degrees1):
                prop1_satisfied_vertices.append(i)
    if len(prop1_satisfied_vertices) == 0:
        print("Graph does not satisfy prop1")
        return False
    return prop1_satisfied_vertices

# adj_list = [[5, 6], [5], [6], [6], [6], [0, 1], [0, 2, 3, 4]]
# dist_lists = dist_list1_new(adj_list)
# degrees = degrees(adj_list)
# print(dist_lists)

with open("graph4c.g6", 'r') as f:
    graph_number = 1
    for line in f:
        graph6_string = line.strip()
        adjacency_list = graph6_to_adjacency_list(graph6_string)
        ecc3list = prop1(adjacency_list)
        if ecc3list != False:
            visited = brute(adjacency_list)
            print(ecc3list)
            for i in range (len(adjacency_list)):
                if ecc3list[i]==1 and visited[i]==0:
                    print("Test failed for graph", graph_number, "at vertex", i)
                    print(visited)
                    print(ecc3list)
                    with open("failures.txt", "a") as fail_file:
                        fail_file.write(f"Test failed for graph {graph_number} at vertex {i}\n{adjacency_list}\n and visited {visited}\n stalker {ecc3list}\n")
        graph_number += 1
