import brain
import data_giver as dg
import executioner
import csv
import os
import pandas
import data_collection as dc
import numpy as np

ticker = 'NIFTYBANK'

def run():
    
    capital = 10000000
    icap = capital
    stop_loss = None

    expected = 1.4
    p_win = 0.42
    p_loss = 0.58
    capital_perc_kelly = (expected*p_win - p_loss)/expected
    #capital_perc_kelly = 1


    positions = []
    date_ctr = 0
    date_checking = 0
    max_trades_per_day = 5

    percent = 1

    i = 0
    tn = 0

    all_actions = []
    all_actions_refined = []

    while True:
        # print('INDEXING AT - ', i)
        n = dg.next(i)

        zero_data = np.zeros(shape=(10,10))
        dummydf = pandas.DataFrame()    

        if type(n) != type(dummydf):
            break
        
        session_date = n.iloc[0]['date_actual']
    
        if date_checking != session_date:
            date_checking = session_date
            date_ctr = 0
        
        execute, trade_type, eod, stop_loss = brain.calculate(capital*capital_perc_kelly, n, positions, stop_loss)

        if eod or date_ctr < max_trades_per_day*2:
            extra_cap, executed, positions = executioner.trade(execute, capital*capital_perc_kelly, positions)
            capital = capital*(1 - capital_perc_kelly) + extra_cap

            if len(execute) > 0:

                print('TRADE DATE: ', session_date)
                # print('TRADE NUMBER: ', date_ctr)
                # tn += 1

                date_ctr += 1

                if execute[0].sell and trade_type:
                    percent -= .2
                    capital*percent

                    if capital < icap*.2:
                        capital = icap*.2

                elif execute[0].sell and  not trade_type:
                    capital = icap

            for j in executed:
                all_actions.append(j)

        i+=1

    eval = capital
    for i in positions:
        eval += i.buy_val

    print(eval)
    print(date_ctr)

    #refining transaction log to trade log:
    fields = ['Date', 'Outcome', 'Time of Entry', 'Option Symbol', 'Entry Price', 'Exit Price', 'Time of Exit', 'Quantity', 'SL', 'PnL', 'Cumulative PnL', 'Equity']
    timeofentry = 0
    entryprice = 0
    total_pnl = 0
    equity = 0
    for a in all_actions:
        if (a[0] == 'SOLD' and a[5] == True) or (a[0] == 'BOUGHT' and a[5] == False): #sold long or bought short
            date = a[4][:11]
            qty = a[6]
            timeofexit = a[4][11:]
            exitprice = a[2]/qty
            optionticker = a[1]
            profit = a[2] - entryprice*a[6]
            total_pnl += profit
            outcome = 'Bullish'
            if profit <= 0:
                outcome = 'Bearish'
            SL = None

            #calculating equity value
            if a[5]:
                equity -= a[2]
            else:
                equity += a[2]


            new_row = (date, outcome, timeofentry, optionticker, entryprice, exitprice, timeofexit, qty, SL, profit, total_pnl, equity)
            all_actions_refined.append(new_row)

            #resting values as it will allow easier debuging
            timeofentry = 0
            entryprice = 0
        else: #sold short or bought long
            #calculating equity value
            if a[5]:
                equity += a[2]
            else:
                equity -= a[2]

            timeofentry = a[4][11:]
            entryprice = a[2]/a[6]

        

    # writing to csv file
    with open('refined_writing/actions' + ticker + '.csv', 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

         # writing the fields
        csvwriter.writerow(fields)
        
        # writing the data rows
        csvwriter.writerows(all_actions_refined)


    with open('writing/actions' + ticker + '.csv', 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        
        # writing the data rows
        csvwriter.writerows(all_actions)
    
    


if __name__ == '__main__':
    run()