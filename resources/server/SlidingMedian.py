from collections import defaultdict

#importing heaps to use for the median stream strategy
from Heap import MinHeap, MaxHeap

class SlidingMedian:
    def __init__(self):
        #double heaps to store middlemost elements
        self.lowerHalf = MaxHeap()
        self.upperHalf = MinHeap()
        #hashmap for tracking delayed deletions
        self.deleting = defaultdict(int)

    def add(self, price):
        if len(self.lowerHalf) == len(self.upperHalf):
            self.upperHalf.heapPush(price)
            self.lowerHalf.heapPush(self.upperHalf.heapPop())
        else:
            self.lowerHalf.heapPush(price)
            self.upperHalf.heapPush(self.lowerHalf.heapPop())

    def delayedDelete(self, heap):
        while heap.totalSize() != 0 and self.deleting[heap.heapTop()] != 0:
            self.deleting[heap.heapTop()] -= 1
            heap.heapPop()

    def remove(self, price):
        self.deleting[price] += 1
        if price <= self.lowerHalf.heapTop():
            self.delayedDelete(self.lowerHalf)
        else:
            self.delayedDelete(self.upperHalf)