import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests
#Provide your IBM Watson Device Credentials
organization = "m4xk0q"
deviceType = "raspberrypi"
deviceId = "12345"
authMethod = "token"
authToken = "123456789"


def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data['command'])

        if cmd.data['command']=='motoron':
                print("MOTOR ON IS RECEIVED")
                
        elif cmd.data['command']=='motoroff':
                print("MOTOR OFF IS RECEIVED")

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        temp =random.randint(30, 50)
        #print(temp)
        hum=random.randint(10, 40)
        #print(hum)
        IR=random.randint(10, 100)
        LDR=random.randint(10, 100)
        #Send Temperature & Humidity to IBM Watson
        data = { 'Temperature' : temp, 'Humidity': hum, 'IR': IR, 'LDR': LDR }
        #print (data)
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Humidity = %s %%" % hum, "IR = %s %%" % IR, "LDR = %s %%" % LDR, "to IBM Watson")

        success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
        if(temp<50):
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=FbePY3fU4GjBnm07gCoAL5KkpNZVcDTt6rzxa1qyO9hui2XQlWkvTej34F5PbMhOGaRxmU9tqiWBNl6z&sender_id=FSTSMS&message=Temperature is low.Please switch on the motor fan&language=english&route=p&numbers=6005411299')
                print(r.status_code)
        if(hum<50):
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=FbePY3fU4GjBnm07gCoAL5KkpNZVcDTt6rzxa1qyO9hui2XQlWkvTej34F5PbMhOGaRxmU9tqiWBNl6z&sender_id=FSTSMS&message=Humidity is low.Please switch on the motor fan&language=english&route=p&numbers=6005411299')
                print(r.status_code)
        if(LDR<50):
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=FbePY3fU4GjBnm07gCoAL5KkpNZVcDTt6rzxa1qyO9hui2XQlWkvTej34F5PbMhOGaRxmU9tqiWBNl6z&sender_id=FSTSMS&message=Light intensity is low...&language=english&route=p&numbers=6005411299')
                print(r.status_code)
        if(IR<50):
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=FbePY3fU4GjBnm07gCoAL5KkpNZVcDTt6rzxa1qyO9hui2XQlWkvTej34F5PbMhOGaRxmU9tqiWBNl6z&sender_id=FSTSMS&message=No object is detected in the truck.&language=english&route=p&numbers=6005411299')
                print(r.status_code)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
