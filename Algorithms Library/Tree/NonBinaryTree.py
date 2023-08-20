class TreeNode:
    def __init__(self, key, depth = 0):
        self.key = key # value of the node
        self.children = [] # children of the node
        self.depth = depth # depth of the node, 0 is root node
    def addChildren(self, *children: list['TreeNode']):
        for child in children:
            child.depth = self.depth + 1 # automatically assigns depth
            self.children.append(child)
    def __repr__(self) -> str:
        return str(self.key)
    
class Tree:

    """
    Traversal functions default to root node of the entire tree if root argument is missing
    If specified, the traversal would only be performed on that particular sub-branch 
    """

    def __init__(self, root: TreeNode = None):
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
    def preOrder(self, root: TreeNode = None) -> list[TreeNode]: # root, children
        if root == None:
            return []
        order = [root]
        for child in root.children:
            order += self.preOrder(child)
        return order

    # in-order traversal does not exist for non-binary trees
    
    @default_to_tree_root
    def postOrder(self, root: TreeNode = None) -> list[TreeNode]: # children, root
        if root == None:
            return []
        order = []
        for child in root.children:
            order += self.postOrder(child)
        order += [root]
        return order
    
    def getDiameter(self) -> int: # maximum distance from one treenode to another
        branch_diameters = []
        for subroot in self.root.children:
            stack = [(subroot, 1)] # node, depth
            visited = set()
            diameter = 0
            while stack:
                node, depth = stack.pop()
                visited.add(node) # objects are hashable
                if not node.children:
                    diameter = max(diameter, depth)
                for childnode in node.children:
                    stack.append((childnode, depth+1))
            branch_diameters.append(diameter)
        return sum(sorted(branch_diameters)[-2:]) + 1


# a = TreeNode("A")
# b = TreeNode("B")
# c = TreeNode("C")
# d = TreeNode("D")
# e = TreeNode("E")
# a.addChildren(b, c, d)
# b.addChildren(e)
# # a.children += [b, c, d]
# # b.children += [e]

# tree = Tree(a)
# #print(tree)

# print(tree.preOrder())
# print(tree.postOrder())
# print(tree.getDiameter())