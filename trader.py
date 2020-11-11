
import sys
import pandas as pd
import numpy as np
from datetime import datetime
from matplotlib import pyplot


balance = 0
last_buy = None

SHORT_WINDOW = 30
LONG_WINDOW = 100
SYMBOL = 'PFE'
FILENAME = 'data/PFE-1999-05-31-to-2009-03-05.csv'


def onBuy(price):
    global last_buy, balance
    print("BUY  @ $%s" % round(price, 2))    
    last_buy = price
    if last_buy is None:
        balance = 0


def onSell(price):
    global balance, last_buy
    if last_buy is not None:
        balance += price - last_buy
        print("SELL @ $%s, Balance: $%s" % (round(price, 2), round(balance, 2)))



def strategy(data):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1

    for i in range(len(data)):
        if data['SMA_SHORT'][i] > data['SMA_LONG'][i]:
            if flag != 1:
                sigPriceBuy.append(data[SYMBOL][i])
                sigPriceSell.append(np.nan)
                flag = 1
                onBuy(data[SYMBOL][i])
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        elif data['SMA_SHORT'][i] < data['SMA_LONG'][i]:
            if flag != 0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data[SYMBOL][i])
                flag = 0 
                onSell(data[SYMBOL][i])
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)

    print(balance)
    return (sigPriceBuy, sigPriceSell)



if __name__ == '__main__':


    VALUE = pd.read_csv(FILENAME)
    
    SMA_SHORT = pd.DataFrame()
    SMA_SHORT['Adj Close'] = VALUE['Adj Close'].rolling(window=SHORT_WINDOW).mean()

    SMA_LONG = pd.DataFrame()
    SMA_LONG['Adj Close'] = VALUE['Adj Close'].rolling(window=LONG_WINDOW).mean()


    data = pd.DataFrame()
    data[SYMBOL] = VALUE['Adj Close']
    data['SMA_SHORT'] = SMA_SHORT['Adj Close']
    data['SMA_LONG'] = SMA_LONG['Adj Close']
    N = len(data[SYMBOL])
    _strategy = strategy(data)
    balance = round(balance, 2)
    data['Buy Signal'] = _strategy[0]
    data['Sell Signal'] = _strategy[1]


    X_STEP = N / 7


    pyplot.figure(figsize=(12.5, 4.5))
    pyplot.xticks(np.arange(0, N, step=X_STEP))
    pyplot.plot(VALUE['Date'], VALUE['Adj Close'], label=SYMBOL, alpha=.3)
    pyplot.plot(SMA_SHORT['Adj Close'], label='SMA_SHORT', alpha=.3)
    pyplot.plot(SMA_LONG['Adj Close'], label='SMA_LONG', alpha=.3)
    pyplot.title('%s Adjusted Close Price History' % SYMBOL)
    pyplot.xlabel('Dec 12, 1980 - Nov 9, 2020')
    pyplot.ylabel('Adj Close Price (USD)')
    pyplot.legend(loc='upper left')
    pyplot.scatter(data.index, data['Buy Signal'], label='Buy', marker='^', color='green')
    pyplot.scatter(data.index, data['Sell Signal'], label='Sell', marker='v', color='red')
    pyplot.text(X_STEP * 6, 0, 'Balance: $%s' % balance, fontsize=12)
    print('Showing.... (Balance: %s)' % balance)
    pyplot.show()
    print('Done')
