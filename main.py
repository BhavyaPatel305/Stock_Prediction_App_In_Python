#Import required modules
import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly

# Import module for graphs
from plotly import graph_objs as go


# Date from which data is needed
START = "2015-01-01"

# Date to which data is needed
# strftime used to get date in string format(%Y-%m-%d)
TODAY = date.today().strftime("%Y-%m-%d")

# Title of the app
st.title("Stock Prediction App")

# Create choices of stocks that can be used
#1: AAPL: Apple Inc.
#2: GOOG: Google
#3: MSFT: Microsoft
#4: GME: GameStop Corp.
stocks = ("AAPL", "GOOG", "MSFT", "GME")

# Creating select box
selected_stock = st.selectbox("Select dataset for prediction", stocks)

# Slider to select the number of years for prediction
# slider("label", start, end)
n_years = st.slider("Years of prediction:", 1, 4)

# Calculate the period
period = n_years*365

# Function to load stock data
# ticker: Selected stock
def load_data(ticker):
        # Using Yahoo Finance
        data = yf.download(ticker, START, TODAY)
        
        # Data will be returned in a pandas dataframe
        data.reset_index(inplace=True) # Resetting index: It will place date on the first column
        
        # return data
        return data

data_load_state = st.text("Load Data...")
data = load_data(selected_stock)
data_load_state.text("Loading Data...done!")
