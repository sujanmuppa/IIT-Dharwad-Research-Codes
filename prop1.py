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

# New functions with renamed bfs and dist_list1
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
    print("i", i, "dist_lists", dist_lists[i])
    degree_1_at_dist_1 = 0
    degree_1_at_dist_2 = 0
    for j, k in dist_lists[i]:
        if k == 1:
            print(dist_lists[j])
            for (l, m) in dist_lists[j]:
                if m == 1 and degrees[l] == 1:
                    degree_1_at_dist_1 += 1
        if k == 2:
            for (l, m) in dist_lists[j]:
                if m == 1 and degrees[l] == 1:
                    degree_1_at_dist_2 += 1
    if degree_1_at_dist_1 >= 3:
        return False
    elif degree_1_at_dist_1 == 1 and degree_1_at_dist_2 > 2:
        return False
    elif degree_1_at_dist_1 == 2 and degree_1_at_dist_2 > 3:
        return False
    return True

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

def check2(i, dist_lists, degrees,net):
    val=0
    for k,l in dist_lists[i]:
        if degrees[k]==1 and l==1:
            val+=1
   
    if val>3:

        return False
    if val==3:
        net=net-1

    if net<0 :
       
        return False    
    
    return net     

def check1(j,i, dist_lists, degrees):
    net=0
    for k,l in dist_lists[j]:
        if degrees[k]==1 and k!=i and l==1:
           
            net+=1
    
    if net>=2:
        return False

    for k,l in dist_lists[j]:
        if l==1 and k!=i :
            temp=check2(k,dist_lists,degrees,net)
            if not temp and type(temp)==bool:
               return False
            else:
                net=temp
    return True   
    


def check0(i, dist_lists, degrees):
    temp = dist_lists[i]
    for j,k in temp:
        if k == 1:
            if not check1(j, i,dist_lists, degrees):
            
              return False
    return True
def prop1(adj_list):
    degrees1 = degrees(adj_list)
    dist_lists = dist_list1_new(adj_list)
    # check if the graph is a tree
    check1 = is_tree(adj_list)
    if check1 != False:
        print("Graph is a tree")
        return False
    # check if the graph has eccentricity 3
    ecc3_vertices = []
    flg, flg1 = False, False
    for i in range(len(adj_list)):
        (flg, flg1) = is_ecc3(dist_lists[i])
        if flg and flg1:
            ecc3_vertices.append(i)
    # give output by above checks
    if len(ecc3_vertices) == 0:
        return False
    stacker = [0 for i in range (len(adj_list))]
    for i in ecc3_vertices:
        if check0(i, dist_lists, degrees1):    
            stacker[i] = 1
    return (stacker, ecc3_vertices)

def test(adj_list):
    return prop1(adj_list)
# adj_list =[[2, 3], [3], [0], [0, 1]]
# ecc3list = prop1(adj_list)
# visited = brute(adj_list)
# print(visited)
# print(ecc3list)
# print(visited)
# print(ecc3list)
# dist_lists = dist_list1_new(adj_list)
# degrees1 = degrees(adj_list)
# for i in dist_lists:
#     print(i)
#     for j in i:
#         if j[1] > 3:
#             print("NOt")
# print(dist_lists)
# print(prop1(adj_list))  
# print(prop1(adj_list))
# Example Usage
with open("graph7c.g6", 'r') as f:
    graph_number = 1
    count = 0
    for line in f:
        graph6_string = line.strip()
        adjacency_list = graph6_to_adjacency_list(graph6_string)
        ecc3list = prop1(adjacency_list)
        if ecc3list != False:
            graph_number += 1   
            visited = brute(adjacency_list)
            stacker, ecc3vertices = ecc3list
            print(adjacency_list)
            for i in range(len(stacker)):
                if i in ecc3vertices and stacker[i] != visited[i]:
                    print("Test failed for graph", graph_number, "at vertex", i)
                    print(visited)
                    print(ecc3list)

                    with open("failures.txt", "a") as fail_file:
                        fail_file.write(f"Test failed for graph {graph_number} at vertex {i}\n{adjacency_list}\n and visited {visited}\n stalker {ecc3list}\n")
                else:
                    count += 1
    print(count,graph_number)