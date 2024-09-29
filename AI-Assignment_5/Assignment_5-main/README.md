# Assignment_5

# Gaussian HMM Financial Analysis

This project implements Gaussian Hidden Markov Models (HMMs) to analyze financial time series data, focusing on identifying hidden market regimes. The financial market often exhibits distinct periods of volatility that are not directly observable, making it challenging for investors to make informed decisions. By applying HMMs, this analysis aims to uncover these hidden states, providing valuable insights into stock behavior over time.

## Description

This project analyzes financial time series data using Gaussian Hidden Markov Models (HMMs) to identify hidden market regimes. The goal is to enhance our understanding of stock price movements and provide insights for informed financial decision-making.

## Objectives

- 1. Data Collection: Utilize the Yahoo Finance API to download historical stock price data, focusing on daily adjusted closing prices.
- 2.  Preprocessing: Calculate daily returns from the adjusted closing prices to prepare the data for modeling.
- 3. Model Fitting: Fit a Gaussian HMM to the daily returns data, selecting an appropriate number of hidden states to represent different market conditions (e.g., high and low volatility).
- 4. Parameter Analysis: Analyze the mean and variance of each hidden state to interpret their significance in the context of financial markets (e.g., identifying bull and bear markets).
5. Visualization: Create visualizations to plot stock prices along with inferred hidden states and to display the transition matrix, which illustrates the probabilities of switching between hidden regimes.
6. Insights and Predictions: Discuss how the inferred hidden states can inform financial decision-making, such as risk management and portfolio adjustments. Predict the likely future state of the market based on the most recent data.

## Features

- Fetches historical stock prices from Yahoo Finance.
- Calculates daily returns for volatility analysis.
- Fits a Gaussian HMM to the daily returns data.
- Identifies and visualizes hidden market regimes.
- Displays the transition matrix to understand market dynamics.

## Installation

To run the analysis, you will need Python 3.x and the following libraries:

- `yfinance`: for downloading stock price data
- `numpy`: for numerical operations
- `pandas`: for data manipulation
- `matplotlib`: for plotting
- `hmmlearn`: for implementing Gaussian HMMs

1)You can install the required packages using pip.  `requirements.txt` 

$ pip install -r requirements.txt

2)To run the analysis, execute the following command:

python chellenge5.py

3)When prompted, enter a stock ticker:
Enter the stock ticker (e.g., AAPL, TSLA, GOOGL): GOOGL

