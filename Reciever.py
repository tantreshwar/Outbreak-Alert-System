from boltiot import Bolt
import json, time,requests
api_key = "e90ab9b0-1def-4da5-90cf-2c2c9165fdf9" #Receiver device api
device_id  = "BOLT1115146"                       #Receiver device id
mybolt = Bolt(api_key, device_id)
telegram_chat_id="@XXXX"              #Telegram channel for particular area receiver
telegram_bot_id="botXXXX"  #Telegram channel bot for particular area receiver(used for posting message)

#Sends telegram message to particular telegram channel
def send_telegram_message(message):
    """Sends message via Telegram"""
    url = "https://api.telegram.org/" + telegram_bot_id + "/sendMessage"
    data = {
        "chat_id": telegram_chat_id,
        "text": message
    }
    try:
        response = requests.request(
            "POST",
            url,
            params=data
        )
        telegram_data = json.loads(response.text)
        return telegram_data["ok"]
    except Exception as e:
        print("An error occurred in sending the alert message via Telegram")
        print(e)
        return False

response = mybolt.digitalWrite('0','HIGH') #ACK PIN Setted
data = json.loads(response)
time.sleep(3)

#Since Receiver should be always ready,hence permanent loop
while 1:
    response = mybolt.digitalRead('3') #ACK PIN
    data = json.loads(response)

    #Low ACK pin means active transission
    if int(data['value'])==0:   
        print("Found Info!!")
        flag=1
        #Is kept high because on transmitter part there might be delay mismatch so it waits for data
        while flag:
            time.sleep(10)
            response = mybolt.digitalRead('1') #Corona Pin
            data = json.loads(response)
            time.sleep(10)
            response = mybolt.analogRead('A0') #Corona Recovery Pin
            data1 = json.loads(response)
            if int(data['value'])==1:
                flag=0
                print("Corona Case!!")
                send_telegram_message("Alert!!Corona Case in your Area")
                response = mybolt.digitalWrite('4','LOW')
            elif int(data1['value'])>=255:
                flag=0
                print("Corona Recovery Case!!")
                time.sleep(10)
                send_telegram_message("Corona Case Recovered in your Area")
                response = mybolt.digitalWrite('2','LOW')

        #flag=0 means data has been received
        if flag==0:
            time.sleep(10)
            print("Recieved the data!!...setting acknowledgemnt pin")
            mybolt = Bolt(api_key, device_id)
            response = mybolt.digitalWrite('0','HIGH') #ACK PIN Setted
    else:
        print("Huh!!Feels Safe...")
    time.sleep(10)
        
    
                
            
    
