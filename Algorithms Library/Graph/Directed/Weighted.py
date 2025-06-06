from copy import deepcopy
from collections import defaultdict
from heapq import *
from collections import deque

class DWGraph: # directed weighted simple graph
    
    """
    Graph Representations
    1. Adjacency list, a list where every index represents a node and contains a list representing the node's neighbours (and weight of the edge to that neighbour)
    2. Adjacency matrix, a 2D list where matrix[a][b] represents the weight of the edge from a to b, if there is one
    3. Edge list, an unordered list of edges in the form [a, b, w] representing an edge from a to b with weight w
    4. Adjacency table*, a dictionary version of adjacency list, useful when node names cannot be easily sorted

    Representation 4 will be the default representation of the graph within this class, due to its maximum compatibility.
    Sets are used to represent neighbours in place of tuples for maximum flexibility during runtime.

    The graph is directed, therefore edges are one-directional.
    """

    def __init__(self, AdjacencyTable) -> None:
        self.graph = AdjacencyTable
        self.nodecount = len(AdjacencyTable)

    # CONSTRUCTORS

    # ==============================================================================

    def construct_via_AdjacencyList(AdjacencyList) -> 'DWGraph':
        """
        Format:
        [[(node1, weight1), (node2, weight2), (node3, weight3)], [(node2, weight4)], ...]
        where inner lists contain neighbours and the weight of the edge to that neighbour

        Note that node names are not supported by this method.
        Therefore indexes are assigned to the name of each node.
        Nodes with an out degree of 0 are represented in the adjacency list, therefore additional entries are not required.
        """
        l = len(AdjacencyList)
        AdjacencyList = [[tuple(neighbour) for neighbour in AdjacencyList[i]] for i in range(l)] # auto-convert to tuple
        AdjacencyTable = {}
        for i in range(l):
            AdjacencyTable[i] = set(AdjacencyList[i])            
        return DWGraph(AdjacencyTable)

    def construct_via_AdjacencyMatrix(AdjacencyMatrix) -> 'DWGraph':
        """
        Format:
        [
            [2, None, 5], 
            [3, 1, None], 
            ...
        ]
        where matrix[a][b] contains a numeric value representing the weight of the edge from a to b, or None if edge does not exist

        Note that node names are not supported by this method.
        Therefore indexes are assigned to the name of each node.
        Nodes with an out degree of 0 are not represented in the adjacency list, therefore additional entries are required.
        """
        l = len(AdjacencyMatrix)
        AdjacencyTable = {}
        all_nodes = {i for i in range(l)}
        included_nodes = set()
        for i in range(l):
            AdjacencyTable[i] = set((j, AdjacencyMatrix[i][j]) for j in range(l) if AdjacencyMatrix[i][j] != None)
            included_nodes.add(i)
        for node in all_nodes: # make empty entries for nodes with an out degree of 0
            if node not in included_nodes:
                AdjacencyTable[node] = set()
        return DWGraph(AdjacencyTable)

    def construct_via_EdgeList(EdgeList) -> 'DWGraph':
        """
        Format:
        [[node1, node2, weight1], [node2, node3, weight2] ...]
        where inner lists contain edges between two nodes and the weight of the edge

        Note that node names are supported by this method.
        Nodes with an out degree of 0 are not represented in the adjacency list, therefore additional entries are required.
        """
        AdjacencyTable = {}
        all_nodes = set()
        included_nodes = set()
        for node1, node2, weight in EdgeList:
            all_nodes.add(node1)
            all_nodes.add(node2)
        for edge in EdgeList:
            srcNode, dstNode, weight = edge
            if srcNode in AdjacencyTable:
                AdjacencyTable[srcNode].add((dstNode, weight))
            else:
                AdjacencyTable[srcNode] = {(dstNode, weight)}
            included_nodes.add(srcNode)
        for node in all_nodes: # make empty entries for nodes with an out degree of 0
            if node not in included_nodes:
                AdjacencyTable[node] = set()
        return DWGraph(AdjacencyTable)

    def construct_via_AdjacencyTable(AdjacencyTable) -> 'DWGraph':
        """
        Format:
        {node0: {(node1, weight1), (node2, weight2), (node3, weight3)}, node1: {(node2, weight4)}, ...}
        where inner lists contain neighbours and the weight of the edge to that neighbour

        Note that node names are supported by this method.
        Nodes with an out degree of 0 are represented in the adjacency list, therefore additional entries are not required.
        """
        return DWGraph(AdjacencyTable)

    # ==============================================================================

    # CONVERTERS

    def convert_to_bidirectional(self, defaultweight=None) -> 'DWGraph': # returns a new graph
        """
        Necessary for bipartite property check.
        Every edge becomes bi-directional after conversion, with duplicated weights.
        Runs in O(VE) time.
        Note that if two (or more) edges already exist between two nodes, duplicate edges will still be created.
        """
        newgraph = deepcopy(self.graph)
        for node in newgraph:
            for neighbour, weight in newgraph[node]:
                if defaultweight:
                    newgraph[neighbour].add((node, defaultweight))
                else:
                    newgraph[neighbour].add((node, weight))
        return DWGraph.construct_via_AdjacencyTable(newgraph)
    
    # ==============================================================================

    # TRAVERSALS

    def dijkstras(self, srcNode): # dijkstra's algorithm
        """
        Returns a dictionary where keys are destination nodes and values are minimum weights/costs
        """
        ordered_costs = {}
        heap = [(0, srcNode)]
        while heap:
            cost, current_node = heappop(heap)
            if current_node in ordered_costs:
                continue
            ordered_costs[current_node] = cost
            for neighbour, newcost in self.graph[current_node]:
                heappush(heap, (cost + newcost, neighbour))
        return ordered_costs

    def bellman_fords(self, srcNode): # belmann ford's algorithm, use this when edges have negative weights
        """
        Returns a dictionary where keys are destination nodes and values are minimum weights/costs
        """
        ordered_costs = {node: float("inf") for node in self.graph}
        ordered_costs[srcNode] = 0
        for i in range(self.nodecount-1):
            for node in self.graph:
                if ordered_costs[node] != float("inf"):
                    for neighbour, newcost in self.graph[node]:
                        ordered_costs[neighbour] = min(ordered_costs[neighbour], ordered_costs[node] + newcost)
        return ordered_costs

    def find_path(self, srcNode, dstNode, artificial_weights: dict[dict] = None): # bfs
        """
        Path includes srcNode and dstNode
        O(n) space complexity using dicationary backtracking to reconstruct path
        Artificial weights are used by max flow function to avoid reconstructing graph
        """
        prev_node = {srcNode: None} # maps each node to the previous node for path construction
        queue = deque([srcNode])
        visited = set()
        while queue:
            node = queue.pop()
            visited.add(node)
            for neighbour, weight in self.graph[node]:
                # only paths with positive capcities are considered
                if artificial_weights and artificial_weights[node][neighbour] <= 0:
                    continue
                elif weight <= 0: 
                    continue
                # dstNode has been reached, a path has been found
                if neighbour == dstNode: 
                    path = [dstNode, node]
                    pathnode = node
                    while prev_node[pathnode]:
                        pathnode = prev_node[pathnode]
                        path.append(pathnode)
                    return path[::-1]
                # add neighbour to queue
                if neighbour not in visited: 
                    prev_node[neighbour] = node
                    queue.appendleft(neighbour)
        return None # no path has been found
    
    # ==============================================================================

    # MAX FLOW & MIN CUT

    def max_flow(self, source, sink) -> int: # ford-fulkerson algorithm
        """
        Returns the max flow / min cut of the current graph
        Parameters source and sink are the source and sink of the graph
        BFS is used to find a path from the sink to the node each time
        NOTE: Does not work if there are two (or more) edges between two nodes in the graph
        """
        specialgraph = self.convert_to_bidirectional(defaultweight=0)
        artificial_weights = {node: {edge[0]: edge[1] for edge in specialgraph.graph[node]} for node in specialgraph.graph}
        total_flow = 0
        while True:
            # construct path from source to sink
            path = specialgraph.find_path(source, sink, artificial_weights=artificial_weights)
            if not path:
                return total_flow
            # find minimum capacity along the path
            min_capacity = float("inf")
            for i in range(len(path)-1):
                min_capacity = min(min_capacity, artificial_weights[path[i]][path[i+1]])
            # update capcities
            for i in range(len(path)-1):
                artificial_weights[path[i]][path[i+1]] -= min_capacity
                artificial_weights[path[i+1]][path[i]] += min_capacity
            # update total flow
            total_flow += min_capacity
    
    # ==============================================================================

    # TOPOLOGICAL SORT

    def _topological_sort(self, node, visited: dict, stack: list):
        visited[node] = True
        for neighbour, weight in self.graph[node]:
            if visited[neighbour] == False:
                self._topological_sort(neighbour, visited, stack)
        stack.append(node)

    def topological_sort(self):
        visited = defaultdict(lambda: False)
        stack = []
        for node in self.graph:
            if visited[node] == False:
                self._topological_sort(node, visited, stack)
        return stack[::-1]
    
    # ==============================================================================

    # PROPERTY CHECKS

    def is_bipartite(self) -> bool:
        """
        Detects cycles of odd length using dfs
        Each node is assigned a depth upon exploration
        When a visited node is encountered, compare its depth with that of the source node
        If the difference is even, then the graph is not bipartite

        NOTE: Remember to firstly convert (a copy of) the graph to bidirectional first
        Runs in O(V+E) time 
        """
        srcNode = tuple(self.graph.keys())[0] # any starting node would work
        visited = dict() # node: depth
        stack = [(srcNode, 0)]
        while stack:
            current_node, depth = stack.pop()
            visited[current_node] = depth
            for neighbour, weight in self.graph[current_node]:
                if neighbour in visited:
                    diff = depth - visited[neighbour]
                    if not diff % 2:
                        return False
                else:
                    stack.append((neighbour, depth+1))
        return True



