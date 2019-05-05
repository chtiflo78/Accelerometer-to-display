##**********************************************************
## Written by: Florent Spriet (alias chtiflo78)
## Date: April 2019
##
## Data are sent by I2C by an Arduino, ref to separate program
##**********************************************************

import serial 
import numpy
import matplotlib.pyplot as plt
from drawnow import *

## CALIBRATION OF MY PMU 6050
offsetAcX=0.10
offsetAcY=-0.05
offsetAcZ=1.96
offsetGyX=-9.78
offsetGyY=-1.60
offsetGyZ=1.25

## 
AcX=[]
AcY=[]
AcZ=[]
temp=[]
GyX=[]
GyY=[]
GyZ=[]

count=0

plt.ion()

## Open serial link
serie=serial.Serial('COM3',baudrate=115200) 											

## Remove the first data otherwise it fails
for i in range(0,10):
    lecture= serie.readline()                       

## Display the 2 graphs: one for acceleration data, one for gyro data
def plotValeurs():
    plt.subplot(2,1,1)
    plt.title('Sensor Data: Acceleration (m/s^2)')     
    plt.ylim(-11, 11)
    plt.grid(True)                                  
    plt.plot(AcX, 'b>-', label='Accel X')          
    plt.plot(AcY, 'g^-', label='Accel Y')
    plt.plot(AcZ, 'm*-', label='Accel Z')

    plt.subplot(2,1,2)
    plt.title('Sensor Data: Gyroscope (deg/s)')       
    plt.ylim(-150,+150)
    plt.grid(True)                                  
    plt.plot(GyX, 'b>-', label='Accel X')           
    plt.plot(GyY, 'g^-', label='Accel Y')
    plt.plot(GyZ, 'm*-', label='Accel Z')

## Main program
while True:
    while(serie.inWaiting()==0):
        pass
    ## reads data from serial link
    lecture= serie.readline().decode('ascii')
    dataArray=lecture.split(',')
    ## converts into regular units
    AcX.append(float(dataArray[0])/16384*9.81+offsetAcX)
    AcY.append(float(dataArray[1])/16384*9.81+offsetAcY)
    AcZ.append(float(dataArray[2])/16384*9.81+offsetAcZ)
    temp.append(float(dataArray[3]))
    GyX.append(float(dataArray[4])/131+offsetGyX)
    GyY.append(float(dataArray[5])/131+offsetGyY)
    GyZ.append(float(dataArray[6])/131+offsetGyZ)
    count=count+1
    ## removes excess data to scroll the graph
    if count>30:
        AcX.pop(0)
        AcY.pop(0)
        AcZ.pop(0)
        temp.pop(0)
        GyX.pop(0)
        GyY.pop(0)
        GyZ.pop(0)               
    ## display the graph
    drawnow(plotValeurs)                      

