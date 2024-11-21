import pandas as pd
import ta
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import backtest
import strategie



# Créer un tableau grâce aux données
df = pd.read_csv('C:/Users/ETOUNDI/Downloads/ETHUSD2H.csv')
df = df.iloc[::-1].reset_index(drop=True)
# Supprime les colonnes inutiles
# df.columns=['timestamp','close','open','high','low','volume','change %']
df.drop(columns=df.columns.difference(['timestamp', 'open', 'high', 'low', 'close']), inplace=True)

# Convertit les dates dans un format lisible
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.set_index("timestamp", drop=True)
# Convertit les colonnes en numéric
for col in df.columns:
    df[col] = pd.to_numeric(df[col])


df["ema30"] = ta.trend.ema_indicator(close=df["close"], window=30)  # Moyenne mobile exponenciel sur 30 période
df["ema50"] = ta.trend.ema_indicator(close=df["close"], window=50)  # Moyenne mobile exponenciel sur 50 période
trix = strategie.Trix(df["close"])

df['TRiX LINE'] = trix.Trix_Line()
df['TRiX SIGNAL'] = trix.Trix_Signal_line()
df['TRIX PCTCHANGE'] = trix.Trix_Pct_Line()
df['TRIX HISTORY'] = trix.Trix_History_line()
df["STOCH RSI"] = trix.Shoth_RSI()

buy_condition,sell_condition =  trix.TrixStragie()


bactesting = backtest.Backtesting(close=df["close"],period=df.index)
list_trade = bactesting.execute_trades(df,buy_condition=buy_condition, sell_condition=sell_condition)
days_trade = bactesting.wallet_evolution()
print(days_trade)
print(list_trade)
l=list_trade["results"]
bactesting.analyses(days_trade, list_trade)
bactesting.plot_wallet_vs_asset(days_trade)
plt.figure(figsize=(12, 6))
plt.plot(df["close"], color='blue')
plt.plot(df["ema50"], color='red')
plt.plot(df['TRiX SIGNAL'], color='green')
plt.grid(True)
plt.show()






