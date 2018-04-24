import daily
import intraday
import stock


history = daily.History()
symbols = stock.Symbol().symbols()
history.download(symbols)  # ,true
print('done...')

'''
selection = stock.Selection()
selected = selection.select(['FIXED','UPTREND'])
selection.save('FIXED_UPTREND', selected)
print('done...')
'''
'''
selection = stock.Selection()
selection.update()
print('done...')
'''
'''
selection = stock.Selection()
selected = selection.select(['UPTREND','MORE_20','LIQUID','CRSI_20'])
selection.save('UMLC', selected)
print('done...')
'''

'''
history = intraday.History()
selected_FIXED = []
for symbol in stock.Symbol().symbols():
    hdf = history.to_dataframe(symbol)
    if hdf is not None and len(hdf) == 140:
        selected_FIXED.append(symbol)
selection = stock.Selection()
selection.save("FIXED", selected_FIXED)
print('done...')
'''