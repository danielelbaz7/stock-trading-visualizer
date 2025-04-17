class MinHeap:
    def __init__(self):
        self.prices = []
        self.actualSize = 0 #Necessary due to lazy deletion provess fcr sliding window

    def heapifyUp(self, index):
        while index > 0:
            #heapifies up until either the price is in a valid position, or the price is the root of the heap
            if self.prices[index] >= self.prices[(index-1)//2]:
                break
            self.prices[index], self.prices[(index-1)//2] = self.prices[(index-1)//2], self.prices[index]
            index = (index-1)//2

    def heapPush(self, price):
        self.prices.append(price)
        self.heapifyUp(self.actualSize)
        self.actualSize += 1