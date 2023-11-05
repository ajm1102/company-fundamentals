from flask import Flask, jsonify, request, session
from flask_cors import CORS, cross_origin
from flask_session import Session

from main import return_metrics
import json
import pandas as pd
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_PERMANENT"] = True
app.config["SECRET_KEY"] = "sdfsdfs"
app.config["SESSION_TYPE"] = "filesystem"

app.config.from_object(__name__)


CORS(app, supports_credentials=True)
Session(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/getMetrics", methods=['GET'])
@cross_origin(supports_credentials=True)
def return_stock_metrics():

    args = request.args
    stock_ticker = args['stockTicker'] 

    metrics, balance, income = return_metrics(stock_ticker)
    metrics = sorted(metrics, reverse=False)

    session['balance'] = balance.to_dict()
    session['income'] = income.to_dict()
    return json.dumps(metrics)

@app.route('/metricHistory', methods=['GET'])
@cross_origin(supports_credentials=True)
def metric_history():
    # extract 
    args = request.args
    metric = args['metric']

    # extract dataframes from session
    income_statement = pd.DataFrame(session['income'])
    balance_statement = pd.DataFrame(session['balance'])
    
    
    if metric in income_statement.index:
        output = income_statement.loc[metric]
    elif metric in balance_statement.index:
        output = balance_statement.loc[metric]

    output = output.reindex(index=output.index[::-1])
     
    output.index.name = "date"
    output = output.fillna('null')
    output = output.reset_index().to_dict(orient='records')
    return json.dumps(output)

@app.route('/download_update_dataset', methods=['GET'])
@socketio.on('message_from_server')
@cross_origin(supports_credentials=True)
def download_update_dataset():
    from downloader_socket import download_update_clean_files

    args = request.args
    metric = args['update']

    updated = {"updated": False}
    if metric == 'true':
        download_update_clean_files(socketio)
        updated['updated'] = True
    return json.dumps(updated)


@app.route('/share_price_hist', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_share_price_history():
    import yfinance as yf
    args = request.args

    stock_ticker = args['stockTicker'].upper()   

    # get dataframe of daily data for stock
    stock_data = yf.Ticker(stock_ticker)
    hist = stock_data.history(start="2009-01-01")
    dates = hist.index
    dates = [date.strftime('%Y%m%d') for date in dates]
    share_prices = list(hist['Close'].values)

    comb = []
    for date, price in zip(dates, share_prices):
        comb.append({"date": date, "price": price})

    return json.dumps(comb)

if __name__ == "__main__":
    socketio.run(app, debug=True, port="8080")