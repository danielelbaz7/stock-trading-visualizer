class Node:
    def __init__(self, price, color = True, height = 1):
        self.price = price
        self.left = None
        self.right = None
        self.isRed = color
        self.height = height #Traditionally Red-Black trees don't store height, but I'm using this for efficient IQR-finding purposes.

class RBTree:
    def __init__(self):
        self.nullNode = Node(None, False, 0) #Null node to satisfy the invariant of black null nodes attached to leaves
        self.root = self.nullNode
