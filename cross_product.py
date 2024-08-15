import sys
import os
from collections import deque
from functools import lru_cache
import networkx as nx
import re
import json

def graph6_to_adjacency_list(graph6_string):
    G = nx.from_graph6_bytes(graph6_string.encode('utf-8'))
    adjacency_list = nx.to_dict_of_lists(G)
    nodes = sorted(adjacency_list.keys())
    adjacency_list = [adjacency_list[node] for node in nodes]
    return adjacency_list

def make_nx_graph(adj_list):
    G = nx.Graph()
    for i in range(len(adj_list)):
        for j in adj_list[i]:
            G.add_edge(i, j)
    return G

def get_adj_list_from_nx_graph(G):
    adj = {}
    for node in G.nodes():
        adj[node] = list(G.neighbors(node))
    return adj

def cross_product_of_two_graphs(adj_list1, adj_list2):
    adj1 = make_nx_graph(adj_list1)
    adj2 = make_nx_graph(adj_list2)
    adj = nx.cartesian_product(adj1, adj2)
    adj = get_adj_list_from_nx_graph(adj)
    
    # Convert adjacency dict of tuples back to list of lists
    node_to_index = {node: i for i, node in enumerate(sorted(adj.keys()))}
    list_adj = [[] for _ in range(len(node_to_index))]
    for node, neighbors in adj.items():
        list_adj[node_to_index[node]] = [node_to_index[neighbor] for neighbor in neighbors]
    
    return list_adj

def bfs(graph_alist, start):
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
            print(visited)
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
                        return tuple(visited)
                    result = recur((tuple(weights), tuple(visited)), dist_list)
                    
                    if result is not None and sum(result) > sum(visited):
                        visited = list(result)
                    weights = original_weights
    return tuple(visited)

def brute(graph_alist):
    weights = tuple([1] * len(graph_alist))
    dist_list = dist_list1(graph_alist)
    visited = tuple([0] * len(graph_alist))
    return recur((weights, visited), dist_list)

def get_stackable_graphs(filename):
    stackable_graphs = []
    with open(filename, 'r') as f:
        for line in f:
            graph6_string = line.strip()
            adjacency_list = graph6_to_adjacency_list(graph6_string)
            final_visited = brute(adjacency_list)
            if final_visited.count(1) == len(final_visited):
                stackable_graphs.append(adjacency_list)
    return stackable_graphs


def get_path_graph(n):
    G = nx.path_graph(n)
    G = get_adj_list_from_nx_graph(G)
    return G

def get_graphs(filename):
    graphs = []
    with open(filename, 'r') as f:
        for line in f:
            graph6_string = line.strip()
            adjacency_list = graph6_to_adjacency_list(graph6_string)
            graphs.append(adjacency_list)
    return graphs


# for graph in graphs:
#     graph_visited = brute(graph)
#     if graph_visited.count(1) == len(graph_visited):
#         product = cross_product_of_two_graphs(graph, line)
#         product_visited = brute(product)
#         if product_visited.count(1) != len(product_visited):
#             print("Graph is not stackable")
#             print(graph)
#             print(line)
#             print(product)
# print("Done")

def dfs_path(adj_list):
    path = []
    for i in range (len(adj_list)):
        if dfs(i, adj_list, path):
            return 1
        else:
            path = []
    return 0


def dfs(vertex, adj_list, path):
    path.append(vertex)
    for neighbor in adj_list[vertex]:
        if neighbor not in path:
            if dfs(neighbor, adj_list, path):
                return True
            if len(path) == len(adj_list):
                return True
            path.pop()
            return False

# p = get_graphs("graph5c.g6")
# q = get_graphs("graph5c.g6")
# for i in range(len(p)):
#     for j in range(len(q)):
#         isline1 = dfs_path(p[i])
#         isline2 = dfs_path(q[j])
#         if isline1 and isline2:
#             product = cross_product_of_two_graphs(p[i], q[j])
#             isline3 = dfs_path(product)
#             if not isline3:
#                 print("Intresting")
#                 print(p[i])
#                 print(q[j])
#                 print(product)
# print("Done")


adj_list1 = [[1,5],[0,2,3],[1,3],[2,4],[7,3,5],[4,0],[7,1],[6,4]]
# adj_list2 = get_path_graph(4)
# product = cross_product_of_two_graphs(adj_list1, adj_list2)
# print(product)
# print(brute(product))
# print(adj_list2)
print(brute(adj_list1))