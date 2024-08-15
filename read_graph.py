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
            if flg:
                f.write("We are Cooked\n\n")
        print(f"Graph {graph_number} information and final visited state appended to {SAVE_FILE}")
    except IOError as e:
        print(f"Error saving graph information: {e}")

# def main(graph6_file):
#     """
#     Read a Graph6 file and process each graph, saving its information.
#     """
#     # false_positive1 = []
#     # false_positive2 = []
#     with open(graph6_file, 'r') as f:
#         graph_number = 1
#         for line in f:
#             graph6_string = line.strip()
#             adjacency_list = graph6_to_adjacency_list(graph6_string)
#             final_visited = brute(adjacency_list)
#             flg = 1
#             dangling_vertices = 0
#             for i in adjacency_list:
#                 if len(i) == 1:
#                     dangling_vertices += 1
#             if dangling_vertices/len(adjacency_list) == 0.5 and final_visited.count(1) != len(final_visited):
#                 save_graph_info(graph_number, adjacency_list, final_visited, flg)
#                 graph_number += 1
#             # dangling_vertices = 0
#             # for i in adjacency_list:
#             #     if len(i) == 1:
#             #         dangling_vertices += 1
#             # if dangling_vertices == 1:
#             #     final_visited = brute(adjacency_list)
#             #     flg = 1 if final_visited.count(1) != len(final_visited) else 0
#             #     if flg:
#             #         with open(SAVE_FILE, 'a') as f:
#             #             f.write(f"Graph {graph_number}\n")
#             #             f.write('Adjacency List: ' + str(adjacency_list) + "\n")
#             #             f.write('Final Visited: ' + ','.join(map(str, final_visited)) + "\n\n")
#             #         graph_number += 1
                    
#             # flg = 0
#             # for i in adjacency_list:
#             #     if len(i) <= 1:
#             #         flg = 1
#             #         break
#             # final_visited = brute(adjacency_list)
#             # # error_need1 = []
#             # # error_need2 = []
#             # if flg and final_visited.count(1) == len(final_visited):
#             #     false_positive1.append(adjacency_list)
#             #     false_positive2.append(final_visited)
#             #     print(false_positive1[-1],false_positive2[-1])

#             # if not flg and final_visited.count(1) != len(final_visited):
#             #     error_need1.append(adjacency_list)
#             #     error_need2.append(final_visited)
#             # save_graph_info(graph_number, adjacency_list, final_visited, flg)
#             # graph_number += 1
#         # with open(SAVE_FILE, 'a') as f:
#         #     if len(false_positive1) == 0 and len(false_positive2) == 0:
#         #         f.write("\n\n\n\nNOPE\n\n\n\n")
#         #     else:
#         #         num = 1
#         #         for i in range (len(false_positive1)):
#         #             f.write(f"Graph {num}")
#         #             f.write('Adjacency List: ' + str(false_positive1[i]) + "\n")
#         #             f.write('Final Visited: ' + ','.join(map(str, false_positive2[i])) + "\n\n")

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python process_graphs.py <graph6_file>")
#     else:
#         main(sys.argv[1])

# adj_list = [[1],[0,2,4,3],[1,5],[1],[1],[2]]
# print(brute(adj_list))

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

adj_list = neighbors(5)
print(brute(adj_list))