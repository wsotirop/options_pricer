import yfinance as yf
import pandas as pd

def get_stock_option_data(ticker, expiry=None):
    """
    Fetches current spot price and option chain for the given ticker.

    Parameters:
        ticker (str): e.g. "AAPL"
        expiry (str): expiration date as "YYYY-MM-DD". If None, uses the nearest expiry.

    Returns:
        S (float): Latest closing stock price
        calls (pd.DataFrame): Calls chain for that expiry
        puts  (pd.DataFrame): Puts  chain for that expiry
        expiry (str): Expiration date used
    """
    # Download ticker object
    stock = yf.Ticker(ticker)

    # Spot price from last close
    hist = stock.history(period="1d")
    S = hist["Close"].iloc[-1]

    # Determine expiration date
    expirations = stock.options
    if expiry is None:
        expiry = expirations[0]
    elif expiry not in expirations:
        raise ValueError(f"Expiry {expiry} not in available dates: {expirations}")

    # Fetch option chain
    chain = stock.option_chain(expiry)
    calls = chain.calls
    puts  = chain.puts

    # Ensure data types
    calls = calls.astype({"strike": float, "lastPrice": float})
    puts  = puts.astype({"strike": float, "lastPrice": float})

    return S, calls, puts, expiry

def get_historical_volatility(ticker, window=30):
    """
    Computes annualized historical volatility from daily returns over a rolling window.

    Parameters:
        ticker (str): e.g. "AAPL"
        window (int): Number of trading days for volatility (e.g., 30)

    Returns:
        float: Annualized volatility
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period=f"{window + 10}d")  # Add buffer for clean returns
    returns = hist["Close"].pct_change().dropna()

    daily_vol = returns[-window:].std()
    annual_vol = daily_vol * (252 ** 0.5)
    return round(annual_vol, 4)
