from heapq import *

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
    
    # ==============================================================================

    # PROPERTY CHECKS

    def is_bipartite(self) -> bool:
        """
        Detects cycles of odd length using dfs
        Each node is assigned a depth upon exploration
        When a visited node is encountered, compare its depth with that of the source node
        If the difference is even, then the grahh is not bipartite
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
    

# if __name__ == "__main__":

#     mygraph = DWGraph.construct_via_EdgeList([("A", "B", 3), ("A", "C", 1), ("C", "B", 4), ("C", "D", 1)])
#     print(mygraph.dijkstras("A"))
#     print(mygraph.is_bipartite())

#     mygraph = DWGraph.construct_via_EdgeList([("A", "B", 3), ("B", "C", 1), ("C", "A", 4), ("C", "D", 1)])
#     print(mygraph.is_bipartite())

#     mygraph = DWGraph.construct_via_EdgeList([("A", "B", 1), ("B", "D", 1), ("A", "C", 10), ("C", "D", -10)])
#     print(mygraph.dijkstras("A"))
#     print(mygraph.bellman_fords("A"))
#     print(mygraph.is_bipartite())