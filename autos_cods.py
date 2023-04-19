import paramiko
import threading
from threading import Thread
import schedule
host = "3.6.153.152"
username = "Administrator"
password = "R!@#g123"
port = "22"
client = paramiko.client.SSHClient()
a=client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

c=client.connect(host, port,  username, password)



def bit_rsi():
    output1 = ""
    host1=host
    username1=username
    password1=password
    port1=port
    command='pythonw C:\\Users\\Administrator\\Desktop\\RSI\\bit_rsi.py'
    client1 = client
    b=a
    d=c
    stdin, stdout,stderr = client.exec_command(command)
    stdout.channel.set_combine_stderr(True)
    output = stdout.readlines()
    print(output)
    

def liveprice():
    output1 = ""
    host1=host
    username1=username
    password1=password
    port1=port
    command='pythonw C:\\Users\\Administrator\\Desktop\\priceupdate\\liveprice.py'
    client1 = client
    b=a
    d=c
    stdin, stdout,stderr = client.exec_command(command)
    stdout.channel.set_combine_stderr(True)
    output = stdout.readlines()
    

def rsi():
    output1 = ""
    host2=host
    username2=username
    password2=password
    port3=port
    command='pythonw C:\\Users\\Administrator\\Desktop\\RSI\\main.py'
    client2 = client
    k=a
    l=c
    stdin, stdout,stderr = client.exec_command(command)
    stdout.channel.set_combine_stderr(True)
    output = stdout.readlines()
    

def all_file():
    if __name__ == '__main__':
        Thread(target = bit_rsi).start()
        Thread(target = liveprice).start()
        Thread(target = rsi).start()
       
       

all_file()



