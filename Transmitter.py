from boltiot import Bolt
import json, time
import pymysql
import random

#Finds the api of receiver device located in particular area,finds by hashing index
def findapi(i):
    sql=("Select api from Disease_Record where Hindex=%d"%(i,))
    cursor.execute(sql)
    s=cursor.fetchall()
    return s[0][0]

#Finds the device id of receiver device located in particular area,finds by hashing index
def finddevid(i):
    sql=("Select Dev_id from Disease_Record where Hindex=%d"%(i,))
    cursor.execute(sql)
    s=cursor.fetchall()
    return s[0][0]

#Transmits the data to particular receiver device,whose device details is given
def transmit(api,dev_id,i):
    print("Transmitter ON")
    mybolt = Bolt(api, dev_id)
    flag=1
    while flag:
        time.sleep(10)
        response = mybolt.digitalRead('3') #ACK PIN Read
        data = json.loads(response)
        if int(data['value'])==1:
            rantime=random.choice(range(2,5,1))#random time is selected
            time.sleep(rantime)                #waits for random time
            response = mybolt.digitalRead('3') #ACK PIN Read
            data = json.loads(response)
            if int(data['value'])==1:
                time.sleep(3)
                response = mybolt.digitalWrite('0','LOW')   #ack pin made zero,indicate active transmission
                time.sleep(5)
                response = mybolt.digitalWrite(str(i),'HIGH')# i is the pin number of device to be made high
                return
            
# Transmits red column of corresponding hashing index(corona positive counts)
def transmitred(i,dev_id,api):
    sql=("Select Red from Disease_Record where Hindex=%d"%(i,))
    cursor.execute(sql)
    s=cursor.fetchall()
    red=temp=s[0][0]
    if red==0 or red==None:
        return

    #Below loop transmits each counts one by one
    for i in range(red):
        print("Red Transmitting...")
        transmit(api,dev_id,4)
        temp=temp-1
        sql=("Update Disease_Record set Red=%d where Hindex=%d"%(temp,i))
        cursor.execute(sql)
        connection.commit()
        
# Transmits green column of corresponding hashing index(corona recovery counts)
def transmitgreen(i,dev_id,api):
    sql=("Select Green from Disease_Record where Hindex=%d"%(i,))
    cursor.execute(sql)
    s=cursor.fetchall()
    green=temp=s[0][0]
    if green==0 or green==None:
        return
    #Below loop transmits each counts one by one
    for i in range(green):
        print("Green Transmitting...")
        transmit(api,dev_id,2)
        temp=temp-1
        sql=("Update Disease_Record set Green=%d where Hindex=%d"%(temp,i))
        cursor.execute(sql)
        connection.commit()

#Transmits all column counts for particular row
def rowtransmit(i,dev_id,api):
   if api=='-1':
       return 0
   else:
       transmitred(i,dev_id,api)
       transmitgreen(i,dev_id,api)

maxhindex=3
#Permanent iteration as database is dynamic
while 1:
    #Below loop transmits the counts for all hasing index.Per iteration it scans database for a particular area
    for i in range(maxhindex): #iterate by hashing index
        connection=pymysql.connect(host="localhost",user="root",passwd="Tantra123",db='disease')
        cursor=connection.cursor()
        api=findapi(i)
        devid=finddevid(i)
        rowtransmit(i,devid,api)    
        connection.close()
                
            
    
