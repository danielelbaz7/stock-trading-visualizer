from resources.Test.Strategies import SecondStrategy


class Node:
    def __init__(self, price, parent, color = True):
        self.price = price
        self.left = None
        self.right = None
        self.parent = parent
        self.isRed = color
        self.size = 1 #Storing size of subtrees for IQR-tracking purposes

class RBTree:
    def __init__(self):
        self.nullNode = Node(None, None, False) #Null node to satisfy the invariant of black null nodes attached to leaves
        self.nullNode.size = 0
        self.nullNode.left, self.nullNode.right, self.nullNode.parent = self.nullNode, self.nullNode, self.nullNode
        self.root = self.nullNode

    def updateSize(self, node):
        if node == self.nullNode:
            return
        node.size = 1 + node.left.size + node.right.size

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
        self.updateSize(node)
        self.updateSize(newParent)

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
        self.updateSize(node)
        self.updateSize(newParent)


    def balance(self, node): #Done with help of slide 141 from deck 4 - Balanced Trees. Credit to the C++ code Aman provided in the slides.
        if node == self.nullNode or node.parent == self.nullNode: #If the root is red, color it black and we're done (or if we somehow end up at a nullNode)
            node.isRed = False
            return
        if node.parent.parent == self.nullNode:
            node.parent.isRed = False
            return
        parent, grandparent = node.parent, node.parent.parent
        if parent ==  grandparent.right:
            uncle = grandparent.left
        else:
            uncle = grandparent.right
        if uncle != self.nullNode and uncle.isRed:
            uncle.isRed, parent.isRed, grandparent.isRed = False, False, True
            self.balance(grandparent)
            return
        if node == parent.right and parent == grandparent.left:
            self.rotateLeft(parent)
            node, parent = parent, parent.parent
        elif node == parent.left and parent == grandparent.right:
            self.rotateRight(parent)
            node, parent = parent, parent.parent
        parent.isRed, grandparent.isRed = False, True
        if node == parent.left:
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
            current.size += 1
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

    #A lot of credit to Thomas Cormen's "Introduction to Algorithms" and Michael Sambol on Youtube for explaining to me how RB deletion works
    def transplant(self, a, b): #algorithm to move around two different subtrees, helper for deletion method
        if a.parent == self.nullNode:
            self.root = b
        elif a.parent.left == a:
            a.parent.left = b
        else:
            a.parent.right = b
        if b != self.nullNode:
            b.parent = a.parent

    def inorderSuccessor(self, node):
        if node.left == self.nullNode:
            return node
        return self.inorderSuccessor(node.left)

    def remove_fix(self, node):
        if node == self.root or node.isRed:
            node.isRed = False
            return
        if node == node.parent.left:
            sibling = node.parent.right
        else:
            sibling = node.parent.left
        if sibling.isRed:
            sibling.isRed = False
            node.parent.isRed = True
            if node == node.parent.left:
                self.rotateLeft(node.parent)
                sibling = node.parent.right
            else:
                self.rotateRight(node.parent)
                sibling = node.parent.left
        if not (sibling.left.isRed or sibling.right.isRed):
            sibling.isRed = True
            node = node.parent
        else:
            if node == node.parent.left and not sibling.right.isRed:
                sibling.left.isRed = False
                sibling.isRed = True
                self.rotateRight(sibling)
                sibling = sibling.parent.right
            if node == node.parent.right and not sibling.left.isRed:
                sibling.right.isRed = False
                sibling.isRed = True
                self.rotateLeft(sibling)
                sibling = sibling.parent.left
            sibling.isRed = node.parent.isRed
            node.parent.isRed = False
            if node == node.parent.left:
                sibling.right.isRed = False
                self.rotateLeft(node.parent)
            else:
                sibling.left.isRed = False
                self.rotateRight(node.parent)
            node = self.root
        self.remove_fix(node)




    def remove(self, price):
        cur = self.root
        while cur != self.nullNode and cur.price != price:
            if price < cur.price:
                cur = cur.left
            elif price >= cur.price:
                cur = cur.right
        if cur == self.nullNode:
            return
        originalColor = cur.isRed
        if cur.left == self.nullNode:
            replacement = cur.right
            self.transplant(cur, replacement)
        elif cur.right == self.nullNode:
            replacement = cur.left
            self.transplant(cur, replacement)
        else:

            inorderSuccessor = self.inorderSuccessor(cur.right)
            originalColor = inorderSuccessor.isRed
            replacement = inorderSuccessor.right
            if inorderSuccessor.parent != cur:
                self.transplant(inorderSuccessor, replacement)
                if replacement != self.nullNode:
                    replacement.parent = inorderSuccessor
                    replacement.right = cur.right
                    replacement.right.parent = replacement
            replacement.left = cur.left
            replacement.left.parent = replacement
            self.transplant(cur, replacement)
            replacement.isRed = cur.isRed
        if not cur.isRed:
            self.remove_fix(replacement)
        temp = replacement
        while temp != self.nullNode:
            self.updateSize(temp)
            temp = temp.parent
        cur = None
