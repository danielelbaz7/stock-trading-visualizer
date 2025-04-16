import pandas as pd
import yfinance as yf

def modify_dataframe(raw_data: pd.DataFrame) -> pd.DataFrame:
    modified_data = raw_data.copy()
    modified_data.columns = modified_data.columns.droplevel('Ticker')
    modified_data[['Open', 'Close']] = modified_data[['Close', 'Open']]
    modified_data.rename(columns={'Open': 'Close', 'Close': 'Open'}, inplace=True)
    modified_data.index.name = None
    modified_data.columns.name = None
    return modified_data

class DataFrameReturner:
    _dataframe = None
    def __init__(self, ticker: str, start_date: str, end_date: str):
        raw_data = yf.download(ticker, start=start_date, end=end_date)
        self.dataframe = modify_dataframe(raw_data)

    @classmethod
    def load_data(cls, ticker: str, start_date: str, end_date: str):
        raw_data = yf.download(ticker, start=start_date, end=end_date, group_by='ticker')
        cls._dataframe = modify_dataframe(raw_data)

    @classmethod
    def get_dataframe(cls):
        return cls._dataframe

