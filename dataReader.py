#Name: Jacob Ratzlaff
#Date: Feb 22, 2018
#A lab to read acceleration off of a simple 3 dof sensor
import smbus 
import time


#Accelerometer class

class Accelerometer:
	def __init__(self, data, adjuster=0):
		self.xA = (data[1]*256 + data[0])/16
		self.yA = (data[3]*256 + data[2])/16
		self.zA = (data[5]*256 + data[4])/16
		#x=pitch
		#y=roll
		#z=yaw		
		self.xG = (data[7]*256 + data[6])/16
		self.yG = (data[9]*256 + data[8])/16
		self.zG = (data[11]*256 + data[10])/16
		
				
		if self.xA > 2047:
			self.xA -=4096
		if self.yA > 2047:
			self.yA -=4096
		if self.zA > 2047:
			self.zA -=4096
		if self.xG > 2047:
			self.xG -=4096
		if self.yG > 2047:
			self.yG -=4096
		if self.zG > 2047:
			self.zG -=4096
		if adjuster!=0:
			self.xA-=adjuster.xA
			self.yA-=adjuster.yA
			self.zA-=adjuster.zA
			self.xG-=adjuster.xG
			self.yG-=adjuster.yG
			self.zG-=adjuster.zG


	def printData(self):
		print("Acceleration in x is {}".format(self.xA))
		print("Acceleration in y is {}".format(self.yA))
		print("Acceleration in z is {}".format(self.zA))
		print("Gyro in x is {}".format(self.xG))
		print("Gyro in y is {}".format(self.yG))
		print("Gyro in z is {}".format(self.zG))
	def printVec(self):
		print('({},{},{})'.format(self.xA,self.yA,self.zA))
	def sum(self, other):
		self.xA+=other.xA
		self.yA+=other.yA
		self.zA+=other.zA
		self.xG+=other.xG
		self.yG+=other.yG
		self.zG+=other.zG
	def average(self, quantity):
		self.xA/=quantity
		self.yA/=quantity
		self.zA/=quantity
		self.xG/=quantity
		self.yG/=quantity
		self.zG/=quantity

class Position:
	def __init__(self):
		self.x=0
		self.y=0
		self.z=0
		self.xV=0
		self.yV=0
		self.zV=0
		self.pitch=0
		self.roll=0
		self.yaw=0
	def update(self, accel, time):
		self.pitch+=accel.xG*time
		#self.pitch %=800
		self.roll+=accel.yG*time
		#self.roll %=800
		self.yaw+=accel.zG*time
		#self.yaw %=800
		#200 = 90 degrees
		self.xV+=1000*time*(self.pitch/200-self.roll/200)
		self.yV-=1000*time*(self.roll/200-self.pitch/200)
		self.zV-=1000*time*(1 -self.pitch/200 -self.roll/200)
		#TODO:Remove gravity

		self.xV+=accel.xA*time
		self.yV+=accel.yA*time
		self.zV+=accel.zA*time
		self.x+=self.xV*time
		self.y+=self.yV*time
		self.z+=self.zV*time
	def print(self):
		print('Location:\t({},{},{})'.format(self.x,self.y,self.z))
		print('Velocity:\t({},{},{})'.format(self.xV,self.yV,self.zV))
		print('Orientation:\t({},{},{})'.format(self.pitch,self.roll,self.yaw), end='\n\n\n')

def printList(l):
	str =""
	for i in l:
		i.printVec()

# Sends enable bytes to control registers
def initSensors(accel = False, gyro = False, magno = False):
	if gyro == True:
		bus.write_byte_data(0x6B, 0x20, 0b11000000)
	if accel == True:
		bus.write_byte_data(0x6B, 0x10, 0b11001011)
	if magno == True:
		bus.write_byte_data(0x1E, 0x20, 0b01011000)

def readAccel(delay, adjuster=0):
	#Parameters for write_byte_data
	#1. Address of the device
	#2. Communication data - active mode control register, sub address
	#3. Settings and or mode
	#Gyro
	#bus.write_byte_data(0x6B, 0x10, 0b11001011) 
	bus.write_byte_data(0x6B, 0x1E, 0b00111000)
	
	#Accel
	#bus.write_byte_data(0x6B, 0x20, 0b11000000)
	bus.write_byte_data(0x6B, 0x1F, 0b00111000)
	
	#Magno
	#bus.write_byte_data(0x1E, 0x20, 0b01011000)
	#bus.write_byte_data(0x1E, 0x, 0b01011000)
	
	time.sleep(delay/2.0)

	gyro = bus.read_i2c_block_data(0x6B, 0x18, 6)
	accel = bus.read_i2c_block_data(0x6B, 0x28,6)
	data = Accelerometer(data=accel+gyro, adjuster=adjuster)

	#put register in standbye mode
	bus.write_byte_data(0x6B, 0x1E, 0b00000000) 
	bus.write_byte_data(0x6B, 0x1F, 0b00000000)
	time.sleep(delay/2.0)
	#data.printData()
	#print(data)
	return data

def calibrateAccel(calibrationTime):
	sum = Accelerometer([0]*12)
	for i in range(calibrationTime*100):
		data = readAccel(.01)
		sum.sum(data)
	sum.average(calibrationTime*100)
	sum.zA -= 1000
	return sum

if __name__ == "__main__":
	# Get I2C bus - initial bus to channel 1
	bus = smbus.SMBus(1) 
	adj = calibrateAccel(5)
	initSensors(accel = True, gyro = True)
	pos = Position()
	try:
		for i in range(100000):
			data = readAccel(.01, adj)
			pos.update(data,.01)
			if i % 100 == 0:
				pos.print()
	#capture the control c and exit cleanly
	except(KeyboardInterrupt, SystemExit):
		print("User requested exit.")
