from collections import deque
import networkx as nx

# def dfs_labeling(adj_list, initial_labels):
#     labels = [0]*len(adj_list)
#     labels[0] = initial_labels[0]
#     # dfs
#     stack = [0]
#     visited = [False]*len(adj_list)
#     visited[0] = True
#     first_time = True
#     sum_label = 0
#     while stack:
#         vertex = stack.pop()
#         for neighbor in adj_list[vertex]:
#             if not visited[neighbor]:
#                 visited[neighbor] = True
#                 stack.append(neighbor)
#                 if first_time:
#                     labels[neighbor] = initial_labels[1]
#                     sum_label = initial_labels[1] + labels[vertex]
#                     first_time = False
#                 else:
#                     labels[neighbor] = sum_label 
#                     sum_label = labels[vertex] + labels[neighbor]
#     return labels


def dfs_labeling(adj_list, vertex, visited, labels, count, putlabel,parent):
    labels[vertex] = putlabel
    if parent == -1:
        putlabel+=1
    else:
        putlabel+=labels[parent]
    count+=1
    visited[vertex]=True
    for i in adj_list[vertex]:
        if visited[i]==False:
            putlabel,visited,labels,count=dfs_labeling(adj_list,i,visited,labels,count,putlabel,vertex)
    
    return (putlabel,visited,labels,count)
  
    
    
    
    
 
# Example usage
# adj_list = [[1,2,3,4],[0],[0],[0],[0],[]]  # Example graph adjacency list
# initial_labels = (3,4)  # Starting labels
# putlabel=3
# count = 0
# visited = [False]*len(adj_list)
# labels = [0]*len(adj_list)


# print(labels)

def is_edge(adj_list, vertex1, vertex2):
    return vertex2 in adj_list[vertex1]

def isvalid_labelling(adj_list, graph_labels):
    edge_sum = set()
    non_edge_sum = set()

    for i in range(len(adj_list)):
        for j in range(i + 1, len(adj_list)):
            sum_label = graph_labels[i] + graph_labels[j]
            if is_edge(adj_list, i, j):
                edge_sum.add(sum_label)
            else:
                non_edge_sum.add(sum_label)
    for i in edge_sum:
        if i not in graph_labels:
            return False
    for i in non_edge_sum:
        if i in graph_labels:
            return False
    return True

# print(isvalid_labelling(adj_list, labels))

def dfs(adj_list, visited, node, parent=None):
    visited.add(node)
    for neighbor in adj_list[node]:
        if neighbor not in visited:
            if dfs(adj_list, visited, neighbor, node) == False:
                return False
        elif neighbor != parent:
            return False
    return True


def is_tree(adj_list):
    visited = set()
    flg = dfs(adj_list, visited, 0)
    return flg

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

def degree_sort(adj_list):
    degrees = [len(i) for i in adj_list]
    degree_list = []
    for i in range(len(degrees)):
        degree_list.append((i,degrees[i]))
    degree_list.sort(key = lambda x: x[1])
    return degree_list


adj_list = [[1,2,3,4,5,6],[0,2],[0,1],[0,4],[0,3],[0],[0],[]]
degree_list1 = degree_sort(adj_list)
temp = degree_list1[0]
degree_list1 = degree_list1[1:]
degree_list1.append(temp)
putlabel=1
count = 0
visited = [False]*len(adj_list)
labels = [0]*len(adj_list)
for i in degree_list1:
    if visited[i[0]]==False:
        putlabel,visited,labels,count=dfs_labeling(adj_list, i[0], visited,labels,count,putlabel,-1)

print(isvalid_labelling(adj_list, labels))
from itertools import permutations
print(labels)
for i in permutations(labels):
    if isvalid_labelling(adj_list, i):
        print("Valid labelling found.")
        break


# adj_list = neighbors(3)
# adj_list.append([])
# degree_list1 = degree_sort(adj_list)
# temp = degree_list1[0]
# degree_list1 = degree_list1[1:]
# degree_list1.append(temp)
# print(degree_list1)
# # print(isvalid_labelling(adj_list, labels))
# putlabel=3
# count = 0
# visited = [False]*len(adj_list)
# labels = [0]*len(adj_list)
# for i in degree_list1:
#     if visited[i[0]]==False:
#         putlabel,visited,labels,count=dfs_labeling(adj_list, i[0], visited,labels,count,putlabel,-1)

# print(isvalid_labelling(adj_list, labels))
# from itertools import permutations

# for perm in permutations(labels):
#     if isvalid_labelling(adj_list, perm):
#         if isvalid_labelling(adj_list, perm):
#             print("Valid labelling found.")
#             break
# else:
#     print("No valid labelling found.")
# with open("gra9c.g6", 'r') as f:
#     graph_number = 1
#     count = 0
#     count1 = 0
#     count2 = 0
#     for line in f:
#         graph6_string = line.strip()
#         adj_list = graph6_to_adjacency_list(graph6_string)
#         if is_tree(adj_list):
#             count1 += 1
#             adj_list.append([])
#             degree_list1 = degree_sort(adj_list)
#             temp = degree_list1[0]
#             degree_list1 = degree_list1[1:]
#             degree_list1.append(temp)

#             putlabel=3
#             count = 0
#             visited = [False]*len(adj_list)
#             labels = [0]*len(adj_list)
#             for i in degree_list1:
#                 if visited[i[0]]==False:
#                     putlabel,visited,labels,count=dfs_labeling(adj_list, i[0], visited,labels,count,putlabel,-1)
#             if not isvalid_labelling(adj_list, labels):
#                 print("Invalid labelling")
#                 print(degree_list1)
#                 print(labels)
#                 print(adj_list)
#         else:


#     print(f"Total number of trees: {count1}")