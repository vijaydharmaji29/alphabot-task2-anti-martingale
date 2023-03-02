#independent program to check if my actions are valid

import csv

# capital = 10000000
position_ticker = []

# opening the CSV file
with open('writing/actionsRELIANCE.csv', mode='r') as file:
    # reading the CSV file
    csvFile = csv.reader(file)

    # displaying the contents of the CSV file
    for row in csvFile:
        action, ticker, val = row[0], row[1], row[2]
        if action == 'BOUGHT':
            if ticker not in position_ticker:
                # capital -= float(val)
                position_ticker.append(ticker)
            else:
                print("ERROR: ", row)
                break
        elif action == 'SOLD':
            if ticker in position_ticker:
                # capital += float(val)
                position_ticker.remove(ticker)
            else:
                print("ERROR: ", row)
                break
        else:
            if ticker not in position_ticker:
                print("ERROR: ", row)
                break
        print('GOOD: -', row)
    else:
        print("ALL GOOD!")