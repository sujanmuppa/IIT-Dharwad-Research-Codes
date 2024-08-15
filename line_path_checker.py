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

import sys
import os
from collections import deque
from functools import lru_cache
import networkx as nx

sys.setrecursionlimit(100000)

SAVE_FILE = "visited_state3.txt"

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

def save_graph_info(graph_number, adjacency_list, final_visited, flg):
    """Append the graph number, adjacency list, and final visited array to a text file."""
    try:
        with open(SAVE_FILE, 'a') as f:
            f.write(f"Graph {graph_number}\n")
            f.write('Adjacency List: ' + str(adjacency_list) + "\n")
            f.write('Final Visited: ' + ','.join(map(str, final_visited)) + "\n\n")
            if not flg:
                f.write("We are Cooked\n\n")
        print(f"Graph {graph_number} information and final visited state appended to {SAVE_FILE}")
    except IOError as e:
        print(f"Error saving graph information: {e}")



def main(graph6_file):
    """
    Read a Graph6 file and process each graph, saving its information.
    """
    # false_positive1 = []
    # false_positive2 = []
    with open(graph6_file, 'r') as f:
        graph_number = 1
        for line in f:
            graph6_string = line.strip()
            adjacency_list = graph6_to_adjacency_list(graph6_string)
            is_line = dfs_path(adjacency_list)
            if not is_line:
                final_visited = brute(adjacency_list)
                flg = 0
                for i in final_visited:
                    if i == 0:
                        flg = 1
                        break
                if not flg:
                    save_graph_info(graph_number, adjacency_list, final_visited, flg)
                    graph_number += 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_graphs.py <graph6_file>")
    else:
        main(sys.argv[1])
