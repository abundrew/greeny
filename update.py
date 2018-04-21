import pandas as pd
import os
import sys
import config
import daily
import stock

# 1. Download US Equities
#    at http://eoddata.com/myaccount/accountdetails.aspx to '../data/daily/eoddata/USE_{}.txt'
#    Don't download files for holidays (http://www.theholidayschedule.com/nyse-holidays.php)

# 2. Update symbols.csv (symbols from US Equities file) in '../data/symbols/symbols.csv'
#    Replace '^([^,]+)(.*)$' with '\1'

# 3. Download missing daily files

'''
history = daily.History()
symbols = stock.Symbol().symbols()
history.download(symbols)
print('done...')
exit()
'''

# 4. Update daily files with the content of US Equities file by dates

history = daily.History()
symbols = stock.Symbol().symbols()
start_date = '2018-04-20'
end_date = '2018-04-20'
for di in pd.date_range(start_date, end_date):
    eoddate = str(di)[:10]
    print(eoddate)
    fname = config.FORMAT_DAILY_EODDATA.format(eoddate[:4] + eoddate[5:7] + eoddate[8:])
    if not os.path.isfile(fname):
        print('- file not found -')
        continue
    with open(fname, 'r') as f:
        for line in f:
            parts = line.split(',')
            symbol = parts[0]
            if symbol in symbols:
                sdate = pd.Timestamp('{}-{}-{}'.format(parts[1][:4], parts[1][4:6], parts[1][6:]))
                hdf = history.to_dataframe(symbol)
                if not sdate in hdf.index:
                    try:
                        hdf.loc[sdate] = [parts[2], parts[3], parts[4], parts[5], parts[6].strip()]
                        hdf = hdf.sort_index()
                        hdf.to_csv(config.FORMAT_DAILY_HISTORY.format(symbol))
                    except:
                        print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
