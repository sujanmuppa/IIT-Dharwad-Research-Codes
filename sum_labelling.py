from itertools import permutations
import networkx as nx

def is_edge(adj_list, vertex1, vertex2):
    return vertex2 in adj_list[vertex1]

def isvalid_labelling(adj_list, graph_labels):
    edge_sum = set()
    non_edge_sum = set()

    for i in range(len(adj_list)):
        for j in range(i + 1, len(adj_list)):  # Check pairs only once (i < j)
            sum_label = graph_labels[i] + graph_labels[j]
            print(i, j, sum_label)
            if is_edge(adj_list, i, j):
                edge_sum.add(sum_label)
            else:
                non_edge_sum.add(sum_label)
    print(edge_sum, non_edge_sum)
    for i in edge_sum:
        if i not in graph_labels:
            return False
    for i in non_edge_sum:
        if i in graph_labels:
            return False
    return True

def sum_labelling(n, adj_list):
    for graph_labels in permutations(range(1, n + 1), len(adj_list)):
        if isvalid_labelling(adj_list, graph_labels):
            return graph_labels
    return "No valid labelling found."


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

with open("graph4c.g6") as f:
    
    adj_list = graph6_to_adjacency_list(f.readline().strip())
    adj_list.append([])
    with open("graph4c_out.txt", "w") as f:
        f.write("Adjacency List: " + str(adj_list) + "\n")
        f.write(" ".join(map(str, sum_labelling(20, adj_list))) + "\n")

