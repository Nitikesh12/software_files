import pandas as pd
import numpy as np
from scipy.stats import skew,kurtosis,norm,skewtest,kurtosistest
from statsmodels.graphics.tsaplots import plot_pacf,plot_acf
from tvDatafeed import TvDatafeed, Interval
import time
import mysql.connector
import requests
import sys
import subprocess
# df=pd.read_csv("Desktop\\nifty.csv")
# df1=df.set_index('datetime')


a=['5410035740','1677109047']
i=0
while i<2:
    b=a[i]
    apiToken = '5985340781:AAHBYJJSwv7Ku62JOR5z6NzrB9-z7MMGBxI'
    chatID = b
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    message = "RSI Update Started..."

    response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
    
    i+=1

mydb1=mysql.connector.connect(host="85.187.128.49",user="python_rajeev",password="rajeev!@#123",database="python_trading")
mycursor1=mydb1.cursor()
mycursor1.execute("select script,exchange from rsi")
result=mycursor1.fetchall()
mydb1.close()
tv = TvDatafeed()

while True:
    
    
    i=0
    a=list(map(lambda x:x[0],result))
    b=list(map(lambda x:x[1],result))
    c=len(list(map(lambda x:x[0],result)))
    count=0
    while i<c:
        nf=str(a[i])
        bf=str(b[i])
        

    
    
    



        
        df = tv.get_hist(symbol=nf,exchange=bf,interval=Interval.in_3_minute,n_bars=1000)
    # print(nifty_index_data)


        def rsi(df, periods = 14, ema = True):
        
    #     """
    #     Returns a pd.Series with the relative strength index.
    #     """
    # #     date=df["datetime"]
        
            close_delta = df['close'].diff()
        
        
            global nf,bf
        # Make two series: one for lower closes and one for higher closes
            up = close_delta.clip(lower=0)
            down = -1 * close_delta.clip(upper=0)
            
            if ema == True:
                # Use exponential moving average
                ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
                ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
            else:
                # Use simple moving average
                ma_up = up.rolling(window = periods, adjust=False).mean()
                ma_down = down.rolling(window = periods, adjust=False).mean()
                
            rsi = ma_up / ma_down
        #     rsi = 100 - (100/(1 + rsi))
            df["rsi"]=round(100 - (100/(1 + rsi)),2)
            df["sm14"]=round(df['rsi'].rolling(14).mean(),2)
            new_df=df.drop(["symbol","open","volume"],axis=1)
            # df2=new_df.to_csv("tvdata2.csv",mode='a')
            #print("success")

            high=float(new_df["high"].iat[-1])
            low=float(new_df['low'].iat[-1])
            date=new_df.index[-1]
            # print(date)
            # return new_df
            # print(new_df)
            # print(high,low)
            last_close = float(new_df['close'].iat[-1])
            last_rsi=float(new_df['rsi'].iat[-1])
           
            last_rsi_avg=float(new_df["sm14"].iat[-1])
            print(f"{count} {nf} {last_close} {last_rsi} {last_rsi_avg}   SUCCESS")
            # print(last_close,last_rsi,last_rsi_avg)
            
                


            
            
            mydb=mysql.connector.connect(host="85.187.128.49",user="python_rajeev",password="rajeev!@#123",database="python_trading")
            mycursor=mydb.cursor()
            k=last_rsi<30
            l=last_rsi>70
            if last_rsi<30 or last_rsi>70:
                
                
                
                
                if last_rsi<30:
                    # print("True")
                    a="1"
                    buy_rsi=a
                    sql="UPDATE rsi set close=%s,rsi=%s,rsi_avg=%s,buy_rsi=%s where script=%s and exchange=%s"
                    values=(last_close,last_rsi,last_rsi_avg,buy_rsi,nf,bf)
                    mycursor.execute(sql,values)
                    mydb.commit()
                else:
                    a="1"
                    buy_rsi=a
                    sql="UPDATE rsi set close=%s,rsi=%s,rsi_avg=%s,sell_rsi=%s where script=%s and exchange=%s"
                    values=(last_close,last_rsi,last_rsi_avg,buy_rsi,nf,bf)
                    mycursor.execute(sql,values)
                    mydb.commit()


                # values=(last_close,last_rsi,last_rsi_avg,buy_rsi,nf,bf)
                # mycursor.execute(sql,values)
                # mydb.commit()
            else:
                sql="UPDATE rsi set close=%s,rsi=%s,rsi_avg=%s where script=%s and exchange=%s"
                values=(last_close,last_rsi,last_rsi_avg,nf,bf)
                mycursor.execute(sql,values)
                mydb.commit()
                mycursor.execute("select rsi,rsi_avg ,buy_rsi,sell_rsi,buy_rsi2,sell_rsi2,high,low,datetime from rsi")
                result1=mycursor.fetchall()
                e=list(map(lambda x:x[0],result1))
                f=list(map(lambda x:x[1],result1))
                g=list(map(lambda x:x[2],result1))
                h=list(map(lambda x:x[3],result1))

                if e[i]>f[i] and g[i]==1 or f[i]>e[i] and h[i]==1 :
                

                    def nit(message):
                        
                        apiToken = '5985340781:AAHBYJJSwv7Ku62JOR5z6NzrB9-z7MMGBxI'
                        chatID = '436179993'
                        apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

                        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
                        return response
                    
                    if e[i]>f[i] and g[i]==1:
                        nit(f"BUY ALERT : {nf}")
                        print("####sent")
                        l="0"
                        t="1"
                        m=nf
                        sql="UPDATE rsi set buy_rsi=%s,buy_rsi2=%s,sell_rsi2=%s,high=%s,low=%s,datetime=%s where script=%s"
                        values=(l,t,l,high,low,date,m)
                        mycursor.execute(sql,values)
                        mydb.commit()

                    else:
                        nit(f"SELL ALERT : {nf}")
                        print("###sent")
                        l="0"
                        t="1"
                        m=nf
                        sql="UPDATE rsi set sell_rsi=%s,sell_rsi2=%s,buy_rsi2=%s,high=%s,low=%s,datetime=%s where script=%s"
                        values=(l,t,l,high,low,date,m)
                        mycursor.execute(sql,values)
                        
                        mydb.commit()
                        
                    
            # else: 
            #     print("no")

                mydb.close()
        rsi(df)
        time.sleep(0)
        count+=1
        i+=1
            
        


    
    time.sleep(180)
    mydb1.close()