import yfinance as yf
import pandas as pd
from datetime import datetime as dt
from backtesting import Backtest
from Strategies import FirstStrategy, SecondStrategy

def modify_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    Modifies the input DataFrame by:
    - Dropping the 'Ticker' level from columns.
    - Swapping 'Open' and 'Close' columns.
    - Renaming columns accordingly.
    - Removing index and column names.
    - Printing the modified DataFrame.
    :param raw_data: The input DataFrame.
    :return: The modified DataFrame.
    """
    modified_data = raw_data.copy()
    modified_data.columns = modified_data.columns.droplevel('Ticker')
    modified_data[['Open', 'Close']] = modified_data[['Close', 'Open']]
    modified_data.rename(columns={'Open': 'Close', 'Close': 'Open'}, inplace=True)
    modified_data.index.name = None
    modified_data.columns.name = None
    print(modified_data)
    return modified_data


def is_valid_ticker(ticker: str) -> bool:
    """
    Checks if ticker symbol is within Yahoo Finance's dataset.
    :param ticker: The ticker symbol.
    :return: True or False
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        return not hist.empty
    except Exception:
        return False

def is_valid_start_date(ticker: str, start_date: str) -> bool:
    """
    Checks if start date has data for a given ticker.
    :param ticker: The ticker symbol.
    :param start_date: The start date.
    :return:
    """

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

def is_valid_end_date(ticker: str, end_date: str) -> bool:
    """
    Checks if end date has data for a given ticker.
    :param ticker: The ticker symbol.
    :param end_date: The end date.
    :return: True or False
    """
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

def run_btpy(ticker: str, start_date: str, end_date: str, ):
    """
    Creates Backtester.py object and runs strategy.
    :param ticker: The ticker symbol.
    :param start_date: The start date.
    :param end_date: The end date.
    :return: None
    """
    raw_data = yf.download(ticker, start=start_date, end=end_date)
    modified_data = modify_data(raw_data)
    btpy = Backtest(modified_data, FirstStrategy,
                    exclusive_orders=True)
    stats = btpy.run()
    my_plot = btpy.plot(open_browser=False) # Change This
    print(my_plot)
    btpy2 = Backtest(modified_data, SecondStrategy,
                    exclusive_orders=True)
    stats = btpy2.run()
    my_plot2 = btpy2.plot(open_browser=False) # Change This

    return my_plot, my_plot2