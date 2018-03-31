#!/bin/python3

import numpy as np

# -------------------------------------------------------------------------------
# Relative Strength Index
# https://en.wikipedia.org/wiki/Relative_strength_index
# -------------------------------------------------------------------------------
def RSI(values, n):
    rsi = np.zeros(len(values), dtype=np.float)
    deltas = np.diff(values)
    seed = deltas[:n + 1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    if down == 0:
        down = 0.000000001
    rs = up / down
    rsi[:n] = 100. - 100. / (1. + rs)
    for i in range(n, len(values)):
        delta = deltas[i - 1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n
        if down == 0:
            down = 0.000000001
        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)
    return rsi
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# Updown Streak
# https://www.tradingview.com/wiki/Connors_RSI_(CRSI)
# -------------------------------------------------------------------------------
def updown_streak(values):
    s = np.zeros(len(values), dtype=np.int)
    for i in range(1, len(values)):
        if values[i] > values[i - 1]:
            s[i] = max(s[i - 1], 0) + 1
        elif values[i] < values[i - 1]:
            s[i] = min(s[i - 1], 0) - 1
        else:
            s[i] = 0
    return s
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# RSI Streak
# https://www.tradingview.com/wiki/Connors_RSI_(CRSI)
# -------------------------------------------------------------------------------
def RSI_streak(values, n):
    return RSI(updown_streak(values), n)
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# Percentile - Percent Rank of a Trading Indicator
# https://www.quantshare.com/item-549-percentile-percent-rank-of-a-trading-indicator
# -------------------------------------------------------------------------------
def percent_rank(values, n):
    rank = np.full(len(values), 50.0)
    ix = 1
    while len(values) > ix + n:
        last = 100.0 * values[-ix] / values[-ix - 1] - 100
        prev = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(values[-n - ix:-ix], values[-n - ix - 1:-ix])])
        rank[-ix] = 100.0 * np.sum([prev < last]) / n
        ix += 1
    return rank
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# Connors RSI
# https://www.tradingview.com/wiki/Connors_RSI_(CRSI)
# -------------------------------------------------------------------------------
def Connors_RSI(prices, n_rsi=3, n_streak=2, n_rank=100):
    rsi = RSI(prices, n_rsi)
    rsi_streak = RSI_streak(prices, n_streak)
    rank = percent_rank(prices, n_rank)
    return (rsi + rsi_streak + rank) / 3
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# Connors RSI for a guess price
# -------------------------------------------------------------------------------
def guess_Connors_RSI_by_price(prices, guess_price, n_rsi=3, n_streak=2, n_rank=100):
    prices2 = np.append(prices, guess_price)
    rsi = RSI(prices2, n_rsi)
    rsi_streak = RSI_streak(prices2, n_streak)
    rank = percent_rank(prices2, n_rank)
    crsi = (rsi + rsi_streak + rank) / 3
    return crsi[-1]


# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# Guess a price by Connors RSI to set SELL LMT
# -------------------------------------------------------------------------------
def guess_price_by_Connors_RSI(prices, crsi_limit, n_rsi=3, n_streak=2, n_rank=100):
    guess_price = prices[-1]
    while guess_Connors_RSI_by_price(prices, guess_price, n_rsi, n_streak, n_rank) < crsi_limit:
        guess_price *= 2
    delta = guess_price
    while delta > 0.05:
        delta /= 2
        crsi = guess_Connors_RSI_by_price(prices, guess_price, n_rsi, n_streak, n_rank)
        if crsi < crsi_limit:
            guess_price += delta
        else:
            guess_price -= delta
    return guess_price
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# Wilder's Moving Average
# -------------------------------------------------------------------------------
def Wilders_MA(values, n):
    ma = np.zeros(len(values), dtype=np.float)
    ma[:n] = np.sum(values[:n]) / n
    for i in range(n, len(values)):
        ma[i] = (values[i] + ma[i - 1] * (n - 1)) / n
    return ma
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# Average Directional Index
# https://en.wikipedia.org/wiki/Average_directional_movement_index
# -------------------------------------------------------------------------------
def ADX(hi_vals, lo_vals, cl_vals, n):
    tr = np.zeros(len(hi_vals), dtype=np.float)
    plus_dm = np.zeros(len(hi_vals), dtype=np.float)
    minus_dm = np.zeros(len(hi_vals), dtype=np.float)
    for i in range(1, len(tr)):
        tr[i] = max(abs(hi_vals[i] - lo_vals[i]),
                    abs(hi_vals[i] - cl_vals[i - 1]),
                    abs(lo_vals[i] - cl_vals[i - 1]))
        hi_diff = hi_vals[i] - hi_vals[i - 1]
        lo_diff = lo_vals[i - 1] - lo_vals[i]
        plus_dm[i] = hi_diff if hi_diff > lo_diff and hi_diff > 0 else 0
        minus_dm[i] = lo_diff if lo_diff > hi_diff and lo_diff > 0 else 0
    atr = Wilders_MA(tr, n)
    plus_di = 100. * Wilders_MA(plus_dm, n) / atr
    minus_di = 100. * Wilders_MA(minus_dm, n) / atr
    dx = np.zeros(len(plus_di), dtype=np.float)
    for i in range(len(dx)):
        pm_di = plus_di[i] + minus_di[i]
        dx[i] = 100. * abs(plus_di[i] - minus_di[i]) / pm_di if pm_di > 0 else 0
    adx = Wilders_MA(dx, n)
    return adx
# -------------------------------------------------------------------------------
