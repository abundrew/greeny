#!/bin/python3

import webbrowser

CHROME_PATH = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
CHART_URL = 'https://www.tradingview.com/chart/?symbol={}'

def chart(stock):
    url = CHART_URL.format(stock)
    webbrowser.get(CHROME_PATH).open(url)
