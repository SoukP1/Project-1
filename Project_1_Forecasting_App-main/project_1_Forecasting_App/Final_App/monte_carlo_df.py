import os
import requests
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi
import streamlit as st
import copy 
from api_caller import api_call
from dotenv import load_dotenv
from make_close_price import make_daily_close
from find_portfolio_weights import portfolio_weights
from MCForecastTools import MCSimulation


# Creating a function to create a dataframe that fits the specific format of the monte carlo simulation 
def create_simulation_df(df_portfolio):
    # creating an empty dictionary
    test = {}
    # Using a for loop to iterate through each stock symbol in the created alpaca dataframe 
    for ticker in df_portfolio['symbol'].unique():
        # Creating a key:value pair for the ticker and its data to seperate the dataframe
        test[ticker] = copy.deepcopy(df_portfolio.loc[df_portfolio['symbol'] == ticker])
        # Dropping the symbol column from each dataframe
        test[ticker].drop(columns = ['symbol'], inplace = True)
    # Using pd.concat to concatenate the seperated data frames 
    # using a for loop to iterate through the key in test dictionary
    testing_df = pd.concat([test[key] for key in test.keys()], axis=1, keys=test.keys())
    return testing_df
