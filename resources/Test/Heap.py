class MinHeap:
    def __init__(self):
        self.prices = []
        self.actualSize = 0 #Necessary due to lazy deletion provess fcr sliding window
