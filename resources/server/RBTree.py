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

    def rotateRight(self, node):
        newParent = node.left
        node.left = newParent.right
        if newParent.right != self.nullNode:
            newParent.right.parent = node
        newParent.right = node
        newParent.parent = node.parent
        if node.parent == self.nullNode:
            self.root = newParent
        elif node == node.parent.right:
            newParent.parent.right = newParent
        else:
            newParent.parent.left = newParent
        node.parent = newParent

    def rotateLeft(self, node):
        newParent = node.right
        node.right = newParent.left
        if newParent.left != self.nullNode:
            newParent.left.parent = node
        newParent.left = node
        newParent.parent = node.parent
        if node.parent == self.nullNode:
            self.root = newParent
        elif node ==  node.parent.right:
            newParent.parent.right = newParent
        else:
            newParent.parent.left = newParent
        node.parent = newParent


    def balance(self, node): #Done with help of slide 141 from deck 4 - Balanced Trees. Credit to the C++ code Aman provided in the slides.
        if node.parent == self.nullNode and node.isRed: #If the root is red, color it black and we're done
            node.isRed = False
            return
        parent, grandparent = node.parent, node.parent.parent
        if parent ==  grandparent.right:
            uncle = grandparent.left
        else:
            uncle = grandparent.right
        if uncle != self.nullNode and uncle.isRed:
            uncle.isRed, parent.isRed = False, False
            grandparent.isRed = True
            self.balance(grandparent)
            return
        if node == parent.right and parent == grandparent.left:
            self.rotateLeft(parent)
            node, parent = parent, parent.parent
        elif node == parent.left and parent == grandparent.right:
            self.rotateRight(parent)
            node, parent = parent, parent.parent
        parent.isRed, grandparent.isRed = False, True
        if node.price < parent.price:
            self.rotateRight(grandparent)
        else:
            self.rotateLeft(grandparent)


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
        if newNode.parent.isRed:
            self.balance(newNode)
        self.root.isRed = False

