# Description: This file contains the functions that will be used to solve the problem.
import sys
sys.setrecursionlimit(100000)
def dfs(graph_alist, start):
    visited = [(False,0) for i in range (len(graph_alist))]
    stack = []
    stack.append(start)
    visited[start] = (True,0)
    while stack:
        vertex = stack.pop()
        for i in graph_alist[vertex]:
            if visited[i][0] == False:
                stack.append(i)
                visited[i] = (True, visited[vertex][1]+1)
    return visited

graph_alist = [[1,2],[0,3,4],[0,5,6],[1,7,8],[1,9,10],[2,11,12],[2,13,14],[3],[3],[4],[4],[5],[5],[6],[6]]
def dist_list1(graph_alist):
    dist_list = {}
    for i in range (len(graph_alist)):
        temp = dfs(graph_alist,i)
        dist_list[i] = []
        for j in range (len(temp)):
            if temp[j][0] == True:
                dist_list[i].append((j,temp[j][1]))
    return dist_list


def recur(visited, weights, dist_list,ecc):
    for i in range(len(weights)):
        if weights[i]>ecc:
            return visited
        if weights[i] == len(weights):
            visited[i] = 1
            # print(visited)
            return visited

    for i in dist_list:
        w1 = weights[i]
        for j in dist_list[i]:
            w2 = weights[j[0]]
            if j[1] == w2 and weights[i] != 0:
                weights[i] += weights[j[0]]
                weights[j[0]] = 0
                visited = recur(visited,weights,dist_list)
                weights[j[0]] = w2
                weights[i] = w1
    
    # print(visited)
    return visited

    

def brute(graph_alist):
    weights = [1 for i in range (len(graph_alist))] # all weights are 1
    stack=0
    dist_list = {}
    dist_list = dist_list1(graph_alist)
    ecc = 0
    for i in dist_list[stack]:
        ecc = max(ecc,i[1])
    visited = [0 for i in range (len(dist_list))]
    visited = recur(visited,weights,dist_list,ecc)
    return visited


print(brute(graph_alist))