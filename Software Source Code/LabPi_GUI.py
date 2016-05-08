import Tkinter as Tk                    # import Tkinter for GUI
from SensorReader import SensorReader   # import SensorReader for reading data
from DataLogger import DataLogger       # import DataLogger for working with data
import time                             # import time
import matplotlib.pyplot as plt         # import pyplot for data vis


# single measurement mode class
class SingleMode:
    # init function, sets up global variables and objects, builds the GUI
    def __init__(self, master):

        # global variables
        self.master = master

        # available sensors list
        self.Sensors = ["----",
                        "TMP36",
                        "LMT86",
                        "ADXL335 X-axis",
                        "ADXL335 Y-axis",
                        "ADXL335 Z-axis",
                        "ADXL335 Total",
                        "BMP180 Temp",
                        "BMP180 Pressure",
                        "TSL2561"]

        # State controls if the software actively measures
        self.State = False

        # Interval controls the interval between measurements
        self.Interval = 100

        # Sensor_values displays actual measured values
        self.Sensor_value1 = Tk.StringVar(master)
        self.Sensor_value1.set("0.0")

        # SensorSelects controls which sensor are selected
        self.SensorSelect1 = Tk.StringVar(master)
        self.SensorSelect1.set(self.Sensors[0])

        # ChannelSelects controls which channels are selected
        self.ChannelSelect1 = Tk.IntVar(master)
        self.ChannelSelect1.set(0)

        # FreqeuncySelect controls frequency of measurements
        self.FrequencySelect = Tk.IntVar(master)
        self.FrequencySelect.set(10)

        # Sensor_units displays units of actively measured values
        self.Sensor_unit1 = Tk.StringVar(master)
        self.Sensor_unit1.set("--")

        # creates SensorReader and DataLogger objects
        self.sr = SensorReader(True, True, False)
        self.DL1 = DataLogger(False)


        # configures the grid layout
        master.columnconfigure(1, weight=0)
        master.columnconfigure(2, weight=2)
        master.columnconfigure(3, weight=1)
        master.columnconfigure(4, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=0)
        master.rowconfigure(3, weight=0)
        master.rowconfigure(4, weight=0)

        # configures the window properties
        master.resizable(0, 0)
        master.geometry("500x250+300+300")
        master.title("LabPi SINGLE MODE")


        # GUI elements config
        # labels which display current value and unit
        self.sensor_value1 = Tk.Label(master, textvariable=self.Sensor_value1, font=("Helvetica", 60))
        self.sensor_value1.grid(row=1, column=1, columnspan=3)
        self.sensor_unit1 = Tk.Label(master, textvariable=self.Sensor_unit1, font=("Helvetica", 50))
        self.sensor_unit1.grid(row=1, column=4, columnspan=3)

        # static labels
        self.Select_label1 = Tk.Label(master, text="Sensor 1:")
        self.Select_label1.grid(row=2, column=1, sticky="nsew")
        self.Select_label2 = Tk.Label(master, text="Channel 1:")
        self.Select_label2.grid(row=3, column=1, sticky="nsew")
        self.Select_label3 = Tk.Label(master, text="Frequency:")
        self.Select_label3.grid(row=4, column=1, sticky="nsew")

        # optionmenus for configuring
        self.sensor_Select1 = Tk.OptionMenu(master, self.SensorSelect1, *self.Sensors)
        self.sensor_Select1.grid(row=2, column=2, sticky="nsew")
        self.channel_Select1 = Tk.OptionMenu(master, self.ChannelSelect1, 0, 1, 2, 3)
        self.channel_Select1.grid(row=3, column=2, sticky="nsew")
        self.frequency_Select = Tk.OptionMenu(master, self.FrequencySelect, 1, 2, 5, 10, 25, 50)
        self.frequency_Select.grid(row=4, column=2, sticky="nsew")

        # control buttons
        self.Start_button = Tk.Button(master, text="Start", command=self.start)
        self.Start_button.grid(row=2, column=3, sticky="nsew")
        self.Stop_button = Tk.Button(master, text="Stop", command=self.stop)
        self.Stop_button.grid(row=3, column=3, sticky="nsew")
        self.Save_button = Tk.Button(master, text="Save", command=self.save)
        self.Save_button.grid(row=2, column=4, sticky="nsew")
        self.Plot_button = Tk.Button(master, text="Plot", command=self.plot)
        self.Plot_button.grid(row=3, column=4, sticky="nsew")

    # refresh function, checks if State=True, then runs measurement again after set interval
    def refresh(self):
        if self.State:
            self.master.after(self.Interval, self.refresh)
            self.updateVar1()

    # start function, configures app for measurement, then starts the refresh function
    def start(self):

        # clean previously logged data
        self.DL1.eraseData()

        # update measuring frequency
        self.updateFrequency()

        # update unit
        self.updateUnit1()

        # write info block into data log
        self.DL1.writeInfo(info="sensor:" + str(self.SensorSelect1.get()) +
                               ", date:" + time.strftime("%Y-%m-%d %H:%M:%S") +
                               ", interval: " + str(self.Interval))

        # disable GUI elements
        self.sensor_Select1.configure(state="disabled")
        self.Start_button.configure(state="disabled")
        self.channel_Select1.configure(state="disabled")
        self.frequency_Select.configure(state="disabled")
        self.Save_button.configure(state="disabled")
        self.Plot_button.configure(state="disabled")

        # set state to True and run refresh function
        self.State = True
        self.refresh()

    # save function, saves the logged data via DataLogger function
    def save(self):
        self.DL1.saveData(location="measurements/", name=("Sensor1"+time.strftime("%Y-%m-%d-%H%M%S")))

    # plot function, plots logged data with pyplot, configure pyplot
    def plot(self):
        plt.plot(self.DL1.readData())
        plt.ylabel(self.Sensor_unit1.get())
        plt.xlabel("Samples")
        plt.grid(True)
        plt.show()

    # stop function, sets State to False, enables disabled GUI elements
    def stop(self):
        self.State = False
        self.sensor_Select1.configure(state="normal")
        self.Start_button.configure(state="normal")
        self.channel_Select1.configure(state="normal")
        self.frequency_Select.configure(state="normal")
        self.Save_button.configure(state="normal")
        self.Plot_button.configure(state="normal")

    # updateUnit function, updates displayed unit to proper one
    def updateUnit1(self):
        if self.SensorSelect1.get() == "----":
            self.Sensor_unit1.set("--")
        elif self.SensorSelect1.get() == "TMP36":
            self.Sensor_unit1.set("C")
        elif self.SensorSelect1.get() == "LMT86":
            self.Sensor_unit1.set("C")
        elif self.SensorSelect1.get() == "ADXL335 X-axis":
            self.Sensor_unit1.set("m/s2")
        elif self.SensorSelect1.get() == "ADXL335 Y-axis":
            self.Sensor_unit1.set("m/s2")
        elif self.SensorSelect1.get() == "ADXL335 Z-axis":
            self.Sensor_unit1.set("m/s2")
        elif self.SensorSelect1.get() == "ADXL335 Total":
            self.Sensor_unit1.set("m/s2")
        elif self.SensorSelect1.get() == "BMP180 Temp":
            self.Sensor_unit1.set("C")
        elif self.SensorSelect1.get() == "BMP180 Pressure":
            self.Sensor_unit1.set("Pa")
        elif self.SensorSelect1.get() == "TSL2561":
            self.Sensor_unit1.set("lux")

    # updateVar function, updates displayed unit to proper one, writes data to data log
    def updateVar1(self):
        if self.SensorSelect1.get() == "TMP36":
            value = self.sr.readTMP36(self.ChannelSelect1.get())
        elif self.SensorSelect1.get() == "LMT86":
            value = self.sr.readLMT86(self.ChannelSelect1.get())
        elif self.SensorSelect1.get() == "ADXL335 X-axis":
            value = self.sr.readADXL335XAccel(self.ChannelSelect1.get())
        elif self.SensorSelect1.get() == "ADXL335 Y-axis":
            value = self.sr.readADXL335YAccel(self.ChannelSelect1.get())
        elif self.SensorSelect1.get() == "ADXL335 Z-axis":
            value = self.sr.readADXL335ZAccel(self.ChannelSelect1.get())
        elif self.SensorSelect1.get() == "ADXL335 Total":
            value = self.sr.readADXL335TotalAccel(0, 1, 2)
        elif self.SensorSelect1.get() == "BMP180 Temp":
            value = self.sr.readBMP085Temp()
        elif self.SensorSelect1.get() == "BMP180 Pressure":
            value = self.sr.readBMP085Pressure()
        elif self.SensorSelect1.get() == "TSL2561":
            value = self.sr.readTSL2561Lux()
        else:
            value = 0
        self.Sensor_value1.set(str(value))
        self.DL1.writeData(value)

    # updateFrequency function, sets interval between measurements to selected value
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


