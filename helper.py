import nsepy
import datetime


def get_historic_data_by_symbol_days(stock_name,days):
    today = datetime.date.today()
    start = today + datetime.timedelta(-days)
    stock_data = nsepy.get_history(symbol = stock_name,start=start,end=today)
    return stock_data