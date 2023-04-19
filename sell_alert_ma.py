import datetime as dt
import time
from datetime import datetime
from tvDatafeed import TvDatafeed, Interval
import numpy as np
import pandas as pd
import ta
import mysql.connector
import csv
import requests
import schedule
import threading
import sys

mydb1=mysql.connector.connect(host="85.187.128.49",user="python_rajeev",password="rajeev!@#123",database="python_trading")
mycursor1=mydb1.cursor()
tv = TvDatafeed('md@yogya.co.in','R@g123456')
mycursor1.execute("select script,exchange from atr")
result=mycursor1.fetchall()
a=list(map(lambda x:x[0],result))
b=list(map(lambda x:x[1],result))
def nit():
	global tv,a,b,mycursor1
	
	i=0
	while i<len(a):
		nf=str(a[i])
		bf=str(b[i])
		
		df = tv.get_hist(symbol=nf,exchange=bf,interval=Interval.in_15_minute,n_bars=500)
		
		df["ma_44_close"] = df['close'].rolling(window=44).mean()
		df["ma_44_high"]=df["high"].rolling(window=44).mean()
		df["ma_44_low"]=df["low"].rolling(window=44).mean()
		selected_rows=df.loc[(df['ma_44_low']<df["high"]) & (df["ma_44_low"]>df["close"])].index
		low_values = df.loc[selected_rows, 'low']
		
		last_index=low_values.index[-1]
		last_low_date = low_values.index[-1].date()
		low_values=low_values[-1]
		time_string = "15:15:00"
		time_obj = datetime.strptime(time_string, "%H:%M:%S").time()
		today = dt.date.today()
		if today==last_low_date:
			before_low = df.loc[(df.index < last_index), ['high', 'ma_44_low']]
			m = before_low.tail(7)
			if all(m["high"] < m["ma_44_low"]) and last_low_date !=time_obj:
				print(last_index,nf,low_values)
				apiToken = '5985340781:AAHBYJJSwv7Ku62JOR5z6NzrB9-z7MMGBxI'
				chatID = '5410035740'
				apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
				message = f"time {last_index} sell {nf}"
				response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
		i+=1
		print("not found")
nit()
def thread_nit():
    while True:
        nit()
        time.sleep(60*15)
thread1 = threading.Thread(target=thread_nit)
thread1.start()