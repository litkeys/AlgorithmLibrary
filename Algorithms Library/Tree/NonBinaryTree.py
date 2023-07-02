class TreeNode:
    def __init__(self, key):
        self.key = key # value of the node
        self.children = [] # children of the node
        self.depth = 0 # depth of the node, 0 is root node
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
    

# if __name__ == "__main__":

#     a = TreeNode("A")
#     b = TreeNode("B")
#     c = TreeNode("C")
#     d = TreeNode("D")
#     a.children += [b, c, d]

#     tree = Tree(a)
#     #print(tree)

#     print(tree.preOrder())
#     print(tree.postOrder())