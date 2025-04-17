class MinHeap:
    def __init__(self):
        self.prices = []
        self.actualSize = 0 #Necessary due to lazy deletion process fcr sliding window

    def heapifyUp(self, index):
        while index > 0:
            #heapifies up until either the price is in a valid position, or the price is the root of the heap
            if self.prices[index] >= self.prices[(index-1)//2]:
                break
            self.prices[index], self.prices[(index-1)//2] = self.prices[(index-1)//2], self.prices[index]
            index = (index-1)//2

    def heapPush(self, price):
        self.prices.append(price)
        self.heapifyUp(len(self.prices) - 1)
        self.actualSize += 1

    def heapifyDown(self, index):
        while index < len(self.prices)//2:
            if self.prices[index] > self.prices[(index+1)*2 - 1]:
                if len(self.prices) >= (index+1)*2 and self.prices[(index+1)*2] < self.prices[(index+1)*2 - 1]:
                    self.prices[index], self.prices[(index+1)*2] = self.prices[(index+1)*2], self.prices[index]
                    index = (index+1)*2
                else:
                    self.prices[index], self.prices[(index+1)*2-1] = self.prices[(index+1)*2 - 1], self.prices[index]
                    index = (index+1)*2 - 1
            elif len(self.prices) >= (index+1)*2 and self.prices[index] > self.prices[(index+1)*2]:
                self.prices[index], self.prices[(index+1)*2] = self.prices[(index+1)*2], self.prices[index]
                index = (index+1)*2
            else:
                break

    def heapPop(self):
        self.prices[0], self.prices[len(self.prices) - 1] = self.prices[len(self.prices) - 1], self.prices[0]
        self.prices.pop()
        self.heapifyDown(0)