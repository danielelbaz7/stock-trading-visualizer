import pandas as pd
import yfinance as yf
from datetime import datetime as dt
from backtesting import Backtest

# Modifies dataframe from yfinance to be readable for backtesting.py
def modify_dataframe(raw_data: pd.DataFrame) -> pd.DataFrame:
    modified_data = raw_data.copy()
    modified_data.columns = modified_data.columns.droplevel('Ticker')
    modified_data[['Open', 'Close']] = modified_data[['Close', 'Open']]
    modified_data.rename(columns={'Open': 'Close', 'Close': 'Open'}, inplace=True)
    modified_data.index.name = None
    modified_data.columns.name = None
    return modified_data

# Checks if ticker symbol is present in yfinance
def is_valid_ticker(ticker: str) -> bool:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        return not hist.empty
    except Exception:
        return False

# Checks if start date has data for a given ticker
def is_valid_start_date(ticker: str, start_date: str) -> bool:
    try:
        date_obj = dt.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        return False

    try:
        end_date = (date_obj + pd.Timedelta(days=5)).strftime('%Y-%m-%d')
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        return not data.empty
    except Exception:
        return False

# Checks if end date has data for a given ticker
def is_valid_end_date(ticker: str, end_date: str) -> bool:
    try:
        date_obj = dt.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return False

    try:
        start_date = (date_obj - pd.Timedelta(days=5)).strftime('%Y-%m-%d')
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        return not data.empty
    except Exception:
        return False

# Encapsulates important backtesting functionality, might rename later
class DataFrameReturner:
    _dataframe = None
    _result = None
    _btpy = None

    def __init__(self, ticker: str, start_date: str, end_date: str):
        if is_valid_ticker(ticker) and is_valid_start_date(ticker, start_date) and is_valid_end_date(ticker, end_date):
            raw_data = yf.download(ticker, start=start_date, end=end_date)
            self.dataframe = modify_dataframe(raw_data)

    @classmethod
    def load_data(cls, ticker: str, start_date: str, end_date: str):
        if is_valid_ticker(ticker) and is_valid_start_date(ticker, start_date) and is_valid_end_date(ticker, end_date):
            raw_data = yf.download(ticker, start=start_date, end=end_date)
            cls._dataframe = modify_dataframe(raw_data)

    @classmethod
    def run_btpy(cls, strategy):
        cls._btpy = Backtest(cls._dataframe, strategy, exclusive_orders=True)
        cls._result = cls._btpy.run()
        return cls._result

    # Only for testing purposes
    @classmethod
    def plot(cls):
        cls._btpy.plot()

    @classmethod
    def get_dataframe(cls):
        return cls._dataframe

    @classmethod
    def get_result(cls):
        return cls._result


