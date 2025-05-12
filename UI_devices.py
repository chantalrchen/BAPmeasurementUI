import tkinter as tk
from tkinter import messagebox, ttk
import propar   # Bronkhorst MFC
import serial   # Cooling and Valve
import time 
import amfTools

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
            self.initialize()
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
        self.dummy = 0;
    
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

####CLASS RVM AHAHHSDAHASIJDKKJSAHDKJASHDJKSAH
class RVM:
    def __init__(self, port = "COM5"):
        self.port = port
        self.connected = False
        self.instrument = None
        self.currentposition = 0 #home status
        self.rotation_delay = 0.4  #the rotation time for 180 degree for RVMLP (1.5 s) and RVMFS (400 ms / 0.4s),

    def connect(self):
        valve_list = amfTools.util.getProductList() # get the list of AMF products connected to the computer
        for valve in valve_list:
            if "RVM" in valve.deviceType:
                self.instrument = amfTools.AMF(valve)
                break

        if self.instrument is None:
            # Try forced port connection if no RVM detected
            self.instrument = amfTools.AMF(self.port)

        self.instrument.connect() 
        self.initialize_valve()
        
       ##the following is used only for simulation
        self.connected = True
        return self.connected
        ##
    
    def disconnect(self):
        if self.connected and self.instrument:
            try:
                self.instrument.disconnect()
                print("RVM disconnected.")
            except Exception as err: 
                messagebox.showerror("Error",
                    f"An error occurred while disconnecting RVM Industrial Microfluidic Rotary Valve: {err}")
        self.connected = False

    #home status 
    def initialize_valve(self): 
        if not self.connected:
            raise ConnectionError("RVM Industrial Microfluidic Rotary Valve is not connected.")
        
        # Check if the product is homed (if not, home it)
        try:
            if not self.instrument.getHomeStatus(): 
                self.instrument.home()
                time.sleep(self.rotation_delay)  # Give time for homing

            else:
                print("RVM Industrial Microfluidic Rotary Valve is already homed.")

            # Always move to position 1 after homing (default start position)
            self.instrument.valveShortestPath(1)
            time.sleep(self.rotation_delay) #give time for rotation
            self.currentposition = 1
            print("RVM Industrial Microfluidic Rotary Valve moved to position 1/ON State.")

        except Exception as err:
            messagebox.showerror("Error",
                 f"An error occurred while initializing the RVM Industrial Microfluidic Rotary Valve : {err}")
            
    
    def set_valve(self, position: int):  
        if self.connected:
            if position != 1 and position != 2:
                messagebox.showerror("Error",
                    f"The position of the RVM Industrial Microfluidic Rotary Valve can only be 1 or 2, but received: {position}"
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
                    self.instrument.valveShortestPath(2)
                    time.sleep(self.rotation_delay)
                    self.currentposition = 2
                    print(f"RVM Industrial Microfluidic Rotary Valve moved to position 2/OFF state.")
                    return True
                except Exception as err:
                    messagebox.showerror("Error",
                        f"An error occurred while moving to position 2/OFF state : {err}")
            elif position == 1:
                print(f"RVM Industrial Microfluidic Rotary Valve is already at position {self.currentposition}")
            else:
                print(f"Invalid position: {position}")
           
        elif self.currentposition == 2:
            if position == 1:
                # Move to position 1
                try:
                    self.instrument.valveShortestPath(1)
                    self.currentposition = 1
                    print(f"RVM Industrial Microfluidic Rotary Valve moved to position 1/ON state")
                    return True
                except Exception as err:
                   messagebox.showerror("Error",
                        f"An error occurred while moving to position 1/ON tate : {err}")
            elif position == 2:
                print(f"RVM Industrial Microfluidic Rotary Valve is already at position {self.currentposition}")
            else:
                print(f"Invalid position: {position}")

class AutomatedSystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated System")
        self.root.geometry("1400x800")
        
        ##Het volgende is niet zo logisch, alleen als je het niet zo doet, krijg je dus dat profilemanager en UI een andere bronkhorst te pakken gaan krijgen
        ##Daarnaast zijn de porten dan ook niet aligned aahh
        self.mfcs = [BronkhorstMFC(port = 'COM1', channel = 0),  BronkhorstMFC(port = 'COM1', channel = 1), BronkhorstMFC(port = 'COM1', channel = 2)]
        self.cooling = Koelingsblok()
        self.valve = RVM()
        
        # Header frame for connection and status
        header_frame = ttk.Frame(self.root)
        header_frame.pack(side='top', fill='x', padx=5, pady=5)
        
        # Connection status frame
        connection_frame = ttk.Frame(header_frame)
        connection_frame.pack(side='right', padx=10)
        
        ttk.Label(connection_frame, text="Device Connections", font=("Arial", 11, "bold")).pack(fill = 'both', expand = True)
        # Connection status labels
        self.connection_mfc1_port_label = ttk.Label(connection_frame, 
                                                 text=f"MFC Port: {self.mfcs[0].port}, Connected: {self.mfcs[0].connected}")
        self.connection_mfc1_port_label.pack(fill='both', expand=True)
        
        self.connection_mfc2_port_label = ttk.Label(connection_frame, 
                                                 text=f"MFC Port: {self.mfcs[1].port}, Connected: {self.mfcs[1].connected}")
        self.connection_mfc2_port_label.pack(fill='both', expand=True)
        
        self.connection_mfc3_port_label = ttk.Label(connection_frame, 
                                                 text=f"MFC Port: {self.mfcs[2].port}, Connected: {self.mfcs[2].connected}")
        self.connection_mfc3_port_label.pack(fill='both', expand=True)
        
        # Cooling        
        self.connection_cooling_port_label = ttk.Label(connection_frame, 
                                                     text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}")
        self.connection_cooling_port_label.pack(fill='both', expand=True)
        
        self.connection_valve_port_label = ttk.Label(connection_frame, 
                                                  text=f"RVM Port: {self.valve.port}, Connected: {self.valve.connected}")
        self.connection_valve_port_label.pack(fill='both', expand=True)
        
        connect_all_button = ttk.Button(connection_frame, text = "Connect all devices", command = self.connect_all_devices)
        connect_all_button.pack(side='right', fill = 'both', expand = 'true')
        
        othervar_frame  = ttk.Frame(header_frame)
        othervar_frame.pack(side='right', padx=10)
        
        # Ambient temperature section
        ttk.Label(othervar_frame, text="Set Ambient Temperature", font=("Arial", 11, "bold")).pack(fill='both', expand=True)
        # Label and Entry for ambient temperature
        self.ambient_temp_label = tk.Label(othervar_frame, text=f"Ambient Temperature (°C): not set")
        self.ambient_temp_label.pack(fill='both', expand=True)
        self.ambient_temp = tk.DoubleVar()  # Use DoubleVar for floating-point values
        self.ambient_temp_entry = tk.Entry(othervar_frame, textvariable = self.ambient_temp)
        self.ambient_temp_entry.pack(fill='both', expand=True)
        ambient_temp_button = ttk.Button(othervar_frame, text = "Set ambient temperature", command = self.set_ambient_temp)
        ambient_temp_button.pack(fill='both', expand=True)
        
        # Status bar, to show what has been adjusted
        # Status label
        self.status_var = tk.StringVar() 
        self.status_var.set("Status:")
        status_bar = ttk.Label(header_frame, text='Status', textvariable=self.status_var)
        status_bar.pack(fill='both', padx=5, pady=5)
        
        self.running_var_bar = tk.Label(header_frame, text="")
        self.running_var_bar.pack(side= 'bottom', fill='x')
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.create_menu()
        self.create_device_tab()
        
    def set_ambient_temp(self):
        """
        Retrieve the ambient temperature from the entry box and set it.
        """
        try:
            # Get the value from the entry box
            self.ambient_temp = float(self.ambient_temp_entry.get())
            # Update the status bar to show the ambient temperature has been set
            self.ambient_temperature_label.config(text=f"Ambient temperature: {self.ambient_temp} °C")
            self.ambient_temp_label.config(text=f"Ambient temperature: {self.ambient_temp} °C")
            self.status_var.set(f"Ambient temperature set to {self.ambient_temp} °C")
        except ValueError:
            self.status_var.set("Invalid input! Enter a floating number for the ambient temperature.")
            messagebox.showerror("Invalid Input", "Please enter a floating number for ambient temperature.")
            
    def update_run_var(self):
 
        # Get mass flow rates from MFCs
        mass_flow_1 = f"{self.mfcs[0].get_massflow():.2f} mL/min" if self.mfcs[0].connected else "N/A"
        mass_flow_2 = f"{self.mfcs[1].get_massflow():.2f} mL/min" if self.mfcs[1].connected else "N/A"
        mass_flow_3 = f"{self.mfcs[2].get_massflow():.2f} mL/min" if self.mfcs[2].connected else "N/A"

        # Get temperature from cooling system
        temperature = f"{self.cooling.get_temperature(1):.2f} °C" if self.cooling.connected else "N/A"

        # Get valve position from valve
        valve_position = self.valve.current_valve_position() if self.valve.connected else "N/A"
        self.running_var_bar.config(text=f"MFC 1 Mass Flow Rate: {mass_flow_1} | MFC 2 Mass Flow Rate: {mass_flow_2} | MFC 3 Mass Flow Rate: {mass_flow_3} | Temperature: {temperature} | Valve Position: {valve_position}")

        # Schedule the next update
        self.notebook.after(10, lambda: self.update_run_var)
        
    def create_menu(self):
        menu = tk.Menu(self.root)
        
        # Settings menu
        settings_menu = tk.Menu(menu, tearoff=0)
        settings_menu.add_command(label="Communication Settings", command=self.com_settings)
        menu.add_cascade(label="Settings", menu=settings_menu)
        
        self.root.config(menu=menu)
    
    def create_device_tab(self):
        device_tab = ttk.Frame(self.notebook)
        device_tab.pack(fill='both', expand=True)
        self.notebook.add(device_tab, text="Device Control")
        self.notebook.pack(expand=True, fill='both')
        
        ############	MFC		###########################
        self.mfc_frames = []
        self.massflow_vars = []
        self.current_massflow_labels = []
        self.target_massflow_labels = []
        
        all_mfc_frame = ttk.LabelFrame(device_tab)
        all_mfc_frame.pack(fill='x', padx=10, pady=5)
        
        for index in range(3):
            # Create a frame for the MFC
            mfc_frame = ttk.LabelFrame(all_mfc_frame, text=f'MFC {index+1}')
            mfc_frame.grid(row = 0, column = index, padx=10, pady=5)
            self.mfc_frames.append(mfc_frame)  # Store the frame reference

            # Label for mass flow rate
            massflow_label = tk.Label(mfc_frame, text="Mass flow rate (mL/min):")
            massflow_label.grid(row=0, column=0, padx=10, pady=10)

            # Entry field for mass flow rate
            massflow_var = tk.DoubleVar()
            massflow_entry = tk.Entry(mfc_frame, textvariable=massflow_var)
            massflow_entry.grid(row=0, column=1, padx=10, pady=10)
            self.massflow_vars.append(massflow_var)  # Store the variable reference

            # Button to set the mass flow rate
            # lambda: anonymous function means that the function is without a name. 
            # using lambda, such that it doesn't run the function when initiating the program, and passes the value index to the function
            # https://www.geeksforgeeks.org/using-lambda-in-gui-programs-in-python/
            set_massflow_button = tk.Button(mfc_frame, text="Set mass flow rate", command=lambda i = index : self.set_MFCmassflow(i))
            set_massflow_button.grid(row=1, column=0, columnspan=2, pady=10)

            # Label to display the current flow rate
            current_massflow_label = tk.Label(mfc_frame, text="Current mass flow rate: Not available")
            current_massflow_label.grid(row=2, column=0, padx=10, pady=10)
            self.current_massflow_labels.append(current_massflow_label)  # Store the label reference

            # Label to display the target flow rate
            target_massflow_label = tk.Label(mfc_frame, text=f"Target mass flow rate: {self.mfcs[index].targetmassflow:.2f} mL/min")
            target_massflow_label.grid(row=2, column=1, padx=10, pady=10)
            self.target_massflow_labels.append(target_massflow_label)  # Store the label reference
        
        # Connect button
        MFC_connect_button = tk.Button(all_mfc_frame, text="Connect All MFCs", command= lambda: self.connect_MFC())
        MFC_connect_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

		# # Disconnect button
		# MFC_disconnect_button = tk.Button(mfc_frame, text="Disconnect", command= lambda i = index : self.disconnect_MFC(i))
		# MFC_disconnect_button.grid(row=3, column=1, padx=10, pady=10)

        ############	COOLING		###########################
        cooling_frame = ttk.LabelFrame(device_tab, text='Cooling')
        cooling_frame.pack(fill='x', padx=10, pady=5)
        
		# label for the temp
        temperature_label = tk.Label(cooling_frame, text="Temperature (°C):")
        temperature_label.grid(row=0, column=0, padx=10, pady=10)
        
        # entry field for temp
        self.temperature_var = tk.DoubleVar()
        temperature_entry = tk.Entry(cooling_frame, textvariable=self.temperature_var)
        temperature_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # button to set the temp
        set_temperature_button = tk.Button(cooling_frame, text="Set temperature", command=self.set_temperature)
        set_temperature_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Connect button
        cooling_connect_button = tk.Button(cooling_frame, text="Connect", command=self.connect_cooling)
        cooling_connect_button.grid(row=1, column=1, padx=10, pady=10)
        
        # Label to display the ambient temp
        self.ambient_temperature_label = tk.Label(cooling_frame, text=f"Ambient temperature: Not set")
        self.ambient_temperature_label.grid(row=2, column=0, padx=10, pady=10)
        
        # Label to display the current temp
        self.current_temperature_label = tk.Label(cooling_frame, text="Current temperature: Not available")
        self.current_temperature_label.grid(row=2, column=1, padx=10, pady=10)
        
        # Label to display the target temp
        self.target_temperature_label = tk.Label(cooling_frame, text=f"Target temperature: {self.cooling.targettemperature:.2f} °C")
        self.target_temperature_label.grid(row=2, column=2, padx=10, pady=10)


        # # Disconnect button
        # cooling_disconnect_button = tk.Button(cooling_frame, text="Disconnect", command=self.disconnect_cooling)
        # cooling_disconnect_button.grid(row=3, column=1, padx=10, pady=10)

        ############	VALVE		###########################
        valve_frame = ttk.LabelFrame(device_tab, text='Valve')
        valve_frame.pack(fill='x', padx=10, pady=5)
        
        # Valve position control
        ttk.Label(valve_frame, text="Valve Position:").grid(row=0, column=0, padx=10, pady=10)
        self.valve_pos_var = tk.IntVar(value=1)
        ttk.Combobox(valve_frame, textvariable=self.valve_pos_var, values=[1, 2], width=5).grid(row=0, column=1, padx=10, pady=10)
        
        # button to set the position of the valve
        set_valve_button = tk.Button(valve_frame, text="Set valve", command=self.set_valve)
        set_valve_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Connect button
        valve_connect_button = tk.Button(valve_frame, text="Connect", command=self.connect_valve)
        valve_connect_button.grid(row=1, column=1, padx=10, pady=10)
        
        # Label to display the current position of the valve
        self.current_valve_label = tk.Label(valve_frame, text="Current position of the valve: Not available")
        self.current_valve_label.grid(row=2, column=0, padx=10, pady=10)
    
        # # Disconnect button
        # valve_disconnect_button = tk.Button(valve_frame, text="Disconnect", command=self.disconnect_valve)
        # valve_disconnect_button.grid(row=3, column=1, padx=10, pady=10)

    def connect_MFC(self):
        for index in range(3):
            if self.mfcs[index].connect():
                self.update_connection_devices()
                self.status_var.set(f"MFC {index + 1} connected")
            else:
                messagebox.showinfo("Connection Failed", f"MFC {index + 1} is not connected")

    # def disconnect_MFC(self, index):
    #     self.mfcs[index].disconnect()
    #     #messagebox.showinfo("Disconnected", "MFC disconnected successfully.")
    #     #updating the connection info
    #     self.update_connection_devices()
    #     self.status_var.set(f"MFC {index + 1} disconnected")
    
    def connect_cooling(self):  
        if self.cooling.connect():
            #messagebox.showinfo("Connection", "Torrey Pines IC20XR Digital Chilling/Heating Dry Baths successfully connected.")
            #updating the connection info
            self.update_connection_devices()
            self.status_var.set(f"Torrey Pines IC20XR Digital Chilling/Heating Dry Baths connected")
        else:
            messagebox.showinfo("Connection Failed", "Cooling is not connected")
         
    # def disconnect_cooling(self):
    #     self.cooling.disconnect()
    #     #messagebox.showinfo("Disconnected", "Torrey Pines IC20XR Digital Chilling/Heating Dry Baths disconnected successfully.")
    #     #updating the connection info
    #     self.update_connection_devices()
    #     self.status_var.set(f"Torrey Pines IC20XR Digital Chilling/Heating Dry Baths disconnected")

    def connect_valve(self):  
        if self.valve.connect():
            #messagebox.showinfo("Connection", "RVM Industrial Microfluidic Rotary valve is successfully connected.")
            #updating the connection info
            self.update_connection_devices()
            self.status_var.set(f"RVM Industrial Microfluidic Rotary valve connected")
        else:
            messagebox.showinfo("Connection Failed", "RVM is not connected")
         
    # def disconnect_valve(self):
    #     self.valve.disconnect()
    #     #messagebox.showinfo("Disconnected", "RVM Industrial Microfluidic Rotary valve is disconnected successfully.")
    #     #updating the connection info
    #     self.update_connection_devices()
    #     self.status_var.set(f"RVM Industrial Microfluidic Rotary valve disconnected")

    def connect_all_devices(self):
        self.connect_MFC()
        self.connect_cooling()
        self.connect_valve()
        self.status_var.set(f"MFC, Torrey Pines IC20XR Digital Chilling/Heating Dry Baths and RVM Industrial Microfluidic Rotary valve connected")
   
    def update_connection_devices(self):
        
        #Labels at the Header
        self.connection_mfc1_port_label.config (text=f"MFC 1 Port: {self.mfcs[0].port}, Connected: {self.mfcs[0].connected}")
        self.connection_mfc2_port_label.config (text=f"MFC 2 Port: {self.mfcs[1].port}, Connected: {self.mfcs[1].connected}")
        self.connection_mfc3_port_label.config (text=f"MFC 3 Port: {self.mfcs[2].port}, Connected: {self.mfcs[2].connected}")
        self.connection_cooling_port_label.config(text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}")
        self.connection_valve_port_label.config(text=f"RVM Port: {self.valve.port}, Connected: {self.valve.connected}")

    def com_settings(self):
        #Opens een top level window
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Connection Settings")
        settings_window.geometry("400x400")
        
        #this forces all focus on the top level until the toplevel is closed
        settings_window.grab_set()
        
        # Bronkhorst MFC settings
        MFC_frame = ttk.LabelFrame(settings_window, text="Bronkhorst MFC")
        MFC_frame.pack(fill="both", padx=10, pady=10)
        
        ttk.Label(MFC_frame, text="Port:").grid(row=0, column=0, padx=5, pady=5)
        self.MFC_port_var = tk.StringVar(value=self.mfcs[0].port)
        MFC1_port_entry = ttk.Entry(MFC_frame, textvariable=self.MFC_port_var)
        MFC1_port_entry.grid(row=0, column=1, padx=5, pady=5)

        
        # Cooling settings
        cooling_frame = ttk.LabelFrame(settings_window, text="Torrey Pines IC20XR Digital Chilling/Heating Dry Baths")
        cooling_frame.pack(fill="both", padx=10, pady=10)
        
        ttk.Label(cooling_frame, text="Port:").grid(row=3, column=0, padx=5, pady=5)
        self.cooling_port_var = tk.StringVar(value=self.cooling.port)
        cooling_port_entry = ttk.Entry(cooling_frame, textvariable=self.cooling_port_var)
        cooling_port_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # valve settings
        valve_frame = ttk.LabelFrame(settings_window, text="RVM Industrial Microfluidic Rotary valve ")
        valve_frame.pack(fill="both", padx=10, pady=10)
        
        ttk.Label(valve_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        self.valve_port_var = tk.StringVar(value=self.valve.port)
        valve_port_entry = ttk.Entry(valve_frame, textvariable=self.valve_port_var)
        valve_port_entry.grid(row=4, column=1, padx=5, pady=5)
            
        save_button = ttk.Button(settings_window, text="Save", command=self.save_settings)
        save_button.pack(pady=10)
        
    def save_settings(self):
        self.mfcs[0].port = self.MFC_port_var.get()
        self.mfcs[1].port = self.MFC_port_var.get()
        self.mfcs[2].port = self.MFC_port_var.get()
        self.cooling.port = self.cooling_port_var.get()
        self.valve.port = self.valve_port_var.get()
        
        self.update_connection_devices()
        self.status_var.set("Port connections are updated.")

    def set_MFCmassflow(self, index):
        massflowrate = self.massflow_vars[index].get()
        if self.mfcs[index].set_massflow(massflowrate):
            self.target_massflow_labels[index].config(text=f"Target mass flow rate: {self.mfcs[index].targetmassflow} mL/min")
            self.update_massflow(index)
        else:
            self.status_var.set("MFC: Failed to set mass flow rate.")
            
    def update_massflow(self, index):
        current_flow = self.mfcs[index].get_massflow()
        self.update_run_var()
        if current_flow is not None:
            self.current_massflow_labels[index].config(text=f"Current mass flow rate: {current_flow:.2f} mL/min")
        else:
            self.status_var.set("Failed to read mass flow rate.")
        
        # Passing the index to the function by using lambda
        # Lambda are anonymous function means that the function is without a name
        # https://www.geeksforgeeks.org/using-lambda-in-gui-programs-in-python/
        self.root.after(1000, lambda: self.update_massflow(index)) #updating the MFC flow rate reading each 1s
        
    def set_temperature(self):
        if self.cooling.connected == False:
            messagebox.showwarning("Device not connected", "The Torrey Pines IC20XR Digital Chilling/Heating Dry Baths is not connected")
            return False
        elif not isinstance(self.ambient_temp, (int, float)):
            messagebox.showwarning("Invalid Input", "Ambient Temperature has not been set yet or is an non-numeric value.")
            return False
        else:    
            try:
                temperature = float(self.temperature_var.get())
                self.cooling.set_temperature(temperature, self.ambient_temp)
                self.target_temperature_label.config(text=f"Target temperature: {self.cooling.targettemperature:.2f} °C")
                self.update_temperature()
                
                ##if non-floating number, tk.tclerror occurs
            except tk.TclError as e:
                messagebox.showerror("Invalid Input", f"Please enter a floating number for target temperature. {e}")
                
    def update_temperature(self):
        current_temp = self.cooling.get_temperature(1)
        self.update_run_var()
        if current_temp is not None:
            self.current_temperature_label.config(text=f"Current temperature: {current_temp:.2f} °C")
        else:
            self.status_var.set("Failed to read the temperature.")
        
        #Updating temperature every 1s; otherwise the simulation/reading the data won't work. It would only happen one time.
        #https://www.geeksforgeeks.org/python-after-method-in-tkinter/
        self.notebook.after(1000, self.update_temperature) 
        
    def set_valve(self):
        position = self.valve_pos_var.get()
        if self.valve.set_valve(position):
            self.update_valve()

    def update_valve(self):
        current_position = self.valve.current_valve_position()
        self.update_run_var()
        if current_position is not None:
            self.current_valve_label.config(text=f"Current position of the valve: {current_position}")
        else:
            self.status_var.set("Failed to read the position of the valve.")
    
        
def main():
    root = tk.Tk()
    app = AutomatedSystemUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
