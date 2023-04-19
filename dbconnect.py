

import pymysql
import mysql.connector

def get_connection():
    conn = mysql.connector.connect(host="85.187.128.49",user="elitealgo_admin",password="Safi@12345##",database="elitealgo_admin")
    cur = conn.cursor()
    return cur, conn