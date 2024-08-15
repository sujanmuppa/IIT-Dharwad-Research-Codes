import sys
sys.setrecursionlimit(100000)

def dfs(graph_alist, start):
    visited = [(False, 0) for _ in range(len(graph_alist))]
    stack = [start]
    visited[start] = (True, 0)
    
    while stack:
        vertex = stack.pop()
        for neighbor in graph_alist[vertex]:
            if not visited[neighbor][0]:
                stack.append(neighbor)
                visited[neighbor] = (True, visited[vertex][1] + 1)
    
    return visited

def dist_list1(graph_alist):
    dist_list = {}
    for i in range(len(graph_alist)):
        temp = dfs(graph_alist, i)
        dist_list[i] = [(j, temp[j][1]) for j in range(len(temp)) if temp[j][0]]
    return dist_list

# Memoization wrapper function
def recur(visited, weights, dist_list, memo):
    state = (tuple(visited), tuple(weights))
    if state in memo:
        return memo[state]
    
    for i in range(len(weights)):
        if weights[i] == len(weights):
            visited[i] = 1
            memo[state] = visited[:]
            print(visited)
            return visited
    
    for i in dist_list:
        w1 = weights[i]
        for j in dist_list[i]:
            w2 = weights[j[0]]
            if j[1] == w2 and weights[i] != 0:
                weights[i] += weights[j[0]]
                weights[j[0]] = 0
                visited = recur(visited, weights, dist_list, memo)
                weights[j[0]] = w2
                weights[i] = w1
    
    memo[state] = visited[:]
    return visited

def brute(graph_alist):
    weights = [1 for _ in range(len(graph_alist))] # all weights are 1
    dist_list = dist_list1(graph_alist)
    visited = [0 for _ in range(len(dist_list))]
    memo = {}
    visited = recur(visited, weights, dist_list, memo)
    return visited


# print all the neighbours of a perfect binary tree 
def neighbors(level):
    no_of_nodes = 2**level - 1
    parent = -1
    graph_alist = [[] for _ in range(no_of_nodes)]
    for i in range(no_of_nodes):
        if i == 0:
            graph_alist[i] = [1, 2]
        else:
            left = 2*i + 1
            right = 2*i + 2
            parent = (i-1) // 2
            if left < no_of_nodes:
                graph_alist[i].append(left)
            if right < no_of_nodes:
                graph_alist[i].append(right)
            if parent >= 0:
                graph_alist[i].append(parent)
    return graph_alist

graph_alist = neighbors(5)
# graph_alist = [[1, 2], [3, 4, 0], [5, 6, 0], [7, 8, 1], [9, 10, 1], [11, 12, 2], [13, 14, 2], [15, 16, 3], [17, 18, 3], [19, 20, 4], [21, 22, 4], [23, 24, 5], [25, 26, 5], [27, 28, 6], [29, 30, 6], [7], [7], [8], [8], [9], [9], [10], [10], [11], [11], [12], [12], [13], [13], [14], [14]]


print(brute(graph_alist))
