import sys
import os
import networkx as nx

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

def main(graph6_file):
    """
    Read a Graph6 file, print the number of graphs and their configurations (adjacency lists),
    and append the adjacency lists to 'graphs.txt'.

    Parameters:
    graph6_file (str): The path to the Graph6 file.
    """
    graph_count = 0
    with open(graph6_file, 'r') as f, open('graphs.txt', 'a') as output_file:
        for line in f:
            graph6_string = line.strip()
            adjacency_list = graph6_to_adjacency_list(graph6_string)
            
            # Write adjacency list to graphs.txt
            output_file.write(f"Graph {graph_count + 1}:\n")
            output_file.write("Adjacency List:\n")
            for node, neighbors in enumerate(adjacency_list):
                output_file.write(f"{node}: {neighbors}\n")
            output_file.write("\n")
            
            graph_count += 1
    
    print(f"Total number of graphs: {graph_count}")
    print(f"Graphs appended to 'graphs.txt'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <graph6_file>")
    else:
        main(sys.argv[1])
