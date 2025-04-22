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
        while heap.totalSize() != 0 and self.deleting[heap.heapTop()] != 0: #cleaning up any prior deleted values
            self.deleting[heap.heapTop()] -= 1
            heap.popHelper()

    def remove(self, price):
        self.deleting[price] += 1 #essentially marking a price for deletion and NOT deleting it until later if it's not the root of a heap (as this would be costly in terms of time complexity)
        if price <= self.lowerHalf.heapTop():
            self.lowerHalf.actualSize -= 1
            self.delayedDelete(self.lowerHalf)
            if len(self.lowerHalf) != len(self.upperHalf):
                self.lowerHalf.heapPush(self.upperHalf.heapPop())
        else:
            self.upperHalf.actualSize -= 1
            self.delayedDelete(self.upperHalf)
            if len(self.lowerHalf) - len(self.upperHalf) != 1:
                self.upperHalf.heapPush(self.lowerHalf.heapPop())

    def getMedian(self):
        #cleaning up any deleted root values to make sure we get the actual median
        self.delayedDelete(self.lowerHalf)
        self.delayedDelete(self.upperHalf)
        if len(self.lowerHalf) > len(self.upperHalf):
            return self.lowerHalf.heapTop()
        return (self.lowerHalf.heapTop() + self.upperHalf.heapTop()) / 2
