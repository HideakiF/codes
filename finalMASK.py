#!/usr/bin/env python3

import os
import time
import datetime
import requests
#--------------------------------------------------------------
#  Note: ds18b20's data pin must be connected to pin7(GPIO4).
#--------------------------------------------------------------

# Reads temperature from sensor and prints to stdout
# id is the id of the sensor



def readSensor(id):
    tfile = open("/sys/bus/w1/devices/"+id+"/w1_slave")
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    temperature = temperature / 1000
    now = datetime.datetime.now() 
    print (now.strftime("%Y/%m/%d %H:%M:%S")), temperature

#def send_line(text):
    url ='https://notify-api.line.me/api/notify'
    token = "xxxxxxxxxxxxxxxxxxxxxxx"
    headers ={'Authorization' : 'Bearer ' + token}
#    message = text
    if temperature >= 27:  

        message = temperature
 #   else:
 #       message = "normal"
        payload = {'message' : message}
        p = requests.post(url, headers=headers, data=payload)
        print(p)
    else:
        pass

#    now = datetime.datetime.now() 

#text="(now)"
#text=temperature
#    text= "temperature, 25.684" 
#text = "CDF" 
#    send_line(text)



#url = "https://notify-api.line.me/api/notify"
#token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#headers = {"Authorization" : "Bearer "+ token}
#message =  temperature, (now.strftime("%Y/%m"))
#payload = {"message" :  message}
#r = requests.post(url, headers = headers, params=payload) 


# Reads temperature from all sensors found in /sys/bus/w1/devices/
# starting with "28-...
def readSensors():
    count = 0
    sensor = ""
    for file in os.listdir("/sys/bus/w1/devices/"):
        if (file.startswith("28-")):
            readSensor(file)
            count+=1
    if (count == 0):
        print ("No sensor found! Check connection")

# read temperature every 2second for all connected sensors
def loop():
    while True:
        readSensors()
        time.sleep(2)

# Nothing to cleanup
def destroy():
    pass

# Main starts here
if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

