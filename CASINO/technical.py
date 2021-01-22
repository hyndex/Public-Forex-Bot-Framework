import talib
import pandas as pd
import datetime as dt
import time
import copy

   
class watch:
    def ichimoku(self,d):
        d=copy.deepcopy(d)
        high_prices = d['High']
        close_prices = d['Close']
        low_prices = d['Low']
        dates = d.index
        nine_period_high = d['High'].rolling(window= 9 ).max()
        nine_period_low = d['Low'].rolling(window= 9 ).min()
        d['tenkan_sen'] = (nine_period_high + nine_period_low) /2

        # Kijun-sen (Base Line): (26-period high + 26-period low)/2))
        period26_high = d['High'].rolling(window= 26 ).max()
        period26_low = d['Low'].rolling(window= 26 ).min()
        d['kijun_sen'] = (period26_high + period26_low) / 2

        # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2))
        d['senkou_span_a'] = ((d['tenkan_sen'] + d['kijun_sen']) / 2).shift(26)

        # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2))
        period52_high = d['High'].rolling(window= 52 ).max()
        period52_low = d['Low'].rolling(window= 52 ).min()
        d['senkou_span_b'] = ((period52_high + period52_low) / 2).shift(26)

        # The most current closing price plotted 22 time periods behind (optional)
        d['chikou_span'] = close_prices.shift(-22)
        del d['Open'], d['High'], d['Low'], d['Close'], d['Adj Close']
        return d['kijun_sen']



    def downCross(self,ltp,data,offset=0):
        sar=talib.SAR(data['High'],data['Low'],acceleration=0.02,maximum=0.2)
        if float(sar[-1:])<float(data.Close[-1:]):
            if float(sar[-1:])-float(offset)>ltp:
                return True
        return False
    
    def downSARClose(self,ltp,data,offset=0):
        sar=talib.SAR(data['High'],data['Low'],acceleration=0.02,maximum=0.2)
        if float(sar[-1:])<float(data.Close[-2:]):
            if float(sar[-1:])-float(offset)>float(data.Close[-1:]):
                return True
        return False
    
    def upSARClose(self,ltp,data,offset=0):
        sar=talib.SAR(data['High'],data['Low'],acceleration=0.02,maximum=0.2)
        if float(sar[-1:])>float(data.Close[-2:]):
            if float(sar[-1:])+float(offset)<float(data.Close[-1:]):
                return True
        return False
    
    def downBaseCross(self,ltp,data):
        sar=self.ichimoku(data)
        if float(sar[-1:])<float(data.Close[-1:]):
            if float(sar[-1:])>ltp:
                return True
        return False

    def upCross(self,ltp,data,offset=0):
        sar=talib.SAR(data['High'],data['Low'],acceleration=0.02,maximum=0.2)
        if float(sar[-1:])>float(data.Close[-1:]):
            if float(sar[-1:])+float(offset)<ltp:
                return True
        return False
    
    def upClose(self,ltp,data):
        sar=talib.SAR(data['High'],data['Low'],acceleration=0.02,maximum=0.2)
        if float(sar[-2:])>float(data.Close[-2:]):
            if float(sar[-1:])<float(data.Close[-1:]):
                return True
        return False
    
    def downClose(self,ltp,data):
        sar=talib.SAR(data['High'],data['Low'],acceleration=0.02,maximum=0.2)
        if float(sar[-2:])<float(data.Close[-2:]):
            if float(sar[-1:])>float(data.Close[-1:]):
                return True
        return False
    
    def upBaseCross(self,ltp,data):
        data['Adj Close']=data['Close']
        sar=self.ichimoku(data)
        if float(sar[-1:])>float(data.Close[-1:]):
            if float(sar[-1:])<ltp:
                return True
        return False


    def upTrend(self,ltp,data):
        data['Adj Close']=data['Close']
        base=self.ichimoku(data)
        if float(base[-1:])<float(ltp):
            return True
        return False

    def downTrend(self,ltp,data):
        data['Adj Close']=data['Close']
        base=self.ichimoku(data)
        if float(base[-1:])>float(ltp):
            return True
        return False
    
    def downEMA(self,ltp,data):
        data['Adj Close']=data['Close']
        ema=talib.EMA(data['Close'],timeperiod=100)
        if float(ema[-1:])>float(ltp):
            return True
        return False
    
    def downSAR(self,ltp,data,offset=0):
        data['Adj Close']=data['Close']
        ema=talib.SAR(data['High'],data['Low'],acceleration=0.02,maximum=0.2)
        #if float(ema[-1:])>float(data.Close[-1:]):
        if float(ema[-1:])-offset>float(ltp):
            return True
        return False
    
    def upEMA(self,ltp,data):
        data['Adj Close']=data['Close']
        ema=talib.EMA(data['Close'],timeperiod=100)
        if float(ema[-1:])<float(ltp):
            return True
        return False
    
    def upSAR(self,ltp,data,offset=0):
        data['Adj Close']=data['Close']
        ema=talib.SAR(data['High'],data['Low'],acceleration=0.02,maximum=0.2)
        #if float(ema[-1:])<float(data.Close[-1:]):
        if float(ema[-1:])+offset<float(ltp):
            return True
        return False