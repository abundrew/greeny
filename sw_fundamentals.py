#!/bin/python3

import os
import json
import sys
import iex_api
import sw_config
import sw_stock

class Fundamentals:
    def __init__(self,
                 path_financials=sw_config.PATH_FINANCIALS,
                 path_peers=sw_config.PATH_PEERS,
                 path_stats=sw_config.PATH_STATS):
        self._path_financials = path_financials
        self._path_peers = path_peers
        self._path_stats = path_stats

        fname = self._path_financials
        if not os.path.isfile(fname):
            self.update()
        with open(fname) as f:
            self._financials = json.load(f)

        fname = self._path_peers
        if not os.path.isfile(fname):
            self.update()
        with open(fname) as f:
            self._peers = json.load(f)

        fname = self._path_stats
        if not os.path.isfile(fname):
            self.update()
        with open(fname) as f:
            self._stats = json.load(f)

    def financials(self, stock):
        try:
            return self._financials['data'][stock]['financials']['financials']
        except:
            error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
            print(error)

    def peers(self, stock):
        try:
            return self._peers['data'][stock]['peers']
        except:
            error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
            print(error)

    def stats(self, stock):
        try:
            return self._stats['data'][stock]['stats']
        except:
            error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
            print(error)

    def update(self):
        stocks = sw_stock.Stock()
        component = {'financials':self._path_financials, 'peers':self._path_peers, 'stats':self._path_stats}
        for key in component:
            fname = component[key]
            bname = fname + '.bak'
            if os.path.isfile(fname):
                if os.path.isfile(bname):
                    os.remove(bname)
                os.rename(fname, fname + '.bak')
            data = iex_api.stock_batch_100(stocks, key)
            s = json.dumps(data)
            with open(fname, 'w') as f:
                f.write(s)

