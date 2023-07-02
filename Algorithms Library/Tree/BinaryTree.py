class BinaryTreeNode(object):
    def __init__(self, key):
        self.key = key # value of the node
        self.left = None # left child
        self.right = None # right child
        self.depth = 0 # depth of the node, 0 is root node
    def __repr__(self) -> str:
        return str(self.key)

class BinaryTree(object):

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
    

# if __name__ == "__main__":

#     a = BinaryTreeNode("A")
#     b = BinaryTreeNode("B")
#     c = BinaryTreeNode("C")
#     a.left = b
#     a.right = c

#     tree = BinaryTree(a)
#     #print(tree)

#     print(tree.preOrder())
#     print(tree.inOrder())
#     print(tree.postOrder())