import yfinance as yf
import pandas as pd

data=yf.download(tickers="TCS.NS",period='1000d',interval='5m')
print(data)