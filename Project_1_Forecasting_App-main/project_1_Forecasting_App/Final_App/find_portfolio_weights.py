import pandas as pd
import numpy as np

# Creating a function called portfolio_weights which takes the cleaned data frame, the quantity of their positions, and the tickers for their positions 
def portfolio_weights(clean_data, portfolio_positions, tickers):
    # creating a variable to hold a list of the tickers 
    x = clean_data.iloc[-1,1:].to_list()
    # Creating a variable to hold a list of quantity for each ticker
    y = portfolio_positions["Quantity"].to_list()
    # using the numpy dot function to find the total portfolio value
    total = np.dot(x, y)
    # creating an empty dictionary to hold a key value pair of the ticker and its weight
    ticker_weights = {}
    # Using a for loop to iterate through the list of tickers
    for ticker in tickers:
        # Finding the stock price from the clean data dataframe
        stock_price = clean_data[ticker].to_list()[-1]
        # Finding the stock quantity from the portfolio_positions dataframe 
        stock_quantity = portfolio_positions.loc[portfolio_positions['Ticker'] == ticker, 'Quantity'].item()
        # Finding the weight of each stock by dividing the stock position by the total 
        stock_position = stock_price * stock_quantity
        # Appending to the ticker weights list and rounding
        ticker_weights[ticker] = round(stock_position / total, 2)
    # Creating an empty list to hold each stocks weight 
    weight = []
    # Using a for loop to iterate through the ticker weights dictionary 
    for value in ticker_weights.values():
        # appending only the value from the dictionary in the list 
        weight.append(value)
    # returning a list of each stocks weight
    return weight

# creating a function to find the total value of the portfolio; uses same code as above 
def portfolio_total(clean_data, portfolio_positions):
    x = clean_data.iloc[-1,1:].to_list()
    y = portfolio_positions["Quantity"].to_list()
    total = np.dot(x, y)
    return total
