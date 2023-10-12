import requests

def convert_ticker_cik(ticker):
    ticker = ticker.upper()
    r = requests.get('https://www.sec.gov/files/company_tickers.json')
    map_ticker_to_cik = r.json() # if response type was set to JSON, then you'll automatically have a JSON response here...
    
    ticker_key_map = {data['ticker']: data['cik_str'] for index, data in map_ticker_to_cik.items()}
    cik = ticker_key_map[ticker]
    return cik
