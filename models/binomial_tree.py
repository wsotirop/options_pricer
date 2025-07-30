import numpy as np

def binomial_tree_price(S, K, T, r, sigma,N=100, option_type='call', american=True):
    dt = T / N
    u  = np.exp(sigma * np.sqrt(dt))
    d  = 1 / u
    p  = (np.exp(r*dt) - d) / (u - d)

    # Prices at maturity
    ST = np.array([S * u**j * d**(N-j) for j in range(N+1)])
    if option_type == 'call':
        values = np.maximum(ST - K, 0)
    else:
        values = np.maximum(K - ST, 0)

    # Backward induction
    for i in range(N, 0, -1):
        ST     = ST[:-1] / d
        values = np.exp(-r * dt) * (p * values[1:] + (1-p) * values[:-1])
        if american:
            if option_type == 'call':
                values = np.maximum(values, ST - K)
            else:
                values = np.maximum(values, K - ST)

    return values[0]
