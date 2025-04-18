from collections import defaultdict
from email.policy import default

#importing heaps to use for the median stream strategy
from Heap import MinHeap, MaxHeap

class SlidingMedian:
    def __init__(self):
        #double heaps to store middlemost elements
        self.lowerHalf = MaxHeap()
        self.upperHalf = MinHeap()
        #hashmap for tracking delayed deletions
        self.deleting = defaultdict(int)