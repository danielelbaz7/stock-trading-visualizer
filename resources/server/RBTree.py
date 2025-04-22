class Node:
    def __init__(self, price, parent, color = True):
        self.price = price
        self.left = None
        self.right = None
        self.parent = parent
        self.isRed = color
        self.height = 0 #Traditionally Red-Black trees don't store height, but I'm using this for efficient IQR-finding purposes.

class RBTree:
    def __init__(self):
        self.nullNode = Node(None, None, False) #Null node to satisfy the invariant of black null nodes attached to leaves
        self.nullNode.left, self.nullNode.right, self.nullNode.parent = self.nullNode, self.nullNode, self.nullNode
        self.root = self.nullNode

    def balance(self, node): #Done with help of slide 141 from deck 4 - Balanced Trees
        if node.parent == self.nullNode and node.isRed: #If the root is red, color it black and we're done
            node.isRed = False
            return

    def insert(self, price):
        if self.root == self.nullNode:
            self.root = Node(price, self.nullNode, False)
            self.root.left, self.root.right = self.nullNode, self.nullNode
            return
        current, previous = self.root, self.nullNode
        while current != self.nullNode:
            if price < current.price:
                previous, current = current, current.left
            elif price >= current.price:
                previous, current = current, current.right
        newNode = Node(price, previous)
        newNode.left, newNode.right = self.nullNode, self.nullNode
        if price < previous.price:
            previous.left = newNode
        else:
            previous.right = newNode
        #TODO: Balancing the tree

