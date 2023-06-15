from copy import deepcopy
from heapq import *

class UWGraph: # undirected weighted simple graph
    
    """
    Graph Representations
    1. Adjacency list, a list where every index represents a node and contains a list representing the node's neighbours (and weight of the edge to that neighbour)
    2. Adjacency matrix, a 2D list where matrix[a][b] represents the weight of the edge from a to b, if there is one
    3. Edge list, an unordered list of edges in the form [a, b, w] representing an edge from a to b with weight w
    4. Adjacency table*, a dictionary version of adjacency list, useful when node names cannot be easily sorted

    Representation 4 will be the default representation of the graph within this class, due to its maximum compatibility.
    Sets are used to represent neighbours in place of tuples for maximum flexibility during runtime.

    Note that due to the graph being undirected, each edge is bi-directional i.e. edge from a to b automatically spawns edge from b to a.
    """

    def __init__(self, AdjacencyTable) -> None:
        self.graph = AdjacencyTable
        self.nodecount = len(AdjacencyTable)

    # CONSTRUCTORS

    # ==============================================================================

    def construct_via_AdjacencyList(AdjacencyList) -> 'UWGraph':
        """
        Format:
        [[(node1, weight1), (node2, weight2), (node3, weight3)], [(node2, weight4)], ...]
        where inner lists contain neighbours and the weight of the edge to that neighbour

        Note that node names are not supported by this method.
        Therefore indexes are assigned to the name of each node.
        """
        l = len(AdjacencyList)
        AdjacencyList = [[tuple(neighbour) for neighbour in AdjacencyList[i]] for i in range(l)] # auto-convert to tuple
        AdjacencyTable = {}
        for i in range(l):
            AdjacencyTable[i] = set(AdjacencyList[i])
        newAdjacencyTable = deepcopy(AdjacencyTable)
        for node in AdjacencyTable: # make edge bi-directional
            for neighbour, weight in AdjacencyTable[node]:
                if neighbour in newAdjacencyTable:
                    newAdjacencyTable[neighbour].add((node, weight))
                else:
                    newAdjacencyTable[neighbour] = {(node, weight)}
        return UWGraph(newAdjacencyTable)

    def construct_via_AdjacencyMatrix(AdjacencyMatrix) -> 'UWGraph':
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
        """
        l = len(AdjacencyMatrix)
        AdjacencyTable = {}
        for i in range(l):
            AdjacencyTable[i] = set((j, AdjacencyMatrix[i][j]) for j in range(l) if AdjacencyMatrix[i][j] != None)
        newAdjacencyTable = deepcopy(AdjacencyTable)
        for node in AdjacencyTable: # make edge bi-directional
            for neighbour, weight in AdjacencyTable[node]:
                if neighbour in newAdjacencyTable:
                    newAdjacencyTable[neighbour].add((node, weight))
                else:
                    newAdjacencyTable[neighbour] = {(node, weight)}
        return UWGraph(newAdjacencyTable)

    def construct_via_EdgeList(EdgeList) -> 'UWGraph':
        """
        Format:
        [[node1, node2, weight1], [node2, node3, weight2] ...]
        where inner lists contain edges between two nodes and the weight of the edge

        Note that node names are supported by this method.
        """
        AdjacencyTable = {}
        for edge in EdgeList:
            srcNode, dstNode, weight = edge
            if srcNode in AdjacencyTable:
                AdjacencyTable[srcNode].add((dstNode, weight))
            else:
                AdjacencyTable[srcNode] = {(dstNode, weight)}
        newAdjacencyTable = deepcopy(AdjacencyTable)
        for node in AdjacencyTable: # make edge bi-directional
            for neighbour, weight in AdjacencyTable[node]:
                if neighbour in newAdjacencyTable:
                    newAdjacencyTable[neighbour].add((node, weight))
                else:
                    newAdjacencyTable[neighbour] = {(node, weight)}
        return UWGraph(newAdjacencyTable)

    def construct_via_AdjacencyTable(AdjacencyTable) -> 'UWGraph':
        """
        Format:
        {node0: {(node1, weight1), (node2, weight2), (node3, weight3)}, node1: {(node2, weight4)}, ...}
        where inner lists contain neighbours and the weight of the edge to that neighbour

        Note that node names are supported by this method.
        """
        newAdjacencyTable = deepcopy(AdjacencyTable)
        for node in AdjacencyTable: # make edge bi-directional
            for neighbour, weight in AdjacencyTable[node]:
                if neighbour in newAdjacencyTable:
                    newAdjacencyTable[neighbour].add((node, weight))
                else:
                    newAdjacencyTable[neighbour] = {(node, weight)}
        return UWGraph(newAdjacencyTable)
    
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
    
    # Note that Bellman Ford's is not supported in undirected graphs with negative edge weights
    # This is due to the fact that any edge with a negative weight forms a negative cycle
    
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
    

if __name__ == "__main__":

    mygraph = UWGraph.construct_via_EdgeList([("A", "B", 3), ("A", "C", 1), ("C", "B", 4), ("C", "D", 1)])
    print(mygraph.dijkstras("A"))
    print(mygraph.is_bipartite())