# dual measurement mode class
class DualMode:
    # init function, sets up global variables and objects, builds the GUI
    def __init__(self, master):

        # global variables
        self.master = master

        # available sensors list
        self.Sensors = ["----",
                        "TMP36",
                        "LMT86",
                        "ADXL335 X-axis",
                        "ADXL335 Y-axis",
                        "ADXL335 Z-axis",
                        "ADXL335 Total",
                        "BMP180 Temp",
                        "BMP180 Pressure",
                        "TSL2561"]

        # State controls if the software actively measures
        self.State = False

        # Interval controls the interval between measurements
        self.Interval = 100

        # Sensor_values displays actual measured values
        self.Sensor_value1 = Tk.StringVar(master)
        self.Sensor_value1.set("0.0")

        self.Sensor_value2 = Tk.StringVar(master)
        self.Sensor_value2.set("0.0")

        # SensorSelects controls which sensor are selected
        self.SensorSelect1 = Tk.StringVar(master)
        self.SensorSelect1.set(self.Sensors[0])

        self.SensorSelect2 = Tk.StringVar(master)
        self.SensorSelect2.set(self.Sensors[0])

        # ChannelSelects controls which channels are selected
        self.ChannelSelect1 = Tk.IntVar(master)
        self.ChannelSelect1.set(0)

        self.ChannelSelect2 = Tk.IntVar(master)
        self.ChannelSelect2.set(0)

        # FreqeuncySelect controls frequency of measurements
        self.FrequencySelect = Tk.IntVar(master)
        self.FrequencySelect.set(10)

        # Sensor_units displays units of actively measured values
        self.Sensor_unit1 = Tk.StringVar(master)
        self.Sensor_unit1.set("--")

        self.Sensor_unit2 = Tk.StringVar(master)
        self.Sensor_unit2.set("--")

        # creates SensorReader and DataLogger objects
        self.sr = SensorReader(True, True, False)
        self.DL1 = DataLogger(False)
        self.DL2 = DataLogger(False)


        # configures the grid layout
        master.columnconfigure(1, weight=0)
        master.columnconfigure(2, weight=2)
        master.columnconfigure(3, weight=1)
        master.columnconfigure(4, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=1)
        master.rowconfigure(3, weight=0)
        master.rowconfigure(4, weight=0)
        master.rowconfigure(5, weight=0)
        master.rowconfigure(6, weight=0)
        master.rowconfigure(7, weight=0)

        # configures the window properties
        master.resizable(0, 0)
        master.geometry("500x500+300+300")
        master.title("LabPi DUAL MODE")


        # GUI elements config
        # labels which display current value and unit
        self.sensor_value1 = Tk.Label(master, textvariable=self.Sensor_value1, font=("Helvetica", 60))
        self.sensor_value1.grid(row=1, column=1, columnspan=3)
        self.sensor_unit1 = Tk.Label(master, textvariable=self.Sensor_unit1, font=("Helvetica", 50))
        self.sensor_unit1.grid(row=1, column=4, columnspan=3)
        self.sensor_value2 = Tk.Label(master, textvariable=self.Sensor_value2, font=("Helvetica", 60))
        self.sensor_value2.grid(row=2, column=1, columnspan=3)
        self.sensor_unit2 = Tk.Label(master, textvariable=self.Sensor_unit2, font=("Helvetica", 50))
        self.sensor_unit2.grid(row=2, column=4, columnspan=3)

        # static labels
        self.Select_label1 = Tk.Label(master, text="Sensor 1:")
        self.Select_label1.grid(row=3, column=1, sticky="nsew")
        self.Select_label2 = Tk.Label(master, text="Channel 1:")
        self.Select_label2.grid(row=4, column=1, sticky="nsew")
        self.Select_label3 = Tk.Label(master, text="Sensor 2:")
        self.Select_label3.grid(row=5, column=1, sticky="nsew")
        self.Select_label4 = Tk.Label(master, text="Channel 2:")
        self.Select_label4.grid(row=6, column=1, sticky="nsew")
        self.Select_label5 = Tk.Label(master, text="Frequency:")
        self.Select_label5.grid(row=7, column=1, sticky="nsew")

        # optionmenus for configuring
        self.sensor_Select1 = Tk.OptionMenu(master, self.SensorSelect1, *self.Sensors)
        self.sensor_Select1.grid(row=3, column=2, sticky="nsew")
        self.channel_Select1 = Tk.OptionMenu(master, self.ChannelSelect1, 0, 1, 2, 3)
        self.channel_Select1.grid(row=4, column=2, sticky="nsew")
        self.sensor_Select2 = Tk.OptionMenu(master, self.SensorSelect2, *self.Sensors)
        self.sensor_Select2.grid(row=5, column=2, sticky="nsew")
        self.channel_Select2 = Tk.OptionMenu(master, self.ChannelSelect2, 0, 1, 2, 3)
        self.channel_Select2.grid(row=6, column=2, sticky="nsew")
        self.frequency_Select = Tk.OptionMenu(master, self.FrequencySelect, 1, 2, 5, 10, 25, 50)
        self.frequency_Select.grid(row=7, column=2, sticky="nsew")

        # control buttons
        self.Start_button = Tk.Button(master, text="Start", command=self.start)
        self.Start_button.grid(row=3, column=3, rowspan=2, sticky="nsew")
        self.Stop_button = Tk.Button(master, text="Stop", command=self.stop)
        self.Stop_button.grid(row=5, column=3, rowspan=2, sticky="nsew")
        self.Save_button = Tk.Button(master, text="Save", command=self.save)
        self.Save_button.grid(row=3, column=4, rowspan=2, sticky="nsew")
        self.Plot_button = Tk.Button(master, text="Plot", command=self.plot)
        self.Plot_button.grid(row=5, column=4, rowspan=2, sticky="nsew")

    # refresh function, checks if State=True, then runs measurement again after set interval
    def refresh(self):
        if self.State:
            self.master.after(self.Interval, self.refresh)
            self.updateVar1()
            self.updateVar2()

    # start function, configures app for measurement, then starts the refresh function
    def start(self):

        # clean previously logged data
        self.DL1.eraseData()
        self.DL2.eraseData()

        # update measuring frequency
        self.updateFrequency()

        # update unit
        self.updateUnit1()
        self.updateUnit2()

        # write info block into data log
        self.DL1.writeInfo(info="sensor:" + str(self.SensorSelect1.get()) +
                               ", date:" + time.strftime("%Y-%m-%d %H:%M:%S") +
                               ", interval: " + str(self.Interval))
        self.DL2.writeInfo(info="sensor:" + str(self.SensorSelect2.get()) +
                               ", date:" + time.strftime("%Y-%m-%d %H:%M:%S") +
                               ", interval: " + str(self.Interval))

        # disable GUI elements
        self.sensor_Select1.configure(state="disabled")
        self.sensor_Select2.configure(state="disabled")
        self.Start_button.configure(state="disabled")
        self.channel_Select1.configure(state="disabled")
        self.channel_Select2.configure(state="disabled")
        self.frequency_Select.configure(state="disabled")
        self.Save_button.configure(state="disabled")
        self.Plot_button.configure(state="disabled")

        # set state to True and run refresh function
        self.State = True
        self.refresh()

    # save function, saves the logged data via DataLogger function
    def save(self):
        self.DL1.saveData(location="measurements/", name=("Sensor1"+time.strftime("%Y-%m-%d-%H%M%S")))
        self.DL2.saveData(location="measurements/", name=("Sensor2"+time.strftime("%Y-%m-%d-%H%M%S")))

    # plot function, plots logged data with pyplot, configure pyplot
    def plot(self):
        plt.subplot(2, 1, 1)
        plt.plot(self.DL1.readData())
        plt.ylabel(self.Sensor_unit1.get())
        plt.grid(True)
        plt.subplot(2, 1, 2)
        plt.plot(self.DL2.readData())
        plt.ylabel(self.Sensor_unit2.get())
        plt.xlabel("Samples")
        plt.grid(True)
        plt.show()

    # stop function, sets State to False, enables disabled GUI elements
    def stop(self):
        self.State = False
        self.sensor_Select1.configure(state="normal")
        self.sensor_Select2.configure(state="normal")
        self.Start_button.configure(state="normal")
        self.channel_Select1.configure(state="normal")
        self.channel_Select2.configure(state="normal")
        self.frequency_Select.configure(state="normal")
        self.Save_button.configure(state="normal")
        self.Plot_button.configure(state="normal")

    # updateUnit function, updates displayed unit to proper one
    def updateUnit1(self):
        if self.SensorSelect1.get() == "----":
            self.Sensor_unit1.set("--")
        elif self.SensorSelect1.get() == "TMP36":
            self.Sensor_unit1.set("C")
        elif self.SensorSelect1.get() == "LMT86":
            self.Sensor_unit1.set("C")
        elif self.SensorSelect1.get() == "ADXL335 X-axis":
            self.Sensor_unit1.set("m/s2")
        elif self.SensorSelect1.get() == "ADXL335 Y-axis":
            self.Sensor_unit1.set("m/s2")
        elif self.SensorSelect1.get() == "ADXL335 Z-axis":
            self.Sensor_unit1.set("m/s2")
        elif self.SensorSelect1.get() == "ADXL335 Total":
            self.Sensor_unit1.set("m/s2")
        elif self.SensorSelect1.get() == "BMP180 Temp":
            self.Sensor_unit1.set("C")
        elif self.SensorSelect1.get() == "BMP180 Pressure":
            self.Sensor_unit1.set("Pa")
        elif self.SensorSelect1.get() == "TSL2561":
            self.Sensor_unit1.set("lux")

    def updateUnit2(self):
        if self.SensorSelect2.get() == "----":
            self.Sensor_unit2.set("--")
        elif self.SensorSelect2.get() == "TMP36":
            self.Sensor_unit2.set("C")
        elif self.SensorSelect2.get() == "LMT86":
            self.Sensor_unit2.set("C")
        elif self.SensorSelect2.get() == "ADXL335 X-axis":
            self.Sensor_unit2.set("m/s2")
        elif self.SensorSelect2.get() == "ADXL335 Y-axis":
            self.Sensor_unit2.set("m/s2")
        elif self.SensorSelect2.get() == "ADXL335 Z-axis":
            self.Sensor_unit2.set("m/s2")
        elif self.SensorSelect2.get() == "ADXL335 Total":
            self.Sensor_unit2.set("m/s2")
        elif self.SensorSelect2.get() == "BMP180 Temp":
            self.Sensor_unit2.set("C")
        elif self.SensorSelect2.get() == "BMP180 Pressure":
            self.Sensor_unit2.set("Pa")
        elif self.SensorSelect2.get() == "TSL2561":
            self.Sensor_unit2.set("lux")

    # updateVar function, updates displayed unit to proper one, writes data to data log
    def updateVar1(self):
        if self.SensorSelect1.get() == "TMP36":
            value = self.sr.readTMP36(self.ChannelSelect1.get())
        elif self.SensorSelect1.get() == "LMT86":
            value = self.sr.readLMT86(self.ChannelSelect1.get())
        elif self.SensorSelect1.get() == "ADXL335 X-axis":
            value = self.sr.readADXL335XAccel(self.ChannelSelect1.get())
        elif self.SensorSelect1.get() == "ADXL335 Y-axis":
            value = self.sr.readADXL335YAccel(self.ChannelSelect1.get())
        elif self.SensorSelect1.get() == "ADXL335 Z-axis":
            value = self.sr.readADXL335ZAccel(self.ChannelSelect1.get())
        elif self.SensorSelect1.get() == "ADXL335 Total":
            value = self.sr.readADXL335TotalAccel(0, 1, 2)
        elif self.SensorSelect1.get() == "BMP180 Temp":
            value = self.sr.readBMP085Temp()
        elif self.SensorSelect1.get() == "BMP180 Pressure":
            value = self.sr.readBMP085Pressure()
        elif self.SensorSelect1.get() == "TSL2561":
            value = self.sr.readTSL2561Lux()
        else:
            value = 0
        self.Sensor_value1.set(str(value))
        self.DL1.writeData(value)

    def updateVar2(self):
        if self.SensorSelect2.get() == "TMP36":
            value = self.sr.readTMP36(self.ChannelSelect2.get())
        elif self.SensorSelect2.get() == "LMT86":
            value = self.sr.readLMT86(self.ChannelSelect2.get())
        elif self.SensorSelect2.get() == "ADXL335 X-axis":
            value = self.sr.readADXL335XAccel(self.ChannelSelect2.get())
        elif self.SensorSelect2.get() == "ADXL335 Y-axis":
            value = self.sr.readADXL335YAccel(self.ChannelSelect2.get())
        elif self.SensorSelect2.get() == "ADXL335 Z-axis":
            value = self.sr.readADXL335ZAccel(self.ChannelSelect2.get())
        elif self.SensorSelect2.get() == "ADXL335 Total":
            value = self.sr.readADXL335TotalAccel(0, 1, 2)
        elif self.SensorSelect2.get() == "BMP180 Temp":
            value = self.sr.readBMP085Temp()
        elif self.SensorSelect2.get() == "BMP180 Pressure":
            value = self.sr.readBMP085Pressure()
        elif self.SensorSelect2.get() == "TSL2561":
            value = self.sr.readTSL2561Lux()
        else:
            value = 0
        self.Sensor_value2.set(str(value))
        self.DL2.writeData(value)

    # updateFrequency function, sets interval between measurements to selected value
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


# default launch app class, launches either single or dual mode
class App:

    # init function
    def __init__(self, master):
        self.master = master

        # setting up window properties
        master.resizable(0, 0)
        master.geometry("+300+300")
        master.title("LabPi GUI")

        # building the GUI - simple frame with two buttons
        self.frame = Tk.Frame(self.master)
        self.button1 = Tk.Button(self.frame, text='Single Mode', width=25,font=("Helvetica", 18),
                                 command = self.single_mode)
        self.button1.pack()
        self.button2 = Tk.Button(self.frame, text='Dual Mode', width=25,font=("Helvetica", 18),
                                 command = self.dual_mode)
        self.button2.pack()
        self.frame.pack()

    # single mode launch function
    def single_mode(self):

        # launch app in TopLevel window
        self.newWindow = Tk.Toplevel(self.master)
        self.app = SingleMode(self.newWindow)

    # dual mode launch function
    def dual_mode(self):

        # launch app in TopLevel window
        self.newWindow = Tk.Toplevel(self.master)
        self.app = DualMode(self.newWindow)

# run the app
root = Tk.Tk()
app = App(root)
root.mainloop()
