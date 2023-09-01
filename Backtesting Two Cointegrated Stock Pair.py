# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Y28t8g5BXgDKfZwYFyduP1rGeyUwCcK3
"""

import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression

# Define the stock symbols and the date range
stock_symbols = ['TCS.NS','INFY.NS']
start_date = '1992-01-01'
end_date = '2023-08-01'

# Fetch stock data using yfinance
stock_data = yf.download(stock_symbols, start=start_date, end=end_date)['Close']

# Drop rows with missing values
stock_data.dropna(inplace=True)

# Extract adjusted closing prices
stock1 = stock_data['INFY.NS']
stock2 = stock_data['TCS.NS']
#print("stock1 & stock 2:", stock1 , stock2)

# Create a linear regression model
model = LinearRegression()

# Reshape the data for regression
X = stock1.values.reshape(-1, 1)
y = stock2.values

# Fit the model
model.fit(X, y)

#making it of same value..................................................................................................
#stock1=stock1p*4
#stock2=stock2p

# Calculate residuals
residuals = y - model.predict(X)

# Calculate standard deviation of residuals
std_dev_residuals = np.std(residuals)

# Print results
print("Standard Deviation of Residuals:", std_dev_residuals)

# Backtesting Logic
capital=0
position_open = False
num_of_days = 0
pnl = 0
tpnl=0
p=0
q=0
lot_size_of_stock1=0
lot_size_of_stock2=0
start_date=0
end_date=0
cnt=0

for i in range(len(stock_data)):
    if not position_open:
        if residuals[i] <= -2*std_dev_residuals:  # Buy condition
            position_open = True

            lot_size_of_stock2= int(stock1[i])
            buy_price = stock2[i] *lot_size_of_stock2
            print("buying price of stock2 : ", buy_price)

            lot_size_of_stock1=int(stock2[i])
            sell_price = stock1[i]*lot_size_of_stock1
            print("selling price of stock1 : ", sell_price)
            fund_used= buy_price + sell_price
            print("fund used :", fund_used)

            q=1
            print(f"...Buying... Date: {stock_data.index[i]}")
            start_date= stock_data.index[i]

        if residuals[i] >= 2*std_dev_residuals:  # Short condition
            position_open = True
            lot_size_of_stock1=int(stock2[i])
            buy_price = stock1[i] * lot_size_of_stock1
            print("buying price of stock1 : ", buy_price)

            lot_size_of_stock2= int(stock1[i])
            sell_price = stock2[i]*lot_size_of_stock2
            print("selling price of stock2 : ", sell_price)
            fund_used= buy_price + sell_price
            print("fund used :", fund_used)

            p=1
            print(f"...Shorting... Date: {stock_data.index[i]}")
            start_date= stock_data.index[i]

    if position_open :
        if residuals[i] >= -std_dev_residuals and q==1 :
            position_open = False
            q=0
            cnt += 1
            sell_price = stock2[i]*lot_size_of_stock2
            print("selling price of stock2 :",sell_price)
            buy_price = stock1[i]*lot_size_of_stock1
            print("buying price of stock1 :",buy_price)
            pnl = (sell_price - buy_price)
            tpnl += (sell_price - buy_price)
            print(f"...Selling... Date: {stock_data.index[i]}")

            end_date = stock_data.index[i]
            num_of_days = (end_date - start_date).days
            roi=int((pnl/fund_used)*100)
            print("number of days :",num_of_days )
            print("p&l :", pnl)
            print("ROI : ", roi,"%")
            print("-----------------------------------------------------------------------------------------------------")

            # Square off condition

        if residuals[i] <= std_dev_residuals and p==1:
            position_open = False
            p=0
            cnt += 1
            sell_price = stock1[i]*lot_size_of_stock1
            print("selling price of stock1 :",sell_price)
            buy_price = stock2[i]*lot_size_of_stock2
            print("buying price of stock2 :",buy_price)
            pnl = (sell_price - buy_price)
            tpnl += (sell_price - buy_price)
            print(f"...Exiting Short...   Date: {stock_data.index[i]}")

            end_date = stock_data.index[i]
            num_of_days = (end_date - start_date).days
            roi=int((pnl/fund_used)*100)
            print("number of days :",num_of_days )
            print("p&l :", pnl)
            print("ROI : ", roi,"%")
            print("-----------------------------------------------------------------------------------------------------")

print("Total P&L:", tpnl)
print("Total number of trades :", cnt)