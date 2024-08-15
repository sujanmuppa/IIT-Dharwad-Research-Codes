from itertools import product
from itertools import permutations, combinations

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

def setup(adj_list):
    n = len(adj_list)
    label = [0] * n
    label1 = 0
    label2 = 0
    return (n, label, label1, label2)  

def find_valid_labelling(adj_list):
    n = len(adj_list)
    labels = [0] * n
    
    for l, m in combinations(range(3, 50), 2):
        i = l
        j = m 
        visited = [False for i in range (n)]
        while visited.count(True) != n:
            
                    
        for perm in permutations(labels):
            if isvalid_labelling(adj_list, perm):
                return perm
    
    return "No valid labelling found."


adj_list = [[1,2,3,4],[0],[0],[0],[0],[]]
print(find_valid_labelling(adj_list))