import os	 #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient 
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library
import dataReader
ESC=5  #Connect the ESC in this GPIO pin 

pi = pigpio.pi()
ESC_pins = [4,5,6,12]
ESC_speeds = [1100,1100,1100,1100]
for i in ESC_pins:
	pi.set_servo_pulsewidth(ESC, 0) 

max_value = 2000 #change this if your ESC's max value is different or leave it be
min_value = 750  #change this if your ESC's min value is different or leave it be


def stop(): #This will stop every action your Pi is performing for ESC ofcourse.
	for i in ESC_pins:
		pi.set_servo_pulsewidth(i, 0)
	pi.stop()
stop()
