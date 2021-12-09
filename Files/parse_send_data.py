#parse through data and call Twilio api to send to user

from __future__ import division
from twilio.rest import Client
import csv
import sys
import os
import datetime
import time
import string

#for sending only once (running script only once every interval)
#File1 = 'sensor_date.csv' #need to change to this based on file location, sensor data
#File2 = 'plant_data.csv' #need to change to this based on file location, camera plant data
def send_sms_data(File1, File2):
    '''sends sms text with the averaged values found in File1 and File2'''
    items = []
    items2 = []
    items3 = []
    #items4 = []

    with open(File1) as csvfile:
        csvReader = csv.reader(csvfile)
        for col in csvReader:
                items.append(col[0])
                items2.append(col[1])
                items3.append(col[2])

    sensor1 = items[0]
    items.pop(0)
    l1 = len(items)
    items = map(int, items)
    sensor2 = items2[0]
    items2.pop(0)
    l2 = len(items2)
    items2 = map(int, items2)
    sensor3 = items3[0]
    items3.pop(0)
    l3 = len(items3)
    items3 = map(int, items3)
    '''sensor4 = items4[0]
    items4.pop(0)
    l4 = len(items4)
    items4 = map(int, items4)'''

    avg1 = sum(items) / l1
    avg2 = sum(items2) / l2
    avg3 = sum(items3) / l3
    #avg4 = sum(items4) / l4

    with open(File2, "r") as file:
        first_line = file.readline()
        for last_line in file:
            pass

    percentage = last_line.split(',')
    percentage2 = percentage[1].split('\n')
    percentage3 = percentage2[0]

    timee = datetime.datetime.now()


    account_sid = os.environ['TWILIO_ACCOUNT_SID'] = ''
    auth_token = os.environ['TWILIO_AUTH_TOKEN'] = ''
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body="The current averages of the sensor data are: \n" + sensor1 + ": " + str(avg1) + "\n" + sensor2 + ": "
                         + str(avg2) + "\n" + sensor3 + ": " + str(avg3) + "\nGrowth of plant: " + percentage3 + " %",
                         from_='',
                         to=''
                     )

    print(message.sid)



