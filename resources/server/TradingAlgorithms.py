from backtesting import Strategy
from SlidingMedian import SlidingMedian
from collections import deque

class MedianAlgorithm(Strategy):
    def init(self):
       self.median = SlidingMedian()
       self.prices = deque()

    def next(self):
        currentPrice = self.data.Close[-1]
        self.prices.append(currentPrice)
        self.median.add(currentPrice)
        if len(self.prices) < 100:
            return
        medianPrice = self.median.getMedian()
        if currentPrice < medianPrice * 0.98:
            self.buy()
        elif currentPrice > medianPrice * 1.02 and self.position:
            self.sell()
        self.median.remove(self.prices.popleft())
