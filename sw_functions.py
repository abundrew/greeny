import time
import sw_config
import sw_stock
import sw_stock_filter
import sw_history
import sw_study
import sw_fundamentals
import sw_data_hub

stock = sw_stock.Stock()
stock_filter = sw_stock_filter.StockFilter()
history = sw_history.History()
study = sw_study.Study(history)
fundamentals = sw_fundamentals.Fundamentals()
data_hub = sw_data_hub.DataHub(stock.stocks(), history, study, fundamentals)
print(time.strftime('%Y-%m-%d %H:%M:%S ready...', time.localtime()))

def select_50_200():
    print(time.strftime('%Y-%m-%d %H:%M:%S started...', time.localtime()))
    fname = sw_config.FORMAT_SELECTED.format('50_200')
    selected = []
    for _stock in stock.stocks():
        hdf = data_hub.history(_stock)
        sdf = data_hub.study(_stock)
        if sdf is None: continue
        if not hdf.iloc[-1]['close'] > sdf.iloc[-1]['ma_50']: continue
        if not sdf.iloc[-1]['ma_50'] > sdf.iloc[-1]['ma_200']: continue
        selected.append(_stock)
        with open(fname, 'w') as f:
            for s in selected:
                f.write(s + '\n')
    print(time.strftime('%Y-%m-%d %H:%M:%S finished...', time.localtime()))

def update_50_200():
    print(time.strftime('%Y-%m-%d %H:%M:%S started...', time.localtime()))
    selected = stock.select("50_200")
    history.update(selected)
    study.update(selected)
    print(time.strftime('%Y-%m-%d %H:%M:%S updating...', time.localtime()))
    global data_hub
    data_hub = sw_data_hub.DataHub(stock.stocks(), history, study, fundamentals)
    print(time.strftime('%Y-%m-%d %H:%M:%S finished...', time.localtime()))

def rocket_stocks():
    selected = stock.select("rocket", stock_filter.rocket_filter, stock.select('50_200'))
    print('Rocket stocks: {} {} {}'.format(len(selected), ' '.join(selected[:50]), '...' if len(selected) > 50 else ''))