# mygraph = DWGraph.construct_via_EdgeList([("A", "B", 3), ("A", "C", 1), ("C", "B", 4), ("C", "D", 1)])
# print(mygraph.dijkstras("A"))
# print(mygraph.convert_to_bidirectional().is_bipartite()) # False

# mygraph = DWGraph.construct_via_EdgeList([("A", "B", 3), ("B", "C", 1), ("C", "A", 4), ("C", "D", 1)])
# print(mygraph.convert_to_bidirectional().is_bipartite()) # False

# mygraph = DWGraph.construct_via_EdgeList([("A", "B", 1), ("B", "D", 1), ("A", "C", 10), ("C", "D", -10)])
# print(mygraph.dijkstras("A"))
# print(mygraph.bellman_fords("A"))
# print(mygraph.convert_to_bidirectional().is_bipartite()) # True

# mygraph = DWGraph.construct_via_EdgeList([(4, 1, 1), (4, 5, 2), (1, 2, 3), (5, 2, 5), (2, 3, 3), (5, 3, 4), (3, 6, 1)])
# print(mygraph.topological_sort())

# mygraph = DWGraph.construct_via_EdgeList([(1, 2, 5), (1, 4, 4), (4, 2, 3), (2, 3, 6), (4, 5, 1), (3, 5, 8), (3, 6, 5), (5, 6, 2)])
# print(mygraph.max_flow(1, 6))