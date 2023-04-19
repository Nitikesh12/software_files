import pandas as pd
import numpy as np
from scipy.stats import skew,kurtosis,norm,skewtest,kurtosistest
from statsmodels.graphics.tsaplots import plot_pacf,plot_acf
from tvDatafeed import TvDatafeed, Interval
import time
import mysql.connector
import requests
import sys
import os
mydb1=mysql.connector.connect(host="85.187.128.49",user="python_rajeev",password="rajeev!@#123",database="python_trading")
mycursor1=mydb1.cursor()
mycursor1.execute("select script,exchange from atr")
result=mycursor1.fetchall()
tv = TvDatafeed()


a=list(map(lambda x:x[0],result))
# print(a)
b=list(map(lambda x:x[1],result))
# print(b)
i=0
while i<len(a):
	nf=str(a[i])
	bf=str(b[i])
	
	df = tv.get_hist(symbol=nf,exchange=bf,interval=Interval.in_daily,n_bars=1000)
	
	# print(df)
	df['atr'] = round(df.apply(lambda x: x['high'] - x['low'], axis=1),2)
	df['atrp']=round(df.apply(lambda x:x['atr']/x['close']*100,axis=1),2)
	df["rolling7"]=round(df['atrp'].rolling(7).mean(),2)
	df["rolling30"]=round(df['atrp'].rolling(30).mean(),2)
	df["7high"]=round(df['high'].rolling(7).max(),2)
	df["7low"]=round(df["low"].rolling(7).min(),2)
	df["30high"]=round(df['high'].rolling(30).max(),2)
	df["30low"]=round(df["low"].rolling(30).min(),2)
	df['7atr'] = round(df.apply(lambda x: x['7high'] - x['7low'], axis=1),2)
	df['7atrp']=round(df.apply(lambda x:x['7atr']/x['close']*100,axis=1),2)
	df['30atr'] = round(df.apply(lambda x: x['30high'] - x['30low'], axis=1),2)
	df['30atrp']=round(df.apply(lambda x:x['30atr']/x['close']*100,axis=1),2)

	df['7rolling7']=round(df["7atrp"].rolling(7).mean(),2)
	df["30rolling"]=round(df["7atrp"].rolling(30).mean(),2)
	df['30rolling7']=round(df["30atrp"].rolling(7).mean(),2)
	df['30rolling30']=round(df["30atrp"].rolling(30).mean(),2)






	

	new_df=df.drop(["open","volume","symbol","low","high"],axis=1)
	last_close = new_df['close'].iat[-1]
	last_atr=new_df["atr"].iat[-1]
	last_atrp=new_df["atrp"].iat[-1]
	last_atr7=new_df["rolling7"].iat[-1]
	last_atr30=new_df["rolling30"].iat[-1]
	last_7atr=new_df["7atr"].iat[-1]
	last_7atrp=new_df["7atrp"].iat[-1]
	last_7rolling=new_df["7rolling7"].iat[-1]
	last_30rolling=new_df["30rolling"].iat[-1]
	last_30atr=new_df["30atr"].iat[-1]
	last_30atrp=new_df["30atrp"].iat[-1]
	last_30rolling7=new_df["30rolling7"].iat[-1]
	last_30rolling30=new_df["30rolling30"].iat[-1]

	sql="UPDATE atr set close=%s,atr_value=%s,atr_percent=%s,atr_7=%s,atr_30=%s,7atr=%s,7atrp=%s,7rolling7=%s,7rolling30=%s,30atr=%s,30atrp=%s,30rolling7=%s,30rolling30=%s where script=%s and exchange=%s"
	values=(last_close,last_atr,last_atrp,last_atr7,last_atr30,last_7atr,last_7atrp,last_7rolling,last_30rolling,last_30atr,last_30atrp,last_30rolling7,last_30rolling30,nf,bf)
	mycursor1.execute(sql,values)
	mydb1.commit()
	# new_df.to_csv("atr.csv",mode='a')
	
	print(new_df)
	
	
	i+=1

mydb1.close()
