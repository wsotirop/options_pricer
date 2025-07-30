from scipy.optimize import brentq
from models.black_scholes import black_scholes_price

def implied_volatility(market_price, S, K, T, r, option_type='call', tol=1e-6, max_iter=100):
    """
    Solves for implied volatility using Brent's method.

    Parameters:
        market_price (float): Observed option market price
        S (float): Spot price
        K (float): Strike price
        T (float): Time to maturity (in years)
        r (float): Risk-free rate
        option_type (str): 'call' or 'put'
        tol (float): Solver tolerance
        max_iter (int): Max iterations

    Returns:
        float: Implied volatility (annualized)
    """
    def objective(sigma):
        return black_scholes_price(S, K, T, r, sigma, option_type) - market_price

    try:
        # Use Brent’s method in a reasonable sigma range
        return brentq(objective, 1e-5, 5.0, xtol=tol, maxiter=max_iter)
    except ValueError:
        return float('nan')  # No solution found
