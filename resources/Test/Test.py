import yfinance as yf
from backtesting import Backtest
from resources.server.Helper import modify_data
from Strategies import FirstStrategy, SecondStrategy

def main():
    print("Enter stock ticker symbol: ", end="")
    ticker = input()
    print("Enter start date (XXXX-XX-XX): ", end="")
    start_date = input()
    print("Enter end date (XXXX-XX-XX): ", end="")
    end_date = input()

    raw_data = yf.download(ticker, start=start_date, end=end_date)
    modified_data = modify_data(raw_data)

    btpy = Backtest(modified_data, FirstStrategy,
              exclusive_orders=True)
    stats = btpy.run()
    btpy.plot()

    btpy2 = Backtest(modified_data, SecondStrategy,
              exclusive_orders=True)
    stats = btpy2.run()
    btpy2.plot()

if __name__ == "__main__":
    main()