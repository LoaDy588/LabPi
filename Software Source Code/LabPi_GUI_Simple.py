import Tkinter as Tk                   #import Tkinter for GUI
from SensorReader import SensorReader  #import SensorReader for reading data
from DataLogger import DataLogger      #import DataLogger for working with data
import time                            #import time
import matplotlib.pyplot as plt        #import pyplot for data vis


class App:

    #init function, sets up global variables and objects, builds the GUI
    def __init__(self, master):

        #global variables
        self.master = master

        #available sensors list
        self.Sensors = ["TMP36",
                        "ADXL335 X-axis",
                        "ADXL335 Y-axis",
                        "ADXL335 Z-axis",
                        "ADXL335 Total",
                        "BMP180 Temp",
                        "BMP180 Pressure",
                        "TSL2561"]

        #State controls if the software actively measures
        self.State = False

        #Interval controls the interval between measurements
        self.Interval = 100

        #Sensor_value displays actual measured value
        self.Sensor_value = Tk.StringVar(master)
        self.Sensor_value.set("0.0")

        #SensorSelect controls which sensor is selected
        self.SensorSelect = Tk.StringVar(master)
        self.SensorSelect.set(self.Sensors[0])

        #ChannelSelect controls which channel is selected
        self.ChannelSelect = Tk.IntVar(master)
        self.ChannelSelect.set(0)

        #FreqeuncySelect controls frequency of measurements
        self.FrequencySelect = Tk.IntVar(master)
        self.FrequencySelect.set(10)

        #Sensor_unit displays unit of actively measured value
        self.Sensor_unit = Tk.StringVar(master)
        self.Sensor_unit.set("--")

        #creates SensorReader and DataLogger objects
        self.sr = SensorReader(True, True, False)
        self.dl = DataLogger(False)


        #configures the grid layout
        master.columnconfigure(1, weight=0)
        master.columnconfigure(2, weight=2)
        master.columnconfigure(3, weight=1)
        master.columnconfigure(4, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=0)
        master.rowconfigure(3, weight=0)
        master.rowconfigure(4, weight=0)

        #configures the window properties
        master.resizable(0, 0)
        master.geometry("500x250+300+300")
        master.title("LabPi GUI")


        #GUI elements config
        #labels which display current value and unit
        self.sensor_value = Tk.Label(master, textvariable=self.Sensor_value, font=("Helvetica", 60))
        self.sensor_value.grid(row=1, column=1, columnspan=3)
        self.sensor_unit = Tk.Label(master, textvariable=self.Sensor_unit, font=("Helvetica", 50))
        self.sensor_unit.grid(row=1, column=4, columnspan=3)

        #static labels
        self.Select_label1 = Tk.Label(master, text="Sensor:")
        self.Select_label1.grid(row=2, column=1, sticky="nsew")
        self.Select_label2 = Tk.Label(master, text="Channel:")
        self.Select_label2.grid(row=3, column=1, sticky="nsew")
        self.Select_label3 = Tk.Label(master, text="Frequency:")
        self.Select_label3.grid(row=4, column=1, sticky="nsew")

        #optionmenus for configuring
        self.sensor_Select = Tk.OptionMenu(master, self.SensorSelect, *self.Sensors)
        self.sensor_Select.grid(row=2, column=2, sticky="nsew")
        self.channel_Select = Tk.OptionMenu(master, self.ChannelSelect, 0, 1, 2, 3)
        self.channel_Select.grid(row=3, column=2, sticky="nsew")
        self.frequency_Select = Tk.OptionMenu(master, self.FrequencySelect, 1, 2, 5, 10, 25, 50)
        self.frequency_Select.grid(row=4, column=2, sticky="nsew")

        #control buttons
        self.Start_button = Tk.Button(master, text="Start", command=self.start)
        self.Start_button.grid(row=2, column=3, sticky="nsew")
        self.Stop_button = Tk.Button(master, text="Stop", command=self.stop)
        self.Stop_button.grid(row=3, column=3, sticky="nsew")
        self.Save_button = Tk.Button(master, text="Save", command=self.save)
        self.Save_button.grid(row=2, column=4, sticky="nsew")
        self.Plot_button = Tk.Button(master, text="Plot", command=self.plot)
        self.Plot_button.grid(row=3, column=4, sticky="nsew")


    #refresh function, checks if State=True, then runs measurement again after set interval
    def refresh(self):
        if self.State:
            self.master.after(self.Interval, self.refresh)
            self.updateVar()


    #start function, configures app for measurement, then starts the refresh function
    def start(self):

        #clean previously logged data
        self.dl.eraseData()

        #update measuring frequency
        self.updateFrequency()

        #update unit
        self.updateUnit()

        #write info block into data log
        self.dl.writeInfo(info="sensor:"+str(self.SensorSelect.get())+
                          ", date:"+time.strftime("%Y-%m-%d %H:%M:%S")+
                          ", interval: "+str(self.Interval))

        #disable GUI elements
        self.sensor_Select.configure(state="disabled")
        self.Start_button.configure(state="disabled")
        self.channel_Select.configure(state="disabled")
        self.Save_button.configure(state="disabled")
        self.Plot_button.configure(state="disabled")

        #set state to True and run refresh function
        self.State = True
        self.refresh()


    #save function, saves the logged data via DataLogger function
    def save(self):
        self.dl.saveData(location="measurements/", name=time.strftime("%Y-%m-%d %H:%M:%S"))


    #plot function, plots logged data with pyplot, configure pyplot
    def plot(self):
        plt.plot(self.dl.readData())
        plt.ylabel(self.Sensor_unit.get())
        plt.xlabel("Samples")
        plt.grid(True)
        plt.show()


    #stop function, sets State to False, enables disabled GUI elements
    def stop(self):
        self.State = False
        self.sensor_Select.configure(state="normal")
        self.Start_button.configure(state="normal")
        self.channel_Select.configure(state="normal")
        self.Save_button.configure(state="normal")
        self.Plot_button.configure(state="normal")


    #updateUnit function, updates displayed unit to proper one
    def updateUnit(self):
        if self.SensorSelect.get() == "TMP36":
            self.Sensor_unit.set("C")
        elif self.SensorSelect.get() == "ADXL335 X-axis":
            self.Sensor_unit.set("m/s2")
        elif self.SensorSelect.get() == "ADXL335 Y-axis":
            self.Sensor_unit.set("m/s2")
        elif self.SensorSelect.get() == "ADXL335 Z-axis":
            self.Sensor_unit.set("m/s2")
        elif self.SensorSelect.get() == "BMP180 Temp":
            self.Sensor_unit.set("C")
        elif self.SensorSelect.get() == "BMP180 Pressure":
            self.Sensor_unit.set("Pa")
        elif self.SensorSelect.get() == "TSL2561":
            self.Sensor_unit.set("lux")


    #updateVar function, updates displayed unit to proper one, writes data to data log
    def updateVar(self):
        if self.SensorSelect.get() == "TMP36":
            value = self.sr.readAnalogTemp(self.ChannelSelect.get())
        elif self.SensorSelect.get() == "ADXL335 X-axis":
            value = self.sr.readXAccel(self.ChannelSelect.get())
        elif self.SensorSelect.get() == "ADXL335 Y-axis":
            value = self.sr.readYAccel(self.ChannelSelect.get())
        elif self.SensorSelect.get() == "ADXL335 Z-axis":
            value = self.sr.readZAccel(self.ChannelSelect.get())
        elif self.SensorSelect.get() == "ADXL335 Total":
            value = self.sr.readTotalAccel(0, 1, 2)
        elif self.SensorSelect.get() == "BMP180 Temp":
            value = self.sr.readTemp()
        elif self.SensorSelect.get() == "BMP180 Pressure":
            value = self.sr.readPressure()
        elif self.SensorSelect.get() == "TSL2561":
            value = self.sr.readLux()
        self.Sensor_value.set(str(value))
        self.dl.writeData(value)


    #updateFrequency function, sets interval between measurements to selected value
    def updateFrequency(self):
        if self.FrequencySelect.get() == 1:
            self.Interval = 1000
        elif self.FrequencySelect.get() == 2:
            self.Interval = 500
        elif self.FrequencySelect.get() == 5:
            self.Interval = 200
        elif self.FrequencySelect.get() == 10:
            self.Interval = 100
        elif self.FrequencySelect.get() == 25:
            self.Interval = 40
        elif self.FrequencySelect.get() == 50:
            self.Interval = 20


#run the app
root = Tk.Tk()
app = App(root)
root.mainloop()
