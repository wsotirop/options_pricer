from models.black_scholes import black_scholes_price
from models.binomial_tree import binomial_tree_price
from utils.fetch_data import get_stock_option_data
from utils.fetch_data import get_historical_volatility
from utils.implied_vol import implied_volatility
import numpy as np

def run_pricer(ticker="AAPL", option_type="call", num_options=10):
    S, calls, puts, expiry = get_stock_option_data(ticker)
    r = 0.05
    T = 5 / 365
    sigma = get_historical_volatility(ticker)


    chain = calls if option_type == "call" else puts
    print(f"\n{ticker} — {option_type.upper()} OPTIONS — Expiry: {expiry}")
    print(f"{'Strike':>8} | {'Market':>8} | {'B-S':>8} | {'BinTree':>8} | {'ImplVol':>8}")
    print("-" * 55)


    for i, row in chain.iterrows():
        if i >= num_options:
            break
        K = row["strike"]
        market_price = row["lastPrice"]

        bs = black_scholes_price(S, K, T, r, sigma, option_type)
        bt = binomial_tree_price(S, K, T, r, sigma, N=100, option_type=option_type, american=(option_type == "put"))

        iv = implied_volatility(market_price, S, K, T, r, option_type)
        iv_str = f"{iv:8.4f}" if not np.isnan(iv) else "    N/A"
        print(f"{K:8.2f} | {market_price:8.2f} | {bs:8.2f} | {bt:8.2f} | {iv_str}")

if __name__ == "__main__":
    run_pricer("AAPL", option_type="call", num_options=10)
