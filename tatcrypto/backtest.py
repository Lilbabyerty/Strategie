import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ta
import datetime
import seaborn as sns


class Backtesting:
        def __init__(self,close:pd.Series,period:pd.Series,initial_wallet=1000, fee=0.00087):
            """This method """

            self.initial_wallet = initial_wallet
            self.wallet = initial_wallet
            self.coin = 0
            self.fee = fee
            self.trades_history = []
            self.days_history = []
            self.days_trade = None
            self.usdt = initial_wallet
            self.close = close
            self.period = period
        def execute_trades(self, df, buy_condition, sell_condition):
            previous_day = 0
            for index, row in df.iterrows():
                current_day = index.day
                if previous_day != current_day:
                    temp_wallet = self.wallet
                    if self.coin > 0:
                        temp_wallet = self.coin * row['close']
                    self.days_history.append({
                        "day": f"{index.year}-{index.month}-{index.day}",
                        "wallet": temp_wallet,
                        "price": row['close']
                    })

                previous_day = current_day

                if buy_condition(row) and self.usdt > 0:
                    self._buy(row, index)
                elif sell_condition(row) and self.coin > 0:
                    self._sell(row, index)

            return self.get_trade_data()

        def _buy(self, row, index):
            self.coin = self.usdt / row['close'] * (1 - self.fee)
            self.wallet = self.coin*row['close']
            self.usdt = 0
            buy_data = {
                'day': index,
                'position': 'buy',
                'wallet': self.wallet,
                'reason': 'market',
                'price': row['close'],
                'coin': self.coin,
                'fee': self.fee * self.coin,
                'usdt': self.usdt,
            }
            self.trades_history.append(buy_data)

        def _sell(self, row, index):
            self.usdt = self.coin * row['close'] * (1 - self.fee)
            self.coin = 0
            self.wallet = self.usdt
            sell_data = {
                "day": index,
                "position": "sell",
                "wallet": self.wallet,
                "reason": "market",
                "price": row['close'],
                "coin": self.coin,
                "fee": self.fee * self.wallet,
                "usdt": self.usdt,
            }
            self.trades_history.append(sell_data)

        def get_trade_data(self):
            self.days_trade = pd.DataFrame(self.days_history)
            df_trades = pd.DataFrame(self.trades_history).set_index("day")
            df_trades['results'] = df_trades['wallet'].diff()
            df_trades['results%'] = df_trades['wallet'].pct_change().round(4) * 100
            df_trades.loc[df_trades['position'] == 'buy', 'results'] = None
            df_trades.loc[df_trades['position'] == 'buy', 'results%'] = None
            df_trades['TradesIs'] = ''
            df_trades.loc[df_trades['results'] > 0, 'TradesIs'] = 'Good trade'
            df_trades.loc[df_trades['results'] <= 0, 'TradesIs'] = 'Bad trade'
            return df_trades



        def wallet_evolution(self) -> pd.DataFrame:
            return self.days_trade

        def analyses(self,days_trade:pd.DataFrame,df_trades:pd.DataFrame):
            wallet = df_trades['wallet'].iloc[-1]
            besTradde = df_trades['results%'].max()
            inihold = self.close.iloc[0]
            lasthold = self.close.iloc[-1]
            HoldPerformance = (lasthold - inihold) / inihold * 100
            iddext = df_trades.loc[df_trades['TradesIs'] == 'Good trade', 'results%'].idxmax()
            badTrade = df_trades['results%'].min()
            iddext2 =df_trades.loc[df_trades['TradesIs'] == 'Bad trade', 'results%'].idxmin()
            TradePerformance = (wallet - self.initial_wallet) / self.initial_wallet * 100
            totalGoodTrade = df_trades.loc[df_trades['TradesIs'] == 'Good trade', 'TradesIs'].count()
            totalBadTrade = df_trades.loc[df_trades['TradesIs'] == 'Bad trade', 'TradesIs'].count()
            Trade_vs_Hold = (TradePerformance - HoldPerformance) / TradePerformance * 100
            win_rate = totalGoodTrade / (totalBadTrade + totalGoodTrade) * 100
            final_wallet = df_trades['wallet'].iloc[-1]
            total_fee = df_trades['fee'].sum()
            avg_profit = df_trades["results%"].mean()
            print(f'Period: [{days_trade.iloc[0]["day"]}] -> [{days_trade.iloc[-1]["day"]}]')
            print(f"Initial wallet: {round(self.initial_wallet, 2)} $")

            print("\n--- General Information ---")
            print(f'Final wallet: {round(final_wallet, 2)} $')
            print(f'Total Good Trade: {totalGoodTrade}')
            print(f'Total Bad Trade: {totalBadTrade}')
            print(f"Total Trade: {totalGoodTrade + totalBadTrade}")
            print(f'Global winning rate: {round(win_rate, 2)} %')
            print(f'Average Profit : {avg_profit} %')
            print(f"Hold Performance: {round(HoldPerformance, 2)}%")
            print(f'Trade Performance: {round(TradePerformance, 2)}%')
            print(f'Trade vs Hold: {round(Trade_vs_Hold, 2)}%')
            print(f'Total free: {round(total_fee, 2)} $')
            print(f'\nBest Trade: +{besTradde}% the {iddext}')
            print(f'Bad Trade: {badTrade}% the {iddext2}')

        def plot_bar_by_month(self,df_days:pd.DataFrame):
            sns.set(rc={'figure.figsize': (11.7, 8.27)})
            custom_palette = {}

            last_month = int(df_days.iloc[-1]['day'].month)
            last_year = int(df_days.iloc[-1]['day'].year)

            current_month = int(df_days.iloc[0]['day'].month)
            current_year = int(df_days.iloc[0]['day'].year)
            current_year_array = []
            while current_year != last_year or current_month - 1 != last_month:
                #date_string = str(datetime.datetime(year=current_year,month=current_month,day=22))
                date_string = str(current_year) + "-" + str(current_month)
                monthly_perf = (df_days.loc[date_string]['wallet'].iloc[-1] - df_days.loc[date_string]['wallet'].iloc[0]) / df_days.loc[date_string]['wallet'].iloc[0]
                monthly_row = {
                    'date': str(datetime.date(1900, current_month, 1).strftime('%B')),
                    'result': round(monthly_perf * 100)
                }
                if monthly_row["result"] >= 0:
                    custom_palette[str(datetime.date(1900, current_month, 1).strftime('%B'))] = 'g'
                else:
                    custom_palette[str(datetime.date(1900, current_month, 1).strftime('%B'))] = 'r'
                current_year_array.append(monthly_row)
                # print(monthly_perf*100)
                if ((current_month == 12) or (current_month == last_month and current_year == last_year)):
                    current_df = pd.DataFrame(current_year_array)
                    # print(current_df)
                    g = sns.barplot(data=current_df, x='date', y='result', palette=custom_palette)
                    for index, row in current_df.iterrows():
                        if row.result >= 0:
                            g.text(row.name, row.result, '+' + str(round(row.result)) + '%', color='black', ha="center",
                                   va="bottom")
                        else:
                            g.text(row.name, row.result, '-' + str(round(row.result)) + '%', color='black', ha="center",
                                   va="top")
                    g.set_title(str(current_year) + ' performance in %')
                    g.set(xlabel=current_year, ylabel='performance %')

                    year_result = (df_days.loc[str(current_year)]['wallet'].iloc[-1] -
                                   df_days.loc[str(current_year)]['wallet'].iloc[0]) / \
                                  df_days.loc[str(current_year)]['wallet'].iloc[0]
                    print("----- " + str(current_year) + " Cumulative Performances: " + str(
                        round(year_result * 100, 2)) + "% -----")
                    plt.show()

                    current_year_array = []

                current_month += 1
                if current_month > 12:
                    current_month = 1
                    current_year += 1

        def plot_wallet_vs_asset(self,df_days:pd.DataFrame):
            fig, axes = plt.subplots(figsize=(15, 12), nrows=2, ncols=1)
            df_days['wallet'].plot(ax=axes[0])
            df_days['price'].plot(ax=axes[1], color='orange')



