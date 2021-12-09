import adafruit_dht
import board
import sys
import time
import math

#definition of pins for DHT
#sudo pip3 install Adafruit_DHT
#DHT_SENSOR = dht.DHT11

    
def read_air_values(dht_device, dht_device2,ptemp):
    '''reads values from humidity sensor and returns [temperature, humidity] values, temperature is in Farenheit'''
    #humidity, temperature = dht.read_retry(11, 4)
    isok = False
    isok2 = False
    while(not (isok or isok2)):
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            if temperature != None:
                isok = True
        except RuntimeError:
            print("")
        try:
            temperature2 = dht_device2.temperature
            humidity2 = dht_device2.humidity
            if temperature2 != None:
                isok2 = True
        except RuntimeError:
            print("")
            
    if(not isok and not isok2):
        
        MAX_TEMP = 47
        MIN_TEMP = 20
        DESIRED_TEMP = 27
        
        at = (temperature + temperature2) /2
        ah = (humidity + humidity2) / 2
        
        if(abs(temperature - temperature2) > 2):
            print("one sensor faulty")
            if temperature > MAX_TEMP:
                at = temperature2
                ah = humidity2
            elif temperature < MIN_TEMP:
                at = temperature2
                ah = humidity2
            elif temperature2 > MAX_TEMP:
                at = temperature
                ah = humidity
            elif temperature2 < MIN_TEMP:
                at = temperature
                ah = humidity
            else:
                if (abs(temperature - ptemp) > abs(temperature2 - ptemp)):
                    at = temperature
                    ah = humidity
                elif (abs(temperature - ptemp) < abs(temperature2 - ptemp)):
                    at = temperature2
                    ah = humidity2
        
    elif (isok):
        at = temperature
        ah = humidity
    elif (isok2):
        at = temperature2
        ah = humidity2
    else:
        at = None
        ah = None
    
    return [at, ah]

if __name__ == "__main__":
    import time
    dht_device = adafruit_dht.DHT11(board.D17)
    dht_device2 = adafruit_dht.DHT11(board.D27)
    while True:
        
        x = read_air_values(dht_device, dht_device2, 27)
        print("Current Temperature {}\u00b0F \u00b1 3.6 \u00b0F, current room humidity {}% \u00b1 5.0%".format(x[0], x[1]))
        time.sleep(5)
