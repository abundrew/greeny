import intraday
import stock

#selection = stock.Selection()
#selected = selection.select(['UPTREND','MORE_20','LIQUID','CRSI_20'])
#selection.save('UMLC', selected)
#print('done...')

history = intraday.History()
selected_FIXED = []
for symbol in stock.Symbol().symbols():
    hdf = history.to_dataframe(symbol)
    if hdf is not None and len(hdf) == 140:
        selected_FIXED.append(symbol)
selection = stock.Selection()
selection.save("FIXED", selected_FIXED)
print('done...')