import yfinance as yf
import pandas as pd

def get_stock_option_data(ticker, expiry_index=0):
    """
    Fetches current spot price and option chain for the given ticker.

    Parameters:
        ticker (str): e.g. "AAPL"
        expiry_index (int): 0 = nearest expiry, 1 = next expiry, etc.

    Returns:
        S (float): Latest closing stock price
        calls (pd.DataFrame): Calls chain for that expiry
        puts  (pd.DataFrame): Puts  chain for that expiry
        expiry (str): The expiration date used
        expirations (list): Full list of available expiries
    """
    # Download ticker object
    stock = yf.Ticker(ticker)

    # Spot price from last close
    hist = stock.history(period="1d")
    S = hist["Close"].iloc[-1]

    # Determine expiration date by index
    expirations = stock.options
    if expiry_index >= len(expirations):
        raise IndexError(f"expiry_index={expiry_index} out of range. Only {len(expirations)} expiries available.")
    expiry = expirations[expiry_index]

    # Fetch option chain
    chain = stock.option_chain(expiry)
    calls = chain.calls
    puts  = chain.puts

    # Ensure data types
    calls = calls.astype({"strike": float, "lastPrice": float})
    puts  = puts.astype({"strike": float, "lastPrice": float})

    return S, calls, puts, expiry, expirations

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

    # Use tail() for last `window` days to avoid ambiguous negative indexing
    daily_vol = returns.tail(window).std()
    annual_vol = daily_vol * (252 ** 0.5)
    return round(annual_vol, 4)
