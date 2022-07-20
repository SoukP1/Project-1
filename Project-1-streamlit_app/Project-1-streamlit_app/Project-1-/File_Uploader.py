import os
import requests
import json
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi
import streamlit as st
from api_caller import api_call
from dotenv import load_dotenv
from make_close_price import make_daily_close
from find_portfolio_weights import portfolio_weights

portfolio_data = st.file_uploader("Upload Portfolio Information Here")
if portfolio_data is not None: 
    df = pd.read_csv(portfolio_data)
    tickers = list(df['Ticker'].unique()) 
    st.table(df)


    initial_price_date = st.date_input("Please enter a start date for the simulation.")
    end_price_date = st.date_input("Please enter an end date for the simulation.")
    start_date = pd.Timestamp(str(initial_price_date), tz="America/New_York").isoformat()
    end_date = pd.Timestamp(str(end_price_date), tz="America/New_York").isoformat()
    timeframe = "1Day"

    alpaca_data = api_call()

    historical_data = alpaca_data.get_bars(
        tickers,
        timeframe, 
        start = start_date,
        end = end_date
    ).df

   
    cleaned_df = make_daily_close(historical_data, tickers)
    st.table(cleaned_df)

    
    weights = portfolio_weights(cleaned_df, df, tickers)
    st.write(weights)

    




    
    

    
   
    
    


        
    