#Author: Jacob Ratzlaff and Austin Leo
#Purpose: Control the speeds of four ESCs via pigpio, also self correcting from an accelerometer

import os	 #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient 
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library
import dataReader
import smbus
import threading
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

bus = smbus.SMBus(1)
input('Press enter to begin calibration.')
adj = dataReader.calibrateAccel(bus,5)
#time.sleep(5)

for i in ESC_pins:
	pi.set_servo_pulsewidth(i,0)
print('Starting motor soon...')
time.sleep(2)

for i in ESC_pins:
	pi.set_servo_pulsewidth(i,min_value+50)
time.sleep(1)
#TODO: start threads to controll individual speeds
# Get I2C bus - initial bus to channel 1
def increaseSpeeds():
	while True:
		global ESC_speeds
		val = input("want to go fast?")
		if(val == '' or val =='y'):
			for i in range(4):
				ESC_speeds[i]+=20
		else:
			for i in range(4):
				ESC_speeds[i]-=20
try:
	t = threading.Thread(target=increaseSpeeds)
	t.daemon=False
	t.start()
	dataReader.initSensors(bus, accel = True, gyro = True)
	pos = dataReader.Position()
	for i in range(1000000):
		data = dataReader.readAccel(bus, .001, adj)
		pos.update(data,.001)
		if i % 10 == 0:
			if i %100 == 0:
				print(ESC_speeds)
				pos.print()
			if pos.roll > 3:
				ESC_speeds[2]+=1
				ESC_speeds[3]+=1
				ESC_speeds[0]-=1
				ESC_speeds[1]-=1
				#inc 6,12
			if pos.roll < -3:
				ESC_speeds[0]+=1
				ESC_speeds[1]+=1
				ESC_speeds[2]-=1
				ESC_speeds[3]-=1
				#inc 4,5
			if pos.pitch > 3:
				ESC_speeds[0]+=1
				ESC_speeds[3]+=1
				ESC_speeds[1]-=1
				ESC_speeds[2]-=1
				#inc 5,12
			if pos.pitch < -3:
				ESC_speeds[1]+=1
				ESC_speeds[2]+=1
				ESC_speeds[0]-=1
				ESC_speeds[3]-=1
				#inc 4,6
			
			for i in range(4):
				pi.set_servo_pulsewidth(ESC_pins[i], ESC_speeds[i])
		#capture the control c and exit cleanly
except(KeyboardInterrupt, SystemExit):
	print("User requested exit.")
finally:
	stop()
"""try:
	for i in ESC_pins:
		pi.set_servo_pulsewidth(i,800)
	time.sleep(2)
	for j in range(20):
		for i in range(4):
			pi.set_servo_pulsewidth(ESC_pins[i],800+j*50)
			time.sleep(2)
			pi.set_servo_pulsewidth(ESC_pins[i],0)
			time.sleep(2)
		print(800+j*50)
	#input('Say something to stop')
except(KeyboardInterrupt, SystemExit):
	print('Exiting')
finally:
	stop()

"""
