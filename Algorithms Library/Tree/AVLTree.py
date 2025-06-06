import sys

class AVLTreeNode:
    def __init__(self, key):
        self.key = key # value of the node
        self.left = None # left child
        self.right = None # right child
        self.height = 1 # height of the node, 1 is the lowest leaf node
    def __repr__(self) -> str:
        return str(self.key)


class AVLTree:

    """
    Note:
    AVL Tree is a self-balancing binary search tree
    It performs better for frequent searches compared to Red Black Trees
    All tree nodes should be inserted into the tree rather than assigning their own children.
    All keys must be distinct, meaning duplicates are not allowed
    All modifications i.e. insertion and deletion MUST occur at root of the tree
    """

    def __init__(self):
        self.root = None # root of the entire tree

    # decorator, only applicable to non-static tree functions that accept root as a parameter
    def default_to_tree_root(tree_function): 
        def new_tree_function(self, *args, **kwargs):
            # args could be positional or keyword, assume that root is always the first positional argument
            if ("root" not in kwargs or kwargs["root"] == None) and len(args) == 0:
                kwargs["root"] = self.root
            return tree_function(self, *args, **kwargs)
        return new_tree_function

    # CORE FUNCTIONS

    # ==============================================================================

    # Function to insert a node, returns the updated root
    def __insert_node(self, root: AVLTreeNode, key) -> AVLTreeNode:

        # Find the correct location and insert the node
        if not root:
            return AVLTreeNode(key)
        elif key < root.key:
            root.left = self.__insert_node(root.left, key)
        else:
            root.right = self.__insert_node(root.right, key)

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        # Update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)
        if balanceFactor > 1:
            if key < root.left.key:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)

        if balanceFactor < -1:
            if key > root.right.key:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        
        return root
    
    def insert_node(self, key) -> AVLTreeNode: # Call this to insert a node
        self.root = self.__insert_node(self.root, key)
        return self.root

    # Function to delete a node, returns the updated root
    def __delete_node(self, root: AVLTreeNode, key) -> AVLTreeNode:

        # Find the node to be deleted and remove it
        if not root:
            return root
        elif key < root.key:
            root.left = self.__delete_node(root.left, key)
        elif key > root.key:
            root.right = self.__delete_node(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.getMinValueNode(root.right)
            root.key = temp.key
            root.right = self.__delete_node(root.right, temp.key)
        if root is None:
            return root

        # Update the balance factor of nodes
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        balanceFactor = self.getBalance(root)

        # Balance the tree
        if balanceFactor > 1:
            if self.getBalance(root.left) >= 0:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balanceFactor < -1:
            if self.getBalance(root.right) <= 0:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
            
        return root
    
    def delete_node(self, key) -> AVLTreeNode: # Call this to delete a node
        self.root = self.__delete_node(self.root, key)
        return self.root

    # Function to perform left rotation
    def leftRotate(self, z: AVLTreeNode) -> AVLTreeNode:
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    # Function to perform right rotation
    def rightRotate(self, z: AVLTreeNode) -> AVLTreeNode:
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y
    
    # Get the height of the node
    def getHeight(self, root: AVLTreeNode):
        if not root:
            return 0
        return root.height

    # Get balance factore of the node
    def getBalance(self, root: AVLTreeNode):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    # Function to search the tree for a node that contains a particular key, returns the node
    def __searchNode(self, root: AVLTreeNode, key) -> AVLTreeNode:
        if root == None or root.key == key:
            return root
        if key < root.key:
            return self.searchTree(root.left, key)
        else:
            return self.searchTree(root.right, key)
        
    def searchNode(self, key) -> AVLTreeNode: # Call this to search for a node with a particular key
        return self.__searchNode(self.root, key)
    
    # ==============================================================================

    # PRIORITY QUEUE RELATED FUNCTIONS

    # Get min value in O(log n) time
    @default_to_tree_root
    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)

    # Get max value in O(log n) time
    @default_to_tree_root
    def getMaxValueNode(self, root):
        if root is None or root.right is None:
            return root
        return self.getMaxValueNode(root.right)
    
    # ==============================================================================

    # TRAVERSALS

    @default_to_tree_root
    def preOrder(self, root: AVLTreeNode):
        if root == None:
            return []
        return [root] + self.preOrder(root.left) + self.preOrder(root.right)

    @default_to_tree_root
    def inOrder(self, root: AVLTreeNode):
        if root == None:
            return []
        return self.preOrder(root.left) + [root] + self.preOrder(root.right)

    @default_to_tree_root
    def postOrder(self, root: AVLTreeNode):
        if root == None:
            return []
        return self.preOrder(root.left) + self.preOrder(root.right) + [root]
    
    def getDiameter(self) -> int: # maximum distance from one treenode to another
        branch_diameters = []
        for subroot in (self.root.left, self.root.right):
            stack = [(subroot, 1)] # node, depth
            visited = set()
            diameter = 0
            while stack:
                node, depth = stack.pop()
                visited.add(node) # objects are hashable
                if not node.left and not node.right:
                    diameter = max(diameter, depth)
                for childnode in (node.left, node.right):
                    if childnode != None:
                        stack.append((childnode, depth+1))
            branch_diameters.append(diameter)
        return sum(branch_diameters) + 1

    # ==============================================================================

    # TREE DISPLAY FUNCTIONS

    # Print the tree
    def __printTree(self, currPtr, indent, last):
        if currPtr != None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print(currPtr.key)
            self.__printTree(currPtr.left, indent, False)
            self.__printTree(currPtr.right, indent, True)

    def printTree(self): # Call this to print the Tree in a vertical format
        self.__printTree(self.root, "", True)


# myTree = AVLTree()
# root = None
# nums = [33, 13, 52, 9, 21, 61, 8, 11]
# for num in nums:
#     root = myTree.insert_node(num)
# myTree.printTree()
# key = 13
# root = myTree.delete_node(key)
# print("After Deletion: ")
# myTree.printTree()

# myTree = AVLTree()
# root = None
# nums = [33, 13, 52, 9, 21, 61, 8, 11]
# for num in nums:
#     root = myTree.insert_node(num)

# print(myTree.preOrder(root))
# myTree.printTree()
# print(myTree.getDiameter())