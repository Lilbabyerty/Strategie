import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ta



class Trix():
    def __init__(self,close:pd.Series,TrixSignal:int=21,TrixLength:int=9):
        self.close = close
        self.TrixSignal = TrixSignal
        self.TrixLength = TrixLength
        self.Trix_indicateur()
    def Trix_indicateur(self):
        self.TrixLine = ta.trend.ema_indicator(
            ta.trend.ema_indicator(
                ta.trend.ema_indicator(close=self.close, window=self.TrixLength)))
        self.Trix_pctchange = self.TrixLine.pct_change()*100
        self.TrixLineSignal = ta.trend.ema_indicator(close=self.Trix_pctchange, window=self.TrixSignal)
        self.TrixHistory =  self.Trix_pctchange - self.TrixLineSignal

        self.Stoch_rsi = ta.momentum.stochrsi(close=self.close, window=14, smooth1=3, smooth2=3)


    def Trix_Line(self) -> pd.Series:
        """
            Trix line
        :return: pd.Series
        """
        return pd.Series(self.TrixLine,name='TRIX LINE')
    def Trix_Signal_line(self) -> pd.Series:
        """
            Trix signal line
        :return: pd.Series
        """
        return pd.Series(self.TrixLineSignal,name='TRIX SIGNAL')

    def Trix_Pct_Line(self) -> pd.Series:
        """
            Trix line percentage change
        :return: pd.Series
        """
        return pd.Series(self.Trix_pctchange,name='TRIX PCTCHANGE')
    def Trix_History_line(self) -> pd.Series:
        """
            Trix line History
        :return: pd.Series
        """
        return pd.Series(self.TrixHistory,name='TRIX HISTORY')
    def Shoth_RSI(self) -> pd.Series:
        """
        Indicator Stoch RSI
        :return: pd.Series
        """
        return pd.Series(self.Stoch_rsi,name='STOCH RSI')
    def TrixStragie(self):

        buy_condition = lambda row: row["TRIX HISTORY"] > 0 and row["STOCH RSI"] < 0.8
        sell_condition = lambda row: row["TRIX HISTORY"] < 0 and row["STOCH RSI"] > 0.2

        return buy_condition,sell_condition



