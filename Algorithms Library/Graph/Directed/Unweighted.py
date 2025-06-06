from copy import deepcopy
from collections import defaultdict

class DUGraph: # directed unweighted simple graph
    
    """
    Graph Representations
    1. Adjacency list, a list where every index represents a node and contains a list representing the node's neighbours
    2. Adjacency matrix, a 2D list where matrix[a][b] represents if there is an edge from a to b
    3. Edge list, an unordered list of edges in the form [a, b] representing an edge from a to b
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

    def construct_via_AdjacencyList(AdjacencyList) -> 'DUGraph':
        """
        Format:
        [[node1, node2, node3], [node2, node4], ...]
        where inner lists contain neighbours

        Note that node names are not supported by this method.
        Therefore indexes are assigned to the name of each node.
        Nodes with an out degree of 0 are represented in the adjacency list, therefore additional entries are not required.
        """
        AdjacencyTable = {}
        for i in range(len(AdjacencyList)):
            AdjacencyTable[i] = set(AdjacencyList[i])
        return DUGraph(AdjacencyTable)

    def construct_via_AdjacencyMatrix(AdjacencyMatrix) -> 'DUGraph':
        """
        Format:
        [
            [1, 0, 1], 
            [1, 1, 0], 
            ...
        ]
        where matrix[a][b] contains 1 if there is an edge from a to b and 0 if there is no edge between them

        Note that node names are not supported by this method.
        Therefore indexes are assigned to the name of each node.
        Nodes with an out degree of 0 are not represented in the adjacency list, therefore additional entries are required.
        """
        l = len(AdjacencyMatrix)
        AdjacencyTable = {}
        all_nodes = {i for i in range(l)}
        included_nodes = set()
        for i in range(l):
            AdjacencyTable[i] = set(j for j in range(l) if AdjacencyMatrix[i][j] != 0)
            included_nodes.add(i)
        for node in all_nodes: # make empty entries for nodes with an out degree of 0
            if node not in included_nodes:
                AdjacencyTable[node] = set()
        return DUGraph(AdjacencyTable)

    def construct_via_EdgeList(EdgeList) -> 'DUGraph':
        """
        Format:
        [[node1, node2], [node2, node3] ...]
        where inner lists contain edges between two nodes

        Note that node names are supported by this method.
        Nodes with an out degree of 0 are not represented in the adjacency list, therefore additional entries are required.
        """
        AdjacencyTable = {}
        all_nodes = set()
        included_nodes = set()
        for node1, node2 in EdgeList:
            all_nodes.add(node1)
            all_nodes.add(node2)
        for edge in EdgeList:
            srcNode, dstNode = edge
            if srcNode in AdjacencyTable:
                AdjacencyTable[srcNode].add(dstNode)
            else:
                AdjacencyTable[srcNode] = {dstNode}
            included_nodes.add(srcNode)
        for node in all_nodes: # make empty entries for nodes with an out degree of 0
            if node not in included_nodes:
                AdjacencyTable[node] = set()
        return DUGraph(AdjacencyTable)

    def construct_via_AdjacencyTable(AdjacencyTable) -> 'DUGraph':
        """
        Format:
        {node0: {node1, node2, node3}, node1: {node2, node4}, ...}
        where inner lists contain neighbours

        Note that node names are supported by this method.
        Nodes with an out degree of 0 are represented in the adjacency list, therefore additional entries are not required.
        """
        return DUGraph(AdjacencyTable)

    # ==============================================================================

    # CONVERTERS

    def convert_to_bidirectional(self) -> 'DUGraph': # returns a new graph
        """
        Necessary for bipartite property check.
        Every edge becomes bi-directional after conversion.
        Runs in O(VE) time.
        """
        newgraph = deepcopy(self.graph)
        for node in newgraph:
            for neighbour in newgraph[node]:
                newgraph[neighbour].add(node)
        return DUGraph.construct_via_AdjacencyTable(newgraph)
    
    # ==============================================================================

    # TRAVERSALS

    def dfs(self, srcNode): # depth first search from srcNode
        order = []
        stack = [srcNode]
        visited = set()
        while stack:
            current_node = stack.pop()
            if current_node in visited:
                continue
            visited.add(current_node)
            order.append(current_node)
            for neighbour in self.graph[current_node]:
                stack.append(neighbour)
        return order
    
    def bfs(self, srcNode): # breadth first search from srcNode
        order = []
        queue = [srcNode]
        visited = set()
        while queue:
            current_node = queue.pop()            
            if current_node in visited:
                continue
            visited.add(current_node)
            order.append(current_node)
            for neighbour in self.graph[current_node]:
                queue.insert(0, neighbour)
        return order
    
    # ==============================================================================

    # TOPOLOGICAL SORT

    def _topological_sort(self, node, visited: dict, stack: list):
        visited[node] = True
        for neighbour in self.graph[node]:
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
            for neighbour in self.graph[current_node]:
                if neighbour in visited:
                    diff = depth - visited[neighbour]
                    if not diff % 2:
                        return False
                else:
                    stack.append((neighbour, depth+1))
        return True



# mygraph = DUGraph.construct_via_EdgeList([("A", "B"), ("A", "C"), ("C", "B"), ("C", "D")])
# print(mygraph.dfs("A"))
# print(mygraph.bfs("A"))
# print(mygraph.convert_to_bidirectional().is_bipartite()) # False

# mygraph = DUGraph.construct_via_AdjacencyList([(1, 2), (2,), (3, 4), {}, {}])
# print(mygraph.dfs(0))
# print(mygraph.bfs(0))
# print(mygraph.convert_to_bidirectional().is_bipartite()) # False

# mygraph = DUGraph.construct_via_EdgeList([(4, 1), (4, 5), (1, 2), (5, 2), (2, 3), (5, 3), (3, 6)])
# print(mygraph.topological_sort())