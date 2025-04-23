from flask import Flask, jsonify
from flask_cors import CORS

from TradingAlgorithms import MedianAlgorithm
from TradingAlgorithms import IQRBreakoutAlgorithm
from toolkit import DataFrameReturner
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

metrics = {'return%': 0, 'return$': 0, 'trade#': 0, 'winrate%': 0, 'exposuretime%': 0, 'avgtrade%': 0}

@app.route('/data/<ticker>/<start_date>/<end_date>/<strategy>', methods=['GET'])
def get_trades(ticker, start_date, end_date, strategy):
    DataFrameReturner.load_data(ticker, start_date=start_date, end_date=end_date)
    data = DataFrameReturner.get_dataframe()[['Close']]

    price_list = [
        {"date": index.strftime("%Y-%m-%d"), "Price": round(float(row['Close']), 2)}
        for index, row in data.iterrows()
    ]

    DataFrameReturner.load_data(ticker, start_date=start_date, end_date=end_date)
    stats = DataFrameReturner.run_btpy(MedianAlgorithm)
    if(strategy == "2"):
        stats = DataFrameReturner.run_btpy(IQRBreakoutAlgorithm)
    trades = stats['_trades']
    entrances = [
        {"date": row.EntryTime.strftime("%Y-%m-%d"), "Price": round(float(row.EntryPrice), 2)}
        for index, row in trades.iterrows()
        if row.Size > 0
    ]
    exits = [
        {"date": row.EntryTime.strftime("%Y-%m-%d"), "Price": round(float(row.EntryPrice), 2)}
        for index, row in trades.iterrows()
        if row.Size < 0
    ]
    #places entry and exit prices into the price_list list if there were trades on that day
    entry_map = {e["date"]: e["Price"] for e in entrances}
    exit_map = {e["date"]: e["Price"] for e in exits}

    for p in price_list:
        p["EntryPrice"] = entry_map.get(p["date"])
        p["ExitPrice"] = exit_map.get(p["date"])

    return jsonify(price_list)

if __name__ == '__main__':
    app.run(debug=True)
