# Import necessary libraries
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM

def dwnld_data(tkr,start,end):
    """Download historical stock price data from Yahoo Finance"""
    data = yf.download(tkr,start=start,end=end)
    data['Ret'] =data['Adj Close'].pct_change().dropna()
    return data.dropna()

def get_latest_price(tkr):
    """Get the latest stoc price for a given ticker symbol."""
    stock=yf.Ticker(tkr)
    latest_data=stock.history(period='1d')
    return latest_data['Close'].iloc[-1]

# Step 3: Fit Gaussian Hidden Markov Model
def fit_hmm(ret,n_comp=2):
    """Fit a Gaussian HMM to the daily returns"""
    model=GaussianHMM(n_components=n_comp,covariance_type="full",n_iter=1000)
    model.fit(ret)
    return model

# Step 4: Parameter Analysis
def analyze_params(model):
    """Analyze the mean and variance of each hidden state"""
    means=model.means_
    vars=np.sqrt(np.array([np.diag(cov) for cov in model.covars_]))
    return means,vars

# Step 5: Visualization
def visualize_res(data,states):
    """Visualize stock prices and inferred hidden states"""
    plt.figure(figsize=(14,8))
    plt.plot(data.index, data['Adj Close'], label='Prices', color='blue')
    plt.scatter(data.index, data['Adj Close'], c=data['Hidden_State'], cmap='viridis', label='States', s=10)
    plt.title("Stock Prices with Hidden States")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.legend()
    plt.show()

    # Transition Matrix Visualization
    plt.figure(figsize=(8,6))
    trans_matrix = model.transmat_
    plt.imshow(trans_matrix, cmap='viridis', interpolation='none')
    plt.colorbar(label='Transition Probability')
    plt.title("HMM Transition Matrix")
    plt.xlabel("To State")
    plt.ylabel("From State")
    plt.show()

# Main Function
if __name__=="__main__":
    tkr=input("Enter the stock ticker (e.g., AAPL, TSLA, GOOGL): ")
    start='2013-01-01'
    end='2023-12-31'
    
    # Step 1Download Data
    data= dwnld_data(tkr,start,end)

    # Step 2Fetch Latest Stock Price
    latest_price=get_latest_price(tkr)
    print(f"The stock price of  {tkr} is:${latest_price:.2f}")

    # Step 3:Fit HMM Model
    ret=data['Ret'].values.reshape(-1,1)
    model=fit_hmm(ret)

    # Predict hidden states
    states=model.predict(ret)
    data['Hidden_State']=states

    # Step 4 Parameter Analysis
    means,vars=analyze_params(model)
    print("Means of each hidden state:")
    print(means)
    print("Variances of each hidden state:")
    print(vars)

    # Step 5:Visualization
    visualize_res(data,states)
    
    # Step 6: Predicting the Future State
    last_state=states[-1]
    trans_matrix=model.transmat_
    trans_probs=trans_matrix[last_state]
    print(f"Transition probabilities from state{last_state}:{trans_probs}")
