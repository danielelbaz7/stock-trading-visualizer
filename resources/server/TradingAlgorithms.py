from toolkit import DataFrameReturner
from backtesting import Strategy
from SlidingMedian import SlidingMedian
from RBTree import RBTree
from collections import deque

class MedianAlgorithm(Strategy):
    def init(self):
       self.median = SlidingMedian()
       self.prices = deque()

    def next(self):
        currentPrice = self.data.Close[-1]
        if len(self.prices) < 20:
            self.prices.append(currentPrice)
            self.median.add(currentPrice)
            return
        medianPrice = self.median.getMedian()
        if currentPrice < medianPrice * 0.97 and self.position:
            self.sell()
        elif currentPrice > medianPrice * 1.03:
            self.buy()
        self.prices.append(currentPrice)
        self.median.add(currentPrice)
        self.median.remove(self.prices.popleft())

class IQRBreakoutAlgorithm(Strategy):
    def init(self):
        self.tree = RBTree()
        self.prices = deque()

    def next(self):
        p = self.data.Close[-1]

        self.prices.append(p)
        if len(self.prices) > 20:
            self.prices.popleft()

        self.tree = RBTree()  # rebuilding tree due to excessive issues with deleting and inserting new node
        for price_in_window in self.prices:
            self.tree.insert(price_in_window)

        if len(self.prices) < 20:
            return

        n = self.tree.root.size
        k1, k3 = n // 4, 3 * n // 4
        if n % 4 == 0:
            q1 = (self.tree.kthPrice(k1) + self.tree.kthPrice(k1 + 1)) / 2
            q3 = (self.tree.kthPrice(k3) + self.tree.kthPrice(k3 + 1)) / 2
        else:
            q1 = self.tree.kthPrice(k1 + 1)
            q3 = self.tree.kthPrice(k3 + 1)

        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr

        if p <= lower and self.position:
            self.sell()
        elif p >= upper:
            self.buy()


def main():
    print("Enter stock ticker symbol: ", end="")
    ticker = input()
    print("Enter start date (XXXX-XX-XX): ", end="")
    start_date = input()
    print("Enter end date (XXXX-XX-XX): ", end="")
    end_date = input()

    DataFrameReturner.load_data(ticker, start_date, end_date)
    # Change this to any other strategy you wanna test
    stats = DataFrameReturner.run_btpy(IQRBreakoutAlgorithm)
    DataFrameReturner.plot()
    trades = stats['_trades']
    print(stats)
    print()
    print(trades)

if __name__ == "__main__":
    main()