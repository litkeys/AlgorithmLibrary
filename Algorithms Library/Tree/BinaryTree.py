class BinaryTreeNode:
    def __init__(self, key, depth = 0):
        self.key = key # value of the node
        self.left = None # left child
        self.right = None # right child
        self.depth = depth # depth of the node, 0 is root node
    def setLeftChild(self, child: 'BinaryTreeNode'):
        child.depth = self.depth + 1 # automatically assigns depth
        self.left = child
    def setRightChild(self, child: 'BinaryTreeNode'):
        child.depth = self.depth + 1 # automatically assigns depth
        self.right = child
    def __repr__(self) -> str:
        return str(self.key)

class BinaryTree:

    """
    Traversal functions default to root node of the entire tree if root argument is missing
    If specified, the traversal would only be performed on that particular sub-branch 
    """

    def __init__(self, root: BinaryTreeNode = None):
        self.root = root # root of the entire tree

    # decorator, only applicable to non-static tree functions that accept root as a parameter
    def default_to_tree_root(tree_function): 
        def new_tree_function(self, *args, **kwargs):
            # args could be positional or keyword, assume that root is always the first positional argument
            if ("root" not in kwargs or kwargs["root"] == None) and len(args) == 0:
                kwargs["root"] = self.root
            return tree_function(self, *args, **kwargs)
        return new_tree_function

    @default_to_tree_root
    def preOrder(self, root: BinaryTreeNode = None) -> list[BinaryTreeNode]: # root, left child, right child
        if root == None:
            return []
        return [root] + self.preOrder(root.left) + self.preOrder(root.right)

    @default_to_tree_root
    def inOrder(self, root: BinaryTreeNode) -> list[BinaryTreeNode]: # left child, root, right child
        if root == None:
            return []
        return self.inOrder(root.left) + [root] + self.inOrder(root.right)

    @default_to_tree_root
    def postOrder(self, root: BinaryTreeNode) -> list[BinaryTreeNode]: # left child, right child, root
        if root == None:
            return []
        return self.postOrder(root.left) + self.postOrder(root.right) + [root]
    
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


# a = BinaryTreeNode("A")
# b = BinaryTreeNode("B")
# c = BinaryTreeNode("C")
# a.setLeftChild(b)
# a.setRightChild(c)
# # a.left = b
# # a.right = c

# tree = BinaryTree(a)
# #print(tree)

# print(tree.preOrder())
# print(tree.inOrder())
# print(tree.postOrder())
# print(tree.getDiameter())