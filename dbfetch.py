import check_sql


cur, conn = check_sql.get_connection()

cur.execute("select lastprice from liveprice")
result=cur.fetchall()
for i in result:
	print(i)