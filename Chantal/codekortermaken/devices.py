import tkinter as tk
from tkinter import messagebox, ttk
import propar   # Bronkhorst MFC
import serial   # Cooling and Valve
import time 

#MFC
class BronkhorstMFC:
    def __init__(self, port = "COM3"):
        self.port = port
        self.connected = False
        self.instrument = None
        # self.channel = channel
        self.massflow = 0
        self.targetmassflow = 0
        self.maxmassflow = 4.0
        
    def connect(self):
        # try:
        #     self.instrument = propar.instrument(self.port) # channel = self.channel)
        #     print("I am in the MFC connecting function. My port is ", self.port)
            
        #     ##toegevoegd om te checken whether it is really connected
        #     if self.get_massflow() is not False:
        #         self.connected = True
        #         self.initialize()
        #         return self.connected
        # except Exception as err:
        #     messagebox.showerror("Error",
        #         f"An error occurred while connecting the Bronkhorst MFC with port {self.port}: {err}"
        #     )
        # return False  


        ##FOR SIMULATION
        self.connected = True
        return self.connected
    
    # reset the value, fsetpoint = 0 
    def disconnect(self):
        # try:
        #     param = [{'proc_nr':33 , 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT, 'data': 0}]
        #     self.instrument.write_parameters(param) #Fsetpoint
            
        # except Exception as err:
        #     messagebox.showerror("Error",
        #      f"An error occurred while disconnecting the Bronkhorst MFC: {err}")
     
        self.connected = False
        self.instrument = None
        
    
    def initialize(self):
        # try:
        #     # controlfunction, the instrument works as a flow controller or a pressure controller; manual flexi-flow
        #     param = [{'proc_nr':115 , 'parm_nr': 10, 'parm_type': propar.PP_TYPE_INT8, 'data': 0}]
        #     print("HI I AM IN MFC INITIALIZE FUNCTION MY CONNECTION IS", self.connected )
        #     self.instrument.write_parameters(param)


        # except Exception as err:
        #     messagebox.showerror("Error",
        #         f"An error occurred while initializing the Bronkhorst MFC with channel"# {self.channel}: {err}"
        #     )
        # return False  
    
        #FOR SIMULATION
        return True
  
    def get_massflow(self):
        ##the following should be connected when connected with Bronkhorst MFC
        # if self.connected and self.instrument is not None:  # device is connected and assigned
        #     try:
        #         param = [{'proc_nr':  33, 'parm_nr': 0, 'parm_type': propar.PP_TYPE_FLOAT}] #Fmeasure
        #         self.massflow = self.instrument.read_parameters(param)
        #         return self.massflow  
        #     except Exception as err:
        #         messagebox.showerror("Error",
        #             f"An error occurred while reading the mass flow rate: {err}"
        #         )
        #         return False  
        # else:
        #     messagebox.showerror("Error", "The Bronkhorst MFC is not connected.")
        #     return False  

        #FOR SIMULATION
        if self.connected:
            try:
                self.massflow += (self.targetmassflow - self.massflow) * 0.1
                if abs(self.massflow - self.targetmassflow) < 0.001:
                    self.massflow = self.targetmassflow
                return self.massflow
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while reading the mass flow rate: {err}"
                )
                return False
        else:
            messagebox.showerror("Error","The Bronkhorst MFC is not connected.")
            return False 

    def set_massflow(self, value: float):
        # ##the following should be connected when connected with Bronkhorst MFC
        # if self.connected and self.instrument is not None:  # device is connected and assigned
        if self.connected:
            try:
                # print("HI I AM IN THE SET_MASSFLOW LOOP AND SELF.CONNECTED IS", self.connected)
                # print(value, self.targetmassflow, self.maxmassflow)
                if value < 0:
                    messagebox.showwarning("Mass flow rate can't be negative", f"The mass flow rate can't be negative.")
                    return False             
                elif value > self.maxmassflow:
                    messagebox.showwarning("Value exceeds the maximum mass flow rate", f"The mass flow rate may not exceed {self.maxmassflow:.2f} mL/min. The mass flow rate will be set to {self.maxmassflow:.2f} mL/min.")
                    self.targetmassflow = self.maxmassflow
                    
                    # ####
                    # ##the following should be connected when connected with Bronkhorst MFC
                    # param = [{'proc_nr':33 , 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT, 'data': self.maxmassflow}]
                    # self.instrument.write_parameters(param)
                    # print("HI IM NOW SETTING A MASSFLOW TO ", self.maxmassflow)
                    # ###
                    
                    return True
                else:
                    self.targetmassflow = value
                    
                    #####
                    ###the following should be connected when connected with Bronkhorst MFC
                    # param1 = [{'proc_nr':33 , 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT, 'data': value}]
                    # self.instrument.write_parameters(param1) #Fsetpoint
                    # print("HI IM NOW SETTING A MASSFLOW TO ", value)
                    ####
                    
                    return True  
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while setting the mass flow rate: {err}"
                )
                return False  
        else:
            messagebox.showerror("Error", "The Bronkhorst MFCs is not connected.")
            return False  
        ##

