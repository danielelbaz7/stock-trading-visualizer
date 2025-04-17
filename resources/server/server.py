from flask import Flask, jsonify
from flask_cors import CORS
from toolkit import DataFrameReturner
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

# returns ticket data from start date to end date as a json file to be parsed
@app.route('/data/<ticker>/<start_date>/<end_date>', methods=['GET'])
def get_data(ticker, start_date, end_date):

    DataFrameReturner.load_data(ticker, start_date=start_date, end_date=end_date)
    data = DataFrameReturner.get_dataframe()

    return jsonify({'ticker': ticker, 'start_date': start_date, 'end_date': end_date})
