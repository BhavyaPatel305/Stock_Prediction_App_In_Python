#Import required modules
import streamlit as st
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly

# Install module for graphs
from plotly import graph_objs as go

