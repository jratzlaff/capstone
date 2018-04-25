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

def printList(l):
    str =""
    for i in l:
        i.printVec()



# Get I2C bus - initial bus to channel 1
bus = smbus.SMBus(1) 
arr = []
try:
    for i in range(1000):
        #Parameters for write_byte_data
        #1. Address of the device
        #2. Communication data - active mode control register
        #3. Settings and or mode
        #Gyro
        bus.write_byte_data(0x6B, 0x10, 0b11001011) 
        bus.write_byte_data(0x6B, 0x1E, 0b00111000)
        #Accel
        bus.write_byte_data(0x6B, 0x20, 0b11000000)
        bus.write_byte_data(0x6B, 0x1F, 0b00111000)
        #Magno
        #bus.write_byte_data(0x1E, 0x20, 0b01011000)
        #bus.write_byte_data(0x1E, 0x, 0b01011000)
        
        time.sleep(0.005)

        gyro = bus.read_i2c_block_data(0x6B, 0x18, 6)
        accel = bus.read_i2c_block_data(0x6B, 0x28,6)
        data = Accelerometer(data=accel+gyro)

        #put register in standbye mode
        bus.write_byte_data(0x6B, 0x1E, 0b00000000) 
        bus.write_byte_data(0x6B, 0x1F, 0b00000000)
        time.sleep(0.005)
        #data.printData()
        #print(data)
        arr.append(data)
#capture the control c and exit cleanly
except(KeyboardInterrupt, SystemExit): 
    printList(arr)
    print("User requested exit... bye!")
sum = Accelerometer([0]*12)
for val in arr: 
    sum.sum(val)
sum.average(1000)
sum.printData()
time.sleep(1)

try:
    for i in range(1000):
        #Parameters for write_byte_data
        #1. Address of the device
        #2. Communication data - active mode control register
        #3. Settings and or mode
        #Gyro
        bus.write_byte_data(0x6B, 0x10, 0b11001011) 
        bus.write_byte_data(0x6B, 0x1E, 0b00111000)
        #Accel
        bus.write_byte_data(0x6B, 0x20, 0b11000000)
        bus.write_byte_data(0x6B, 0x1F, 0b00111000)
        #Magno
        #bus.write_byte_data(0x1E, 0x20, 0b01011000)
        #bus.write_byte_data(0x1E, 0x, 0b01011000)
        
        time.sleep(0.5)

        gyro = bus.read_i2c_block_data(0x6B, 0x18, 6)
        accel = bus.read_i2c_block_data(0x6B, 0x28,6)
        data = Accelerometer(data=accel+gyro, adjuster=sum)

        #put register in standbye mode
        bus.write_byte_data(0x6B, 0x1E, 0b00000000) 
        bus.write_byte_data(0x6B, 0x1F, 0b00000000)
        time.sleep(0.5)
        data.printData()
        #print(data)
        arr.append(data)
#capture the control c and exit cleanly
except(KeyboardInterrupt, SystemExit):
    print("User requested exit.")
