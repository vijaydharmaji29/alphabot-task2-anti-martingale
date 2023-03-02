import data_giver as dg
import pandas as pd

class action(object):
    def __init__(self, ticker, qty, buy, sell, buy_val, sell_val, date, trade_type):
        self.ticker = ticker
        self.qty = qty
        self.buy = buy
        self.sell = sell
        self.buy_val = buy_val
        self.sell_val = sell_val
        self.date = date
        self.trade_type = trade_type #True for longing, False for shorting

    def show(self):
        print(self.ticker, self.buy,
              self.sell, self.buy_val, self.sell_val)


def calculate(capital, df, positions):
    execute = []

    lot_size = 25

    for i in range(len(df)):

        trade_type = False
        eod = False

        #squaring off at the end of the day
        if (df.iloc[i]['time'] == '15:29:00'): 
            for p in positions:
                sell_val = p.qty*df.iloc[i]['close']
                new_action = action(p.ticker, p.qty, False, True, 0, sell_val, df.iloc[i]['date'])
                execute.append(new_action)
                # print('yes')
                eod = True
            continue

        #longing stocks
        if (df.iloc[i]['close'] > df.iloc[i]['filt']) and (df.iloc[i]['close_dif'] > 0) and (df.iloc[i]['direction'] == 1) and (df.iloc[i]['pivot'] == 1) and (len(positions) == 0): #long buy
            qty = int(capital/(df.iloc[i]['close']*lot_size))
            buy_val = qty*df.iloc[i]['close']*lot_size
            new_action = action(df.iloc[i]['symbol'], qty, True, False, buy_val, 0, df.iloc[i]['date'], True)
            execute.append(new_action)
        elif (df.iloc[i]['close'] < df.iloc[i]['filt']) and (df.iloc[i]['close_dif'] < 0) and (df.iloc[i]['direction'] == -1) and (df.iloc[i]['pivot'] == -1) and (len(positions) == 1) and positions[0].trade_type == True: #long sell
            qty = positions[0].qty
            sell_val = qty*df.iloc[i]['close']*lot_size
            new_action = action(df.iloc[i]['symbol'], qty, False, True, 0, sell_val, df.iloc[i]['date'], True)
            
            if positions[0].buy_val < df.iloc[i]['close']:
                trade_type = True

            execute.append(new_action)
        
        #shorting stocks
        elif (df.iloc[i]['close'] < df.iloc[i]['filt']) and (df.iloc[i]['close_dif'] < 0) and (df.iloc[i]['direction'] == -1) and (df.iloc[i]['pivot'] == -1) and (len(positions) == 0): #short sell
            qty = lot_size

            sell_val = qty*df.iloc[i]['close']*lot_size
            new_action = action(df.iloc[i]['symbol'], qty, False, True, 0, sell_val, df.iloc[i]['date'], False)

            execute.append(new_action) 

        elif (df.iloc[i]['close'] > df.iloc[i]['filt']) and (df.iloc[i]['close_dif'] > 0) and (df.iloc[i]['direction'] == 1) and (df.iloc[i]['pivot'] == 1) and (len(positions) == 1) and positions[0].trade_type == False: #short buy
            qty = positions[0].qty
            buy_val = qty*df.iloc[i]['close']*lot_size
            new_action = action(df.iloc[i]['symbol'], qty, True, False, buy_val, 0, df.iloc[i]['date'], False)

            if positions[0].buy_val < df.iloc[i]['close']:
                trade_type = True

            execute.append(new_action)

        print(df.iloc[i]['close'], df.iloc[i]['filt'], df.iloc[i]['close_dif'], df.iloc[i]['direction'], df.iloc[i]['pivot'], len(positions))


    return execute, trade_type, eod



if __name__ == '__main__':
    calculate()
    pass
