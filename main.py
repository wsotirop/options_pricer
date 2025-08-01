from models.black_scholes import black_scholes_price
from models.binomial_tree import binomial_tree_price
from utils.fetch_data import get_stock_option_data, get_historical_volatility
from utils.implied_vol import implied_volatility
import numpy as np
from datetime import datetime


def run_pricer(ticker="AAPL", option_type="call", num_options=10):
    r = 0.05

    # 1) Fetch nearest expiry
    S, calls, puts, expiry, expirations = get_stock_option_data(ticker, expiry_index=0)

    # 2) Compute days to expiry
    expiry_dt      = datetime.strptime(expiry, "%Y-%m-%d").date()
    days_to_expiry = (expiry_dt - datetime.today().date()).days

    # 3) If nearest expiry is today/past, switch to next one
    if days_to_expiry <= 0:
        print(f"Nearest expiry ({expiry}) is today/past — switching to next expiry.")
        S, calls, puts, expiry, expirations = get_stock_option_data(ticker, expiry_index=1)
        expiry_dt      = datetime.strptime(expiry, "%Y-%m-%d").date()
        days_to_expiry = (expiry_dt - datetime.today().date()).days

    # 4) Now compute T safely
    T = days_to_expiry / 365

    # 5) Historical volatility
    sigma = get_historical_volatility(ticker)
    print(f"\nEstimated volatility (sigma): {sigma:.4f}")

    # 6) Select option chain
    chain = calls if option_type == "call" else puts

    print(f"\n{ticker} — {option_type.upper()} OPTIONS — Expiry: {expiry}")
    print(f"{'Strike':>8} | {'Market':>8} | {'B-S':>8} | {'BinTree':>8} | {'ImplVol':>8}")
    print("-" * 65)

    # 7) Loop and print
    for i, row in chain.iterrows():
        if i >= num_options:
            break
        K = row["strike"]
        market_price = row["lastPrice"]

        bs = black_scholes_price(S, K, T, r, sigma, option_type)
        bt = binomial_tree_price(
            S, K, T, r, sigma,
            N=100,
            option_type=option_type,
            american=(option_type == "put")
        )

        iv = implied_volatility(market_price, S, K, T, r, option_type)
        iv_str = f"{iv:8.4f}" if not np.isnan(iv) else "    N/A"

        print(f"{K:8.2f} | {market_price:8.2f} | {bs:8.2f} | {bt:8.2f} | {iv_str}")


if __name__ == "__main__":
    run_pricer("AAPL", option_type="call", num_options=10)
