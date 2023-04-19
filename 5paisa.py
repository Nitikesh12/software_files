import json
from py5paisa import FivePaisaClient
import pandas as pd
import mysql.connector
import time
import sys
import os
import datetime
from datetime import datetime
import time
import threading
import datetime
import schedule
import sys

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


req_list_=[{"Exch":"N","ExchType":"C","Symbol":"NIFTY"},
        {"Exch":"N","ExchType":"C","Symbol":"BANKNIFTY"}]

def test():
    print("start")

    def nit():
        print(sys.argv)
        print(sys.executable)
        print("restart now")
        os.execv(sys.executable,["python"]+sys.argv)
    try:

        


        


        data=client.fetch_market_feed(req_list_)

        result = (data['Data'])
        df = json.dumps(result)
        df = pd.read_json(df)
        print(result)

        Symbol=result[0]["Symbol"]

        Chg=result[0]["Chg"]
        Lprice=result[0]["LastRate"]
        Symbal2=result[1]["Symbol"]
        print(Symbal2)
        Chg2=result[1]["Chg"]
        Lprice2=result[1]["LastRate"]


        mydb=mysql.connector.connect(host="85.187.128.49",user="python_rajeev",password="rajeev!@#123",database="python_trading")
        mycursor = mydb.cursor()
        mycursor.execute("select lastprice  from liveprice ")
        myresult = mycursor.fetchall()
        a=list(map(lambda x:x[0],myresult))
        print(a)
        Nold=a[0]
    
        Bold=a[1]
        status=""
        if (Nold)>str(Lprice):
            a="0"
            status=a
        else:
            status="1"
    


        status2=""
    
        if Bold>str(Lprice2):
            c="0"
            status2=c
        else:
            status2="1"

        sql='UPDATE liveprice set lastprice=%s,status=%s,chg=%s where symbol=%s'
        values=(Lprice,Chg,Symbol)
        sql2='UPDATE liveprice set lastprice=%s,status=%s,chg=%s where symbol=%s'
        values=(Lprice,status,Chg,Symbol)
        values2=(Lprice2,status2,Chg2,Symbal2,)


        mycursor.execute(sql,values)
        mycursor.execute(sql2,values2)





        mydb.commit()
        mydb.close()
        
        

    except:
        nit()
def exit():
    print("bye")
    sys.exit()
schedule.every(60).seconds.do(test)
schedule.every().day.at("01:37").do(exit)

while True:
    schedule.run_pending()
    