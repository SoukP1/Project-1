import os
import requests
import json
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi
import streamlit as st
import copy
import matplotlib.pyplot as plt
from api_caller import api_call
from dotenv import load_dotenv
from make_close_price import make_daily_close
from find_portfolio_weights import portfolio_weights
from find_portfolio_weights import portfolio_total
from monte_carlo_df import create_simulation_df
from MCForecastTools import MCSimulation

# Creating a title for the web application using the st.title function from streamlit 
st.title("Portfolio Forecasting App")

# Creating a sidebar markdown using st.sidebar to give the user instructions on how to use the app
st.sidebar.markdown('''
Use the following instructions to correctly format your portfolio data for the simulation:

- The app takes a single CSV file. To start, open an excel workbook and create two columns: 'Ticker' and 'Quantity' 
    - Add the company ticker to the ticker column
    - Add the quantity to the quantity column
    - Save the excel book as a CSV file
    - Drag and drop file into app to begin simulation

    ''')

# This block asks the user for two date inputs which will be used to access historical pricing data via an API
initial_price_date = st.date_input("Please enter a start date for historical data.")
end_price_date = st.date_input("Please enter an end date for historical data.")

# This block allows the users to upload a csv file of their portfolio tickers and the quantity for each ticker
# Creates a list of their respective tickers
portfolio_data = st.file_uploader("Upload Portfolio Information Here:")
if portfolio_data is not None: 
    member_df = pd.read_csv(portfolio_data)
    tickers = list(member_df['Ticker'].unique()) 

    # This code uses the date inputs from the user early and sets the start and end date variables for the API
    start_date = pd.Timestamp(str(initial_price_date), tz="America/New_York").isoformat()
    end_date = pd.Timestamp(str(end_price_date), tz="America/New_York").isoformat()
    timeframe = "1Day"
    
    # Calling the api_call() function to create the alpaca rest object
    alpaca_data = api_call()
    
    # Creating a historical data dataframe from the user inputs for stocks, start date, and end date
    historical_data = alpaca_data.get_bars(
        tickers,
        timeframe, 
        start = start_date,
        end = end_date
    ).df

    # Calling the make_daily_close function to create a dataframe of the historical data's closing prices for each ticker
    cleaned_df = make_daily_close(historical_data, tickers)
    
    # Calling the portfolio_weights function to find each stock's weight of the total portfolio  
    weight = portfolio_weights(cleaned_df, member_df, tickers)
    
    # Calling the portfolio_total function to calculate the total value of the portfolio
    portfolio_value = round(portfolio_total(cleaned_df, member_df), 2)
    
    # Calling the create_simulation_df to create a dataframe that fits the correct table format for the Monte Carlo Simulation
    simulation_df = create_simulation_df(historical_data)
    
    # Asking the user to input how many years in the future they want to simulate
    # Changing number to integer
    simulation_length = int(st.number_input("How many year do you want to simulate?", min_value=1))
    
    # Creating a metric that displays the starting value of their portfolio 
    st.metric("Starting Portfolio Value", f"${portfolio_value:,}")
    
    # Creating an interactive button the user clicks on to start the portfolio forecast 
    if st.button("Press here to start simulation"):
    
        # Calling the MCSimulation function and entering in the created simulation dataframe, the portfolio weights, and the simulation legnth 
        MC_sim = MCSimulation(
        portfolio_data = simulation_df,
        weights = weight,
        num_simulation = 150,
        num_trading_days = 252 * simulation_length)
        
        # Creating a dataframe to display stock informtion, particulary the closing price for each day
        MC_sim_daily_return = MC_sim.portfolio_data.head()
        
        # Creating a new dataframe that displays the daily return between each trading day
        MC_sim_data = MC_sim.calc_cumulative_return()
        
        # Creating a summary statistics table that displays the 95% upper and lower confidence interval
        MC_summary = MC_sim.summarize_cumulative_return()
       
        # Creating the max statistical loss with a 95% confidence interval 
        # Rounding to two decimal places 
        MC_lower = round(MC_summary[8] * portfolio_value, 2)
        
        # Creating the max statistical gain with a 95% confidence interval 
        # Rounding to two decimal places
        MC_upper = round(MC_summary[9] * portfolio_value, 2)
        
        # Calculating the max statistical value of the portfolio with a 95% confidence interval 
        # Rounding to two decimal places
        upper_net = round(MC_upper - portfolio_value, 2)
        
        # Calculating the minimum statistical value of the portfolio with a 95% confidence interval 
        # Rounding to two decimal places
        lower_net = round(MC_lower - portfolio_value, 2)
        
        # displaying the max gain/loss of the portfolio 
        st.metric("Maximum Gain/Loss", f"${upper_net:,}", delta_color="normal")
        
        # displaying the min gain/loss of the portfolio
        st.metric("Minimum Gain/Loss", f"${lower_net:,}", delta_color="normal")
        
        # Writing a 95% confidence interval estimate for the range of the portfolio over the amount of year the user chooses 
        st.write(f"With a 95% confidence interval, your starting portfolio value of {portfolio_value:,} ranges from {MC_lower:,} to {MC_upper:,} over {simulation_length} year(s).")
          
       
   
        
  
    

    


    
    

    
   
    
    


        
    
