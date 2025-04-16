from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
from backtesting import Backtest
from Strategies import getStrateg
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

# returns ticket data from start date to end date as a json file to be parsed
@app.route('/data/<ticker>/<start_date>/<end_date>', methods=['GET'])
def get_data(ticker, start_date, end_date):

    data = yf.download(ticker, start=start_date, end=end_date)
    data.columns = data.columns.droplevel('Ticker')
    data[['Open', 'Close']] = data[['Close', 'Open']]
    data.rename(columns={'Open': 'Close', 'Close': 'Open'}, inplace=True)
    data.index.name = None
    data.columns.name = None

    return jsonify({'ticker': ticker, 'start_date': start_date, 'end_date': end_date})
