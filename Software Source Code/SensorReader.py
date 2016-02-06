#import digital sensor/ADC libraries
from Adafruit_ADS1x15 import ADS1x15
from Adafruit_BMP085 import BMP085
from Adafruit_TSL2561 import Adafruit_TSL2561

class SensorReader:

    #global digital sensor booleans
    _BMP085_connected = False
    _TSL2561_connected = False
    #global debug
    _debug = False

    #init function    
    def __init__(self, _BMP085_on, _TSL2561_on, debug=False):

        #configure global booleans
        self._BMP085_connected = _BMP085_on
        self._TSL2561_connected = _TSL2561_on
        self._debug = debug

        #initiate ADC
        self.ADC = ADS1x15()
        
        #initiate BMP if connected
        if self._BMP085_connected == True:
            self.BMP=BMP085()

        #initiate TSL if connected
        if self._TSL2561_connected == True:
            self.TSL=Adafruit_TSL2561()

        #debug print to see if everything works
        if self._debug == True:    
            print "ADC Test"
            print self.ADC.readADCSingleEnded(0)
            print self.ADC.readADCSingleEnded(1)
            print self.ADC.readADCSingleEnded(2)
            print self.ADC.readADCSingleEnded(3)
            print "TSL Test"
            if self._TSL2561_connected == True:
                print self.TSL.calculate_lux()
            else:
                print "TSL OFF"
            print "BMP Test"
            if self._BMP085_connected == True:
                print self.BMP.readTemperature()
                print self.BMP.readPressure()
            else:
                print "BMP OFF"
            print "LOAD DONE"
            

    #reads lux from TSL2561, returns 0 if not connected
    def readLux(self):
        if self._debug == True:
            print "Read TSL2561 Lux"
        if self._TSL2561_connected == True:
            return self.TSL.calculate_lux()
        else:
            return 0

    #reads pressure from BMP085, returns 0 if not connected
    def readPressure(self):
        if self._debug == True:
            print "Read BMP085 Pressure"
        if self._BMP085_connected == True:
            return self.BMP.readPressure()
        else:
            return 0

    #reads temperature from BMP085, returns 0 if not connected
    def readTemp(self):
        if self._debug == True:
            print "Read BMP085 Temperature"
        if self._BMP085_connected == True:
            return self.BMP.readTemperature()
        else:
            return 0

    #reads analog distance, requires proper channel
    def readDistance(self, channel):
        if self._debug == True:
            print "reading distance from channel:", channel
        raw_distance = self.ADC.readADCSingleEnded(channel)
        distance = raw_distance  #GET PROPER DATA INTERPRETATION
        return distance

    #reads velocity interpreted from analog distance, requires proper channel
    def readVelocity(self, channel):
        print "NOT FINISHED!!"

    #reads analog X axis accel, requires proper channel
    def readXAccel(self, channel):
        if self._debug == True:
            print "reading X Accel from channel:", channel
        raw_x_accel = self.ADC.readADCSingleEnded(channel)
        x_accel = (raw_x_accel*0.03016426)-49.23503
        return round(x_accel, 2)

    #reads analog y axis accel, requires proper channel
    def readYAccel(self, channel):
        if self._debug == True:
            print "reading Y Accel from channel:", channel
        raw_y_accel = self.ADC.readADCSingleEnded(channel)
        y_accel = (raw_y_accel*0.02983803)-49.01283
        return round(y_accel, 2)

    #reads analog z axis accel, requires proper channel
    def readZAccel(self, channel):
        if self._debug == True:
            print "reading Z Accel from channel:", channel
        raw_z_accel = self.ADC.readADCSingleEnded(channel)
        z_accel = (raw_z_accel*0.02962248)-50.16295
        return round(z_accel, 2)
    
    #reads total accel interpreted from analog accel
    #requires proper channel setting
    def ReadTotalAccel(self, channel_x, channel_y, channel_z):
        print "NOT FINISHED!!"

    #reads analog temperature, requires proper channel
    def readAnalogTemp(self, channel):
        if self._debug == True:
            print "reading temp from channel:", channel
        raw_temp = self.ADC.readADCSingleEnded(channel)
        temp = (raw_temp-500)/10
        return round(temp, 2)
    
    
        
        
