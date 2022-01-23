import nsepy
import datetime
import pandas as pd
import yfinance as yf

def get_historical_data(stock_name,duration_days):
    print(f'Getting historical data for {stock_name} for days :{duration_days}')
    today = datetime.date.today()
    duration = duration_days
    start = today + datetime.timedelta(-duration)
    # df = yf.Ticker("ITC").history(period="2y",interval="1d")
    # print(df)
    stock_data = nsepy.get_history(symbol = stock_name,start=start,end=today)
    data = pd.DataFrame(stock_data)
    data['Date'] = data.index
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data['Date']=data['Date'].dt.strftime('%b/%d/%Y')
    data.to_csv("nse.csv")
    return data

# data = get_historical_data('HDFC',30)
# data=pd.DataFrame(data)
# # data['date']=data['date'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
# # print(data)
#
# #df[['Open','High','Low','Close']].to_csv("nse.csv")
# #print(data[data.columns[0]])
# data.to_csv("nse.csv")
