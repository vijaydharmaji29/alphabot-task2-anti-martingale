class position(object):
    def __init__(self, ticker, qty, buy_val, trade_type):
        self.ticker = ticker
        self.qty = qty
        self.buy_val = buy_val
        self.trade_type = trade_type
    def show(self):
        print(self.ticker, self.qty,
              self.buy_val)

def trade(execute, capital, positions):
    positions = positions
    executed = []
    capital = capital
    transaction_cost = 0
    ctr = 0
    for e in execute:
        print("EXECUTING: - ", ctr)
        if e.buy:
            capital -= e.buy_val
            capital -= transaction_cost
            
            if e.trade_type == True:
                new_pos = position(e.ticker, e.qty, e.buy_val, True)
                positions.append(new_pos)
            else:
                positions.pop()

            print("BOUGHT -", e.ticker, " -", e.buy_val, ' -', e.trade_type)
            executed.append(('BOUGHT', e.ticker, e.buy_val, capital, e.date, e.trade_type))
        elif e.sell:
            capital += e.sell_val
            capital -= transaction_cost

            if e.trade_type == False:
                new_pos = position(e.ticker, e.qty, e.buy_val, False)
                positions.append(new_pos)
            else:
                positions.pop()
            print("SOLD -", e.ticker, " -", e.sell_val)
            executed.append(('SOLD', e.ticker, e.sell_val, capital, e.date, e.trade_type))


        ctr += 1

    return capital, executed, positions

