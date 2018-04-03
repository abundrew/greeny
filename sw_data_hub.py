#!/bin/python3

class DataHub:
    def __init__(self, stocks, history, study, fundamentals):
        self._technical = {}
        self._fundamentals = {}
        for stock in stocks:
            self._technical[stock] = {}
            self._technical[stock]['history'] = history.to_dataframe(stock)
            self._technical[stock]['study'] = study.to_dataframe(stock)
            self._fundamentals[stock] = {}
            self._fundamentals[stock]['financials'] = fundamentals.financials(stock)
            self._fundamentals[stock]['peers'] = fundamentals.peers(stock)
            self._fundamentals[stock]['stats'] = fundamentals.stats(stock)

    def history(self, stock):
        return self._technical[stock]['history']

    def study(self, stock):
        return self._technical[stock]['study']

    def financials(self, stock):
        return self._fundamentals[stock]['financials']

    def peers(self, stock):
        return self._fundamentals[stock]['peers']

    def stats(self, stock):
        return self._fundamentals[stock]['stats']