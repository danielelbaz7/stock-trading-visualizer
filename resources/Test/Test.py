# Copy this class into server to test ya code
'''
from toolkit import DataFrameReturner
from TradingAlgorithms import MedianAlgorithm
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

class DummyStrategy(Strategy):
    # Placeholder strategy
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()

def main():
    print("Enter stock ticker symbol: ", end="")
    ticker = input()
    print("Enter start date (XXXX-XX-XX): ", end="")
    start_date = input()
    print("Enter end date (XXXX-XX-XX): ", end="")
    end_date = input()

    DataFrameReturner.load_data(ticker, start_date, end_date)
    # Change this to any other strategy you wanna test
    stats = DataFrameReturner.run_btpy(MedianAlgorithm)
    DataFrameReturner.plot()
    trades = stats['_trades']
    print(stats)
    print()
    print(trades)

if __name__ == "__main__":
    main()
'''