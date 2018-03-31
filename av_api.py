#!/bin/python3

import json
import pandas as pd
import time
import urllib
from urllib.parse import urlencode, quote_plus
import av_api_key

def av_call(payload):
    time.sleep(2)
    result = {}
    try:
        payload['apikey'] = av_api_key.API_KEY
        url = 'https://www.alphavantage.co/query?{}'
        url = url.format(urlencode(payload, quote_via=quote_plus))
        #print(url)
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        data = resp.read()
        encoding = resp.info().get_content_charset('utf-8')
        data = json.loads(data.decode(encoding))

        result['data'] = data
        result['success'] = True
        result['error'] = None
    except Exception as e:
        result['data'] = None
        result['success'] = False
        result['error'] = str(e)
    return result

# interval: 1min, 5min, 15min, 30min, 60min
# full: 10 days, compact: 100 data points
def time_series_intraday(symbol, interval, full = False):
    payload = {
            'function':'TIME_SERIES_INTRADAY',
            'symbol':symbol,
            'interval':interval,
            'outputsize':'compact',
            'datatype':'json'}
    if full:
        payload['outputsize'] = 'full'
    data = av_call(payload)
    return data

# full: full-length, compact: 100 data points
def time_series_daily(symbol, full = False):
    payload = {
            'function':'TIME_SERIES_DAILY',
            'symbol':symbol,
            'outputsize':'compact',
            'datatype':'json'}
    if full:
        payload['outputsize'] = 'full'
    data = av_call(payload)
    if (data['success']):
        df = pd.DataFrame(data['data']['Time Series (Daily)']).T
        df.index = pd.to_datetime(df.index)
        df.index.names = ['date']
        df.rename(
                columns={
                        '1. open':'open',
                        '2. high':'high',
                        '3. low':'low',
                        '4. close':'close',
                        '5. volume':'volume'
                        }, inplace=True)
        data['data'] = df
    return data

# full: full-length, compact: 100 data points
def time_series_daily_adjusted(symbol, full = False):
    payload = {
            'function':'TIME_SERIES_DAILY_ADJUSTED',
            'symbol':symbol,
            'outputsize':'compact',
            'datatype':'json'}
    if full:
        payload['outputsize'] = 'full'
    data = av_call(payload)
    if (data['success']):
        df = pd.DataFrame(data['data']['Time Series (Daily)']).T
        df.index = pd.to_datetime(df.index)
        df.index.names = ['date']
        df.rename(
                columns={
                        '1. open':'open',
                        '2. high':'high',
                        '3. low':'low',
                        '4. close':'close',
                        '5. adjusted close':'adjclose',
                        '6. volume':'volume',
                        '7. dividend amount':'dividend',
                        '8. split coefficient':'splitcoef'
                        }, inplace=True)
        data['data'] = df
    return data

# symbols - up to 100 synbols
def batch_stock_quotes(symbols):
    payload = {
            'function':'BATCH_STOCK_QUOTES',
            'symbols':','.join(symbols),
            'datatype':'json'}
    data = av_call(payload)
    return data

# function: SMA, EMA, WMA, DEMA, TEMA, TRIMA, KAMA
# interval: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly
# time_period: number of data points
# series_type: close, open, high, low
def MA(function, symbol, interval, time_period, series_type):
    payload = {
            'function':function,
            'symbol':symbol,
            'interval':interval,
            'time_period':time_period,
            'series_type':series_type}
    data = av_call(payload)
    return data

# simple moving average
def SMA(symbol, interval, time_period, series_type):
    return MA('SMA', symbol, interval, time_period, series_type)

# exponential moving average
def EMA(symbol, interval, time_period, series_type):
    return MA('EMA', symbol, interval, time_period, series_type)

# weighted moving average
def WMA(symbol, interval, time_period, series_type):
    return MA('WMA', symbol, interval, time_period, series_type)

# double exponential moving average
def DEMA(symbol, interval, time_period, series_type):
    return MA('DEMA', symbol, interval, time_period, series_type)

# triple exponential moving average
def TEMA(symbol, interval, time_period, series_type):
    return MA('TEMA', symbol, interval, time_period, series_type)

# triangular moving average
def TRIMA(symbol, interval, time_period, series_type):
    return MA('TRIMA', symbol, interval, time_period, series_type)

# Kaufman adaptive moving average
def KAMA(symbol, interval, time_period, series_type):
    return MA('KAMA', symbol, interval, time_period, series_type)

# average directional movement index (ADX)
# interval: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly
# time_period: number of data points used to calculate each ADX value
def ADX(symbol, interval='daily', time_period=10):
    payload = {
            'function':'ADX',
            'symbol':symbol,
            'interval':interval,
            'time_period':time_period}
    data = av_call(payload)
    if (data['success']):
        df = pd.DataFrame(data['data']['Technical Analysis: ADX']).T
        df.index = pd.to_datetime(df.index)
        df.index.names = ['date']
        data['data'] = df
    return data

# relative strength index (ADX)
# interval: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly
# time_period: number of data points used to calculate each RSI value
def RSI(symbol, interval='daily', time_period=14, series_type='close'):
    payload = {
            'function':'RSI',
            'symbol':symbol,
            'interval':interval,
            'time_period':time_period,
            'series_type':series_type}
    data = av_call(payload)
    if (data['success']):
        df = pd.DataFrame(data['data']['Technical Analysis: RSI']).T
        df.index = pd.to_datetime(df.index)
        df.index.names = ['date']
        data['data'] = df
    return data

def sector():
    payload = {
            'function':'SECTOR'}
    data = av_call(payload)
    return data

# -------------------------------------------------------------------------------

if __name__ == "__main__":
    print('-' * 60)
    print('test av_api.py...')
    print('-' * 60)
    try:
        data = time_series_daily('AAPL')
        if data['success']:
            print(data['data'].tail())
        else:
            print('ERROR:')
            print(data['error'])
    except:
        import sys
        error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
        print(error)
    print('-' * 60)
