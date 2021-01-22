import fxcmpy
import socketio
import time
import pandas as pd
import datetime as dt
import json
import threading 
import os
import pandas as pd
import datetime as dt
import json
import os
import time
import subprocess

def log(data):
    print(str(data))
    with open("log.txt", "a") as myfile:
        myfile.write(str(data)+'\n')
        
        
        
def modification_date():
    t = os.path.getmtime('../rtd/EURUSD.json')
    return dt.datetime.fromtimestamp(t)

def save_data(data, dataframe):
    try:
        pair=data['Symbol']
        x={'Bid': data['Rates'][0],
            'Ask': data['Rates'][1],
            'High': data['Rates'][2],
            'Low': data['Rates'][3],
            'ltp': (data['Rates'][0]/2)+(data['Rates'][1]/2),
            'Spread': data['Rates'][1]-data['Rates'][0]}
        with open('../rtd/'+pair.replace('/','')+'.json', 'w') as fp:
            json.dump(x, fp)  
    except:
        pass
    
def check_data():
    import requests
    def modification_date():
        t = os.path.getmtime('../rtd/EURUSD.json')
        return dt.datetime.fromtimestamp(t)>dt.datetime.now()-dt.timedelta(seconds=600)
    msg=False
    if modification_date():
        mesg='Data disconnected '+str(dt.datetime.now())
        url="https://api.telegram.org"+str(mesg)
        requests.get(url)
        msg=True
        return True
    else:
        return False
    
running_time=30*24*60*60
data_start=dt.datetime.now()
TOKEN = 'qwertyuiopsdfghjkl;ertyu'
pairs=['EUR/USD', 'USD/JPY', 'GBP/USD', 'USD/CHF','AUD/USD']
print('init')
con = fxcmpy.fxcmpy(access_token=TOKEN, log_level='error', server='real', log_file='log.hdex')
t1=dt.datetime.now()-dt.timedelta(seconds=61)
refresh_time=60*60*10
otime=dt.datetime.now()
log('rtd started'+ str(running_time))
error = 0
for pair in pairs:
    con.subscribe_market_data(pair,(save_data,))
flag=0
time.sleep(1)
msg=False
telegram_time=dt.datetime.now()


def check_data():
    global telegram_time
    import requests
    def modification_date():
        t = os.path.getmtime('../rtd/EURUSD.json')
        return dt.datetime.fromtimestamp(t)+dt.timedelta(seconds=100)<dt.datetime.now()
    if modification_date() and telegram_time + dt.timedelta(seconds=60) < dt.datetime.now():
        mesg='Data disconnected '+str(dt.datetime.now())
        url="https://api.telegram"+str(mesg)
        #requests.get(url)
        try:
            con.close()
        except:
            pass
        exit()
        time.sleep(5)
        telegram_time=dt.datetime.now()
        return True
    else:
        return False
    
def eurusd_modification_date():
    t = os.path.getmtime('../rtd/EURUSD.json')
    return dt.datetime.fromtimestamp(t)+dt.timedelta(seconds=50)<dt.datetime.now()
while True:
    try:
        if eurusd_modification_date():
            log('refreshing data')
            for pair in pairs:
                con.unsubscribe_market_data(pair)
            for pair in pairs:
                con.subscribe_market_data(pair,(save_data,))
            time.sleep(10)
        if t1 + dt.timedelta(seconds=60) < dt.datetime.now(): 
            for pair in pairs:
                data = con.get_candles(pair, period='m30', number=300)
                data['Open']=(data.bidopen/2)+(data.askopen/2)
                data['High']=(data.bidhigh/2)+(data.askhigh/2)
                data['Low']=(data.bidlow/2)+(data.asklow/2)
                data['Close']=(data.bidclose/2)+(data.askclose/2)
                for col in list(data.keys()[:-4]):
                     del data[col]
                pair=pair.replace('/','')
                data.to_csv('../ohlc/'+pair+'.csv')
                t1=dt.datetime.now()

    except:
        flag=flag+1
    try:
        check_data()
    except:
        log('telegram error')