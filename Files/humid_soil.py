#humd_soil
#import adafruit_dht
import board
import sys
import busio
from adafruit_seesaw.seesaw import Seesaw
import time

#definition of pins for DHT
#sudo pip3 install Adafruit_DHT
'''connnect leftmostpin to GPIO 4, middle to 5v and rightmost to GND'''
#DHT_SENSOR = dht.DHT11

    
def read_soil_values(ss1, ss2, phum):
    '''reads values from humidity sensor and returns '''
    #humidity, temperature = dht.read_retry(11, 4)
    humidity = 0
    humidity2 = 0
    avg_hum = 0
    MAX_HUM = 800
    MIN_HUM = 100
    try: 
        humidity =ss1.moisture_read()
#         humidity =ss.get_temp()
    except RuntimeError:
        humidity = 0
    try:
        humidity2 = ss2.moisture_read()
    except:
        humidity2 = 0
    if(humidity != 0 and humidity2 != 0):
        avg_hum = (humidity+humidity2)/2
        if abs(humidity-humidity2) > 100:
            print("faulty sensor")
        if (humidity < MIN_HUM or humidity > MAX_HUM):
            avg_hum = humidity2
        elif (humidity2< MIN_HUM or humidity2 > MAX_HUM):
            avg_hum = humidity1
        else:
            if (abs(humidity - phum) >= abs(humidity2 - phum)):
                avg_hum = humidity
            elif (abs(humidity - phum) < abs(humidity2 - phum)):
                avg_hum = humidity2
    else:
        avg_hum = phums
    return avg_hum

if __name__ == "__main__":
    i2c1 = busio.I2C(board.SCL, board.SDA)
    i2c2 = busio.I2C(board.SCL, board.SDA)
    #ss=Seesaw(board.D27)
    #print(Seesaw.get_i2c_addr())
    ss1 = Seesaw(i2c1,addr=0x36)
    ss2 = Seesaw(i2c2,addr=0x37)
    while True:
        x1 = read_soil_values(ss1, ss2, 400)
        print("Current soil humidity {}amp \u00b1 5.0 amp".format(x1))
        time.sleep(5)