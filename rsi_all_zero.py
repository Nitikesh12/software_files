import mysql.connector
mydb=mysql.connector.connect(host="85.187.128.49",user="python_rajeev",password="rajeev!@#123",database="python_trading")
mycursor=mydb.cursor()
l="0"

sql="UPDATE rsi set buy_rsi2=%s,sell_rsi2=%s,buy_rsi3=%s,sell_rsi3=%s,high=%s,low=%s,datetime=%s"
values=(l,l,l,l,l,l,l)
mycursor.execute(sql,values)
mydb.commit()
mydb.close()