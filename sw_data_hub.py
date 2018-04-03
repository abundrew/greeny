#!/bin/python3

class DataHub:
    def __init__(self, stocks, history, study, fundamentals):
        self._technical = {}
        self._fundamentals = {}

        for stock in stocks:
            hdf = history.to_dataframe(stock)
            if hdf is not None:
                sdf = study.to_dataframe(stock)
                if sdf is not None:
                    hdf = hdf.join(sdf)
            self._technical[stock] = hdf
            self._fundamentals[stock] = {}
            self._fundamentals[stock]['financials'] = fundamentals.financials(stock)
            self._fundamentals[stock]['peers'] = fundamentals.peers(stock)
            self._fundamentals[stock]['stats'] = fundamentals.stats(stock)

    def technical(self):
        return self._technical

    def fundamentals(self):
        return self._fundamentals