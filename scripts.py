import stock

selection = stock.Selection()
selected = selection.select(['UPTREND','MORE_20','LIQUID','CRSI_20'])
selection.save('UMLC', selected)
print('done...')