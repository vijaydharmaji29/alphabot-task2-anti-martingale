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


def calculate(capital, df, positions, stop_loss_given):
    execute = []
    stop_loss = None

    lot_size = 1

    for i in range(len(df)):

        trade_type = False
        eod = False
        stop_loss = None
        slrl_limit = 20

        #checking for stop_loss
        # if stop_loss_given != None:
        #     if df.iloc[i]['close'] < stop_loss_given and len(positions) and positions[0].trade_type == True:
        #         for p in positions:
        #             sell_val = p.qty*df.iloc[i]['close']
        #             new_action = action(p.ticker, p.qty, False, True, 0, sell_val, df.iloc[i]['date'], p.trade_type)
        #             execute.append(new_action)
        #     elif df.iloc[i]['close'] > stop_loss_given and len(positions) and positions[0].trade_type == False:
        #         for p in positions:
        #             sell_val = p.qty*df.iloc[i]['close']
        #             new_action = action(p.ticker, p.qty, False, True, 0, sell_val, df.iloc[i]['date'], p.trade_type)
        #             execute.append(new_action)
        #     continue

        #squaring off at the end of the day
        if (df.iloc[i]['time'] == '15:29:00'): 
            for p in positions:
                sell_val = p.qty*df.iloc[i]['close']
                new_action = action(p.ticker, p.qty, False, True, 0, sell_val, df.iloc[i]['date'], p.trade_type)
                execute.append(new_action)
                eod = True
            continue

        #longing stocks
        if (df.iloc[i]['close'] > df.iloc[i]['filt']) and (df.iloc[i]['close_dif'] > 0) and (df.iloc[i]['direction'] == 1) and (df.iloc[i]['supports'] - slrl_limit < df.iloc[i]['close']) and (df.iloc[i]['supports'] + slrl_limit < df.iloc[i]['close']) and (len(positions) == 0): #long buy
            qty = int(capital/(df.iloc[i]['close']*lot_size))
            buy_val = qty*df.iloc[i]['close']*lot_size
            new_action = action(df.iloc[i]['symbol'], qty, True, False, buy_val, 0, df.iloc[i]['date'], True)
            stop_loss = 0.9*df.iloc[i]['close']
            if qty > 0:
                execute.append(new_action)
        elif (df.iloc[i]['close'] < df.iloc[i]['filt']) and (df.iloc[i]['close_dif'] < 0) and (df.iloc[i]['direction'] == -1) and (df.iloc[i]['resistances'] + slrl_limit > df.iloc[i]['close']) and (df.iloc[i]['resistances'] - slrl_limit < df.iloc[i]['close']) and (len(positions) == 1) and positions[0].trade_type == True: #long sell
            qty = positions[0].qty
            sell_val = qty*df.iloc[i]['close']*lot_size
            new_action = action(df.iloc[i]['symbol'], qty, False, True, 0, sell_val, df.iloc[i]['date'], True)
            
            if positions[0].buy_val < df.iloc[i]['close']:
                trade_type = True
            
            if qty > 0:
                execute.append(new_action)
        
        #shorting stocks
        elif (df.iloc[i]['close'] < df.iloc[i]['filt']) and (df.iloc[i]['close_dif'] < 0) and (df.iloc[i]['direction'] == -1) and (df.iloc[i]['resistances'] + slrl_limit > df.iloc[i]['close']) and (df.iloc[i]['resistances'] - slrl_limit < df.iloc[i]['close']) and (len(positions) == 0): #short sell
            qty = int(capital/(df.iloc[i]['close']*lot_size))
            sell_val = qty*df.iloc[i]['close']*lot_size
            new_action = action(df.iloc[i]['symbol'], qty, False, True, 0, sell_val, df.iloc[i]['date'], False)
            stop_loss = 1.1*df.iloc[i]['close']
            if qty > 0:
                execute.append(new_action) 

        elif (df.iloc[i]['close'] > df.iloc[i]['filt']) and (df.iloc[i]['close_dif'] > 0) and (df.iloc[i]['direction'] == 1) and (df.iloc[i]['supports'] - slrl_limit < df.iloc[i]['close']) and (df.iloc[i]['supports'] + slrl_limit < df.iloc[i]['close']) and (len(positions) == 1) and positions[0].trade_type == False: #short buy
            qty = positions[0].qty
            buy_val = qty*df.iloc[i]['close']*lot_size
            new_action = action(df.iloc[i]['symbol'], qty, True, False, buy_val, 0, df.iloc[i]['date'], False)

            if positions[0].buy_val < df.iloc[i]['close']:
                trade_type = True

            if qty > 0:
                execute.append(new_action)

        #print(df.iloc[i]['close'], df.iloc[i]['filt'], df.iloc[i]['close_dif'], df.iloc[i]['direction'], df.iloc[i]['pivot'], len(positions))


    return execute, trade_type, eod, stop_loss



if __name__ == '__main__':
    calculate()
    pass
