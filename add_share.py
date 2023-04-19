from tvDatafeed import TvDatafeed, Interval
import mysql.connector
conn=mysql.connector.connect(host="85.187.128.49",user="python_rajeev",password="rajeev!@#123",database="python_trading")
cur = conn.cursor()


var=["HDFCBANK","NIFTY"]




j=0
while j<len(var):
	i=0.5
	
	while i<=30:
		cur.execute("INSERT INTO bnrange (script,percentage) VALUES (%s, %s)", (var[j], i))

		# Commit the changes to the database
		conn.commit()
		
		i+=0.5
	
	j=j+1
		
# Close the cursor and connection
cur.close()
conn.close()
