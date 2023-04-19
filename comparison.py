import json
from py5paisa import FivePaisaClient
import pandas as pd
import mysql.connector
import time


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
mycursor1.execute("select script,high,low,buy_rsi2,sell_rsi2 from rsi where buy_rsi2=1 or sell_rsi2=1 ")
result=mycursor1.fetchall()
mydb1.close()
while True:
    i=0
    a=list(map(lambda x:x[0],result))
    b=list(map(lambda x:x[1],result))
    c=list(map(lambda x:x[2],result))
    d=list(map(lambda x:x[3],result))
    e=list(map(lambda x:x[4],result))
    while i<len(a):
        nf=a[i]
        db_high=b[i]
        db_low=c[i]
        # print(nf,db_high,db_low)
        # print(d[i])


# # print(a)

        req_list=[{"Exch":"N","ExchType":"C","Symbol":nf}]
        

        # print(client.fetch_market_feed(req_list))
        niti=client.fetch_market_feed(req_list)
        # print(niti)
        data=niti["Data"]
        # # high=data[0]['high']
        # print(high)
        # print(data)
        ls=data[0]['LastRate']

        if d[i]==1 and db_low>ls:

            print(data)
            print("buy")
        if e[i]==1 and db_high<ls:
            print("sell")
            print(data)
        i+=1
        time.sleep(0)
    time.sleep(0)