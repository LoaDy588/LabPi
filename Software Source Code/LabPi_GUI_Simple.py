import Tkinter as Tk
from SensorReader import SensorReader
from DataLogger import DataLogger
import time
import matplotlib.pyplot as plt


class App:
    def __init__(self, master):

        self.master = master
        self.Sensors = ["TMP36",
                        "ADXL335 X-axis",
                        "ADXL335 Y-axis",
                        "ADXL335 Z-axis",
                        "BMP180 Temp",
                        "BMP180 Pressure",
                        "TSL2561"]
        self.State = False
        self.Sensor_value = Tk.StringVar(master)
        self.Sensor_value.set("0.0")
        self.SensorSelect = Tk.StringVar(master)
        self.SensorSelect.set(self.Sensors[0])
        self.ChannelSelect = Tk.IntVar(master)
        self.ChannelSelect.set(0)
        self.Sensor_unit = Tk.StringVar(master)
        self.Sensor_unit.set("--")
        self.sr = SensorReader(True, True, False)
        self.dl = DataLogger(False)


        master.columnconfigure(1, weight=0)
        master.columnconfigure(2, weight=2)
        master.columnconfigure(3, weight=1)
        master.columnconfigure(4, weight=1)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=0)
        master.rowconfigure(3, weight=0)
        master.resizable(0, 0)
        master.geometry("500x250+300+300")
        master.title("LabPi GUI")

        self.sensor_value = Tk.Label(master, textvariable=self.Sensor_value, font=("Helvetica", 60))
        self.sensor_value.grid(row=1, column=1, columnspan=3)
        self.sensor_unit = Tk.Label(master, textvariable=self.Sensor_unit, font=("Helvetica", 50))
        self.sensor_unit.grid(row=1, column=4, columnspan=3)
        self.Select_label1 = Tk.Label(master, text="Sensor:")
        self.Select_label1.grid(row=2, column=1, sticky="nsew")
        self.Select_label2 = Tk.Label(master, text="Channel:")
        self.Select_label2.grid(row=3, column=1, sticky="nsew")
        self.sensor_Select = Tk.OptionMenu(master, self.SensorSelect, *self.Sensors)
        self.sensor_Select.grid(row=2, column=2, sticky="nsew")
        self.channel_Select = Tk.OptionMenu(master, self.ChannelSelect, 0, 1, 2, 3)
        self.channel_Select.grid(row=3, column=2, sticky="nsew")
        self.Start_button = Tk.Button(master, text="Start", command=self.start)
        self.Start_button.grid(row=2, column=3, sticky="nsew")
        self.Stop_button = Tk.Button(master, text="Stop", command=self.stop)
        self.Stop_button.grid(row=3, column=3, sticky="nsew")
        self.Save_button = Tk.Button(master, text="Save", command=self.save)
        self.Save_button.grid(row=2, column=4, sticky="nsew")
        self.Plot_button = Tk.Button(master, text="Plot", command=self.plot)
        self.Plot_button.grid(row=3, column=4, sticky="nsew")


    def refresh(self):
        if self.State:
            self.master.after(100, self.refresh)
            self.updateVar()


    def start(self):
        self.dl.eraseData()
        self.dl.writeInfo(info="sensor:"+str(self.SensorSelect.get())+
                          ", date:"+time.strftime("%Y-%m-%d %H:%M:%S"))
        self.updateUnit()
        self.sensor_Select.configure(state="disabled")
        self.Start_button.configure(state="disabled")
        self.channel_Select.configure(state="disabled")
        self.Save_button.configure(state="disabled")
        self.Plot_button.configure(state="disabled")
        self.State = True
        self.refresh()


    def save(self):
        self.dl.saveData(location="measurements/", name=time.strftime("%Y-%m-%d %H:%M:%S"))

    def plot(self):
        plt.plot(self.dl.readData())
        plt.ylabel(self.Sensor_unit.get())
        plt.xlabel("Time")
        plt.grid(True)
        plt.show()


    def stop(self):
        self.State = False
        self.sensor_Select.configure(state="normal")
        self.Start_button.configure(state="normal")
        self.channel_Select.configure(state="normal")
        self.Save_button.configure(state="normal")
        self.Plot_button.configure(state="normal")


    def updateUnit(self):
        if self.SensorSelect.get()=="TMP36":
            self.Sensor_unit.set("C")
        elif self.SensorSelect.get()=="ADXL335 X-axis":
            self.Sensor_unit.set("m/s2")
        elif self.SensorSelect.get()=="ADXL335 Y-axis":
            self.Sensor_unit.set("m/s2")
        elif self.SensorSelect.get()=="ADXL335 Z-axis":
            self.Sensor_unit.set("m/s2")
        elif self.SensorSelect.get()=="BMP180 Temp":
            self.Sensor_unit.set("C")
        elif self.SensorSelect.get()=="BMP180 Pressure":
            self.Sensor_unit.set("Pa")
        elif self.SensorSelect.get()=="TSL2561":
            self.Sensor_unit.set("lux")


    def updateVar(self):
        if self.SensorSelect.get()=="TMP36":
            value = self.sr.readAnalogTemp(self.ChannelSelect.get())
        elif self.SensorSelect.get()=="ADXL335 X-axis":
            value = self.sr.readXAccel(self.ChannelSelect.get())
        elif self.SensorSelect.get()=="ADXL335 Y-axis":
            value = self.sr.readYAccel(self.ChannelSelect.get())
        elif self.SensorSelect.get()=="ADXL335 Z-axis":
            value = self.sr.readZAccel(self.ChannelSelect.get())
        elif self.SensorSelect.get()=="BMP180 Temp":
            value = self.sr.readTemp()
        elif self.SensorSelect.get()=="BMP180 Pressure":
            value = self.sr.readPressure()
        elif self.SensorSelect.get()=="TSL2561":
            value = self.sr.readLux()
        self.Sensor_value.set(str(value))
        self.dl.writeData(value)


root = Tk.Tk()
app = App(root)
root.mainloop()
