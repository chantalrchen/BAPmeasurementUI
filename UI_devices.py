import tkinter as tk
from tkinter import messagebox, ttk
import propar   # Bronkhorst MFC
import serial   # Cooling and Valve
import time 

###
#MFC
class BronkhorstMFC:
    def __init__(self, port = "COM1", channel = 1):
        self.port = port
        self.connected = False
        self.instrument = None
        self.channel = channel
        self.massflow = 0
        self.targetmassflow = 0
        self.maxmassflow = 4.0
        
    def connect(self):
        try:
            self.instrument = propar.instrument(self.port, channel = self.channel)
            self.connected = True
            return self.connected
        except Exception as err:
            messagebox.showerror("Error",
                f"An error occurred while connecting the Bronkhorst MFC with channel {self.channel}: {err}"
            )
        return False  

    # def disconnect(self):
    #     self.connected = False
    #     self.instrument = None
        
    
    def initialize(self):
        try:
            # controlfunction, the instrument works as a flow controller or a pressure controller; manual flexi-flow
            self.instrument.writeParameter(432, 0)
            
            # sensor type = gas volume; manual flex-bus
            self.instrument.writeParameter(22, 3)
            
            # capacity unit index = 2 (mln/min)
            self.instrument.writeParameter(23, 2)
        except Exception as err:
            messagebox.showerror("Error",
                f"An error occurred while initializing the Bronkhorst MFC with channel {self.channel}: {err}"
            )
        return False  
    
    def get_massflow(self):
        ##the following should be connected when connected with Bronkhorst MFC
        if self.connected and self.instrument is not None:  # device is connected and assigned
            try:
                self.massflow = self.instrument.readParameter(205) #Fmeasure
                return self.massflow  
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while reading the mass flow rate: {err}"
                )
                return False  
        else:
            messagebox.showerror("Error", "The Bronkhorst MFC is not connected.")
            return False  

    def set_massflow(self, value: float):
        ##the following should be connected when connected with Bronkhorst MFC
        if self.connected and self.instrument is not None:  # device is connected and assigned
            try:
                if value < 0:
                    messagebox.showwarning("Mass flow rate can't be negative", f"The mass flow rate can't be negative.")
                    return False             
                elif value > self.maxmassflow:
                    messagebox.showwarning("Value exceeds the maximum mass flow rate", f"The mass flow rate may not exceed {self.maxmassflow:.2f} mL/min. The mass flow rate will be set to {self.maxmassflow:.2f} mL/min.")
                    self.targetmassflow = self.maxmassflow
                    ##the following should be connected when connected with Bronkhorst MFC
                    self.instrument.writeParameter(206, self.targetmassflow)
                    return True
                else:
                    self.targetmassflow = value
                    self.instrument.writeParameter(206, self.targetmassflow) 
                return True  # successful operation
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while setting the mass flow rate: {err}"
                )
                return False  # Operation failed
        else:
            messagebox.showerror("Error", "The Bronkhorst MFC is not connected.")
            return False 

class Koelingsblok:
    def __init__(self, port = 'COM4'):
        self.port = port
        self.connected = False
        self.instrument = None
        self.temperature = 0
        self.targettemperature = 0
        self.dummy = 0
    
    def connect(self):
        
        ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
        # p24: 9600 baud, 1 stop bit, no parity, no hardware handshake, 100ms delay after each command sent (after \r)
        # 100 ms delay, so a timeout of 1s should be enough
        try:
            self.instrument = serial.Serial(self.port, 9600, timeout = 1)
            self.connected = True
            return self.connected
        except Exception as err:
            messagebox.showerror("Error",
                f"An error occurred while connecting the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths: {err}"
            )
        return False  
    
    # def disconnect(self):
    #     self.connected = False
    #     self.instrument = None
        
    def get_temperature(self, dummy):
        ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
        if self.connected and self.instrument is not None: 
            try:
                # sending a request to read the temperature; The current plate temperature will be returned in a text string terminated by <CR><LF>, e.g. 14.3\r
                self.instrument.write(b"p\r")  
                # 100ms delay after each command sent (after \r)
                time.sleep(0.1)  
                self.response = self.instrument.read_until(b"\r").decode().strip()  # reads until \r
                return self.response
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while getting the temperature: {err}"
                )
                return False  # Operation failed
        else:
            return False #Operation failed

    def set_temperature(self, value: float, temp_ambient):

        ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
        if self.connected and self.instrument is not None: 
            try:
                #the cooling system can only lower the temperature by 30 degrees below ambient
                min_temp = temp_ambient - 30
                print(temp_ambient, min_temp)
                if value < min_temp:
                    print("hoi")
                    messagebox.showwarning("Value exceeds the minimum temperature", f"The ambient temperature is {temp_ambient:.2f}. The temperature may not exceed {min_temp:.2f} °C")
                    self.targettemperature = min_temp
                    ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
                    self.instrument.write(b"n" + str(min_temp).encode() + "\r") 
                    
                    #if the above does not work, try: 
                    # self.instrument.write(f"n{value}\r".encode()) 
                    
                    # 100ms delay after each command sent (after \r)
                    time.sleep(0.1) 
                    return True
                else:
                    self.targettemperature = value
                    ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
                    self.instrument.write(b"n" + str(value).encode() + "\r") 
                    
                    #if the above does not work, try: self.instrument.write(f"n{value}\r".encode()) 
                    # 100ms delay after each command sent (after \r)
                    time.sleep(0.1) 
                    return True
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while setting the temperature: {err}"
                )
                return False  # Operation failed
        else:
            messagebox.showerror("Error", "The Torrey Pines IC20XR Digital Chilling/Heating Dry Baths is not connected.")
            return False #Operation failed
