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

    positions = []
    date_ctr = 0
    date_checking = 0
    max_trades_per_day = 4

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
        
        

        
        execute, trade_type, eod = brain.calculate(capital, n, positions)

        if eod or date_ctr < 10:
            capital, executed, positions = executioner.trade(execute, capital, positions)

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
    fields = ['Date', 'Outcome', 'Time of Entry', 'Option Symbol', 'Entry Price', 'Exit Price', 'Time of Exit', 'SL', 'PnL', 'Cumulative PnL', 'Equity']
    timeofentry = 0
    entryprice = 0
    total_pnl = 0
    equity = 0
    for a in all_actions:
        if (a[0] == 'SOLD' and a[5] == True) or (a[0] == 'BOUGHT' and a[5] == False): #sold long or bought short
            date = a[4][:11]
            timeofexit = a[4][11:]
            exitprice = a[2]/a[6]
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

            new_row = (date, outcome, timeofentry, optionticker, entryprice, exitprice, timeofexit, SL, profit, total_pnl, equity)
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
    with open('writing/actions' + ticker + '.csv', 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

         # writing the fields
        csvwriter.writerow(fields)
        
        # writing the data rows
        csvwriter.writerows(all_actions_refined)


if __name__ == '__main__':
    run()