import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient 
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library

ESC=5  #Connect the ESC in this GPIO pin 

pi = pigpio.pi()
ESC_pins = [4,5,6,12]
ESC_speeds = [900,900,900,900]
for i in ESC_pins:
    pi.set_servo_pulsewidth(ESC, 0) 

max_value = 2000 #change this if your ESC's max value is different or leave it be
min_value = 750  #change this if your ESC's min value is different or leave it be


def stop(): #This will stop every action your Pi is performing for ESC ofcourse.
    for i in ESC_pins:
        pi.set_servo_pulsewidth(i, 0)
    pi.stop()


for i in ESC_pins:
    pi.set_servo_pulsewidth(i,0)
input('Disconnect the battery and then press enter')
for i in ESC_pins:
    pi.set_servo_pulsewidth(i,max_value)
input('Connect battery and after hearing the beeps and the bleeps, press enter')

for i in ESC_pins:
    pi.set_servo_pulsewidth(i,min_value)

time.sleep(5)

for i in ESC_pins:
    pi.set_servo_pulsewidth(i,0)
print('Starting motor soon...')
time.sleep(2)

for i in ESC_pins:
    pi.set_servo_pulsewidth(i,min_value)
time.sleep(1)
#TODO: start threads to controll individual speeds
try:
    for i in ESC_pins:
        pi.set_servo_pulsewidth(i,800)
    time.sleep(2)
    for i in range(4):
        pi.set_servo_pulsewidth(ESC_pins[i],ESC_speeds[i])
        time.sleep(2)
        pi.set_servo_pulsewidth(ESC_pins[i],0)
        time.sleep(2)
    input('Say something to stop')
except(KeyboardInterrupt, SystemExit):
    print('Exiting')
finally:
    stop()


