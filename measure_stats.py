#independent program to calculate statistics
import math
from datetime import datetime
import csv

capital = 10000000
icap = capital
position_ticker = {}
profitable_trades = []
loss_making_trades = []
start_date = datetime.today()
end_date = datetime.today()

flag = True

max = icap
min = icap

transaction_cost = 0


def calc_drawdown():
    global max
    global min
    tval = capital
    for i in position_ticker:
        tval += position_ticker[i]

    if tval > max:
        max = tval
    if tval < min:
        min = tval

# opening the CSV file
with open('writing/actionsNIFTYBANK.csv', mode='r') as file:
    # reading the CSV file
    csvFile = csv.reader(file)

    # displaying the contents of the CSV file
    for row in csvFile:
        action, ticker, val, date, trade_type = row[0], row[1], float(row[2]), row[4], row[-2]
        date = datetime.strptime(date, "%d-%m-%Y %H:%M")
        if flag:
            start_date = date
            end_date = date
            flag = False

        if date > end_date:
            end_date = date

        if val == 0:
            continue

        if action == 'BOUGHT':
            capital -= val
            
            if trade_type == 'False':
                trade_profit = position_ticker[ticker] - val
                profit_percentage = trade_profit*100/val
                trade = (ticker, position_ticker[ticker], val, trade_profit, profit_percentage)
                if trade_profit > 0:
                    profitable_trades.append(trade)
                else:
                    loss_making_trades.append(trade)
                    
                position_ticker.pop(ticker)
            else:
                position_ticker[ticker] = val

        elif action == 'SOLD':
            capital += val

            if trade_type == 'True':   
                trade_profit = val - position_ticker[ticker]
                profit_percentage = trade_profit*100/position_ticker[ticker]
                trade = (ticker, position_ticker[ticker], val, trade_profit, profit_percentage)
                if trade_profit > 0:
                    profitable_trades.append(trade)
                else:
                    loss_making_trades.append(trade)
                    
                position_ticker.pop(ticker)
            else:
                position_ticker[ticker] = val

        calc_drawdown()

##calculating all stats:
no_proftable_trades = len(profitable_trades)
no_loss_making_trades = len(loss_making_trades)
no_total_trades = no_loss_making_trades+no_proftable_trades
win_rate = no_proftable_trades/no_total_trades

total_profits = 0
avg_profit_per_trade = 0 #only if the trade is profitable
total_loss = 0
avg_loss_per_trade = 0 #only if the trade is loss making

for i in profitable_trades:
    total_profits += i[3]

for i in loss_making_trades:
    total_loss += i[3]

avg_loss_per_trade = total_loss/no_loss_making_trades
avg_profit_per_trade = total_profits/no_proftable_trades

final_val = capital

equity = 0

for i in position_ticker:
    equity += position_ticker[i]

final_val += equity

final_profit = final_val - icap - (transaction_cost*2*no_total_trades)

dtstart = start_date
dtend = end_date
total_days = int((dtend - dtstart).days)

expectancy = win_rate*avg_profit_per_trade + (1 - win_rate)*avg_loss_per_trade

total_loss_profit_perc = 0
for i in loss_making_trades + profitable_trades:
    total_loss_profit_perc += i[-1]

ror = total_loss_profit_perc/no_total_trades

max_drawdown = min - max
max_drawdown_perc = max_drawdown*100/max

cagr = ((math.pow(((final_profit + icap)/icap),365/total_days)) - 1)*100

risk_reward_ratio = total_profits/total_loss

print('BACKTEST START DATE: ', start_date)
print('BACKTEST END DATE: ', end_date)
print('TOTAL DAYS: ', total_days)
print('FINAL PROFIT: ', final_profit)
print('TOTAL TRADES: ', no_total_trades)
print('PROFITABLE TRADES: ', no_proftable_trades)
print('LOSS MAKING TRADES: ', no_loss_making_trades)
print('WIN RATE: ', win_rate)
print('AVG PROFIT PER TRADE: ', avg_profit_per_trade)
print('AVG LOSS PER TRADE: ', avg_loss_per_trade)
print('RISK REWARD RATIO: ', risk_reward_ratio)
print('EXPECTANCY: ', expectancy)
print('AVERAGE ROR PER TRADE: (%)', ror)
print('MAX DRAWDOWN: ', max_drawdown)
print('MAX DRAWDOWN PERCENTAGE: ', max_drawdown_perc)
print('AVG ANNUALISED RETURNS (%): ', cagr)