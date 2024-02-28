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
# st.cache: It will cache the data so that it does not have to download same data again and again.
@st.cache
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

# Raw Pandas Data Frame
st.subheader('Raw Data')
st.write(data.tail())

# Plotting raw data
def plot_raw_data():
        # Creating plotly graph object
        fig = go.Figure()
        # X-axis: Date
        # Y-axis: Open
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        
        # X-axis: Date
        # Y-axis: Close
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
        
        # Slider to zoom in and out
        fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
        
        # Plot the graph
        st.plotly_chart(fig)
        
# Calling the function to plot raw data
plot_raw_data()


# Forecasting with Prophet
# Using Data and Close columns for forecasting
df_train = data[['Date', 'Close']]

# Renaming Columns as Prophet requires data in a certain format
# According to Prophet Documentation:
# Data should be called as ds
# Close should be called as y
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

# Creating Facebook Prophet Model
m = Prophet()

# Fit the data and start the training
m.fit(df_train)

# For forecast, need a dataframe that goes into the future
# periods needs to be in no.of days
future = m.make_future_dataframe(periods=period)

# Predict the future dataframe
forecast = m.predict(future)

# Plot the data frame
st.subheader('Forecast Data')
st.write(forecast.tail())

# Plotting Forecast Data
st.write('Forecasting Data') # Label
fig1 = plot_plotly(m, forecast) # Needs Model and forecast
st.plotly_chart(fig1)

st.write('Forecast Components') # Label
# No need for plotly graph, just a normal graph
fig2 = m.plot_components(forecast)
st.write(fig2) # Not a plotly chart