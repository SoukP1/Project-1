import os
import requests
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi


# Creating a function called api_call()
def api_call():
    # Checking to see if the computer recognizes the env file in the working directory 
    load_dotenv()
    
    # Getting the API key and Secret Key
    alpaca_api = os.getenv("ALPACA_API_KEY")
    alpaca_secret = os.getenv("ALPACA_SECRET_KEY")
    
    # Creating the rest object
    alpaca = tradeapi.REST(
        alpaca_api,
        alpaca_secret,
        api_version="v2"
    )
    
    # returning the rest object
    return alpaca




