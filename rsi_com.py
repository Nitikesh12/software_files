import json
from py5paisa import FivePaisaClient
import pandas as pd
import mysql.connector
import time
import requests


cred={
    "APP_NAME":"5P51573268",
    "APP_SOURCE":"11367",
    "USER_ID":"l6pbDP3Qy5F",
    "PASSWORD":"GnyslRyxffU",
    "USER_KEY":"DFtEQyEQpO5zjOWhXMWaFxDcaDRmP64q",
    "ENCRYPTION_KEY":"ktUMGmNFYgLh0byy10UfJXJ2C5Okccz3"
}
client = FivePaisaClient(email="mail@rajeevgupta.in", passwd="R@g12345", dob="19791011",cred=cred)
client.login()

#req_list=[
#            { "Exch":"N","ExchType":"D","ScripCode":53395},
#            ]
mydb1=mysql.connector.connect(host="85.187.128.49",user="python_rajeev",password="rajeev!@#123",database="python_trading")
mycursor1=mydb1.cursor()



while True:
    mycursor1.execute("select rsi, buy_rsi2, sell_rsi2 from rsi where script='NIFTY'")
    result1=mycursor1.fetchall()
    for demo in result1:
        pass
    
    if demo[1] == 1 and demo[0] < 50:
        print("Buy Condition")
        mycursor1.execute("select script,high,low,buy_rsi2 from rsi where buy_rsi2=1")
        result=mycursor1.fetchall()
        i=0
        count=0
        script=list(map(lambda x:x[0],result))
        high=list(map(lambda x:x[1],result))
        low=list(map(lambda x:x[2],result))
        buy_rsi2=list(map(lambda x:x[3],result))
        
        l=[]
        while i<len(script):
            nf=script[i]
            
            keys = ["Exch","ExchType","Symbol"]
            values = ["N", "C",nf]
            a=dict(zip(keys, values))
            l.append(a)
            
            i+=1
        
        req_list=l
        niti=client.fetch_market_feed(req_list)
        # print(niti)
        # print(niti)
        data=niti["Data"]
        # print(data)
        num=0
        while num<len(data):
            ls=data[num]['LastRate']
            sym=data[num]['Symbol']
            db_high=high[num]
            db_low=low[num]

            
            nf1=script[num]
            

            # print(ls,db_high)
            if buy_rsi2[num]==1 and db_high<ls:
                sql="UPDATE rsi set buy_rsi2=%s,buy_rsi3=%s where script=%s"
                values=("0","1",nf1)
                mycursor1.execute(sql,values)
                mydb1.commit()

                apiToken = '5985340781:AAHBYJJSwv7Ku62JOR5z6NzrB9-z7MMGBxI'
                chatID = '436179993'
                apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
                message = "Buy Condition"
                response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
                
               
                
            num+=1
    if demo[2] == 1 and demo[0] > 50:
        print("sell")
        mycursor1.execute("select script,high,low,sell_rsi2 from rsi where sell_rsi2=1")    
        result=mycursor1.fetchall()
        i=0
        count=0
        script=list(map(lambda x:x[0],result))
        high=list(map(lambda x:x[1],result))
        low=list(map(lambda x:x[2],result))
        sell_rsi2=list(map(lambda x:x[3],result))
        l=[]
        while i<len(script):
            nf=script[i]
            
            keys = ["Exch","ExchType","Symbol"]
            values = ["N", "C",nf]
            a=dict(zip(keys, values))
            l.append(a)
            
            i+=1
        
        req_list=l
        niti=client.fetch_market_feed(req_list)
        # print(niti)
        # print(niti)
        data=niti["Data"]
        # print(data)
        num=0
        while num<len(data):
            ls=data[num]['LastRate']
            sym=data[num]['Symbol']
            db_high=high[num]
            db_low=low[num]
            nf1=script[num]
            if sell_rsi2[num]==1 and db_low>ls:
                # print("buy",sym,ls)
                sql="UPDATE rsi set sell_rsi2=%s,sell_rsi3=%s where script=%s "
                values=("0","1",nf1)
                mycursor1.execute(sql,values)
                mydb1.commit()
            apiToken = '5985340781:AAHBYJJSwv7Ku62JOR5z6NzrB9-z7MMGBxI'
            chatID = '436179993'
            apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
            message = "sell Condition"
            response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
            
            num+=1
    time.sleep(5)
