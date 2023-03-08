import pandas as pd
import math
import numpy as np
import pandas_ta as ta
from datetime import datetime

# pd.set_option('display.max_columns', None)

# smooth range
def smoothrng(x, t, m): #x is close prices
    wper = (t * (2) - 1)
    avrng = ta.ema(abs(x - x.shift(1)), t)
    smoothrng = (ta.ema(avrng, wper)) * m
    return np.array(smoothrng)

#rng filt is some other column, not sure what the calculation is
def rngfilt(x, r): #x is close prices, r is smoothrng
    rngfilt = []
    rngfilt.append(x[0])
    for i in range(1, len(x)):
        if (x[i] > rngfilt[i - 1]):
            if ((x[i] - r[i]) < rngfilt[i - 1]):
                rngfilt.append(rngfilt[i - 1])
            else:
                rngfilt.append(x[i] - r[i])
        else:
            if ((x[i] + r[i]) > rngfilt[i - 1]):
                rngfilt.append(rngfilt[i - 1])
            else:
                rngfilt.append(x[i] + r[i])

    return np.array(rngfilt)

def calculate_close_dif(close):
    close_dif = [None]
    direction = [None]

    for i in range(1, len(close)):
        close_dif.append((close[i] - close[i-1]))
        if (close[i] - close[i-1]) > 0: #calculates if it's upwards or downwards
            direction.append(1)
        else:
            direction.append(-1)
    return np.array(close_dif), np.array(direction)

def calculate_pivot(df):
    resitances = []
    supports = []

    prev_day = {'High': 0, 'Low': 0, 'Close': 0} #high, low, close
    current_day = {'High': 0, 'Low': 0, 'Close': 0} #high, low, close

    pivot, rl3, sl3, sl1, rl1 = 0, 0, 0, 0, 0

    for i in range(len(df)):
        current_day['Close'] = df.iloc[i]['close']
        if current_day['High'] < df.iloc[i]['close']: #adjusting highs
            current_day['High'] = df.iloc[i]['close']
        
        if current_day['Low'] > df.iloc[i]['close']: #adjusting lows
            current_day['Low'] = df.iloc[i]['close']

        #adding pivots, resistance, support levels
        if pivot == 0: #for the first day's values
            resitances.append(None)
            supports.append(None)
        else:
            resitances.append(rl3)
            supports.append(sl3)
        
        if df.iloc[i]['time'] == '15:29:00': #last session of the day
            prev_day = current_day
            pivot = (prev_day['High'] + prev_day['Low'] + prev_day['Close'])/3
            rl3 = prev_day['High'] + 2*(pivot - prev_day['Low'])
            sl3 = prev_day['Low'] - 2*(prev_day['High'] - pivot)
            rl1 = pivot*2 - prev_day['Low']
            sl1 = pivot*2 - prev_day['High']

    return np.array(resitances), np.array(supports)

def fake_pivot(directions):
    pivot = [None]

    for i in range(1, len(directions)):
        if directions[i] == 1 and directions[i - 1] == -1:
            pivot.append(1)
        elif directions[i] == -1 and directions[i - 1] == 1:
            pivot.append(-1)
        else:
            pivot.append(0)

    return np.array(pivot)

def create_time(datetime):
    time = []

    for i in datetime:
        time.append(i[11:])

    return np.array(time)

def create_data(df):

    df['time'] = create_time(df['datetime'])

    smrng = smoothrng(df["close"], 16, 3)
    filt = rngfilt(df["close"], smrng)  # doing one more activity to something to the close prices
    close_diff, direction = calculate_close_dif(df['close'])
    resistances, supports = calculate_pivot(df)

    df = df.astype({'datetime': 'string'})
    df['date'] = df.datetime.str[:10]  # craeting a column for only the date

    df['smrng'] = smrng
    df["filt"] = filt
    df['close_dif'] = close_diff
    df['direction'] = direction
    df['resistances'] = resistances
    df['supports'] = supports
    df['fake_pivot'] = fake_pivot(direction)

    df = df.dropna()

    return df

#main function for this file, returns pandas dataframe with all required columns calculated
def get_data(ticker):
    df = pd.read_csv('data_reduced/' + ticker + '.csv')
    df = create_data(df)

    return df


if __name__ == '__main__':
    ticker = 'TCS'
    df = get_data(ticker)
    print(df.head(20))
    # print(df.iloc[500:1000])