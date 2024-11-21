import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ta




df = pd.read_csv('C:/Users/ETOUNDI/Downloads/AZERO.csv')

df["Date"] = pd.to_datetime(df)
df = df.set_index(df["Date"])
df["ta_essaie"] = ta.trend.ema_indicator(close=df["Price"],window=10)
df["essai"] = ta.trend.sma_indicator(close=df["Price"],window=10)

print(df)

fig, ax = plt.subplots()
ax.plot(df["ta_essaie"])
ax.plot(df["Price"])
ax.plot(df["essai"])
plt.show()