class Koelingsblok:
    def __init__(self, port = 'COM4'):
        self.port = port
        self.connected = False
        self.instrument = None
        self.temperature = 0
        self.targettemperature = 0
        self.dummy = 0
    
    def connect(self):
        
        # ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
        # # p24: 9600 baud, 1 stop bit, no parity, no hardware handshake, 100ms delay after each command sent (after \r)
        # # 100 ms delay, so a timeout of 1s should be enough
        # try:
        #     self.instrument = serial.Serial(self.port, 9600, timeout = 1)
        #     print("I am in the cooling connecting function. My port is ", self.port)
        #     self.connected = True
        #     return self.connected
        # except Exception as err:
        #     messagebox.showerror("Error",
        #         f"An error occurred while connecting the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths: {err}"
        #     )
        # return False  # Operation failed
        # ##
        
        #the following is used only for simulation
        self.connected = True
        return self.connected
        ##
    
    # reset the MFC value, flow rate to 0
    def disconnect(self):
        # param = [{'proc_nr':33 , 'parm_nr': 3, 'parm_type': propar.PP_TYPE_FLOAT, 'data': 0}]
        # self.instrument.write_parameters(param) #Fsetpoint

        self.connected = False
        self.instrument = None
        
    def get_temperature(self):
    
        # # ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
        # if self.connected and self.instrument is not None: 
        #     try:
        #         # sending a request to read the temperature; The current plate temperature will be returned in a text string terminated by <CR><LF>, e.g. 14.3\r
        #         self.instrument.write(b"p\r")  
        #         # 100ms delay after each command sent (after \r)
        #         time.sleep(0.1)  
        #         self.response = self.instrument.read_until(b"\r").decode().strip()  # reads until \r
        #         return self.response
        #     except Exception as err:
        #         messagebox.showerror("Error",
        #             f"An error occurred while getting the temperature: {err}"
        #         )
        #         return False  # Operation failed
        # else:
        #     return False #Operation failed
        # # ##
        
            ##the following is used only for simulation
            # if dummy == 0:
            #     return self.temperature
            # elif dummy == 1:                
        if self.connected:
            try:
                self.temperature += (self.targettemperature - self.temperature) * 0.1
                if abs(self.temperature - self.targettemperature) < 0.001:
                    self.temperature = self.targettemperature
                return self.temperature
            except Exception as err:
                messagebox.showerror("Error",
                    f"An error occurred while reading the temperature: {err}"
                )
                return False
        else:
            messagebox.showerror("Error","The Torrey Pines IC20XR Digital Chilling/Heating Dry Baths is not connected.")
            return False  # Operation failed
        ##

    def set_temperature(self, value: float, temp_ambient):

        ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
        # if self.connected and self.instrument is not None: 
        if self.connected:
            try:
                #the cooling system can only lower the temperature by 30 degrees below ambient
                min_temp = temp_ambient - 30
                if value < min_temp:
                    messagebox.showwarning("Value exceeds the minimum temperature", f"The ambient temperature is {temp_ambient:.2f}. The temperature may not exceed {min_temp:.2f} °C")
                    self.targettemperature = min_temp
                    
                    ###OFFICIAL
                    ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
                    # self.instrument.write(b"n" + str(min_temp).encode() + "\r") 
                    
                    #if the above does not work, try: 
                    # self.instrument.write(f"n{value}\r".encode()) 
                    # 100ms delay after each command sent (after \r)
                    time.sleep(0.1) 
                    return True
                else:
                    self.targettemperature = value
                    
                    ##OFFICIAL
                    ##the following should be connected when connected with the Torrey Pines IC20XR Digital Chilling/Heating Dry Baths
                    # self.instrument.write(b"n" + str(value).encode() + "\r") 
                    
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
            messagebox.showerror("Error", " The Torrey Pines IC20XR Digital Chilling/Heating Dry Baths is not connected.")
            return False #Operation failed

