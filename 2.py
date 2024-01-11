def compute_minimum_cost_child_nodes(node, h, graph):
    min_cost = float('inf')
    min_cost_nodes = []

    for info_list in graph[node]:
        cost, nodes = sum(h[c] + w for c, w in info_list), [c for c, _ in info_list]
        

        if cost < min_cost:
            min_cost = cost
            min_cost_nodes = nodes

    return min_cost, min_cost_nodes


def aostar(status, h, graph, solution, node):
    
    
    print("HEURISTIC VALUES :", h)
    print("SOLUTION GRAPH :", solution)
    print("PROCESSING NODE :", node)
    print("-----------------------------------------------------------------------------------------")
    
    
    if status[node] >= 0:
        min_cost, child_nodes = compute_minimum_cost_child_nodes(node, h, graph)

        h[node] = min_cost
        status[node] = len(child_nodes)
        solved = all(status[child] != -1 for child in child_nodes)

        for child in child_nodes:
            parent[child] = node

        if solved:
            status[node] = -1
            solution[node] = child_nodes

        if node != start:
            aostar(status, h, graph, solution, parent[node])

        for child in child_nodes:
            status[child] = 0
            aostar(status, h, graph, solution, child)


h = {'A': 1, 'B': 6, 'C': 2, 'D': 12, 'E': 2, 'F': 1, 'G': 5, 'H': 7, 'I': 7, 'J': 1}

graph = {
    'A': [[('B', 1), ('C', 1)], [('D', 1)]],
    'B': [[('G', 1)], [('H', 1)]],
    'C': [[('J', 1)]],
    'D': [[('E', 1), ('F', 1)]],
    'G': [[('I', 1)]],
    'I': [],
    'J': []
}

start = 'A'

parent = {}

status = {node: 0 for node in h}

solution = {}

aostar(status, h, graph, solution, start)

print("SOLUTION GRAPH:", solution)
