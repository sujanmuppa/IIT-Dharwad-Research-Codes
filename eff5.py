import sys
import os
from collections import deque
from functools import lru_cache

sys.setrecursionlimit(100000)

SAVE_INTERVAL = 10000  # Save progress every 10,000 recursive calls
SAVE_FILE = "visited_state.txt"

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

def max_distances(dist_list):
    """Find the maximum distance from each node."""
    return tuple(max(distances) for distances in dist_list)


# Memoization cache
recur_calls = 0

@lru_cache(maxsize=None)
def recur(state, dist_list, ecc,stack):
    global recur_calls
    recur_calls += 1
    
    weights, visited = state
    weights = list(weights)
    visited = list(visited)
    
    for i in range(len(weights)):
        if weights[i] == len(weights):
          
            visited[i] = 1
            return tuple(visited)
        if i!=stack and weights[i]>ecc:
            return tuple(visited)
    
    for i in range(len(weights)):
        if weights[i] > 0 :
            for j in range(len(weights)):
                if weights[j] > 0 and dist_list[i][j] == weights[j] and j!=stack:
                    original_weights = weights[:]
                    
                    # Transfer weights
                    weights[i] += weights[j]
                    weights[j] = 0
                    
                    # Set visited if it's a final state
                    if   weights[i] == len(weights):
                        visited[i] = 1
                       
                        return tuple(visited)
                    
                    # Recur to propagate the state
                    result = recur((tuple(weights), tuple(visited)), dist_list, ecc,stack)
                    
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
    print(dist_list)
   
    stack = 0
    ecc = max(dist_list[stack])
    print(ecc)
   
    # ecc = max_distances(dist_list[stack])
    return recur((weights, visited), dist_list, ecc,stack)

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

def save_visited(visited, filename, graph_alist=None):
    """Save the visited array and adjacency list to a text file."""
    try:
        with open(filename, 'a') as f:  # Open in append mode
            f.write(','.join(map(str, visited)) + "\n")
            if graph_alist:
                f.write('Adjacency List: ' + str(graph_alist) + "\n\n")
        print(f"Visited state and adjacency list saved to {filename}")
    except IOError as e:
        print(f"Error saving visited state: {e}")

def load_visited(filename):
    """Load the visited array from a text file."""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                visited = list(map(int, f.read().strip().split(',')))
            print(f"Visited state loaded from {filename}")
            return visited
        except IOError as e:
            print(f"Error loading visited state: {e}")
    return None

graph_alist = [[1],[0,2,4,3],[1,5],[1],[1],[2]]
print("ADJ LIST", graph_alist)
# initial_visited = load_visited(SAVE_FILE) or [0] * len(graph_alist)
print("Final visited:", brute(graph_alist))

# print(dist_list)