class RVM:
    def __init__(self, port = 'COM4'):
        self.port = port
        self.connected = False
        self.instrument = None
        self.currentposition = 1 #home status
        self.rotation_delay = 0.4  #the rotation time for 180 degree for RVMLP (1.5 s) and RVMFS (400 ms / 0.4s),

    def connect(self):
        # #Following should be 
        # try:
        #     product_list = amfTools.util.getProductList() # get the list of AMF products connected to the computer

        #     product : amfTools.Device = None
        #     self.instrument : amfTools.AMF = None
        #     for product in product_list:
        #         if "RVM" in product.deviceType:
        #             self.instrument = amfTools.AMF(product)
        #             break

        #     if self.instrument is None:
        #     # Try forced port connection if no RVM detected
        #        self.instrument = amfTools.AMF(self.port)


        #     self.instrument.connect() 
        #     self.connected = True
        #     print("connection",self.connected)
        #     self.initialize_valve()
        #     return True
    
        # except Exception as err:
        #     messagebox.showerror("Error",
        #             f"An error occurred while connecting RVM Industrial Microfluidic Rotary Valve: {err}")
        #     self.connected = False
        #     return False
        
       #SIMULATION the following is used only for simulation
        self.connected = True
        return self.connected
        #

    def disconnect(self):
        # if self.connected and self.instrument:
        #     try:
        #         self.instrument.disconnect()
        #         print("RVM disconnected.")
        #     except Exception as err: 
        #         messagebox.showerror("Error",
        #             f"An error occurred while disconnecting RVM Industrial Microfluidic Rotary Valve: {err}")
        self.connected = False

    #home status 
    def initialize_valve(self): 
        # if not self.connected:
        #     raise ConnectionError("RVM Industrial Microfluidic Rotary Valve is not connected.")
        
        # # Check if the product is homed (if not, home it)
        # try:
        #     if not self.instrument.getHomeStatus(): 
        #         self.instrument.home()
        #         time.sleep(self.rotation_delay)  # Give time for homing

        #     else:
        #         print("RVM Industrial Microfluidic Rotary Valve is already homed.")

        #     # Always move to position 1 after homing (default start position)
        #     self.instrument.valveShortestPath(1)
        #     time.sleep(self.rotation_delay) #give time for rotation
        #     self.currentposition = 1
        #     print("RVM Industrial Microfluidic Rotary Valve moved to position 1/ON State.")

        # except Exception as err:
        #     messagebox.showerror("Error",
        #          f"An error occurred while initializing the RVM Industrial Microfluidic Rotary Valve : {err}")
        
        ##For simulation
        self.currentposition = 1
            
    
    def set_valve(self, position: int):  
        if self.connected:
            if position != 1 and position != 2:
                messagebox.showerror("Error",
                    f"The position of the RVM Industrial Microfluidic Rotary Valve can only be 1 (ON) or 2 (OFF), but received: {position}"
                )
                return False
        else:
            messagebox.showerror("Error", "RVM Industrial Microfluidic Rotary Valve  is not connected.")
            return False #Operation failed
        
        ## check if is in position 1 then move to postion 2 otherwise give a warning
        if self.currentposition == 1:
            if position == 2:
                # Move to position 2
                try:
                    # ##VOOR SIMULATION UITZETTEN
                    # self.instrument.valveShortestPath(2)
                    # time.sleep(self.rotation_delay)
                    ###
                    
                    self.currentposition = 2
                    # print(f"RVM Industrial Microfluidic Rotary Valve moved to position 2/OFF state.")
                    return True
                except Exception as err:
                    messagebox.showerror("Error",
                        f"An error occurred while moving to position 2/OFF state : {err}")
            elif position == 1:
                # print(f"RVM Industrial Microfluidic Rotary Valve is already at position {self.currentposition}/OFF state")
                return False
            else:
                print(f"Invalid position: {position}")
                # return False
           
        elif self.currentposition == 2:
            if position == 1:
                # Move to position 1
                try:
                    ## VOOR SIMULATION UITZETTEN
                    # self.instrument.valveShortestPath(1)
                    # time.sleep(self.rotation_delay)
                    ###
                    
                    self.currentposition = 1
                    # print(f"RVM Industrial Microfluidic Rotary Valve moved to position 1/ON state")
                    return True
                except Exception as err:
                   messagebox.showerror("Error",
                        f"An error occurred while moving to position 1/ON tate : {err}")
            elif position == 2:
                return False
                # print(f"RVM Industrial Microfluidic Rotary Valve is already at position {self.currentposition}/ON state")
            else:
                print(f"Invalid position: {position}")
