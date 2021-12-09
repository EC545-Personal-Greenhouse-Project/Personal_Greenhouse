import parse_send_data as twmodule #sms module
import time
import datetime
import humid_temp_s as dht_hum #air sensors function
import humid_soil as h_soil
import camera_module as camera
import adafruit_dht #used for humidity sensors
import board #used to get GPIO pins
import sys 
import csv #used to write files
import os.path
from board import SCL, SDA
import busio
from adafruit_seesaw.seesaw import Seesaw
from toggle_smartplug import toggle_plug
import water_pump_module as wpump #module to turn on water pump
import RPi.GPIO as GPIO
import lcd_display as lcd

WATER_PUMP = 21

#__________________________Lowest values___________________________
TEMP_THRESH = 27  
LOW_HUM = 1400 #set to 900
AIR_HUM = 50
# TOP_TEMP = 29

#____________________Write Data to CSV_____________________________
def csv_writer(air_values, filename, soil_values = 0):
    '''writes sensor data to a file each day'''
    row = [air_values[0], air_values[1], soil_values]
    header = []
    if(not os.path.exists(filename)):
            header = ["temp", "humidityRoom", "humiditySoil"]      
    with open(filename, 'a+', newline='') as f:
        writer = csv.writer(f, )
        if(header != []):
            writer.writerow(header)
        writer.writerow(row)
        f.close()
    return True
        
#___________________________Air sensor values_____________________________
def air_sensors(ptemp):
    '''gets the values for the air sensors'''
    air_values = dht_hum.read_air_values(dht_device,dht_device2,ptemp)
    return air_values

#___________________________Soil sensor module____________________________
def soil_sensor(phum):
    soil_hum_val = h_soil.read_soil_values(ss1, ss2, phum)
    return soil_hum_val

#___________________________Camera module_________________________________
def camera_module(filename):
    '''run camera module to calculate green % in image'''
    #turn on heat lamp light
    toggle_plug(True, 'Smart Heater')
    camera.camera_main(filename)
    #turn off heat lamp
    toggle_plug(False, 'Smart Heater') 

#_________________________Get file names____________________________________
def file_names():
    '''gets the file names for each particular day'''
    date_file = datetime.datetime.now()
    month = date_file.month
    day = date_file.day
    year = date_file.year
    File1 = "DataFolder/"+str(month)+"-"+str(day)+"-"+str(year)+"_sensors.csv"
    File2 = "DataFolder/"+"plant_growth.csv"
    return [File1, File2]

#________________________Prepare GPIO pins___________________________________
def start_GPIOs():
    '''starts GPIO_values'''
    import os, signal
    GPIO.cleanup()
    try:
        for line in os.popen("pgrep libgpiod"):
            pid = int(line)
            os.kill(pid, signal.SIGKILL)
    except:
        print("error")

#_________________________Start air sensors_____________________________________
    global dht_device
    dht_device = adafruit_dht.DHT11(board.D16) #GPIO for dht_device is GPIO_16
    global dht_device2
    dht_device2 = adafruit_dht.DHT11(board.D20) #GPIO for dht_device is GPIO_20
    
#__________________________Start soil sensors____________________________________
    i2c1 = busio.I2C(board.SCL, board.SDA) #SDA (white) GPIO_3, SCL (green) GPIO_4
    i2c2 = busio.I2C(board.SCL, board.SDA)
    global ss1
    global ss2
    ss1 = Seesaw(i2c1,addr=0x36) #address for soil humidity sensor 1
    ss2 = Seesaw(i2c2,addr=0x37) #address for soil humidity sensor 1
    
#___________________________Start relay module______________________________
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(WATER_PUMP, GPIO.OUT, initial=GPIO.HIGH) #Water Pump GPIO_21
    
#____________________________Start LCD Display______________________________
    lcd.main()
 
 
#____________________________Actuators______________________________________
def actuator_controller(air_temps, soil_hum):
    '''controlls all the actuators'''
    temp = air_temps[0]
    humidity = air_temps[1]
    heat_on = False
    humidity_on = False
    pump_on = False
    #Heat Lamp
    if temp < TEMP_THRESH:
        print("heat on")
        toggle_plug(True, 'Smart Heater')
        heat_on = True
    #Water pump
    if soil_hum < LOW_HUM:
        print("water on")
        wpump.water_plants(WATER_PUMP)
        pump_on = True
    #Humidifier
    if humidity < AIR_HUM:
        print("humidifier on")
        toggle_plug(True, 'Smart Humidifier')
        humidity_on = True
    
    time.sleep(10)
    
    if(pump_on):
        wpump.off_water(WATER_PUMP) #if toggled the water pump operates for 10seconds (over 20)
        print("pump off")
    
    time.sleep(5)
    
    if(humidity_on):
        toggle_plug(False, 'Smart Humidifier') #if toggled the whumidifier operates for 15seconds (over 20)
        print("humidifier off")
    
    time.sleep(5)
    
    if(heat_on):
        toggle_plug(False, 'Smart Heater') #if toggled the whumidifier operates for 19seconds (over 20)
        print("heat off")
    
    time.sleep(1)
        

        

    
#____________________________________Run top Module________________________________ 
if __name__ == "__main__":
    '''used to run the top_module'''
    i = 0
    #start_GPIOs()
    
    
    ptemp = TEMP_THRESH
    phumsoil = 400
    phum = 40
    current_date = datetime.datetime.now().day
    picture_taken = False
    try:
        while (True):
            start_GPIOs()
            files = file_names()
            if(picture_taken == False):
                camera_module(files[1])
                picture_taken = True
                prev_date = datetime.datetime.today() - datetime.timedelta(days=1)
                month = prev_date.month
                day = prev_date.day
                year = prev_date.year
                file_for_tw = "DataFolder/"+str(month)+"-"+str(day)+"-"+str(year)+"_sensors.csv"
                twmodule.send_sms_data(file_for_tw, files[1])
                
            air_values = air_sensors(ptemp)
            if(air_values != [None,None]):
                ptemp = air_values[0]
                phum = air_values[1]
            soil_humidity = soil_sensor(phumsoil)
            phumsoil = soil_humidity
            print("temperature {}, humidity {}, soil_hum {}".format(ptemp, phum, phumsoil))
            lcd.write_values([ptemp, phum],phumsoil)
            actuator_controller([ptemp, phum], phumsoil)
            csv_writer([ptemp,phum], files[0], phumsoil)
#             time.sleep(15)
            x = datetime.datetime.now().day
            if(x != current_date):
                current_date = x
                picture_taken = False
                
                
                
    except KeyboardInterrupt:
        print("Goodbye")
    finally:
        print("cleaning pins")
        GPIO.cleanup()
        
    