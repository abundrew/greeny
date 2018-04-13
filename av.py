#!/bin/python3

import json
import pandas as pd
import sys
import time
import urllib.request
from urllib.parse import urlencode, quote_plus
import config

class DataReader:
    def __init__(self):
        self._last_run_time = time.time() - config.AV_API_DELAY

    def _av_call(self, payload):
        delay = config.AV_API_DELAY - (time.time() - self._last_run_time)
        if delay > 0:
            time.sleep(delay)
        self._last_run_time = time.time()
        result = {}
        try:
            payload['apikey'] = config.AV_API_KEY
            url = 'https://www.alphavantage.co/query?{}'
            url = url.format(urlencode(payload, quote_via=quote_plus))
            headers = {}
            headers['User-Agent'] = ("Mozilla/5.0 (X11; Linux i686) "
                                     "AppleWebKit/537.17 (KHTML, like Gecko) "
                                     "Chrome/24.0.1312.27 Safari/537.17")
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            data = resp.read()
            encoding = resp.info().get_content_charset('utf-8')
            data = json.loads(data.decode(encoding))
            if 'Information' in data:
                result['data'] = None
                result['success'] = False
                result['error'] = data['Information']
            else:
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
    def time_series_intraday(self, symbol, interval, full=False):
        payload = {
                'function':'TIME_SERIES_INTRADAY',
                'symbol':symbol,
                'interval':interval,
                'outputsize':'compact',
                'datatype':'json'}
        if full:
            payload['outputsize'] = 'full'
        data = self._av_call(payload)
        return data

    # full: full-length, compact: 100 data points
    def time_series_daily(self, symbol, full=False):
        payload = {
                'function':'TIME_SERIES_DAILY',
                'symbol':symbol,
                'outputsize':'compact',
                'datatype':'json'}
        if full:
            payload['outputsize'] = 'full'
        data = self._av_call(payload)
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
    def time_series_daily_adjusted(self, symbol, full=False):
        payload = {
                'function':'TIME_SERIES_DAILY_ADJUSTED',
                'symbol':symbol,
                'outputsize':'compact',
                'datatype':'json'}
        if full:
            payload['outputsize'] = 'full'
        data = self._av_call(payload)
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

    # symbols - up to 100 symbols
    def batch_stock_quotes(self, symbols):
        payload = {
                'function':'BATCH_STOCK_QUOTES',
                'symbols':','.join(symbols),
                'datatype':'json'}
        data = self._av_call(payload)
        return data

    # function: SMA, EMA, WMA, DEMA, TEMA, TRIMA, KAMA
    # interval: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly
    # time_period: number of data points
    # series_type: close, open, high, low
    def MA(self, function, symbol, interval, time_period, series_type):
        payload = {
                'function':function,
                'symbol':symbol,
                'interval':interval,
                'time_period':time_period,
                'series_type':series_type}
        data = self._av_call(payload)
        if data['success']:
            df = data['data']['Technical Analysis: {}'.format(function)]
            data['data'] = df
        return data

    # simple moving average
    def SMA(self, symbol, interval, time_period, series_type):
        return self.MA('SMA', symbol, interval, time_period, series_type)

    # exponential moving average
    def EMA(self, symbol, interval, time_period, series_type):
        return self.MA('EMA', symbol, interval, time_period, series_type)

    # weighted moving average
    def WMA(self, symbol, interval, time_period, series_type):
        return self.MA('WMA', symbol, interval, time_period, series_type)

    # double exponential moving average
    def DEMA(self, symbol, interval, time_period, series_type):
        return self.MA('DEMA', symbol, interval, time_period, series_type)

    # triple exponential moving average
    def TEMA(self, symbol, interval, time_period, series_type):
        return self.MA('TEMA', symbol, interval, time_period, series_type)

    # triangular moving average
    def TRIMA(self, symbol, interval, time_period, series_type):
        return self.MA('TRIMA', symbol, interval, time_period, series_type)

    # Kaufman adaptive moving average
    def KAMA(self, symbol, interval, time_period, series_type):
        return self.MA('KAMA', symbol, interval, time_period, series_type)

    # average directional movement index (ADX)
    # interval: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly
    # time_period: number of data points used to calculate each ADX value
    def ADX(self, symbol, interval='daily', time_period=10):
        payload = {
                'function':'ADX',
                'symbol':symbol,
                'interval':interval,
                'time_period':time_period}
        data = self._av_call(payload)
        if (data['success']):
            df = pd.DataFrame(data['data']['Technical Analysis: ADX']).T
            df.index = pd.to_datetime(df.index)
            df.index.names = ['date']
            data['data'] = df
        return data

    # relative strength index (RSI)
    # interval: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly
    # time_period: number of data points used to calculate each RSI value
    def RSI(self, symbol, interval='daily', time_period=14, series_type='close'):
        payload = {
                'function':'RSI',
                'symbol':symbol,
                'interval':interval,
                'time_period':time_period,
                'series_type':series_type}
        data = self._av_call(payload)
        if (data['success']):
            df = pd.DataFrame(data['data']['Technical Analysis: RSI']).T
            df.index = pd.to_datetime(df.index)
            df.index.names = ['date']
            data['data'] = df
        return data

    def sector(self):
        payload = {
                'function':'SECTOR'}
        data = self._av_call(payload)
        return data

# ----- self-test -------------------------------------------------------------

if __name__ == "__main__":
    print('-' * 80)
    print('test av.DataReader ...')
    print('-' * 80)
    try:
        reader = DataReader()
        data = reader.time_series_daily('AAPL')
        print(time.strftime('%Y-%m-%d %H:%M:%S TIME SERIES DAILY AAPL ...', time.localtime()))
        if data['success']:
            print(data['data'].tail())
        else:
            print('ERROR {}:'.format(data['error']))
        print('-' * 80)
        data = reader.SMA('SMA','daily', 200, 'close')
        print(time.strftime('%Y-%m-%d %H:%M:%S SMA AAPL ...', time.localtime()))
        if data['success']:
            print(data['data'])
        else:
            print('ERROR {}:'.format(data['error']))
        print('-' * 80)
        data = reader.RSI('AAPL')
        print(time.strftime('%Y-%m-%d %H:%M:%S RSI AAPL ...', time.localtime()))
        if data['success']:
            print(data['data'].tail())
        else:
            print('ERROR {}:'.format(data['error']))
        print('-' * 80)
        data = reader.sector()
        print(time.strftime('%Y-%m-%d %H:%M:%S SECTOR ...', time.localtime()))
        if data['success']:
            print(data['data'])
        else:
            print('ERROR {}:'.format(data['error']))
    except:
        print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
    print('-' * 80)
