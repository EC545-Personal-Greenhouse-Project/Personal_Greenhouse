from picamera import PiCamera
import time
import cv2
import numpy as np
import csv
import pandas as pd
from PIL import Image as im 


##### Fucntion calculates the percentage green of a photo using HSV and a white mask #####
def percentGreen(mask):
    '''calculates green% in picture'''
    height, width = mask.shape[:2]
    num_pixels = height*width
    white_count = cv2.countNonZero(mask)
    percent_white = (white_count/num_pixels)*100
    percent_white = round(percent_white,2)
    return percent_white

################################ Begin Main function #####################################

def camera_main(filename):
    '''takes image of plant and writes green percentage to csv'''

    ##### Take picture #####
    camera = PiCamera()
    camera.resolution = (640,480)   # width, height 

    try:
        camera.start_preview()
        time.sleep(10)
        camera.capture('test.jpg')
    finally:
        time.sleep(1)
        camera.stop_preview()
        camera.close()
        
        

    ##### Process image and find percentage green #####
    img_bgr = cv2.imread('test.jpg')
    img_hsv = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2HSV)
    sensitivity = 30
    midpoint = 50
    lower_bound = np.array([midpoint-sensitivity, 120, 0])
    upper_bound = np.array([midpoint+sensitivity, 255, 255])
    print(type(img_hsv))
    mask = cv2.inRange(img_hsv, lower_bound, upper_bound)
    #data = im.fromarray(mask)
    #data.save("hello.png")
    new_percentage_green = percentGreen(mask)
    print("Percentage green of captured image is", new_percentage_green)



#     ##### Find plant size from 24 hrs ago in csv and calculate plant growth  #####
    frequency = 5   #frequency units are in terms of samples per 24 hours
    df = pd.read_csv(filename, sep=',', header=0)
    col = df['plantSize']
    old_percentage_green = col[col.size-frequency]
    print("Percentage green of image taken 24 hours ago", old_percentage_green)
    if(old_percentage_green != 0):
        growth_in_24hrs = (new_percentage_green-old_percentage_green)/old_percentage_green*100
    else:
        growth_in_24_hrs = new_percentage_green
    print("Percentage growth in 24 hours %.2f" % (growth_in_24hrs))
    print("Disclaimer: Percentage green calculated depends a lot on the lighting since the camera is not the best quality")
# 
# 
# 
#     ##### Write to csv #####
    rows = [new_percentage_green,growth_in_24hrs]
    with open(filename,'a') as file:
        writer = csv.writer(file)
        writer.writerow(rows)
    file.close()
    
    
################################ End Main function #####################################