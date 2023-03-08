import os

import pandas as pd
import data_collection as dc

# tickers = os.listdir('big_data/')
tickers = ['TCS']

print('GETTING STOCK DATA')

stocks_data = {}

#getting data for all stocks in the timeframe
for t in tickers:
    ticker_data = dc.get_data(t)
    stocks_data[t] = ticker_data

def next(index):

    if index < len(stocks_data[tickers[0]]):
        data = {
            'symbol': [], 'close':[], 'filt': [], 'close_dif': [], 'direction':[], 'fake_pivot': [], 'resistances': [], 'supports': [], 'date': [], 'time': [], 'date_actual': []
        }

        for t in tickers:
            symbol = stocks_data[t].iloc[index].symbol
            close = stocks_data[t].iloc[index]['close']
            filt = stocks_data[t].iloc[index]['filt']
            close_dif = stocks_data[t].iloc[index]['close_dif']
            direction = stocks_data[t].iloc[index]['direction']
            resistance = stocks_data[t].iloc[index]['resistances']
            supports = stocks_data[t].iloc[index]['supports']
            date = stocks_data[t].iloc[index]['datetime']
            time = stocks_data[t].iloc[index]['time']
            date_actual = stocks_data[t].iloc[index]['date']
            fake_pivot = stocks_data[t].iloc[index]['fake_pivot']

            data['symbol'].append(symbol)
            data['close'].append(close)
            data['filt'].append(filt)
            data['close_dif'].append(close_dif)
            data['direction'].append(direction)
            data['date'].append(date)
            data['time'].append(time)
            data['date_actual'].append(date_actual)
            data['resistances'].append(resistance)
            data['supports'].append(supports)
            data['fake_pivot'].append(fake_pivot)


        df = pd.DataFrame(data, index=data['symbol'])

        return df

    return None

if __name__ == '__main__':
    print('STARTING')
    print(next(20))
    print(next(40))