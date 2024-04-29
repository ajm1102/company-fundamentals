
"""
Echanges use a ticker symbol to identfy stock. But SEC use a Central Index Key (CIK), ticker are more
widly used and known. Function provides a way to map a ticker to CIK.
"""
def convert_ticker_cik(ticker):
    import requests

    # get list of currently used tickers
    ticker = ticker.upper()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    r = requests.get('https://www.sec.gov/files/company_tickers.json', headers=headers)
    map_ticker_to_cik = r.json() # 
    
    # use the obtatied dictionary to convert from key to value
    ticker_key_map = {data['ticker']: data['cik_str'] for index, data in map_ticker_to_cik.items()}
    cik = ticker_key_map[ticker]
    return cik
