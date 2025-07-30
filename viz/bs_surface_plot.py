import numpy as np
import matplotlib.pyplot as plt
from models.black_scholes import black_scholes_price

def plot_bs_surface(S=100, r=0.05, sigma=0.25, option_type="call"):
    """
    Plots Black-Scholes pricing surface for a range of strike prices and times to maturity.
    """
    strikes = np.linspace(50, 150, 50)
    maturities = np.linspace(0.01, 1.0, 50)  # in years

    K_grid, T_grid = np.meshgrid(strikes, maturities)
    prices = np.vectorize(black_scholes_price)(S, K_grid, T_grid, r, sigma, option_type)

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(K_grid, T_grid, prices, cmap='viridis')

    ax.set_title(f"Black-Scholes Surface ({option_type.title()})")
    ax.set_xlabel("Strike Price (K)")
    ax.set_ylabel("Time to Maturity (T)")
    ax.set_zlabel("Option Price")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_bs_surface(S=209.35, r=0.05, sigma=0.275, option_type="call")
