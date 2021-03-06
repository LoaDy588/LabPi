# import digital sensor/ADC libraries
from Adafruit_ADS1x15 import ADS1x15
from Adafruit_BMP085 import BMP085
from Adafruit_TSL2561 import Adafruit_TSL2561
from math import sqrt


class SensorReader:
    # global digital sensor booleans
    _BMP085_connected = False
    _TSL2561_connected = False
    # global debug
    _debug = False

    # init function
    def __init__(self, _BMP085_on, _TSL2561_on, debug=False):

        # configure global booleans
        self._BMP085_connected = _BMP085_on
        self._TSL2561_connected = _TSL2561_on
        self._debug = debug

        # initiate ADC
        self.ADC = ADS1x15()

        # initiate BMP if connected
        if self._BMP085_connected:
            self.BMP = BMP085(address=0x77, mode=3, debug=False)

        # initiate TSL if connected
        if self._TSL2561_connected:
            self.TSL = Adafruit_TSL2561()
            self.TSL.enable_auto_gain(True)

        # debug print to see if everything works
        if self._debug:
            print "ADC Test"
            print self.ADC.readADCSingleEnded(0)
            print self.ADC.readADCSingleEnded(1)
            print self.ADC.readADCSingleEnded(2)
            print self.ADC.readADCSingleEnded(3)
            print "TSL Test"
            if self._TSL2561_connected:
                print self.TSL.calculate_lux()
            else:
                print "TSL OFF"
            print "BMP Test"
            if self._BMP085_connected:
                print self.BMP.readTemperature()
                print self.BMP.readPressure()
            else:
                print "BMP OFF"
            print "LOAD DONE"

    # reads lux from TSL2561, returns 0 if not connected
    def readTSL2561Lux(self):
        if self._debug:
            print "Read TSL2561 Lux"
        if self._TSL2561_connected:
            return self.TSL.calculate_lux()
        else:
            return 0

    # reads pressure from BMP085, returns 0 if not connected
    def readBMP085Pressure(self):
        if self._debug:
            print "Read BMP085 Pressure"
        if self._BMP085_connected:
            return self.BMP.readPressure()
        else:
            return 0

    # reads temperature from BMP085, returns 0 if not connected
    def readBMP085Temp(self):
        if self._debug:
            print "Read BMP085 Temperature"
        if self._BMP085_connected:
            return self.BMP.readTemperature()
        else:
            return 0

    # reads analog distance, requires proper channel
    def readDistance(self, channel):
        print "NOT FINISHED!!"

    # reads velocity interpreted from analog distance, requires proper channel
    def readVelocity(self, channel):
        print "NOT FINISHED!!"

    # reads analog X axis accel from ADXL335 sensor, requires proper channel
    def readADXL335XAccel(self, channel):
        if self._debug == True:
            print "reading X Accel from channel:", channel
        raw_x_accel = self.ADC.readADCSingleEnded(channel, 6144, 250)
        x_accel = (raw_x_accel * 0.03016426) - 49.23503
        return round(x_accel, 2)

    # reads analog y axis accel from ADXL335 sensor, requires proper channel
    def readADXL335YAccel(self, channel):
        if self._debug == True:
            print "reading Y Accel from channel:", channel
        raw_y_accel = self.ADC.readADCSingleEnded(channel, 6144, 250)
        y_accel = (raw_y_accel * 0.02983803) - 49.01283
        return round(y_accel, 2)

    # reads analog z axis accel from ADXL335 sensor, requires proper channel
    def readADXL335ZAccel(self, channel):
        if self._debug == True:
            print "reading Z Accel from channel:", channel
        raw_z_accel = self.ADC.readADCSingleEnded(channel, 6144, 250)
        z_accel = (raw_z_accel * 0.02962248) - 50.16295
        return round(z_accel, 2)

    # reads total accel interpreted from analog accel from ADXL335 sensor
    # requires proper channel setting
    def readADXL335TotalAccel(self, channel_x, channel_y, channel_z):
        if self._debug == True:
            print "reading total accel from channels:", channel_x, ",", channel_y, ",", channel_z
        total_accel = sqrt((self.readADXL335XAccel(channel_x) ** 2)
                           + (self.readADXL335YAccel(channel_y) ** 2)
                           + (self.readADXL335ZAccel(channel_z) ** 2))
        return round(total_accel, 2)

    # reads analog temperature, requires proper channel
    def readTMP36(self, channel):
        if self._debug == True:
            print "reading temp from channel:", channel
        raw_temp = self.ADC.readADCSingleEnded(channel, 6144, 250)
        temp = (raw_temp - 500) / 10
        return round(temp, 2)

    # reads analog temeprature from LMT86 sensor, requires proper channel
    def readLMT86(self, channel):
        if self._debug == True:
            print "reading temp from channel:", channel
        raw_temp = self.ADC.readADCSingleEnded(channel, 6144, 250)
        temp = ((10.888-sqrt((10.888**2)+4*0.00347*(1777.3-raw_temp)))/(2*(-0.00347)))+30
        return round(temp, 2)
