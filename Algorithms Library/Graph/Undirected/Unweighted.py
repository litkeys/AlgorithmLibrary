from copy import deepcopy

class UUGraph: # undirected unweighted simple graph
    
    """
    Graph Representations
    1. Adjacency list, a list where every index represents a node and contains a list representing the node's neighbours
    2. Adjacency matrix, a 2D list where matrix[a][b] represents if there is an edge from a to b
    3. Edge list, an unordered list of edges in the form [a, b] representing an edge from a to b
    4. Adjacency table*, a dictionary version of adjacency list, useful when node names cannot be easily sorted

    Representation 4 will be the default representation of the graph within this class, due to its maximum compatibility.
    Sets are used to represent neighbours in place of tuples for maximum flexibility during runtime.

    Note that due to the graph being undirected, each edge may appear more than once in the internal representation.
    """

    def __init__(self, AdjacencyTable) -> None:
        self.graph = AdjacencyTable

    # CONSTRUCTORS

    # ==============================================================================

    def construct_via_AdjacencyList(AdjacencyList) -> 'UUGraph':
        """
        Format:
        [[node1, node2, node3], [node2, node4], ...]
        where inner lists contain neighbours

        Note that node names are not supported by this method.
        Therefore indexes are assigned to the name of each node.
        """
        AdjacencyTable = {}
        for i in range(len(AdjacencyList)):
            AdjacencyTable[i] = set(AdjacencyList[i])
        newAdjacencyTable = deepcopy(AdjacencyTable)
        for node in AdjacencyTable: # make edge bi-directional
            for neighbour in AdjacencyTable[node]:
                if neighbour in newAdjacencyTable:
                    newAdjacencyTable[neighbour].add(node)
                else:
                    newAdjacencyTable[neighbour] = {node}
        return UUGraph(newAdjacencyTable)

    def construct_via_AdjacencyMatrix(AdjacencyMatrix) -> 'UUGraph':
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
        """
        AdjacencyTable = {}
        l = len(AdjacencyMatrix)
        for i in range(l):
            AdjacencyTable[i] = set(j for j in range(l) if AdjacencyMatrix[i][j] != 0)
        newAdjacencyTable = deepcopy(AdjacencyTable)
        for node in AdjacencyTable: # make edge bi-directional
            for neighbour in AdjacencyTable[node]:
                if neighbour in newAdjacencyTable:
                    newAdjacencyTable[neighbour].add(node)
                else:
                    newAdjacencyTable[neighbour] = {node}
        return UUGraph(newAdjacencyTable)

    def construct_via_EdgeList(EdgeList) -> 'UUGraph':
        """
        Format:
        [[node1, node2], [node2, node3] ...]
        where inner lists contain edges between two nodes

        Note that node names are supported by this method.
        """
        AdjacencyTable = {}
        for edge in EdgeList:
            srcNode, dstNode = edge
            if srcNode in AdjacencyTable:
                AdjacencyTable[srcNode].add(dstNode)
            else:
                AdjacencyTable[srcNode] = {dstNode}
        newAdjacencyTable = deepcopy(AdjacencyTable)
        for node in AdjacencyTable: # make edge bi-directional
            for neighbour in AdjacencyTable[node]:
                if neighbour in newAdjacencyTable:
                    newAdjacencyTable[neighbour].add(node)
                else:
                    newAdjacencyTable[neighbour] = {node}
        return UUGraph(newAdjacencyTable)

    def construct_via_AdjacencyTable(AdjacencyTable) -> 'UUGraph':
        """
        Format:
        {[node1, node2, node3], [node2, node4], ...}
        where inner lists contain neighbours

        Note that node names are supported by this method.
        """
        newAdjacencyTable = deepcopy(AdjacencyTable)
        for node in AdjacencyTable: # make edge bi-directional
            for neighbour in AdjacencyTable[node]:
                if neighbour in newAdjacencyTable:
                    newAdjacencyTable[neighbour].add(node)
                else:
                    newAdjacencyTable[neighbour] = {node}
        return UUGraph(newAdjacencyTable)
    
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
            for neighbour in self.graph[current_node]:
                if neighbour in visited:
                    diff = depth - visited[neighbour]
                    if not diff % 2:
                        return False
                else:
                    stack.append((neighbour, depth+1))
        return True
    

# if __name__ == "__main__":

#     mygraph = UUGraph.construct_via_EdgeList([("A", "B"), ("A", "C"), ("C", "B"), ("C", "D")])
#     print(mygraph.dfs("A"))
#     print(mygraph.bfs("A"))
#     print(mygraph.is_bipartite())
#     mygraph = UUGraph.construct_via_AdjacencyList([(1, 2), (2,), (3, 4), {}, {}])
#     print(mygraph.dfs(0))
#     print(mygraph.bfs(0))
#     print(mygraph.is_bipartite())