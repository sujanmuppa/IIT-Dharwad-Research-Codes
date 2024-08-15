def generate_cycle_graph(num_vertices):
    """Generate an adjacency list for an undirected cycle graph."""
    if num_vertices < 3:
        raise ValueError("Number of vertices in a cycle graph must be at least 3.")
    
    graph_alist = [[] for _ in range(num_vertices)]
    for i in range(num_vertices):
        graph_alist[i].append((i + 1) % num_vertices)
        graph_alist[i].append((i - 1) % num_vertices)
    
    return graph_alist

def recur(adj_list, num_vertices, memo, output_file):
    """Recursively find all possible edge combinations inside the cycle graph"""
    adj_tuple = tuple(tuple(neighbors) for neighbors in adj_list)  # Convert adjacency list to tuple of tuples
    if adj_tuple in memo:
        return memo
    
    memo.add(adj_tuple)
    
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):  # Only consider adding edge once (i < j ensures no duplicate)
            if j not in adj_list[i]:  # Only add if edge doesn't already exist
                adj_list[i].append(j)
                adj_list[j].append(i)
                memo = recur(adj_list, num_vertices, memo, output_file)
                adj_list[i].remove(j)
                adj_list[j].remove(i)
    
    # Write the unique configuration to file
    with open(output_file, 'a') as f:
        f.write(str(adj_tuple) + '\n')
    
    return memo

def possibilities(num_vertices, output_file):
    """Find all possible edge combinations inside the cycle graph"""
    adj_list = generate_cycle_graph(num_vertices)
    memo = set()
    memo = recur(adj_list, num_vertices, memo, output_file)
    return memo

num_vertices = 7
output_file = 'combo.txt'
combinations = possibilities(num_vertices, output_file)
print("Number of Possible Combinations:", len(combinations))
print(f"Unique combinations written to '{output_file}'.")
