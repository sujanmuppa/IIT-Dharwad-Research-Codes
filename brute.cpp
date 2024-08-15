#include <iostream>
#include <vector>
#include <stack>
#include <unordered_map>
#include <numeric>
#include <map>

using namespace std;

// Function to perform DFS to calculate distances from the start node
vector<int> dfs(const vector<vector<int>>& graph_alist, int start) {
    vector<bool> visited(graph_alist.size(), false);
    vector<int> distances(graph_alist.size(), 0);
    stack<int> s;
    s.push(start);
    visited[start] = true;
    
    while (!s.empty()) {
        int vertex = s.top();
        s.pop();
        for (int neighbor : graph_alist[vertex]) {
            if (!visited[neighbor]) {
                s.push(neighbor);
                visited[neighbor] = true;
                distances[neighbor] = distances[vertex] + 1;
            }
        }
    }
    
    return distances;
}

// Function to create a list of distances from each node to all other nodes
map<int, vector<int>> dist_list1(const vector<vector<int>>& graph_alist) {
    map<int, vector<int>> dist_list;
    for (int i = 0; i < graph_alist.size(); ++i) {
        dist_list[i] = dfs(graph_alist, i);
    }
    return dist_list;
}

// Hash function for vector<int>
struct VectorHash {
    size_t operator()(const vector<int>& v) const {
        size_t hash = 0;
        for (int num : v) {
            hash ^= std::hash<int>{}(num) + 0x9e3779b9 + (hash << 6) + (hash >> 2);
        }
        return hash;
    }
};

// Iterative function to process the graph and find the correct visited states
vector<int> recur(vector<int>& visited, vector<int>& weights, const map<int, vector<int>>& dist_list, unordered_map<vector<int>, vector<int>, VectorHash>& memo) {
    vector<int> stack = weights;
    while (!stack.empty()) {
        auto state = stack;
        if (memo.find(state) != memo.end()) {
            return memo[state];
        }
        
        for (int i = 0; i < weights.size(); ++i) {
            if (weights[i] == weights.size()) {
                visited[i] = 1;
                memo[state] = visited;
                return visited;
            }
        }
        
        for (auto it = dist_list.begin(); it != dist_list.end(); ++it) {
            int i = it->first;
            const vector<int>& dist = it->second;
            for (int j = 0; j < dist.size(); ++j) {
                if (dist[j] == weights[j] && weights[i] > 0) {
                    int original_i_weight = weights[i];
                    int original_j_weight = weights[j];
                    
                    weights[i] += weights[j];
                    weights[j] = 0;
                    stack = weights;
                    
                    vector<int> result = recur(visited, weights, dist_list, memo);
                    if (accumulate(result.begin(), result.end(), 0) > accumulate(visited.begin(), visited.end(), 0)) {
                        visited = result;
                    }
                    weights[j] = original_j_weight;  // Restore weights
                    weights[i] = original_i_weight;  // Restore weights
                }
            }
        }
        
        memo[state] = visited;
    }
    return visited;
}

// Function to solve the problem using brute force approach
vector<int> brute(const vector<vector<int>>& graph_alist) {
    vector<int> weights(graph_alist.size(), 1);
    map<int, vector<int>> dist_list = dist_list1(graph_alist);
    vector<int> visited(graph_alist.size(), 0);
    unordered_map<vector<int>, vector<int>, VectorHash> memo;
    return recur(visited, weights, dist_list, memo);
}

// Function to generate adjacency list for a perfect binary tree of given level
vector<vector<int>> neighbors(int level) {
    int no_of_nodes = (1 << level) - 1; // 2^level - 1
    vector<vector<int>> graph_alist(no_of_nodes);
    for (int i = 0; i < no_of_nodes; ++i) {
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        if (left < no_of_nodes) {
            graph_alist[i].push_back(left);
            graph_alist[left].push_back(i);
        }
        if (right < no_of_nodes) {
            graph_alist[i].push_back(right);
            graph_alist[right].push_back(i);
        }
    }
    return graph_alist;
}

int main() {
    vector<vector<int>> graph_alist = neighbors(5);
    vector<int> result = brute(graph_alist);
    cout << "Final visited: ";
    for (int v : result) cout << v << " ";
    cout << endl;
    return 0;
}
