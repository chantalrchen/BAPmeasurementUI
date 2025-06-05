import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import threading
##Koeling Uitzetten omdat hij het nog niet doet
# # Cooling OFF
# from profilemanagers import MFCProfileManager, CoolingProfileManager, RVMProfileManager, OnoffProfileManager, DiffConcProfileManager

from profilemanagers2valves import MFCProfileManager, TwoRVMProfileManager, OnoffProfileManager, DiffConcProfileManager, OnOffConcProfileManager
from settingsmanagers2valves import SettingsManager
import pandas as pd
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AutomatedSystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated System")
        self.root.geometry("1400x800")
        
        # self.path_pureflowrate = "C:/Users/chant/Downloads/Pure and Mixed flow rates.xlsx"
                
        self.settings_manager = SettingsManager()
        settings_path = self.settings_manager.get_profiles_path()
        saved_ports = self.settings_manager.get_com_ports()

        self.mfcprofilemanager = MFCProfileManager(saved_ports["mfc1"], saved_ports["mfc2"], saved_ports["mfc3"], profiles_dir=settings_path)

        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # self.coolingprofilemanager = CoolingProfileManager(saved_ports["cooling"], profiles_dir=settings_path)

        self.valveprofilemanager = TwoRVMProfileManager(saved_ports["valve1"], saved_ports["valve2"], profiles_dir=settings_path)

        self.mfcs = self.mfcprofilemanager.mfcs
        
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # self.cooling = self.coolingprofilemanager.cooling
        
        self.valve = self.valveprofilemanager.valve

        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # self.onoffprofilemanager = OnoffProfileManager(
        #     UImfcs=self.mfcs, UIcooling=self.cooling, UIvalve=self.valve, profiles_dir=settings_path
        # )
        
        # self.diffconcprofilemanager = DiffConcProfileManager(
        #     UImfcs=self.mfcs, UIcooling=self.cooling, UIvalve=self.valve, profiles_dir=settings_path
        # )

        self.onoffprofilemanager = OnoffProfileManager(
            UImfcs=self.mfcs, UIvalve=self.valve, profiles_dir=settings_path
        )
        
        self.diffconcprofilemanager = DiffConcProfileManager(
            UImfcs=self.mfcs, UIvalve=self.valve, profiles_dir=settings_path
        )

        self.onoffconcprofilemanager = OnOffConcProfileManager(
            UImfcs=self.mfcs, UIvalve=self.valve, profiles_dir=settings_path
        )
        
        # Header frame for connection and status
        header_frame = ttk.Frame(self.root)
        header_frame.pack(side='top', fill='x', padx=5, pady=5)
        
        # Connection status frame
        connection_frame = ttk.Frame(header_frame)
        connection_frame.pack(side='right', padx=10)
        
        ttk.Label(connection_frame, text="Device Connections", font=("Arial", 10, "bold")).pack(fill = 'both', expand = True)
        # Connection status labels
        self.connection_mfc1_port_label = ttk.Label(connection_frame, 
                                                 text=f"MFC 1 Port: {self.mfcs[0].port}, Connected: {self.mfcs[0].connected}")
        self.connection_mfc1_port_label.pack(fill='both', expand=True)
        
        self.connection_mfc2_port_label = ttk.Label(connection_frame, 
                                                 text=f"MFC 2 Port: {self.mfcs[1].port}, Connected: {self.mfcs[1].connected}")
        self.connection_mfc2_port_label.pack(fill='both', expand=True)
        
        self.connection_mfc3_port_label = ttk.Label(connection_frame, 
                                                 text=f"MFC 3 Port: {self.mfcs[2].port}, Connected: {self.mfcs[2].connected}")
        self.connection_mfc3_port_label.pack(fill='both', expand=True)
        
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF      
        # self.connection_cooling_port_label = ttk.Label(connection_frame, 
        #                                              text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}")
        # self.connection_cooling_port_label.pack(fill='both', expand=True)
        
        self.connection_valve1_port_label = ttk.Label(connection_frame, 
                                                  text=f"RVM 1 Port: {self.valve[0].port}, Connected: {self.valve[0].connected}")
        self.connection_valve1_port_label.pack(fill='both', expand=True)
        
        self.connection_valve2_port_label = ttk.Label(connection_frame, 
                                                  text=f"RVM 2 Port: {self.valve[1].port}, Connected: {self.valve[1].connected}")
        self.connection_valve2_port_label.pack(fill='both', expand=True)
        
        connect_all_button = ttk.Button(connection_frame, text = "Connect all devices", command = self.connect_all_devices)
        connect_all_button.pack(side='right', fill = 'both', expand = 'true')
        
        othervar_frame  = ttk.Frame(header_frame)
        othervar_frame.pack(side='right', padx=10)

        ### niet meer nodig        
        # Ambient temperature section
        # ttk.Label(othervar_frame, text="Set Ambient Temperature", font=("Arial", 9, "bold")).pack(fill='both', expand=True)
        # # Label and Entry for ambient temperature
        # self.ambient_temp_label = tk.Label(othervar_frame, text=f"Ambient Temperature (°C): not set")
        # self.ambient_temp_label.pack(fill='both', expand=True)
        # self.ambient_temp = tk.DoubleVar()  # Use DoubleVar for floating-point values
        # self.ambient_temp_entry = tk.Entry(othervar_frame, textvariable = self.ambient_temp)
        # self.ambient_temp_entry.pack(fill='both', expand=True)
        # ambient_temp_button = ttk.Button(othervar_frame, text = "Set ambient temperature", command = self.set_ambient_temp)
        # ambient_temp_button.pack(fill='both', expand=True)
        
        # Status bar, to show what has been adjusted
        # Status label
        self.status_var = tk.StringVar() 
        self.status_var.set("Status:")
        status_bar = ttk.Label(header_frame, text='Status', textvariable=self.status_var)
        status_bar.pack(fill='both', padx=5, pady=5)

        self.running_var_bar = tk.Label(header_frame, text="", anchor="w", relief="sunken")
        self.running_var_bar.pack(side='top', fill='x')
        
        overview_profile = ttk.Frame(self.root)
        overview_profile.pack(fill="x", padx=10, pady=5)
        
        ######PROFILE STATUS
        # Create a frame to contain the grid-like status table
        self.profile_status_frame = ttk.LabelFrame(overview_profile, text="Profile Overview")
        self.profile_status_frame.pack(side = "left", padx=10, pady=5)

        # Column headers
        ttk.Label(self.profile_status_frame, text="Profile", font=("Arial", 8, "bold")).grid(row=0, column=0, padx=5, sticky="w")
        ttk.Label(self.profile_status_frame, text="Elapsed Time", font=("Arial", 8, "bold")).grid(row=0, column=1, padx=5, sticky="w")
        ttk.Label(self.profile_status_frame, text="Step", font=("Arial", 8, "bold")).grid(row=0, column=2, padx=5, sticky="w")
        ttk.Label(self.profile_status_frame, text="Value", font=("Arial", 8, "bold")).grid(row=0, column=3, padx=5, sticky="w")

        # Row for MFC profile
        ttk.Label(self.profile_status_frame, text="MFC Running Profile").grid(row=1, column=0, padx=5, sticky="w")
        self.mfc_elapsed_label = ttk.Label(self.profile_status_frame, text="-")
        self.mfc_elapsed_label.grid(row=1, column=1, padx=5, sticky="w")
        self.mfc_step_label = ttk.Label(self.profile_status_frame, text="-")
        self.mfc_step_label.grid(row=1, column=2, padx=5, sticky="w")
        self.mfc_value_label = ttk.Label(self.profile_status_frame, text="-")
        self.mfc_value_label.grid(row=1, column=3, padx=5, sticky="w")

        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # Cooling profile
        # ttk.Label(self.profile_status_frame, text="Cooling Running Profile").grid(row=2, column=0, padx=5, sticky="w")
        # self.cooling_elapsed_label = ttk.Label(self.profile_status_frame, text="-")
        # self.cooling_elapsed_label.grid(row=2, column=1, padx=5, sticky="w")
        # self.cooling_step_label = ttk.Label(self.profile_status_frame, text="-")
        # self.cooling_step_label.grid(row=2, column=2, padx=5, sticky="w")
        # self.cooling_value_label = ttk.Label(self.profile_status_frame, text="-")
        # self.cooling_value_label.grid(row=2, column=3, padx=5, sticky="w")

        # Valve profile
        ttk.Label(self.profile_status_frame, text="Valve Running Profile").grid(row=3, column=0, padx=5, sticky="w")
        self.valve_elapsed_label = ttk.Label(self.profile_status_frame, text="-")
        self.valve_elapsed_label.grid(row=3, column=1, padx=5, sticky="w")
        self.valve_step_label = ttk.Label(self.profile_status_frame, text="-")
        self.valve_step_label.grid(row=3, column=2, padx=5, sticky="w")
        self.valve_value_label = ttk.Label(self.profile_status_frame, text="-")
        self.valve_value_label.grid(row=3, column=3, padx=5, sticky="w")

        # On/Off profile
        ttk.Label(self.profile_status_frame, text="On/Off Running Profile").grid(row=4, column=0, padx=5, sticky="w")
        self.onoff_elapsed_label = ttk.Label(self.profile_status_frame, text="-")
        self.onoff_elapsed_label.grid(row=4, column=1, padx=5, sticky="w")
        self.onoff_step_label = ttk.Label(self.profile_status_frame, text="-")
        self.onoff_step_label.grid(row=4, column=2, padx=5, sticky="w")
        self.onoff_value_label = ttk.Label(self.profile_status_frame, text="-")
        self.onoff_value_label.grid(row=4, column=3, padx=5, sticky="w")
        

        # Different Concentration profile
        ttk.Label(self.profile_status_frame, text="Different Concentration Profile").grid(row=5, column=0, padx=5, sticky="w")
        self.diffconc_elapsed_label = ttk.Label(self.profile_status_frame, text="-")
        self.diffconc_elapsed_label.grid(row=5, column=1, padx=5, sticky="w")
        self.diffconc_step_label = ttk.Label(self.profile_status_frame, text="-")
        self.diffconc_step_label.grid(row=5, column=2, padx=5, sticky="w")
        self.diffconc_value_label = ttk.Label(self.profile_status_frame, text="-")
        self.diffconc_value_label.grid(row=5, column=3, padx=5, sticky="w")
        

        selectprofiles_frame = ttk.LabelFrame(overview_profile, text="Multiple Profile Runner")
        selectprofiles_frame.pack(side="right")

        # Label row

        ttk.Label(selectprofiles_frame, text="Valve Profiles").grid(row=0, column=1)
        
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # ttk.Label(selectprofiles_frame, text="Cooling Profiles").grid(row=0, column=2)

        # MFC listbox with scrollbar
        ttk.Label(selectprofiles_frame, text="MFC Profiles").grid(row=0, column=0)
        mfc_listbox_frame = ttk.Frame(selectprofiles_frame)
        mfc_listbox_frame.grid(row=1, column=0, padx=5, pady=5)
        # # https://www.pythontutorial.net/tkinter/tkinter-listbox/#adding-a-scrollbar-to-the-listbox
        # # Making an empty profile listbox
        # Exportseleciton = False, such that when you select another listbox you still can have your selection
        self.selprof_mfc_listbox = tk.Listbox(mfc_listbox_frame, height=2, exportselection=False)
        self.selprof_mfc_listbox.pack(side='left', fill='y')
        mfc_v_scrollbar = ttk.Scrollbar(mfc_listbox_frame, orient=tk.VERTICAL, command=self.selprof_mfc_listbox.yview)
        mfc_v_scrollbar.pack(side='right', fill='y')
        self.selprof_mfc_listbox.config(yscrollcommand=mfc_v_scrollbar.set)
        
        # Valve Listbox with scrollbar
        valve_listbox_frame = ttk.Frame(selectprofiles_frame)
        valve_listbox_frame.grid(row=1, column=1, padx=5, pady=5)
        self.selprof_valve_listbox = tk.Listbox(valve_listbox_frame, height=2, exportselection=False)
        self.selprof_valve_listbox.pack(side='left', fill='y')
        valve_v_scrollbar = ttk.Scrollbar(valve_listbox_frame, orient=tk.VERTICAL, command=self.selprof_valve_listbox.yview)
        valve_v_scrollbar.pack(side='right', fill='y')
        self.selprof_valve_listbox.config(yscrollcommand=valve_v_scrollbar.set)

        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # Cooling Listbox with scrollbar
        # cooling_listbox_frame = ttk.Frame(selectprofiles_frame)
        # cooling_listbox_frame.grid(row=1, column=2, padx=5, pady=5)
        # self.selprof_cooling_listbox = tk.Listbox(cooling_listbox_frame, height=2, exportselection=False)
        # self.selprof_cooling_listbox.pack(side='left', fill='y')
        # cooling_v_scrollbar = ttk.Scrollbar(cooling_listbox_frame, orient=tk.VERTICAL, command=self.selprof_cooling_listbox.yview)
        # cooling_v_scrollbar.pack(side='right', fill='y')
        # self.selprof_cooling_listbox.config(yscrollcommand=cooling_v_scrollbar.set)


        # Populate listboxes
        for profile in self.mfcprofilemanager.get_profiles():
            self.selprof_mfc_listbox.insert(tk.END, profile)
        for profile in self.valveprofilemanager.get_profiles():
            self.selprof_valve_listbox.insert(tk.END, profile)
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # for profile in self.coolingprofilemanager.get_profiles():
        #     self.selprof_cooling_listbox.insert(tk.END, profile)

        # Run Button
        ttk.Button(selectprofiles_frame, text="Run Selected Profiles", command=self.run_selected_profiles).grid(row=1, column=3, padx=10)

        # Stop Button directly under Run
        self.stop_all_button = ttk.Button(selectprofiles_frame, text="Stop Selected Profiles", command=self.stop_all_profiles)
        self.stop_all_button.grid(row=2, column=3, padx=10, pady= 5)  # Placed under run button
        self.stop_all_button.config(state=tk.DISABLED)


        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.create_menu()
        self.create_device_tab()
        self.create_onoffprofile_tab()
        self.create_mfcprofile_tab()
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # self.create_coolingprofile_tab()
        self.create_valveprofile_tab()
        
        ##EXCEL SHEET TAB UITZETTEN
        # self.create_pureflowrate_tab()
        self.create_voccalculator_tab()
        self.create_diffconc_profile_tab()

    def create_scrollable_tab(self, notebook, tab_name):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=tab_name)

        canvas = tk.Canvas(tab)
        v_scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=v_scrollbar.set)

        v_scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", configure_scroll_region)

        return scrollable_frame
    
    ### NIET MEER NODIG
    # def set_ambient_temp(self):
    #     """
    #     Retrieve the ambient temperature from the entry box and set it.
    #     """
    #     try:
    #         # Get the value from the entry box
    #         self.ambient_temp = float(self.ambient_temp_entry.get())
    #         # Update the status bar to show the ambient temperature has been set
    #         # Cooling not connected
    #         # self.ambient_temperature_label.config(text=f"Ambient temperature: {self.ambient_temp} °C")
    #         self.ambient_temp_label.config(text=f"Ambient temperature: {self.ambient_temp} °C")
    #         self.status_var.set(f"Ambient temperature set to {self.ambient_temp} °C")
    #     except ValueError:
    #         self.status_var.set("Invalid input! Enter a floating number for the ambient temperature.")
    #         messagebox.showerror("Invalid Input", "Please enter a floating number for ambient temperature.")
    
    def update_run_var(self):
        
        #when the UI is closed then this won't be "updating" (to debug)
        try:
            if not self.root.winfo_exists():
                return
        
            ##update device tab
            massflows = []
            
            for i in range(3):
                if self.mfcs[i].connected:
                    
                    # flow = self.mfcs[i].get_massflow()[0]['data']
                
                ###DIT MOET AAN EN DE REGEL HIEBOVEN MOET UIT OM TE SIMULEREN    
                    #TO SIMULATE
                    flow = self.mfcs[i].get_massflow()
            
                    flow_str = f"{flow} mL/min"
                else:
                    flow = None
                    flow_str = "-"
                massflows.append(flow_str)
                self.current_massflow_labels[i].config(text=f"Current mass flow rate: {flow_str}")

            ##Koeling Uitzetten omdat hij het nog niet doet
            # # Cooling OFF
            # if self.cooling.connected:
            #     temp = self.cooling.get_temperature()
            #     temp_str = f"{temp:.3f} °C"
            # else:
            #     temp = None
            #     temp_str = "-"
            # self.current_temperature_label.config(text=f"Current temperature: {temp_str}")

          ##update device tab
            valveposition = []
            
            for i in range(2):
                if self.valve[i].connected:
                    
                ###DIT MOET AAN EN DE REGEL HIEBOVEN MOET UIT OM TE SIMULEREN    
                    #TO SIMULATE
                    pos = self.valve[i].get_position()

                else:
                    pos = "-"
                valveposition.append(pos)
                self.current_position_labels[i].config(text=f"Current position of the valve: {pos}")


            # Summary bar uses same values
            self.running_var_bar.config(
                text=(
                    f"Reading Values   : "
                    f"MFC 1 Mass Flow Rate: {massflows[0]} | "
                    f"MFC 2 Mass Flow Rate: {massflows[1]} | "
                    f"MFC 3 Mass Flow Rate: {massflows[2]} | "
            # # Cooling OFF // Koeling Uitzetten omdat hij het nog niet doet
                    # f"Temperature: {temp_str} | "
                    f"RVM 1 Position: {valveposition[0]} | "
                    f"RVM 2 Position: {valveposition[1]} | "
                )
            )
            # Schedule the next update, per 1s
            self.root.after(1000, self.update_run_var)
        except tk.TclError:
            return

    def create_menu(self):
        menu = tk.Menu(self.root)
        
        # Settings menu
        settings_menu = tk.Menu(menu, tearoff=0)
        settings_menu.add_command(label="Connection Settings", command=self.com_settings)
        
        voc_menu = tk.Menu(menu, tearoff=0)
        voc_menu.add_command(label="Add VOCSs", command=self.voc_settings)
        menu.add_cascade(label="Settings", menu=settings_menu)
        menu.add_cascade(label="VOC Settings", menu=voc_menu)
        
        self.root.config(menu=menu)
    
    def create_device_tab(self):
        # device_tab = ttk.Frame(self.notebook)
        
        ##Make it scrollable
        device_tab = self.create_scrollable_tab(self.notebook, "Device Control")
        # device_tab.pack(fill='both', expand=True)
        # self.notebook.add(device_tab, text="Device Control")
        # self.notebook.pack(expand=True, fill='both')
        
        ############	MFC		###########################
        self.mfc_frames = []
        self.massflow_vars = []
        self.current_massflow_labels = []
        self.target_massflow_labels = []
        
        all_mfc_frame = ttk.LabelFrame(device_tab)
        all_mfc_frame.pack(fill='x', padx=10, pady=5)

        for i in range(len(self.mfcs)):
            self.create_mfc_frame(all_mfc_frame, i)
            
        all_valve_frame = ttk.LabelFrame(device_tab)
        all_valve_frame.pack(fill='x', padx=10, pady=5)

        self.valve_frames = []
        self.position_vars = []
        self.current_position_labels = []
        self.target_position_labels = []
        
        for i in range(len(self.valve)):
            self.create_valve_frame(all_valve_frame, i)
            
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF // Koeling Uitzetten omdat hij het nog niet doet
        ############	COOLING		###########################
        # cooling_frame = ttk.LabelFrame(coolingandvalve_frame, text='Digital chilling/heating dry bath')
        # cooling_frame.grid(row=0, column=0, padx=10, pady=5, sticky='n')
        
        # # label for the temp
        # temperature_label = tk.Label(cooling_frame, text="Temperature (°C):")
        # temperature_label.grid(row=0, column=0, padx=10, pady=10)
        
        # # entry field for temp
        # self.temperature_var = tk.DoubleVar()
        # temperature_entry = tk.Entry(cooling_frame, textvariable=self.temperature_var)
        # temperature_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # # button to set the temp
        # set_temperature_button = tk.Button(cooling_frame, text="Set temperature", command=self.set_temperature)
        # set_temperature_button.grid(row=1, column=0, columnspan=2, pady=10)

        # # Label to display the ambient temp
        # self.ambient_temperature_label = tk.Label(cooling_frame, text=f"Ambient temperature: Not set")
        # self.ambient_temperature_label.grid(row=2, column=0, padx=10, pady=10)
        
        # # Label to display the current temp
        # self.current_temperature_label = tk.Label(cooling_frame, text="Current temperature: Not available")
        # self.current_temperature_label.grid(row=2, column=1, padx=10, pady=10)
        
        # # Label to display the target temp
        # self.target_temperature_label = tk.Label(cooling_frame, text=f"Target temperature: {self.cooling.targettemperature:.2f} °C")
        # self.target_temperature_label.grid(row=2, column=2, padx=10, pady=10)

        # # Connect button
        # cooling_connect_button = tk.Button(cooling_frame, text="Connect", command=self.connect_cooling)
        # cooling_connect_button.grid(row=3, column=0, padx=10, pady=10)
        
        # # Disconnect button
        # cooling_disconnect_button = tk.Button(cooling_frame, text="Disconnect", command=self.disconnect_cooling)
        # cooling_disconnect_button.grid(row=3, column=1, padx=10, pady=10)

        # ############	VALVE		###########################
        # valve_frame = ttk.LabelFrame(coolingandvalve_frame, text='Valve')
        # valve_frame.grid(row=0, column=1, padx=10, pady=5, sticky='n')
                
        # # Valve position control
        # ttk.Label(valve_frame, text="Valve Position:").grid(row=0, column=0, padx=10, pady=10)
        # self.valve_pos_var = tk.IntVar(value=1)
        # ttk.Combobox(valve_frame, textvariable=self.valve_pos_var, values=[1, 2], width=5).grid(row=0, column=1, padx=10, pady=10)
        
        # # button to set the position of the valve
        # set_valve_button = tk.Button(valve_frame, text="Set valve", command=self.set_valve)
        # set_valve_button.grid(row=1, column=0, padx=10, pady=10)
        
        # # Label to display the current position of the valve
        # self.current_valve_label = tk.Label(valve_frame, text="Current position of the valve: Not available")
        # self.current_valve_label.grid(row=2, column=0, padx=10, pady=10)
        
        # # Connect button
        # valve_connect_button = tk.Button(valve_frame, text="Connect", command=self.connect_valve)
        # valve_connect_button.grid(row=3, column=0, padx=5, pady=5)
        
        # # Disconnect button
        # valve_disconnect_button = tk.Button(valve_frame, text="Disconnect", command=self.disconnect_valve)
        # valve_disconnect_button.grid(row=3, column=1, padx=5, pady=5)
    
    def create_valve_frame(self, parent, index):
        valve = self.valve[index]
        frame = ttk.LabelFrame(parent, text=f'Valve {index + 1}')
        frame.grid(row=0, column=index, padx=10, pady=5)

        tk.Label(frame, text="Valve Position").grid(row=0, column=0, padx=10, pady=10)
        var = tk.IntVar()
        entry = ttk.Combobox(frame, textvariable=var, values=[1, 2], width=5, state="readonly")
        entry.grid(row=0, column=1, padx=10, pady=10)
        self.position_vars.append(var)

        tk.Button(frame, text="Set Valve Position", command=lambda i=index: self.set_valve(i)).grid(
            row=1, column=0, columnspan=2, pady=10)

        current_label = tk.Label(frame, text="Current valve position: Not available")
        current_label.grid(row=2, column=0, padx=10, pady=10)
        self.current_position_labels.append(current_label)

        target_label = tk.Label(frame, text=f"Target valve position: Not available")
        target_label.grid(row=2, column=1, padx=10, pady=10)
        self.target_position_labels.append(target_label)

        tk.Button(frame, text="Connect", command=lambda i=index: self.connect_valve(i)).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(frame, text="Disconnect", command=lambda i=index: self.disconnect_valve(i)).grid(row=3, column=1, padx=10, pady=10)
        
    def create_mfc_frame(self, parent, index):
        mfc = self.mfcs[index]
        frame = ttk.LabelFrame(parent, text=f'MFC {index + 1}')
        frame.grid(row=0, column=index, padx=10, pady=5)

        tk.Label(frame, text="Mass flow rate (mL/min):").grid(row=0, column=0, padx=10, pady=10)
        var = tk.DoubleVar()
        entry = tk.Entry(frame, textvariable=var)
        entry.grid(row=0, column=1, padx=10, pady=10)
        self.massflow_vars.append(var)

        tk.Button(frame, text="Set mass flow rate", command=lambda i=index: self.set_MFCmassflow(i)).grid(
            row=1, column=0, columnspan=2, pady=10)

        current_label = tk.Label(frame, text="Current mass flow rate: Not available")
        current_label.grid(row=2, column=0, padx=10, pady=10)
        self.current_massflow_labels.append(current_label)

        target_label = tk.Label(frame, text=f"Target mass flow rate: {mfc.targetmassflow:.2f} mL/min")
        target_label.grid(row=2, column=1, padx=10, pady=10)
        self.target_massflow_labels.append(target_label)

        tk.Button(frame, text="Connect", command=lambda i=index: self.connect_MFC(i)).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(frame, text="Disconnect", command=lambda i=index: self.disconnect_MFC(i)).grid(row=3, column=1, padx=10, pady=10)
        
    def create_onoffprofile_tab(self):
        #Make it scrollable
        profile_tab = self.create_scrollable_tab(self.notebook, "MFC and Management")
        # profile_tab = ttk.Frame(self.notebook)
        # profile_tab.pack(fill = 'both', expand = True)
        # self.notebook.add(profile_tab, text = 'On/Off Profile Management')
        
        ## Split into two frames
        list_frame = ttk.Frame(profile_tab)
        list_frame.pack(side= 'left', fill = 'both', expand=True, padx=5, pady=5)
        
        edit_frame = ttk.Frame(profile_tab)
        edit_frame.pack(side= 'right', fill= 'both', expand=True, padx=5, pady=5)
        
        ### Left frame / list frame
        ## Profile listbox with scrollbar
        # https://www.pythontutorial.net/tkinter/tkinter-listbox/#adding-a-scrollbar-to-the-listbox
        # Making an empty profile listbox
        self.onoffprofile_listbox = tk.Listbox(list_frame, selectmode = tk.SINGLE)
        self.onoffprofile_listbox.pack(fill= 'both', expand=True, padx=5, pady=5)
    
        # Putting all the profiles in the profile listbox
        self.update_onoffprofile_list()
        
        #Adding a scrollbar to the profile listbox
        v_scrollbar = ttk.Scrollbar(self.onoffprofile_listbox, orient = tk.VERTICAL, command = self.onoffprofile_listbox.yview)
        
        self.onoffprofile_listbox['yscrollcommand'] = v_scrollbar.set
        v_scrollbar.pack(side='right', fill='y')
        
        ##Adding the buttons to the left frame (list frame)
        # Profile list buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        load_button = ttk.Button(button_frame, text="Load", command=self.load_onoffprofile)
        load_button.pack(side='left', padx=3, expand=True)
        
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_onoffprofile)
        delete_button.pack(side='left', padx=3, expand=True)

        ##Right frame / edit frame
        # Profile info
        info_frame = ttk.Frame(edit_frame)
        info_frame.pack(fill='both', padx=5, pady=5)
        
        self.new_onoffprofile_label = ttk.Label(info_frame, text="")
        self.new_onoffprofile_label.pack(side = 'left', padx=5, expand=True, fill='x')
        
        profile_name_label = ttk.Label(info_frame, text="Name:").pack(side='left')
        self.onoffname_var = tk.StringVar()
        name_entry = ttk.Entry(info_frame, textvariable=self.onoffname_var)
        name_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        profile_desc_label = ttk.Label(info_frame, text="Description:").pack(side='left')
        self.onoffdesc_var = tk.StringVar()
        desc_entry = ttk.Entry(info_frame, textvariable=self.onoffdesc_var)
        desc_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        new_profile_btn = ttk.Button(info_frame, text = 'New Profile', command = self.create_new_onoffprofile)
        new_profile_btn.pack(side='right', padx=3, expand=True)
        
        # Steps in the right/frame
        steps_frame = ttk.Frame(edit_frame)
        steps_frame.pack(fill = 'both' , expand=True, padx=5, pady=5)
        
        #https://tk-tutorial.readthedocs.io/en/latest/tree/tree.html
        self.onoffsteps_tree = ttk.Treeview(
            steps_frame, 
            ### NO COOLING
            # columns=("time", "flow mfc1", "flow mfc2", "flow mfc3", "temp", "valve"), 
                columns=("time", "flow mfc1", "flow mfc2", "flow mfc3", "valve"), 
            show="headings"
        )
        self.onoffsteps_tree.heading("time", text="Time (s)")
        self.onoffsteps_tree.heading("flow mfc1", text="Flow MFC 1 (mL/min)")
        self.onoffsteps_tree.heading("flow mfc2", text="Flow MFC 2 (mL/min)")
        self.onoffsteps_tree.heading("flow mfc3", text="Flow MFC 3 (mL/min)")
        # # Cooling OFF // Koeling Uitzetten omdat hij het nog niet doet
        # self.onoffsteps_tree.heading("temp", text="Temperature (°C)")
        self.onoffsteps_tree.heading("valve", text="Valve Position (1 or 2)")
        
        self.onoffsteps_tree.column("time", width=80, anchor=tk.CENTER)
        self.onoffsteps_tree.column("flow mfc1", width=100, anchor=tk.CENTER)
        self.onoffsteps_tree.column("flow mfc2", width=100, anchor=tk.CENTER)
        self.onoffsteps_tree.column("flow mfc3", width=100, anchor=tk.CENTER)
        # # Cooling OFF // Koeling Uitzetten omdat hij het nog niet doet
        # self.onoffsteps_tree.column("temp", width=100, anchor=tk.CENTER)
        self.onoffsteps_tree.column("valve", width=80, anchor=tk.CENTER)
        
        self.onoffsteps_tree.pack(fill = 'both' , expand=True)
        
        step_controls_frame = ttk.Frame(edit_frame)
        step_controls_frame.pack(fill='x', padx=5, pady=5)
        
        self.onoffprofile_time_label = ttk.Label(step_controls_frame, text="Time (s):").pack(side='left')
        self.onoffstep_time_var = tk.DoubleVar()
        step_time_entry = ttk.Entry(step_controls_frame, textvariable=self.onoffstep_time_var, width=8)
        step_time_entry.pack(side='left', padx=2)
        
        self.onoffprofile_mfc1_label = ttk.Label(step_controls_frame, text="Flow MFC 1 (mL/min):").pack(side='left')
        self.onoffstep_flow1_var = tk.DoubleVar()
        step_flow1_entry = ttk.Entry(step_controls_frame, textvariable=self.onoffstep_flow1_var, width=8)
        step_flow1_entry.pack(side='left', padx=2)

        self.onoffprofile_mfc2_label = ttk.Label(step_controls_frame, text="Flow MFC 2 (mL/min):").pack(side='left')
        self.onoffstep_flow2_var = tk.DoubleVar()
        step_flow2_entry = ttk.Entry(step_controls_frame, textvariable=self.onoffstep_flow2_var, width=8)
        step_flow2_entry.pack(side='left', padx=2)

        self.onoffprofile_mfc3_label = ttk.Label(step_controls_frame, text="Flow MFC 3 (mL/min):").pack(side='left')
        self.onoffstep_flow3_var = tk.DoubleVar()
        step_flow3_entry = ttk.Entry(step_controls_frame, textvariable=self.onoffstep_flow3_var, width=8)
        step_flow3_entry.pack(side='left', padx=2)

        # # Cooling OFF // Koeling Uitzetten omdat hij het nog niet doet
        # self.onoffprofile_mfc4_label = ttk.Label(step_controls_frame, text="Temperature (°C):").pack(side='left')
        # self.onoffstep_temp_var = tk.DoubleVar()
        # step_temp_entry = ttk.Entry(step_controls_frame, textvariable=self.onoffstep_temp_var, width=8)
        # step_temp_entry.pack(side='left', padx=2)
        
        self.onoffprofile_valve_label =  ttk.Label(step_controls_frame, text="Valve Position:").pack(side='left')
        self.onoffstep_valve_var = tk.IntVar() #integer variable, since the valve should be position on 1/2
        step_onoff_combo = ttk.Combobox(
            step_controls_frame, 
            textvariable=self.onoffstep_valve_var, 
            values=[1, 2], 
            width=5
        )
        step_onoff_combo.pack(side='left', padx=2)
        
        # Step buttons
        step_buttons_frame = ttk.Frame(edit_frame)
        step_buttons_frame.pack(fill='both')
        
        add_step_button = ttk.Button(step_buttons_frame, text="Add Step", command=self.onoffadd_step)
        add_step_button.pack(side='left', padx=2)
        
        remove_step_button = ttk.Button(step_buttons_frame, text="Remove Step", command=self.onoffremove_step)
        remove_step_button.pack(side='left', padx=2)
        
        clear_steps_button = ttk.Button(step_buttons_frame, text="Clear All Steps", command=self.onoffclear_steps)
        clear_steps_button.pack(side='left', padx=2)
        
        # Save and run buttons
        action_buttons_frame = ttk.Frame(edit_frame)
        action_buttons_frame.pack(fill='both')
        
        save_button = ttk.Button(action_buttons_frame, text="Save Profile", command=self.save_onoffprofile)
        save_button.pack(side='left', padx=2)
        
        run_button = ttk.Button(action_buttons_frame, text="Run Profile", command=self.run_onoffprofile)
        run_button.pack(side='left', padx=2)
        
        self.onoffstop_button = ttk.Button(action_buttons_frame, text="Stop", command=self.stop_onoffprofile)
        self.onoffstop_button.pack(side='left', padx=2)
        self.onoffstop_button.config(state=tk.DISABLED)
    
        # Initialize variables
        self.current_loaded_onoffprofile = None
        
    def create_mfcprofile_tab(self):
        # profile_tab = ttk.Frame(self.notebook)
        # profile_tab.pack(fill = 'both', expand = True)
        # self.notebook.add(profile_tab, text = 'MFCs Profile Management')

        ##Make it scrollable
        profile_tab = self.create_scrollable_tab(self.notebook, "MFCs Profile Management")        
        # ## Split into two frames
        list_frame = ttk.Frame(profile_tab, width = 400)
        list_frame.pack(side= 'left', fill = 'both', expand=True, padx=10, pady=10)
        list_frame.pack_propagate(False)

        
        edit_frame = ttk.Frame(profile_tab)
        edit_frame.pack(side= 'right', fill= 'both', expand=True, padx=10, pady=10)
        
        ### Left frame / list frame
        ## Profile listbox with scrollbar
        # https://www.pythontutorial.net/tkinter/tkinter-listbox/#adding-a-scrollbar-to-the-listbox
        # Making an empty profile listbox
        self.mfcprofile_listbox = tk.Listbox(list_frame, selectmode = tk.SINGLE)
        self.mfcprofile_listbox.pack(fill= 'both', expand=True, padx=5, pady=5)
    
        # Putting all the profiles in the profile listbox
        self.update_mfcprofile_list()
        
        #Adding a scrollbar to the profile listbox
        v_scrollbar = ttk.Scrollbar(self.mfcprofile_listbox, orient = tk.VERTICAL, command = self.mfcprofile_listbox.yview)
        
        self.mfcprofile_listbox['yscrollcommand'] = v_scrollbar.set
        v_scrollbar.pack(side='right', fill='y')
        
        ##Adding the buttons to the left frame (list frame)
        # Profile list buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        load_button = ttk.Button(button_frame, text="Load", command=self.load_mfcprofile)
        load_button.pack(side='left', padx=3, expand=True)
        
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_mfcprofile)
        delete_button.pack(side='left', padx=3, expand=True)
        
        ##Right frame / edit frame
        # Profile info
        info_frame = ttk.Frame(edit_frame)
        info_frame.pack(fill='both', padx=5, pady=5)
        
        self.new_mfcprofile_label = ttk.Label(info_frame, text="")
        self.new_mfcprofile_label.pack(side = 'left', padx=5, expand=True, fill='x')
        
        ttk.Label(info_frame, text="Name:").pack(side='left')
        self.mfcname_var = tk.StringVar()
        name_entry = ttk.Entry(info_frame, textvariable=self.mfcname_var)
        name_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        ttk.Label(info_frame, text="Description:").pack(side='left')
        self.mfcdesc_var = tk.StringVar()
        desc_entry = ttk.Entry(info_frame, textvariable=self.mfcdesc_var)
        desc_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        new_profile_btn = ttk.Button(info_frame, text = 'New Profile', command = self.create_new_mfcprofile)
        new_profile_btn.pack(side='right', padx=3, expand=True)
        
        # Steps in the right/frame
        steps_frame = ttk.Frame(edit_frame)
        steps_frame.pack(fill = 'both' , expand=True, padx=5, pady=5)
        
        #https://tk-tutorial.readthedocs.io/en/latest/tree/tree.html
        self.mfcsteps_tree = ttk.Treeview(
            steps_frame, 
            ## NO COOLING
            # columns=("time", "flow mfc1", "flow mfc2", "flow mfc3", "temp", "valve"), 
            columns=("time", "flow mfc1", "flow mfc2", "flow mfc3", "valve"), 
            show="headings"
        )
        self.mfcsteps_tree.heading("time", text="Time (s)")
        self.mfcsteps_tree.heading("flow mfc1", text="Flow MFC 1 (mL/min)")
        self.mfcsteps_tree.heading("flow mfc2", text="Flow MFC 2 (mL/min)")
        self.mfcsteps_tree.heading("flow mfc3", text="Flow MFC 3 (mL/min)")
        
        self.mfcsteps_tree.column("time", width=250, anchor=tk.CENTER)
        self.mfcsteps_tree.column("flow mfc1", width=250, anchor=tk.CENTER)
        self.mfcsteps_tree.column("flow mfc2", width=250, anchor=tk.CENTER)
        self.mfcsteps_tree.column("flow mfc3", width=250, anchor=tk.CENTER)
        
        self.mfcsteps_tree.pack(fill = 'both' , expand=True)
        
        step_controls_frame = ttk.Frame(edit_frame)
        step_controls_frame.pack(fill='x', padx=5, pady=5)
        
        self.mfcprofile_time_label = ttk.Label(step_controls_frame, text="Time (s):").pack(side='left')
        self.mfcstep_time_var = tk.DoubleVar()
        step_time_entry = ttk.Entry(step_controls_frame, textvariable=self.mfcstep_time_var, width=8)
        step_time_entry.pack(side='left', padx=5)
        
        self.mfcprofile_mfc1_label = ttk.Label(step_controls_frame, text="Flow MFC 1 (mL/min):").pack(side='left')
        self.mfcstep_flow1_var = tk.DoubleVar()
        step_flow1_entry = ttk.Entry(step_controls_frame, textvariable=self.mfcstep_flow1_var, width=8)
        step_flow1_entry.pack(side='left', padx=5)

        self.mfcprofile_mfc2_label = ttk.Label(step_controls_frame, text="Flow MFC 2 (mL/min):").pack(side='left')
        self.mfcstep_flow2_var = tk.DoubleVar()
        step_flow2_entry = ttk.Entry(step_controls_frame, textvariable=self.mfcstep_flow2_var, width=8)
        step_flow2_entry.pack(side='left', padx=5)

        self.mfcprofile_mfc3_label = ttk.Label(step_controls_frame, text="Flow MFC 3 (mL/min):").pack(side='left')
        self.mfcstep_flow3_var = tk.DoubleVar()
        step_flow3_entry = ttk.Entry(step_controls_frame, textvariable=self.mfcstep_flow3_var, width=8)
        step_flow3_entry.pack(side='left', padx=5)
        
        # Step buttons
        step_buttons_frame = ttk.Frame(edit_frame)
        step_buttons_frame.pack(fill='both')
        
        add_step_button = ttk.Button(step_buttons_frame, text="Add Step", command=self.add_mfcstep)
        add_step_button.pack(side='left', padx=2)
        
        remove_step_button = ttk.Button(step_buttons_frame, text="Remove Step", command=self.remove_mfcstep)
        remove_step_button.pack(side='left', padx=2)
        
        clear_steps_button = ttk.Button(step_buttons_frame, text="Clear All Steps", command=self.clear_mfcsteps)
        clear_steps_button.pack(side='left', padx=2)
        
        # Save and run buttons
        action_buttons_frame = ttk.Frame(edit_frame)
        action_buttons_frame.pack(fill='both')
        
        save_button = ttk.Button(action_buttons_frame, text="Save Profile", command=self.save_mfcprofile)
        save_button.pack(side='left', padx=2)
        
        run_button = ttk.Button(action_buttons_frame, text="Run Profile", command=self.run_mfcprofile)
        run_button.pack(side='left', padx=2)
        
        self.mfcstop_button = ttk.Button(action_buttons_frame, text="Stop", command=self.stop_mfcprofile)
        self.mfcstop_button.pack(side='left', padx=2)
        self.mfcstop_button.config(state=tk.DISABLED)
        
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF        
    # def create_coolingprofile_tab(self):
    #     profile_tab = ttk.Frame(self.notebook)
    #     profile_tab.pack(fill = 'both', expand = True)
    #     self.notebook.add(profile_tab, text = 'Digital chilling/heating dry bath Profile Management')
        
    #     # ## Split into two frames
    #     list_frame = ttk.Frame(profile_tab, width = 400)
    #     list_frame.pack(side= 'left', fill = 'both', expand=True, padx=10, pady=10)
    #     list_frame.pack_propagate(False)

        
    #     edit_frame = ttk.Frame(profile_tab)
    #     edit_frame.pack(side= 'right', fill= 'both', expand=True, padx=10, pady=10)
        
    #     ### Left frame / list frame
    #     ## Profile listbox with scrollbar
    #     # https://www.pythontutorial.net/tkinter/tkinter-listbox/#adding-a-scrollbar-to-the-listbox
    #     # Making an empty profile listbox
    #     self.coolingprofile_listbox = tk.Listbox(list_frame, selectmode = tk.SINGLE)
    #     self.coolingprofile_listbox.pack(fill= 'both', expand=True, padx=5, pady=5)
    
    #     # Putting all the profiles in the profile listbox
    #     self.update_coolingprofile_list()
        
    #     #Adding a scrollbar to the profile listbox
    #     v_scrollbar = ttk.Scrollbar(self.coolingprofile_listbox, orient = tk.VERTICAL, command = self.coolingprofile_listbox.yview)
        
    #     self.coolingprofile_listbox['yscrollcommand'] = v_scrollbar.set
    #     v_scrollbar.pack(side='right', fill='y')
        
    #     ##Adding the buttons to the left frame (list frame)
    #     # Profile list buttons
    #     button_frame = ttk.Frame(list_frame)
    #     button_frame.pack(fill='x', padx=5, pady=5)
        
    #     load_button = ttk.Button(button_frame, text="Load", command=self.load_coolingprofile)
    #     load_button.pack(side='left', padx=3, expand=True)
        
    #     delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_coolingprofile)
    #     delete_button.pack(side='left', padx=3, expand=True)
        
    #     ##Right frame / edit frame
    #     # Profile info
    #     info_frame = ttk.Frame(edit_frame)
    #     info_frame.pack(fill='both', padx=5, pady=5)
        
    #     self.new_coolingprofile_label = ttk.Label(info_frame, text="")
    #     self.new_coolingprofile_label.pack(side = 'left', padx=5, expand=True, fill='x')
        
    #     ttk.Label(info_frame, text="Name:").pack(side='left')
    #     self.coolingname_var = tk.StringVar()
    #     name_entry = ttk.Entry(info_frame, textvariable=self.coolingname_var)
    #     name_entry.pack(side='left', padx=5, expand=True, fill='x')
        
    #     ttk.Label(info_frame, text="Description:").pack(side='left')
    #     self.coolingdesc_var = tk.StringVar()
    #     desc_entry = ttk.Entry(info_frame, textvariable=self.coolingdesc_var)
    #     desc_entry.pack(side='left', padx=5, expand=True, fill='x')
        
    #     new_profile_btn = ttk.Button(info_frame, text = 'New Profile', command = self.create_new_coolingprofile)
    #     new_profile_btn.pack(side='right', padx=3, expand=True)
        
    #     # Steps in the right/frame
    #     steps_frame = ttk.Frame(edit_frame)
    #     steps_frame.pack(fill = 'both' , expand=True, padx=5, pady=5)
        
    #     #https://tk-tutorial.readthedocs.io/en/latest/tree/tree.html
    #     self.coolingsteps_tree = ttk.Treeview(
    #         steps_frame, 
    #         columns=("time", "temp"), 
    #         show="headings"
    #     )
    #     self.coolingsteps_tree.heading("time", text="Time (s)")
    #     self.coolingsteps_tree.heading("temp", text="Temperature (°C)")
        
    #     self.coolingsteps_tree.column("time", width=250, anchor=tk.CENTER)
    #     self.coolingsteps_tree.column("temp", width=250, anchor=tk.CENTER)
    #     self.coolingsteps_tree.pack(fill = 'both' , expand=True)
        
    #     step_controls_frame = ttk.Frame(edit_frame)
    #     step_controls_frame.pack(fill='x', padx=5, pady=5)
        
    #     self.coolingprofile_time_label = ttk.Label(step_controls_frame, text="Time (s):").pack(side='left')
    #     self.coolingstep_time_var = tk.DoubleVar()
    #     step_time_entry = ttk.Entry(step_controls_frame, textvariable=self.coolingstep_time_var, width=8)
    #     step_time_entry.pack(side='left', padx=5)
        
    #     self.coolingprofile_temp_label = ttk.Label(step_controls_frame, text="Temperature (°C):").pack(side='left')
    #     self.coolingstep_temp_var = tk.DoubleVar()
    #     step_temp_entry = ttk.Entry(step_controls_frame, textvariable=self.coolingstep_temp_var, width=8)
    #     step_temp_entry.pack(side='left', padx=2)
        
    #     # Step buttons
    #     step_buttons_frame = ttk.Frame(edit_frame)
    #     step_buttons_frame.pack(fill='both')
        
    #     add_step_button = ttk.Button(step_buttons_frame, text="Add Step", command=self.add_coolingstep)
    #     add_step_button.pack(side='left', padx=2)
        
    #     remove_step_button = ttk.Button(step_buttons_frame, text="Remove Step", command=self.remove_coolingstep)
    #     remove_step_button.pack(side='left', padx=2)
        
    #     clear_steps_button = ttk.Button(step_buttons_frame, text="Clear All Steps", command=self.clear_coolingsteps)
    #     clear_steps_button.pack(side='left', padx=2)
        
    #     # Save and run buttons
    #     action_buttons_frame = ttk.Frame(edit_frame)
    #     action_buttons_frame.pack(fill='both')
        
    #     save_button = ttk.Button(action_buttons_frame, text="Save Profile", command=self.save_coolingprofile)
    #     save_button.pack(side='left', padx=2)
        
    #     run_button = ttk.Button(action_buttons_frame, text="Run Profile", command=self.run_coolingprofile)
    #     run_button.pack(side='left', padx=2)
        
    #     self.coolingstop_button = ttk.Button(action_buttons_frame, text="Stop", command=self.stop_coolingprofile)
    #     self.coolingstop_button.pack(side='left', padx=2)
    #     self.coolingstop_button.config(state=tk.DISABLED)
        
    #     # # Status bar, to show what has been adjusted
    #     # self.status_var = tk.StringVar() 
    #     # self.status_bar = ttk.Label(edit_frame, textvariable=self.status_var)
    #     # self.status_bar.pack(fill='both', padx=5, pady=5)
        
    #     # Initialize variables
    #     # self.coolingcurrent_loaded_profile = None
    
    def create_valveprofile_tab(self):
        # profile_tab = ttk.Frame(self.notebook)
        # profile_tab.pack(fill = 'both', expand = True)
        # self.notebook.add(profile_tab, text = 'Valve Profile Management')

        ##Make it scrollable
        profile_tab = self.create_scrollable_tab(self.notebook, "Valve Profile Management")      
                
        # ## Split into two frames
        list_frame = ttk.Frame(profile_tab, width = 400)
        list_frame.pack(side= 'left', fill = 'both', expand=True, padx=10, pady=10)
        list_frame.pack_propagate(False)

        edit_frame = ttk.Frame(profile_tab)
        edit_frame.pack(side= 'right', fill= 'both', expand=True, padx=10, pady=10)
        
        ### Left frame / list frame
        ## Profile listbox with scrollbar
        # https://www.pythontutorial.net/tkinter/tkinter-listbox/#adding-a-scrollbar-to-the-listbox
        # Making an empty profile listbox
        self.valveprofile_listbox = tk.Listbox(list_frame, selectmode = tk.SINGLE)
        self.valveprofile_listbox.pack(fill= 'both', expand=True, padx=5, pady=5)
    
        # Putting all the profiles in the profile listbox
        self.update_valveprofile_list()
        
        #Adding a scrollbar to the profile listbox
        v_scrollbar = ttk.Scrollbar(self.valveprofile_listbox, orient = tk.VERTICAL, command = self.valveprofile_listbox.yview)
        
        self.valveprofile_listbox['yscrollcommand'] = v_scrollbar.set
        v_scrollbar.pack(side='right', fill='y')
        
        ##Adding the buttons to the left frame (list frame)
        # Profile list buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        load_button = ttk.Button(button_frame, text="Load", command=self.load_valveprofile)
        load_button.pack(side='left', padx=3, expand=True)
        
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_valveprofile)
        delete_button.pack(side='left', padx=3, expand=True)
        
        ##Right frame / edit frame
        # Profile info
        info_frame = ttk.Frame(edit_frame)
        info_frame.pack(fill='both', padx=5, pady=5)
        
        self.new_valveprofile_label = ttk.Label(info_frame, text="")
        self.new_valveprofile_label.pack(side = 'left', padx=5, expand=True, fill='x')
        
        ttk.Label(info_frame, text="Name:").pack(side='left')
        self.valvename_var = tk.StringVar()
        name_entry = ttk.Entry(info_frame, textvariable=self.valvename_var)
        name_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        ttk.Label(info_frame, text="Description:").pack(side='left')
        self.valvedesc_var = tk.StringVar()
        desc_entry = ttk.Entry(info_frame, textvariable=self.valvedesc_var)
        desc_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        new_profile_btn = ttk.Button(info_frame, text = 'New Profile', command = self.create_new_valveprofile)
        new_profile_btn.pack(side='right', padx=3, expand=True)
        
        # Steps in the right/frame
        steps_frame = ttk.Frame(edit_frame)
        steps_frame.pack(fill = 'both' , expand=True, padx=5, pady=5)
        
        #https://tk-tutorial.readthedocs.io/en/latest/tree/tree.html
        self.valvesteps_tree = ttk.Treeview(
            steps_frame, 
            columns=("time", "valve1", "valve2"), 
            show="headings"
        )
        self.valvesteps_tree.heading("time", text="Time (s)")
        self.valvesteps_tree.heading("valve1", text="RVM 1 Position (1/2)")
        self.valvesteps_tree.heading("valve2", text="RVM 2 Position (1/2)")
        
        self.valvesteps_tree.column("time", width=250, anchor=tk.CENTER)
        self.valvesteps_tree.column("valve1", width=250, anchor=tk.CENTER)
        self.valvesteps_tree.column("valve2", width=250, anchor=tk.CENTER)
                
        self.valvesteps_tree.pack(fill = 'both' , expand=True)
        
        step_controls_frame = ttk.Frame(edit_frame)
        step_controls_frame.pack(fill='x', padx=5, pady=5)
        
        self.valveprofile_time_label = ttk.Label(step_controls_frame, text="Time (s):").pack(side='left')
        self.valvestep_time_var = tk.DoubleVar()
        step_time_entry = ttk.Entry(step_controls_frame, textvariable=self.valvestep_time_var, width=8)
        step_time_entry.pack(side='left', padx=5)
        
        self.valveprofile_valve1_label =  ttk.Label(step_controls_frame, text="Valve 1 Position:").pack(side='left')
        self.valvestep_valve1_var = tk.IntVar() #integer variable, since the valve should be position on 1/2
        step_valve_combo = ttk.Combobox(
            step_controls_frame, 
            textvariable=self.valvestep_valve1_var, 
            values=[1, 2], 
            width=5
        )
        step_valve_combo.pack(side='left', padx=2)

        self.valveprofile_valve2_label =  ttk.Label(step_controls_frame, text="Valve 1 Position:").pack(side='left')
        self.valvestep_valve2_var = tk.IntVar() #integer variable, since the valve should be position on 1/2
        step_valve_combo = ttk.Combobox(
            step_controls_frame, 
            textvariable=self.valvestep_valve2_var, 
            values=[1, 2], 
            width=5
        )
        step_valve_combo.pack(side='left', padx=2)
        
        # Step buttons
        step_buttons_frame = ttk.Frame(edit_frame)
        step_buttons_frame.pack(fill='both')
        
        add_step_button = ttk.Button(step_buttons_frame, text="Add Step", command=self.add_valvestep)
        add_step_button.pack(side='left', padx=2)
        
        remove_step_button = ttk.Button(step_buttons_frame, text="Remove Step", command=self.remove_valvestep)
        remove_step_button.pack(side='left', padx=2)
        
        clear_steps_button = ttk.Button(step_buttons_frame, text="Clear All Steps", command=self.clear_valvesteps)
        clear_steps_button.pack(side='left', padx=2)
        
        # Save and run buttons
        action_buttons_frame = ttk.Frame(edit_frame)
        action_buttons_frame.pack(fill='both')
        
        save_button = ttk.Button(action_buttons_frame, text="Save Profile", command=self.save_valveprofile)
        save_button.pack(side='left', padx=2)
        
        run_button = ttk.Button(action_buttons_frame, text="Run Profile", command=self.run_valveprofile)
        run_button.pack(side='left', padx=2)
        
        self.valvestop_button = ttk.Button(action_buttons_frame, text="Stop", command=self.stop_valveprofile)
        self.valvestop_button.pack(side='left', padx=2)
        self.valvestop_button.config(state=tk.DISABLED)
        
        # # Status bar, to show what has been adjusted
        # self.status_var = tk.StringVar() 
        # self.status_bar = ttk.Label(edit_frame, textvariable=self.status_var)
        # self.status_bar.pack(fill='both', padx=5, pady=5)
        
        # Initialize variables
        # self.valvecurrent_loaded_profile = None

    def connect_MFC(self, index):
        if self.mfcs[index].connect():
            #messagebox.showinfo("Connection", "MFC successfully connected.")
            #updating the connection info
            self.update_connection_devices()
            self.status_var.set(f"MFC {index + 1} connected")
            self.keep_updating_mfc = True
        else:
            messagebox.showinfo("Connection Failed", f"MFC {index + 1} is not connected")

    def disconnect_MFC(self, index):
        self.mfcs[index].disconnect()
        self.keep_updating_mfc = False
        #messagebox.showinfo("Disconnected", "MFC disconnected successfully.")
        #updating the connection info
        self.update_connection_devices()
        self.status_var.set(f"MFC {index + 1} disconnected")
    
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
    # def connect_cooling(self):  
    #     if self.cooling.connect():
    #         #messagebox.showinfo("Connection", "Torrey Pines IC20XR Digital Chilling/Heating Dry Baths successfully connected.")
    #         #updating the connection info
    #         self.keep_updating_cooling = False
    #         self.update_connection_devices()
    #         self.status_var.set(f"Torrey Pines IC20XR Digital Chilling/Heating Dry Baths connected")
    #     else:
    #         messagebox.showinfo("Connection Failed", "Cooling is not connected")
         
    # def disconnect_cooling(self):
    #     self.cooling.disconnect()
    #     self.keep_updating_cooling = False
    #     #messagebox.showinfo("Disconnected", "Torrey Pines IC20XR Digital Chilling/Heating Dry Baths disconnected successfully.")
    #     #updating the connection info
    #     self.update_connection_devices()
    #     self.status_var.set(f"Torrey Pines IC20XR Digital Chilling/Heating Dry Baths disconnected")

    def connect_valve(self, index):  
        if self.valve[index].connect():
            self.keep_updating_valve = True
            #messagebox.showinfo("Connection", "RVM Industrial Microfluidic Rotary valve is successfully connected.")
            #updating the connection info
            self.update_connection_devices()
            
            #initializing the home position of the valve
            self.currentposition = 1
            
            self.status_var.set(f"RVM {index} connected and set to home position {self.currentposition}")
        else:
            messagebox.showinfo("Connection Failed", "RVM is not connected")
         
    def disconnect_valve(self, index):
        self.valve[index].disconnect()
        self.keep_updating_valve = False
        #messagebox.showinfo("Disconnected", "RVM Industrial Microfluidic Rotary valve is disconnected successfully.")
        #updating the connection info
        self.update_connection_devices()
        self.status_var.set(f"RVM {index} disconnected")

    def connect_all_devices(self):
        self.connect_MFC(index = 0)
        self.connect_MFC(index = 1)
        self.connect_MFC(index = 2)
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # self.connect_cooling()
        self.connect_valve(index = 0)
        self.connect_valve(index = 1)
        self.status_var.set(f"MFCs, Torrey Pines IC20XR Digital Chilling/Heating Dry Baths and RVM Industrial Microfluidic Rotary valves connected")
   
    def update_connection_devices(self):
        #Labels at the Header
        self.connection_mfc1_port_label.config (text=f"MFC 1 Port: {self.mfcs[0].port}, Connected: {self.mfcs[0].connected}")
        self.connection_mfc2_port_label.config (text=f"MFC 2 Port: {self.mfcs[1].port}, Connected: {self.mfcs[1].connected}")
        self.connection_mfc3_port_label.config (text=f"MFC 3 Port: {self.mfcs[2].port}, Connected: {self.mfcs[2].connected}")
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # self.connection_cooling_port_label.config(text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}")
        self.connection_valve1_port_label.config(text=f"RVM 1 Port: {self.valve[0].port}, Connected: {self.valve[0].connected}")
        self.connection_valve2_port_label.config(text=f"RVM 2 Port: {self.valve[1].port}, Connected: {self.valve[1].connected}")

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
        
        ttk.Label(MFC_frame, text="MFC 1 Port:").grid(row=0, column=0, padx=5, pady=5)
        self.MFC1_port_var = tk.StringVar(value=self.mfcs[0].port)
        MFC1_port_entry = ttk.Entry(MFC_frame, textvariable=self.MFC1_port_var)
        MFC1_port_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(MFC_frame, text="MFC 2 Port:").grid(row=1, column=0, padx=5, pady=5)
        self.MFC2_port_var = tk.StringVar(value=self.mfcs[1].port)
        MFC2_port_entry = ttk.Entry(MFC_frame, textvariable=self.MFC2_port_var)
        MFC2_port_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(MFC_frame, text="MFC 3 Port:").grid(row=2, column=0, padx=5, pady=5)
        self.MFC3_port_var = tk.StringVar(value=self.mfcs[2].port)
        MFC3_port_entry = ttk.Entry(MFC_frame, textvariable=self.MFC3_port_var)
        MFC3_port_entry.grid(row=2, column=1, padx=5, pady=5)

        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # # Cooling settings
        # cooling_frame = ttk.LabelFrame(settings_window, text="Torrey Pines IC20XR Digital Chilling/Heating Dry Baths")
        # cooling_frame.pack(fill="both", padx=10, pady=10)
        
        # ttk.Label(cooling_frame, text="Port:").grid(row=3, column=0, padx=5, pady=5)
        # self.cooling_port_var = tk.StringVar(value=self.cooling.port)
        # cooling_port_entry = ttk.Entry(cooling_frame, textvariable=self.cooling_port_var)
        # cooling_port_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # valve settings
        valve_frame = ttk.LabelFrame(settings_window, text="RVM Industrial Microfluidic Rotary valve ")
        valve_frame.pack(fill="both", padx=10, pady=10)
        
        ttk.Label(valve_frame, text="RVM 1 Port:").grid(row=4, column=0, padx=5, pady=5)
        self.valve1_port_var = tk.StringVar(value=self.valve[0].port)
        valve1_port_entry = ttk.Entry(valve_frame, textvariable=self.valve1_port_var)
        valve1_port_entry.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(valve_frame, text="RVM 2 Port:").grid(row=5, column=0, padx=5, pady=5)
        self.valve2_port_var = tk.StringVar(value=self.valve[1].port)
        valve2_port_entry = ttk.Entry(valve_frame, textvariable=self.valve2_port_var)
        valve2_port_entry.grid(row=5, column=1, padx=5, pady=5)
        
        # Profile path setting
        profile_frame = ttk.LabelFrame(settings_window, text="Settings Path")
        profile_frame.pack(fill="both", padx=10, pady=10)

        path_label = ttk.Label(profile_frame, text="Path:")
        path_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.settings_path_var = tk.StringVar(value=self.settings_manager.get_profiles_path())
        ttk.Entry(profile_frame, textvariable=self.settings_path_var, width=35).grid(row=0, column=1, padx=5, pady=5)

        def browse_profile_path():
            path = filedialog.askdirectory()
            if path:
                self.settings_path_var.set(path)

        browse_button = ttk.Button(profile_frame, text="Bladeren...", command=browse_profile_path)
        browse_button.grid(row=0, column=2, padx=5, pady=5)

        save_button = ttk.Button(settings_window, text="Save", command=self.save_settings)
        save_button.pack(pady=10)
        
    def save_settings(self):
        com_ports = {
            "mfc1": self.MFC1_port_var.get(),
            "mfc2": self.MFC2_port_var.get(),
            "mfc3": self.MFC3_port_var.get(),
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
            # "cooling": self.cooling_port_var.get(),
            
            "valve1": self.valve1_port_var.get(),
            "valve2": self.valve2_port_var.get()
        }
        self.settings_manager.set_com_ports(com_ports)     
        
        new_path = self.settings_path_var.get()
        self.settings_manager.set_profiles_path(new_path)
        
        self.reload_all_devices()   
        self.status_var.set("The settings are updated.")

    def reload_all_devices(self):
        # Disconnect all devices if they're connected
        if self.mfcs[0].connected:
            self.disconnect_MFC(0)
        if self.mfcs[1].connected:
            self.disconnect_MFC(1)
        if self.mfcs[2].connected:
            self.disconnect_MFC(2)
            
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # if self.cooling.connected:
        #     self.disconnect_cooling()
        if self.valve[0].connected:
            self.disconnect_valve(index = 0)
        if self.valve[1].connected:
            self.disconnect_valve(index = 1)
            
        #Obtain the new assigned comports
        saved_ports = self.settings_manager.get_com_ports()
        new_path = self.settings_path_var.get()
        print(saved_ports, new_path)

        # Update the devices to the new COM-ports
        self.settings_manager = SettingsManager(base_dir = new_path)
        self.mfcprofilemanager = MFCProfileManager(saved_ports["mfc1"], saved_ports["mfc2"], saved_ports["mfc3"], new_path)
            ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # self.coolingprofilemanager = CoolingProfileManager(saved_ports["cooling"], new_path)
        self.valveprofilemanager = TwoRVMProfileManager(saved_ports["valve1"],saved_ports["valve2"], new_path)

        # Update the devices
        self.mfcs = self.mfcprofilemanager.mfcs
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # self.cooling = self.coolingprofilemanager.cooling
        self.valve = self.valveprofilemanager.valve

        # Update the OnOffProfileManager
        self.onoffprofilemanager = OnoffProfileManager(
            UImfcs=self.mfcs,

        ##Koeling Uitzetten omdat hij het nog niet doet
        # # # Cooling OFF
        #     UIcooling=self.cooling,
            UIvalve=self.valve,
            profiles_dir= new_path
        )

        # Update the UI labels
        self.connection_mfc1_port_label.config(text=f"MFC 1 Port: {self.mfcs[0].port}, Connected: {self.mfcs[0].connected}")
        self.connection_mfc2_port_label.config(text=f"MFC 2 Port: {self.mfcs[1].port}, Connected: {self.mfcs[1].connected}")
        self.connection_mfc3_port_label.config(text=f"MFC 3 Port: {self.mfcs[2].port}, Connected: {self.mfcs[2].connected}")
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # self.connection_cooling_port_label.config(text=f"Cooling Port: {self.cooling.port}, Connected: {self.cooling.connected}")
        self.connection_valve1_port_label.config(text=f"RVM 1 Port: {self.valve[0].port}, Connected: {self.valve[0].connected}")
        self.connection_valve2_port_label.config(text=f"RVM 2 Port: {self.valve[1].port}, Connected: {self.valve[1].connected}")

    def set_MFCmassflow(self, index):
        massflowrate = self.massflow_vars[index].get()
        if self.mfcs[index].set_massflow(massflowrate):
            self.target_massflow_labels[index].config(text=f"Target mass flow rate: {self.mfcs[index].targetmassflow} mL/min")
            self.update_massflow(index)
        else:
            self.status_var.set("MFC: Failed to set mass flow rate.")
            
    def update_massflow(self, index):
        #when the UI is closed then this won't be "updating" (to debug)
        try:
            if not self.root.winfo_exists():
                return
            
            if not self.keep_updating_mfc:
                return
            
            # current_flow = self.mfcs[index].get_massflow()[0]['data']
            
            #### TO SIMULATE
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
        except tk.TclError:
            return
            
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
    # def set_temperature(self):
    #     if self.cooling.connected is False:
    #         messagebox.showwarning("Device not connected", "The Torrey Pines IC20XR Digital Chilling/Heating Dry Baths is not connected")
    #         return False
    #     elif not isinstance(self.ambient_temp, (int, float)):
    #         messagebox.showwarning("Invalid Input", "Ambient Temperature has not been set yet or is an non-numeric value.")
    #         return False
    #     else:    
    #         try:
    #             temperature = float(self.temperature_var.get())
    #             self.cooling.set_temperature(temperature, self.ambient_temp)
    #             self.target_temperature_label.config(text=f"Target temperature: {self.cooling.targettemperature:.2f} °C")
    #             self.update_temperature()
                
    #             ##if non-floating number, tk.tclerror occurs
    #         except tk.TclError as e:
    #             messagebox.showerror("Invalid Input", f"Please enter a floating number for target temperature. {e}")
                
    # def update_temperature(self):    
    #     #when the UI is closed then this won't be "updating" (to debug)
    #     if not self.root.winfo_exists():
    #         return
            
    #     if not self.keep_updating_cooling:
    #         return

    #     current_temp = self.cooling.get_temperature()
    #     self.update_run_var()
    #     if current_temp is not None:
    #         self.current_temperature_label.config(text=f"Current temperature: {current_temp:.2f} °C")
    #     else:
    #         self.status_var.set("Failed to read the temperature.")
        
    #     #Updating temperature every 1s; otherwise the simulation/reading the data won't work. It would only happen one time.
    #     #https://www.geeksforgeeks.org/python-after-method-in-tkinter/
    #     self.root.after(1000, self.update_temperature) 
        
    def set_valve(self, index):
        position = self.position_vars[index].get()
        if self.valve[index].switch_position(position):
            self.target_position_labels[index].config(text=f"Target position of the valve: {position}")
            self.update_valve(index)
        else:
            self.status_var.set("Valve:  Failed to set the valve position")

    def update_valve(self, index):
        try:
            if not self.root.winfo_exists():
                return
            
            if not self.keep_updating_valve:
                return
            target_position = self.valve[index].get_position()
            self.update_run_var()
            if target_position is not None:
                if self.currentposition != target_position:                
                    self.current_position_labels[index].config(text=f"Current position of the valve: {target_position}")
                    self.status_var.set(f"The position is set to {target_position}.")
                else:
                    self.status_var.set(f"The target position is the current position, position {target_position}.")
            else:
                self.status_var.set("Failed to read the position of the valve.")
        except tk.TclError:
            return
    ####MFC PROFILE
    def update_mfcprofile_list(self):
        """Refresh the list of available profiles"""
        #https://youtu.be/Vm0ivVxNaA8
        
        #Delete all the items from the listbox
        self.mfcprofile_listbox.delete(0, tk.END)
        
        #Add all the profiles to the listbox
        for profile in self.mfcprofilemanager.get_profiles():
            #Append the profiles at the end
            self.mfcprofile_listbox.insert(tk.END, profile)  #listbox.insert(index, element)

    def load_mfcprofile(self):
        """Load the selected profile into the editor"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.mfcprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to load")
            return
        
        #To ensure that you only select the first selected
        profile_name = self.mfcprofile_listbox.get(selection[0])
        profile = self.mfcprofilemanager.load_profile(profile_name)
        
        self.new_mfcprofile_label.config(text = "")
        
        if profile:
            # self.mfccurrent_loaded_profile = profile_name
            #Update the name of the profile
            self.mfcname_var.set(profile_name)
            #Update the description in the field
            self.mfcdesc_var.set(profile.get("description", ""))
            
            # Clear the existing steps
            for item in self.mfcsteps_tree.get_children():
                self.mfcsteps_tree.delete(item)
            
            # Add new steps
            for step in profile.get("steps", []):
                self.mfcsteps_tree.insert("", tk.END, values=(
                    step["time"],
                    step["flow mfc1"],
                    step["flow mfc2"],
                    step["flow mfc3"]
                ))
            
            self.status_var.set(f"Loaded profile: {profile_name}")
        
    def delete_mfcprofile(self):
        """Delete the selected profile"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.mfcprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete")
            return
            
        profile_name = self.mfcprofile_listbox.get(selection[0]) #To ensure that you only select the first selected
        
        if messagebox.askyesno("Confirm", f"Delete profile '{profile_name}'?"):
            if self.mfcprofilemanager.delete_profile(profile_name):
                #Updating the new profile list
                self.update_mfcprofile_list() 
                #Changing the status
                self.status_var.set(f"Deleted profile: {profile_name}")
            else:
                messagebox.showerror("Error", f"Failed to delete the profile: '{profile_name}'")
                
    def create_new_mfcprofile(self):
        #Clearing all input fields and steps
        self.mfcname_var.set("")
        self.mfcdesc_var.set("")
        self.mfcstep_time_var.set("0")
        self.mfcstep_flow1_var.set("0")
        self.mfcstep_flow2_var.set("0")
        self.mfcstep_flow3_var.set("0")
        # self.mfcstep_temp_var.set("0")
        # self.mfcstep_valve_var.set("0")
        
        for item in self.mfcsteps_tree.get_children():
            self.mfcsteps_tree.delete(item)
        
        self.new_mfcprofile_label.config(text = "New profile", foreground = "green")
        
    def add_mfcstep(self):
        """Add a new step to the current profile"""
        try:
            time_val = float(self.mfcstep_time_var.get())
            flow1_val = float(self.mfcstep_flow1_var.get())
            flow2_val = float(self.mfcstep_flow2_var.get())
            flow3_val = float(self.mfcstep_flow3_var.get())
            # temp_val = float(self.mfcstep_temp_var.get())
            # valve_val = int(self.mfcstep_valve_var.get())
            
            if time_val < 0:
                raise ValueError("Time cannot be negative")
            # if valve_val not in [1, 2]:
            #     raise ValueError("Position of the valve must be 1 or 2")
            
            # Check if the time already exists
            for child in self.mfcsteps_tree.get_children():
                if float(self.mfcsteps_tree.item(child, "values")[0]) == time_val:
                    if not messagebox.askyesno("Confirm", f"Step at time {time_val}s already exists. Overwrite?"):
                        return #if True, thus no then return
                    self.mfcsteps_tree.delete(child)
                    break
            
            self.mfcsteps_tree.insert("", tk.END, values=(time_val, flow1_val, flow2_val, flow3_val)) #, temp_val, valve_val))
            
        except ValueError as error:
            messagebox.showerror("Error", f"Invalid input: {error}")
    
    def remove_mfcstep(self):
        """Remove the selected step"""
        selection = self.mfcsteps_tree.selection()
        if selection:
            self.mfcsteps_tree.delete(selection)
    
    def clear_mfcsteps(self):
        """Clear all steps"""
        if messagebox.askyesno("Confirm", "Clear all the steps?"):
            #Obtain all the steps and delete all the steps
            for item in self.mfcsteps_tree.get_children():
                self.mfcsteps_tree.delete(item)
    
    def save_mfcprofile(self):
        """Save the current profile"""
        #Getting the name
        name = self.mfcname_var.get().strip()
        
        #Ensuring that the name isn't empty
        if not name:
            messagebox.showwarning("Warning", "Profile name cannot be empty")
            return
        
        # Collect steps from the profile
        steps = []
        for child in self.mfcsteps_tree.get_children():
            #To obtain all the values of the steps
            values = self.mfcsteps_tree.item(child, "values")
            steps.append({
                "time": float(values[0]),
                "flow mfc1": float(values[1]),
                "flow mfc2": float(values[2]),
                "flow mfc3": float(values[3])
                # "temperature": float(values[4]),
                # "valve": int(values[5])
            })
        
        # Sort steps by time
        #https://docs.python.org/3/howto/sorting.html
        steps = sorted(steps, key=lambda steps: steps["time"])
        
        # Create the profile data
        profile_data = {
            "description": self.mfcdesc_var.get(),
            "steps": steps
        }
        
        if self.mfcprofilemanager.save_profile(name, profile_data):
            self.update_mfcprofile_list()
            self.status_var.set(f"Saved profile: {name}")
        else:
            messagebox.showerror("Error", f"Failed to save profile '{name}'")
    
    def run_mfcprofile(self):
        """Run the current profile"""    
            
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected): #and self.cooling.connected and self.valve.connected):
            messagebox.showwarning("Error", "One or more devices are not connected")
            return False
          
        #Get the name of the profile without spaces, such that the .json file can be loaded later
        name = self.mfcname_var.get().strip()
        
        #Checking whether the name is empty
        if not name:
            messagebox.showwarning("Warning", "Please load or create a profile first")
            return

        # Load the profile that needs to be runned
        profile = self.mfcprofilemanager.load_profile(name)
        if not profile:
            messagebox.showerror("Error", f"Failed to load profile: '{name}'")
            return
        
        self.update_run_var()
        #Enabling the stop button, since you can now stop a running profile
        self.mfcstop_button.config(state=tk.NORMAL) 
        
        # Start profile in a separate thread, such that the UI doesn't freeze until it finishes
        # And you'll still be able to see what happens, e.g. popup of not connection
        self.mfcprofile_thread = threading.Thread(
            target=self.run_mfcprofile_thread,  
            daemon=True         # Stops threading by pressing an event, e.g. pressing on stop button
        )
        self.mfcprofile_thread.start()
    
    def run_mfcprofile_thread(self):
        """Thread function to run the profile"""
        
        try:
            # Displaying which profile is running
            self.status_var.set(f"Running profile: {self.mfcname_var.get()}")
            self.mfcprofilemanager.run_profile(update_callback=self.update_mfcprofile_var)
            # self.root.after(0, lambda: self.update_run_status)
            self.root.after(0, lambda: self.mfcprofile_complete)

        except Exception as e:
            self.root.after(0, lambda: self.mfcprofile_error(e))
    
    def mfcprofile_complete(self):
        """Called when profile completes successfully"""
        self.mfcstop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run completed")
    
    def mfcprofile_error(self, error):
        """Called when profile run encounters an error"""
        self.mfcstop_button.config(state=tk.DISABLED)
        messagebox.showerror("Error", f"Profile run failed: {error}")
        self.status_var.set("Profile run failed")
    
    def stop_mfcprofile(self):
        """Stop the currently running profile"""
        self.mfcprofilemanager.stop_profile()
        self.mfcstop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run stopped by user")

    def update_mfcprofile_var(self, status):
        #when the UI is closed then this won't be "updating" (to debug)
        try:
            if not self.root.winfo_exists():
                return
        
            self.mfc_elapsed_label.config(text=f"{status['elapsed_time']:.1f}s")
            self.mfc_step_label.config(text=f"{status['current_step']}/{status['total_steps']}")
            self.mfc_value_label.config(text=f"{status['flow mfc1']:.2f}, {status['flow mfc2']:.2f}, {status['flow mfc3']:.2f} mL/min")
                
            # Schedule the next update, per 1s
            self.root.after(1000, lambda: self.update_mfcprofile_var)
        except tk.TclError:
            return
        
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
    # ###COOLING PROFILE
        
    # def update_coolingprofile_list(self):
    #     """Refresh the list of available profiles"""
    #     #https://youtu.be/Vm0ivVxNaA8
        
    #     #Delete all the items from the listbox
    #     self.coolingprofile_listbox.delete(0, tk.END)
        
    #     #Add all the profiles to the listbox
    #     for profile in self.coolingprofilemanager.get_profiles():
    #         self.coolingprofile_listbox.insert(tk.END, profile)  #listbox.insert(index, element)

    # def load_coolingprofile(self):
    #     """Load the selected profile into the editor"""
    #     #https://pythonassets.com/posts/listbox-in-tk-tkinter/
    #     selection = self.coolingprofile_listbox.curselection()
    #     if not selection:
    #         messagebox.showwarning("Warning", "Please select a profile to load")
    #         return
        
    #     #To ensure that you only select the first selected
    #     profile_name = self.coolingprofile_listbox.get(selection[0])
    #     profile = self.coolingprofilemanager.load_profile(profile_name)
        
    #     self.new_coolingprofile_label.config(text = "")
        
    #     if profile:
    #         # self.coolingcurrent_loaded_profile = profile_name
    #         #Update the name of the profile
    #         self.coolingname_var.set(profile_name)
    #         #Update the description in the field
    #         self.coolingdesc_var.set(profile.get("description", ""))
            
    #         # Clear the existing steps
    #         for item in self.coolingsteps_tree.get_children():
    #             self.coolingsteps_tree.delete(item)
            
    #         # Add new steps
    #         for step in profile.get("steps", []):
    #             self.coolingsteps_tree.insert("", tk.END, values=(
    #                 step["time"],
    #                 step["temperature"]
    #             ))
            
    #         self.status_var.set(f"Loaded profile: {profile_name}")
        
    # def delete_coolingprofile(self):
    #     """Delete the selected profile"""
    #     #https://pythonassets.com/posts/listbox-in-tk-tkinter/
    #     selection = self.coolingprofile_listbox.curselection()
    #     if not selection:
    #         messagebox.showwarning("Warning", "Please select a profile to delete")
    #         return
            
    #     profile_name = self.coolingprofile_listbox.get(selection[0]) #To ensure that you only select the first selected
        
    #     if messagebox.askyesno("Confirm", f"Delete profile '{profile_name}'?"):
    #         if self.coolingprofilemanager.delete_profile(profile_name):
    #             #Updating the new profile list
    #             self.update_coolingprofile_list() 
    #             #Changing the status
    #             self.status_var.set(f"Deleted profile: {profile_name}")
    #         else:
    #             messagebox.showerror("Error", f"Failed to delete the profile: '{profile_name}'")
                
    # def create_new_coolingprofile(self):
    #     #Clearing all input fields and steps
    #     self.coolingname_var.set("")
    #     self.coolingdesc_var.set("")
    #     self.coolingstep_time_var.set("0")
    #     self.coolingstep_temp_var.set("0")
        
    #     for item in self.coolingsteps_tree.get_children():
    #         self.coolingsteps_tree.delete(item)
        
    #     self.new_coolingprofile_label.config(text = "New profile", foreground = "green")
        
    # def add_coolingstep(self):
    #     """Add a new step to the current profile"""
    #     try:
    #         time_val = float(self.coolingstep_time_var.get())
    #         temp_val = float(self.coolingstep_temp_var.get())
            
    #         if time_val < 0:
    #             raise ValueError("Time cannot be negative")

    #         # Check if the time already exists
    #         for child in self.coolingsteps_tree.get_children():
    #             if float(self.coolingsteps_tree.item(child, "values")[0]) == time_val:
    #                 if not messagebox.askyesno("Confirm", f"Step at time {time_val}s already exists. Overwrite?"):
    #                     return #if True, thus no then return
    #                 self.coolingsteps_tree.delete(child)
    #                 break
            
    #         self.coolingsteps_tree.insert("", tk.END, values=(time_val, temp_val))
            
    #     except ValueError as error:
    #         messagebox.showerror("Error", f"Invalid input: {error}")
    
    # def remove_coolingstep(self):
    #     """Remove the selected step"""
    #     selection = self.coolingsteps_tree.selection()
    #     if selection:
    #         self.coolingsteps_tree.delete(selection)
    
    # def clear_coolingsteps(self):
    #     """Clear all steps"""
    #     if messagebox.askyesno("Confirm", "Clear all the steps?"):
    #         #Obtain all the steps and delete all the steps
    #         for item in self.coolingsteps_tree.get_children():
    #             self.coolingsteps_tree.delete(item)
    
    # def save_coolingprofile(self):
    #     """Save the current profile"""
    #     #Getting the name
    #     name = self.coolingname_var.get().strip()
        
    #     #Ensuring that the name isn't empty
    #     if not name:
    #         messagebox.showwarning("Warning", "Profile name cannot be empty")
    #         return
        
    #     # Collect steps from the profile
    #     steps = []
    #     for child in self.coolingsteps_tree.get_children():
    #         #To obtain all the values of the steps
    #         values = self.coolingsteps_tree.item(child, "values")
    #         steps.append({
    #             "time": float(values[0]),
    #             "temperature": float(values[1])
    #         })
        
    #     # Sort steps by time
    #     #https://docs.python.org/3/howto/sorting.html
    #     steps = sorted(steps, key=lambda steps: steps["time"])
        
    #     # Create the profile data
    #     profile_data = {
    #         "description": self.coolingdesc_var.get(),
    #         "steps": steps
    #     }
        
    #     if self.coolingprofilemanager.save_profile(name, profile_data):
    #         self.update_coolingprofile_list()
    #         self.status_var.set(f"Saved profile: {name}")
    #     else:
    #         messagebox.showerror("Error", f"Failed to save profile '{name}'")
    
    # def run_coolingprofile(self):
    #     """Run the current profile"""    
            
    #     if not self.cooling.connected:
    #         messagebox.showwarning("Error", "One or more devices are not connected")
    #         return False
        
    #     if not isinstance(self.ambient_temp, (int, float)):
    #         messagebox.showwarning("Invalid Input", "Ambient Temperature has not been set yet or is an non-numeric value.")
    #         return False
    #     #Get the name of the profile without spaces, such that the .json file can be loaded later
    #     name = self.coolingname_var.get().strip()
        
    #     #Checking whether the name is empty
    #     if not name:
    #         messagebox.showwarning("Warning", "Please load or create a profile first")
    #         return

    #     # Load the profile that needs to be runned
    #     profile = self.coolingprofilemanager.load_profile(name)
    #     if not profile:
    #         messagebox.showerror("Error", f"Failed to load profile: '{name}'")
    #         return
        
    #     self.update_run_var()
    #     #Enabling the stop button, since you can now stop a running profile
    #     self.coolingstop_button.config(state=tk.NORMAL) 
        

        
    #     # Start profile in a separate thread, such that the UI doesn't freeze until it finishes
    #     # And you'll still be able to see what happens, e.g. popup of not connection
    #     self.coolingprofile_thread = threading.Thread(
    #         target=self.run_coolingprofile_thread,  
    #         daemon=True         # Stops threading by pressing an event, e.g. pressing on stop button
    #     )
    #     self.coolingprofile_thread.start()
    
    # def run_coolingprofile_thread(self):
    #     """Thread function to run the profile"""
    #     try:
    #         # Displaying which profile is running
    #         self.status_var.set(f"Running profile: {self.coolingname_var.get()}")
    #         self.coolingprofilemanager.run_profile(temp_ambient = self.ambient_temp, update_callback=self.update_coolingprofile_var)
    #         self.root.after(0, lambda: self.coolingprofile_complete)

    #     except Exception as e:
    #         self.root.after(0, lambda: self.coolingprofile_error(e))
    
    # def coolingprofile_complete(self):
    #     """Called when profile completes successfully"""
    #     self.coolingstop_button.config(state=tk.DISABLED)
    #     self.status_var.set("Profile run completed")
    
    # def coolingprofile_error(self, error):
    #     """Called when profile run encounters an error"""
    #     self.coolingstop_button.config(state=tk.DISABLED)
    #     messagebox.showerror("Error", f"Profile run failed: {error}")
    #     self.status_var.set("Profile run failed")
    
    # def stop_coolingprofile(self):
    #     """Stop the currently running profile"""
    #     self.coolingprofilemanager.stop_profile()
    #     self.coolingstop_button.config(state=tk.DISABLED)
    #     self.status_var.set("Profile run stopped by user")

    # def update_coolingprofile_var(self, status):
    #     #when the UI is closed then this won't be "updating" (to debug)
    #     if not self.root.winfo_exists():
    #         return
        
    #     self.cooling_elapsed_label.config(text=f"{status['elapsed_time']:.1f}s")
    #     self.cooling_step_label.config(text=f"{status['current_step']}/{status['total_steps']}")
    #     self.cooling_value_label.config(text=f"{status['temperature']:.2f} °C")
    #     # Schedule the next update, per 1s
    #     self.root.after(1000, lambda: self.update_coolingprofile_var)



    ####VALVE PROFILE
    def update_valveprofile_list(self):
        """Refresh the list of available profiles"""
        #https://youtu.be/Vm0ivVxNaA8
        
        #Delete all the items from the listbox
        self.valveprofile_listbox.delete(0, tk.END)
        
        #Add all the profiles to the listbox
        for profile in self.valveprofilemanager.get_profiles():
            self.valveprofile_listbox.insert(tk.END, profile)  #listbox.insert(index, element)

    def load_valveprofile(self):
        """Load the selected profile into the editor"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.valveprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to load")
            return
        
        #To ensure that you only select the first selected
        profile_name = self.valveprofile_listbox.get(selection[0])
        profile = self.valveprofilemanager.load_profile(profile_name)
        
        self.new_valveprofile_label.config(text = "")
        
        if profile:
            # self.valvecurrent_loaded_profile = profile_name
            #Update the name of the profile
            self.valvename_var.set(profile_name)
            #Update the description in the field
            self.valvedesc_var.set(profile.get("description", ""))
            
            # Clear the existing steps
            for item in self.valvesteps_tree.get_children():
                self.valvesteps_tree.delete(item)
            
            # Add new steps
            for step in profile.get("steps", []):
                self.valvesteps_tree.insert("", tk.END, values=(
                    step["time"],
                    step["valve1"],
                    step["valve2"]
                ))
            
            self.status_var.set(f"Loaded profile: {profile_name}")
        
    def delete_valveprofile(self):
        """Delete the selected profile"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.valveprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete")
            return
            
        profile_name = self.valveprofile_listbox.get(selection[0]) #To ensure that you only select the first selected
        
        if messagebox.askyesno("Confirm", f"Delete profile '{profile_name}'?"):
            if self.valveprofilemanager.delete_profile(profile_name):
                #Updating the new profile list
                self.update_valveprofile_list() 
                #Changing the status
                self.status_var.set(f"Deleted profile: {profile_name}")
            else:
                messagebox.showerror("Error", f"Failed to delete the profile: '{profile_name}'")
                
    def create_new_valveprofile(self):
        #Clearing all input fields and steps
        self.valvename_var.set("")
        self.valvedesc_var.set("")
        self.valvestep_time_var.set("0")
        self.valvestep_valve1_var.set("0")
        self.valvestep_valve2_var.set("0")
        
        for item in self.valvesteps_tree.get_children():
            self.valvesteps_tree.delete(item)
        
        self.new_valveprofile_label.config(text = "New profile", foreground = "green")
        
    def add_valvestep(self):
        """Add a new step to the current profile"""
        try:
            time_val = float(self.valvestep_time_var.get())
            valve1_val = int(self.valvestep_valve1_var.get())
            valve2_val = int(self.valvestep_valve2_var.get())
            
            if time_val < 0:
                raise ValueError("Time cannot be negative")
            
            
            ###ALS WE OOK POSITIE 3 ERIN GAAN DOEN MOET DIT GEWIJZIGD WORDEN
            if (valve1_val not in [1, 2]) and (valve2_val not in [1, 2]) :
                raise ValueError("Position of the valve must be 1 or 2")
            
            # Check if the time already exists
            for child in self.valvesteps_tree.get_children():
                if float(self.valvesteps_tree.item(child, "values")[0]) == time_val:
                    if not messagebox.askyesno("Confirm", f"Step at time {time_val}s already exists. Overwrite?"):
                        return #if True, thus no then return
                    self.valvesteps_tree.delete(child)
                    break
            
            self.valvesteps_tree.insert("", tk.END, values=(time_val, valve1_val, valve2_val))
            
        except ValueError as error:
            messagebox.showerror("Error", f"Invalid input: {error}")
    
    def remove_valvestep(self):
        """Remove the selected step"""
        selection = self.valvesteps_tree.selection()
        if selection:
            self.valvesteps_tree.delete(selection)
    
    def clear_valvesteps(self):
        """Clear all steps"""
        if messagebox.askyesno("Confirm", "Clear all the steps?"):
            #Obtain all the steps and delete all the steps
            for item in self.valvesteps_tree.get_children():
                self.valvesteps_tree.delete(item)
    
    def save_valveprofile(self):
        """Save the current profile"""
        #Getting the name
        name = self.valvename_var.get().strip()
        
        #Ensuring that the name isn't empty
        if not name:
            messagebox.showwarning("Warning", "Profile name cannot be empty")
            return
        
        # Collect steps from the profile
        steps = []
        for child in self.valvesteps_tree.get_children():
            #To obtain all the values of the steps
            values = self.valvesteps_tree.item(child, "values")
            steps.append({
                "time": float(values[0]),
                "valve1": int(values[1]),
                "valve2": int(values[2])
            })
        
        # Sort steps by time
        #https://docs.python.org/3/howto/sorting.html
        steps = sorted(steps, key=lambda steps: steps["time"])
        
        # Create the profile data
        profile_data = {
            "description": self.valvedesc_var.get(),
            "steps": steps
        }
        
        if self.valveprofilemanager.save_profile(name, profile_data):
            self.update_valveprofile_list()
            self.status_var.set(f"Saved profile: {name}")
        else:
            messagebox.showerror("Error", f"Failed to save profile '{name}'")
    
    def run_valveprofile(self):
        """Run the current profile"""    
            
        if not (self.valve[0].connected and self.valve[1].connected):
            messagebox.showwarning("Error", "One or more devices are not connected")
            return False
          
        #Get the name of the profile without spaces, such that the .json file can be loaded later
        name = self.valvename_var.get().strip()
        
        #Checking whether the name is empty
        if not name:
            messagebox.showwarning("Warning", "Please load or create a profile first")
            return

        # Load the profile that needs to be runned
        profile = self.valveprofilemanager.load_profile(name)
        if not profile:
            messagebox.showerror("Error", f"Failed to load profile: '{name}'")
            return
        
        self.update_run_var()
        #Enabling the stop button, since you can now stop a running profile
        self.valvestop_button.config(state=tk.NORMAL) 
        
        # Start profile in a separate thread, such that the UI doesn't freeze until it finishes
        # And you'll still be able to see what happens, e.g. popup of not connection
        self.valveprofile_thread = threading.Thread(
            target=self.run_valveprofile_thread,  
            daemon=True         # Stops threading by pressing an event, e.g. pressing on stop button
        )
        self.valveprofile_thread.start()
    
    def run_valveprofile_thread(self):
        """Thread function to run the profile"""
        
        try:
            # Displaying which profile is running
            self.status_var.set(f"Running profile: {self.valvename_var.get()}")
            self.valveprofilemanager.run_profile(update_callback=self.update_valveprofile_var)
            # self.root.after(0, lambda: self.update_run_status)
            self.root.after(0, lambda: self.valveprofile_complete)

        except Exception as e:
            self.root.after(0, lambda: self.valveprofile_error(e))
    
    def valveprofile_complete(self):
        """Called when profile completes successfully"""
        self.valvestop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run completed")
    
    def valveprofile_error(self, error):
        """Called when profile run encounters an error"""
        self.valvestop_button.config(state=tk.DISABLED)
        messagebox.showerror("Error", f"Profile run failed: {error}")
        self.status_var.set("Profile run failed")
    
    def stop_valveprofile(self):
        """Stop the currently running profile"""
        self.valveprofilemanager.stop_profile()
        self.valvestop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run stopped by user")

    def update_valveprofile_var(self, status):
        #when the UI is closed then this won't be "updating" (to debug)
        try:
            if not self.root.winfo_exists():
                return
            
            self.valve_elapsed_label.config(text=f"{status['elapsed_time']:.1f}s")
            self.valve_step_label.config(text=f"{status['current_step']}/{status['total_steps']}")
            self.valve_value_label.config(text=f"RVM 1: Position {status['valve1']}, RVM 2: Position {status['valve2']}")
            # Schedule the next update, per 1s
            self.root.after(1000, lambda: self.update_valveprofile_var)
        except tk.TclError:
            return

    def run_selected_profiles(self):
        mfc_sel = self.selprof_mfc_listbox.curselection()
        valve_sel = self.selprof_valve_listbox.curselection()
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # cooling_sel = self.selprof_cooling_listbox.curselection()

        # if not mfc_sel or not valve_sel or not cooling_sel:
        if not mfc_sel or not valve_sel:
            messagebox.showwarning("Selection Error", "Please select a profile from each list.")
            return

        mfc_name = self.selprof_mfc_listbox.get(mfc_sel[0])
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # cooling_name = self.selprof_cooling_listbox.get(cooling_sel[0])
        valve_name = self.selprof_valve_listbox.get(valve_sel[0])

        # Load profiles
        if not self.mfcprofilemanager.load_profile(mfc_name):
            messagebox.showerror("Error", f"Failed to load MFC profile '{mfc_name}'")
            return
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # if not self.coolingprofilemanager.load_profile(cooling_name):
        #     messagebox.showerror("Error", f"Failed to load Cooling profile '{cooling_name}'")
        #     return
        if not self.valveprofilemanager.load_profile(valve_name):
            messagebox.showerror("Error", f"Failed to load Valve profile '{valve_name}'")
            return

        # Check devices 
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected):
            messagebox.showerror("Connection Error", "One or more MFCs not connected.")
            return
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # if not self.cooling.connected:
        #     messagebox.showerror("Connection Error", "Cooling not connected.")
        #     return
        if not (self.valve[0].connected and self.valve[1].connected):
            messagebox.showerror("Connection Error", "Valve not connected.")
            return
        # if not isinstance(self.ambient_temp, (int, float)):
        #     messagebox.showerror("Error", "Ambient temperature must be set.")
        #     return
        
        self.update_run_var()
        self.stop_all_button.config(state=tk.NORMAL)
        
        # Start all three profiles in threads
        threading.Thread(target=self.run_mfcprofile_thread, daemon=True).start()
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # threading.Thread(target=self.run_coolingprofile_thread, daemon=True).start()
        threading.Thread(target=self.run_valveprofile_thread, daemon=True).start()

        # self.status_var.set(f"Running MFC: {mfc_name}, Valve: {valve_name}, Cooling: {cooling_name}")

        self.status_var.set(f"Running MFC: {mfc_name}, Valve: {valve_name}")

 ###on/offprofile
    def update_onoffprofile_list(self):
        """Refresh the list of available profiles"""
        #https://youtu.be/Vm0ivVxNaA8
        
        #Delete all the items from the listbox
        self.onoffprofile_listbox.delete(0, tk.END)
        
        #Add all the profiles to the listbox
        for profile in self.onoffprofilemanager.get_profiles():
            self.onoffprofile_listbox.insert(tk.END, profile)  #listbox.insert(index, element)

    def load_onoffprofile(self):
        """Load the selected profile into the editor"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.onoffprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to load")
            return
        
        #To ensure that you only select the first selected
        profile_name = self.onoffprofile_listbox.get(selection[0])
        profile = self.onoffprofilemanager.load_profile(profile_name)
        
        self.new_onoffprofile_label.config(text = "")
        
        if profile:
            self.current_loaded_profile = profile_name
            #Update the name of the profile
            self.onoffname_var.set(profile_name)
            #Update the description in the field
            self.onoffdesc_var.set(profile.get("description", ""))
            
            # Clear the existing steps
            for item in self.onoffsteps_tree.get_children():
                self.onoffsteps_tree.delete(item)
            
            # Add new steps
            for step in profile.get("steps", []):
                self.onoffsteps_tree.insert("", tk.END, values=(
                    step["time"],
                    step["flow mfc1"],
                    step["flow mfc2"],
                    step["flow mfc3"],
        # # Cooling OFF // Koeling Uitzetten omdat hij het nog niet doet
                    # step["temperature"],
                    step["valve"]
                ))
            
            self.status_var.set(f"Loaded profile: {profile_name}")
        
    def delete_onoffprofile(self):
        """Delete the selected profile"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.onoffprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete")
            return
            
        profile_name = self.onoffprofile_listbox.get(selection[0]) #To ensure that you only select the first selected
        
        if messagebox.askyesno("Confirm", f"Delete profile '{profile_name}'?"):
            if self.onoffprofilemanager.delete_profile(profile_name):
                #Updating the new profile list
                self.update_onoffprofile_list() 
                #Changing the status
                self.status_var.set(f"Deleted profile: {profile_name}")
            else:
                messagebox.showerror("Error", f"Failed to delete the profile: '{profile_name}'")
                
    def create_new_onoffprofile(self):
        #Clearing all input fields and steps
        self.onoffname_var.set("")
        self.onoffdesc_var.set("")
        self.onoffstep_time_var.set("0")
        self.onoffstep_flow1_var.set("0")
        self.onoffstep_flow2_var.set("0")
        self.onoffstep_flow3_var.set("0")
        # # Cooling OFF // Koeling Uitzetten omdat hij het nog niet doet
        # self.onoffstep_temp_var.set("0")
        self.onoffstep_valve_var.set("0")
        
        for item in self.onoffsteps_tree.get_children():
            self.onoffsteps_tree.delete(item)
        
        self.new_onoffprofile_label.config(text = "New profile", foreground = "green")
        
    def onoffadd_step(self):
        """Add a new step to the current profile"""
        try:
            time_val = float(self.onoffstep_time_var.get())
            flow1_val = float(self.onoffstep_flow1_var.get())
            flow2_val = float(self.onoffstep_flow2_var.get())
            flow3_val = float(self.onoffstep_flow3_var.get())
        # # Cooling OFF // Koeling Uitzetten omdat hij het nog niet doet
            # temp_val = float(self.onoffstep_temp_var.get())
            valve_val = int(self.onoffstep_valve_var.get())
            
            if time_val < 0:
                raise ValueError("Time cannot be negative")
            if valve_val not in [1, 2]:
                raise ValueError("Position of the valve must be 1 or 2")
            
            # Check if the time already exists
            for child in self.onoffsteps_tree.get_children():
                if float(self.onoffsteps_tree.item(child, "values")[0]) == time_val:
                    if not messagebox.askyesno("Confirm", f"Step at time {time_val}s already exists. Overwrite?"):
                        return #if True, thus no then return
                    self.onoffsteps_tree.delete(child)
                    break
            # # Cooling OFF // Koeling Uitzetten omdat hij het nog niet doet
            # self.onoffsteps_tree.insert("", tk.END, values=(time_val, flow1_val, flow2_val, flow3_val, temp_val, valve_val))
            self.onoffsteps_tree.insert("", tk.END, values=(time_val, flow1_val, flow2_val, flow3_val, valve_val))
            
        except ValueError as error:
            messagebox.showerror("Error", f"Invalid input: {error}")
    
    def onoffremove_step(self):
        """Remove the selected step"""
        selection = self.onoffsteps_tree.selection()
        if selection:
            self.onoffsteps_tree.delete(selection)
    
    def onoffclear_steps(self):
        """Clear all steps"""
        if messagebox.askyesno("Confirm", "Clear all the steps?"):
            #Obtain all the steps and delete all the steps
            for item in self.onoffsteps_tree.get_children():
                self.onoffsteps_tree.delete(item)
    
    def save_onoffprofile(self):
        """Save the current profile"""
        #Getting the name
        name = self.onoffname_var.get().strip()
        
        #Ensuring that the name isn't empty
        if not name:
            messagebox.showwarning("Warning", "Profile name cannot be empty")
            return
        
        # Collect steps from the profile
        steps = []
        for child in self.onoffsteps_tree.get_children():
            #To obtain all the values of the steps
            values = self.onoffsteps_tree.item(child, "values")
            steps.append({
                "time": float(values[0]),
                "flow mfc1": float(values[1]),
                "flow mfc2": float(values[2]),
                "flow mfc3": float(values[3]),
            # # Cooling OFF // Koeling Uitzetten omdat hij het nog niet doet
                # "temperature": float(values[4]),
                # "valve": int(values[5])
                "valve": int(values[4])
            })
        
        # Sort steps by time
        #https://docs.python.org/3/howto/sorting.html
        steps = sorted(steps, key=lambda steps: steps["time"])
        
        # Create the profile data
        profile_data = {
            "description": self.onoffdesc_var.get(),
            "steps": steps
        }
        
        if self.onoffprofilemanager.save_profile(name, profile_data):
            self.update_onoffprofile_list()
            self.status_var.set(f"Saved profile: {name}")
        else:
            messagebox.showerror("Error", f"Failed to save profile '{name}'")
    
    def run_onoffprofile(self):
        """Run the current profile"""    

        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected and self.cooling.connected and self.valve.connected):
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected and self.valve.connected):

            messagebox.showwarning("Error", "One or more devices are not connected")
            return False
          
        #Get the name of the profile without spaces, such that the .json file can be loaded later
        name = self.onoffname_var.get().strip()
        
        #Checking whether the name is empty
        if not name:
            messagebox.showwarning("Warning", "Please load or create a profile first")
            return

        # Load the profile that needs to be runned
        profile = self.onoffprofilemanager.load_profile(name)
        if not profile:
            messagebox.showerror("Error", f"Failed to load profile: '{name}'")
            return
        
        self.update_run_var()
        #Enabling the stop button, since you can now stop a running profile
        self.onoffstop_button.config(state=tk.NORMAL) 
        
        # Start profile in a separate thread, such that the UI doesn't freeze until it finishes
        # And you'll still be able to see what happens, e.g. popup of not connection
        self.onoffprofile_thread = threading.Thread(
            target=self.run_onoffprofile_thread,
            args=(profile,),    
            daemon=True         # Stops threading by pressing an event, e.g. pressing on stop button
        )
        self.onoffprofile_thread.start()
    
    def run_onoffprofile_thread(self, profile):      
        try:
            def safe_update(status):
                self.root.after(0, lambda: self.update_onoffprofile_var(status))

            self.status_var.set(f"Running profile: {self.onoffname_var.get()}")
            self.onoffprofilemanager.run_profile(
                # temp_ambient=self.ambient_temp,
                update_callback=safe_update
            )
            self.root.after(0, self.onoffprofile_complete)

        except Exception as e:
            self.root.after(0, lambda: self.onoffprofile_error(str(e)))

    
    def onoffprofile_complete(self):
        """Called when profile completes successfully"""
        self.onoffstop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run completed")
    
    def onoffprofile_error(self, error):
        """Called when profile run encounters an error"""
        self.onoffstop_button.config(state=tk.DISABLED)
        messagebox.showerror("Error", f"Profile run failed: {error}")
        self.status_var.set("Profile run failed")
    
    def stop_onoffprofile(self):
        """Stop the currently running profile"""
        self.onoffprofilemanager.stop_profile()
        self.onoffstop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run stopped by user")
    
    def update_onoffprofile_var(self, status):
        #when the UI is closed then this won't be "updating" (to debug)
        try:
            if not self.root.winfo_exists():
                return
            
            print(status['elapsed_time'], status['current_step'])
            self.onoff_elapsed_label.config(text=f"{status['elapsed_time']:.1f}s")
            self.onoff_step_label.config(text=f"{status['current_step']}/{status['total_steps']}")
                # # Cooling OFF // Koeling Uitzetten omdat hij het nog niet doet
            # self.onoff_value_label.config(text=f"{status['flow mfc1']:.2f}, {status['flow mfc2']:.2f}, {status['flow mfc3']:.2f}, {status['temperature']:.1f}°C, V{status['valve']}")
            self.onoff_value_label.config(text=f"{status['flow mfc1']:.2f}, {status['flow mfc2']:.2f}, {status['flow mfc3']:.2f}, {status['valve']}")
        except tk.TclError:
            return


    def stop_all_profiles(self):
        """Stop all profiles running from run_selected_profiles"""
        self.mfcprofilemanager.stop_profile()
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # self.coolingprofilemanager.stop_profile()
        self.valveprofilemanager.stop_profile()
        self.status_var.set("All profiles stopped by user")


###EXCEL SHEET TAB
# ### Constant Flow Rate Profile
#     def create_pureflowrate_tab(self):
#         self.pureflowrate_tab = ttk.Frame(self.notebook)
#         self.notebook.add(self.pureflowrate_tab, text="Constant Flow Rate Profile")

#         # Read Excel sheet, sheet 1
#         # skiprows = 4, because the first 4 rows contains the information that we don't want
#         self.pureflowrate_data = pd.read_excel(self.path_pureflowrate, sheet_name=0, skiprows=4)

#         ##Renaming the columns such that it can be read easilier later 
#         #https://www.geeksforgeeks.org/how-to-rename-columns-in-pandas-dataframe/
#         self.pureflowrate_data = self.pureflowrate_data.rename(columns={
#             self.pureflowrate_data.columns[0]: 'VOC',
#             self.pureflowrate_data.columns[1]: 'Concentration',
#             self.pureflowrate_data.columns[2]: 'Temperature',
#             self.pureflowrate_data.columns[4]: 'Flowrate_liquid',
#             self.pureflowrate_data.columns[5]: 'Flowrate_N'
#         })
        
#         #Dropping values that have both VOC and Concentration values
#         #https://www.programiz.com/python-programming/pandas/methods/dropna
#         self.pureflowrate_data = self.pureflowrate_data.dropna(subset=['VOC', 'Concentration'])

#         ttk.Label(self.pureflowrate_tab, text="Select VOC:").grid(row=0, column=0)
#         self.pureflowrate_voc_var = tk.StringVar()
        
#         # Combobox for the type of VOC
#         # https://www.pythontutorial.net/tkinter/tkinter-combobox/
#         self.pureflowrate_voc_dropdown = ttk.Combobox(self.pureflowrate_tab, textvariable=self.pureflowrate_voc_var, state="readonly")
#         self.pureflowrate_voc_dropdown.grid(row=0, column=1)
#         # obtain all unique values in the list
#         voc_list = self.pureflowrate_data['VOC'].unique()
#         self.pureflowrate_voc_dropdown['values'] = sorted(voc_list)
        
#         # the update_concentration_dropdown function will execute when the selected value of the combobox changes.
#         self.pureflowrate_voc_dropdown.bind("<<ComboboxSelected>>", self.pureflowrate_update_concentration_dropdown)

#         ttk.Label(self.pureflowrate_tab, text="Select Concentration (ppm):").grid(row=1, column=0)
#         self.pureflowrate_conc_var = tk.StringVar()
#         self.pureflowrate_conc_dropdown = ttk.Combobox(self.pureflowrate_tab, textvariable=self.pureflowrate_conc_var, state="readonly")
#         self.pureflowrate_conc_dropdown.grid(row=1, column=1)
#         # display excel target function will execute when the selected value of the combobox changes.
#         self.pureflowrate_conc_dropdown.bind("<<ComboboxSelected>>", self.pureflowrate_sel_targets)


#         self.pureflowrate_lbl_selconc_temp = ttk.Label(self.pureflowrate_tab, text="Target Temp: -")
#         self.pureflowrate_lbl_selconc_temp.grid(row=2, column=0, columnspan=2, sticky='w')
#         self.pureflowrate_lbl_selconc_flow1 = ttk.Label(self.pureflowrate_tab, text="Target MFC1 (Fluid): -")
#         self.pureflowrate_lbl_selconc_flow1.grid(row=3, column=0, columnspan=2, sticky='w')
#         self.pureflowrate_lbl_selconc_flowN = ttk.Label(self.pureflowrate_tab, text="Target MFC2 (Nitrogen): -")
#         self.pureflowrate_lbl_selconc_flowN.grid(row=4, column=0, columnspan=2, sticky='w')

#         self.pureflowrate_run_button = ttk.Button(self.pureflowrate_tab, text="Run Continuously", command=self.pureflowrate_run_cnt)
#         self.pureflowrate_run_button.grid(row=5, column=0, padx=5, pady=10, sticky="ew")

#         self.pureflowrate_stop_button = ttk.Button(self.pureflowrate_tab, text="Stop", command=self.pureflowrate_stop_cnt)
#         self.pureflowrate_stop_button.grid(row=5, column=1, padx=5, pady=10, sticky="ew")

#         # For Graph
#         # ttk.Label(self.pureflowrate_tab, text="Start Delay Time (s):").grid(row=6, column=0)
#         # self.start_delay_entry = ttk.Entry(self.pureflowrate_tab)
#         # self.start_delay_entry.grid(row=6, column=1)

#         ttk.Label(self.pureflowrate_tab, text="On Time (s):").grid(row=7, column=0)
#         self.on_time_entry = ttk.Entry(self.pureflowrate_tab)
#         self.on_time_entry.grid(row=7, column=1)

#         ttk.Label(self.pureflowrate_tab, text="Off Time (s):").grid(row=8, column=0)
#         self.off_time_entry = ttk.Entry(self.pureflowrate_tab)
#         self.off_time_entry.grid(row=8, column=1)

#         ttk.Label(self.pureflowrate_tab, text="Run Time (s):").grid(row=9, column=0)
#         self.run_time_entry = ttk.Entry(self.pureflowrate_tab)
#         self.run_time_entry.grid(row=9, column=1)
        
#         self.pureflowrate_run_button = ttk.Button(self.pureflowrate_tab, text="Run On/Off Graph", command=self.pureflowrate_run_onoffprofile)
#         self.pureflowrate_run_button.grid(row=10, column=0, padx=5, pady=10, sticky="ew")
        
#         self.pureflowrate_plotgraph_button = ttk.Button(self.pureflowrate_tab, text="Plot Expected On/Off Graph", command=self.plot_expected_profile)
#         self.pureflowrate_plotgraph_button.grid(row=10, column=1, padx=5, pady=10, sticky="ew")

#         self.elapsed_time_var = tk.StringVar(value="Elapsed Time: 0.0 s")
#         self.elapsed_time_label = ttk.Label(self.pureflowrate_tab, textvariable=self.elapsed_time_var)
#         self.elapsed_time_label.grid(row=11, column=0, columnspan=2, sticky='w')

#         # Graph frame — to the right of all inputs
#         self.graph_frame = ttk.LabelFrame(self.pureflowrate_tab, text="Expected On/Off Graph")
#         self.graph_frame.grid(row=0, column=2, rowspan=10, padx=10, pady=10, sticky="ns")


#     def pureflowrate_update_concentration_dropdown(self, event):
#         selected_voc = self.pureflowrate_voc_var.get()
        
#         # Obtain the filtered data according to the selected_voc
#         # https://www.youtube.com/watch?v=xzslFdjO0Ts  
#         # https://www.geeksforgeeks.org/ways-to-filter-pandas-dataframe-by-column-values/
        
#         # rows are kept where voc = selected_voc
#         filtered = self.pureflowrate_data[self.pureflowrate_data['VOC'] == selected_voc]
#         #gives the sorted unique concentration values of the rows that are kept
#         sorted_unique_voc = sorted(filtered['Concentration'].unique())
#         self.pureflowrate_conc_dropdown['values'] = sorted_unique_voc
#         self.pureflowrate_conc_var.set('')  

#     def pureflowrate_sel_targets(self, event):
#         voc = self.pureflowrate_voc_var.get()
#         conc = float(self.pureflowrate_conc_var.get())
        
#         # #https://www.geeksforgeeks.org/difference-between-loc-and-iloc-in-pandas-dataframe/
#         # using iloc[0] such that only the first one should be selected
#         selectedrow = self.pureflowrate_data.loc[(self.pureflowrate_data['VOC'] == voc) & (self.pureflowrate_data['Concentration'] == conc)].iloc[0]
#         self.pureflowrate_sel_temp = float(selectedrow['Temperature'])
#         self.pureflowrate_sel_flow1 = float(selectedrow['Flowrate_liquid'])
#         self.pureflowrate_sel_flow2 = float(selectedrow['Flowrate_N'])
        
#         # row = self.pureflowrate_data.loc[(self.pureflowrate_data['VOC'] == voc) & (self.pureflowrate_data['Concentration'] == conc)]

#         self.pureflowrate_lbl_selconc_temp.config(text=f"Target Temp: {self.pureflowrate_sel_temp} °C")
#         self.pureflowrate_lbl_selconc_flow1.config(text=f"Target MFC1: {self.pureflowrate_sel_flow1} mL/min")
#         self.pureflowrate_lbl_selconc_flowN.config(text=f"Target MFC2: {self.pureflowrate_sel_flow2} mL/min")

#     def pureflowrate_run_cnt(self):
        
#         # check whether ambient temp is set
#         if not isinstance(self.ambient_temp, (int, float)):
#             messagebox.showerror("Error", "Ambient temperature must be set.")
#             return False
    
#         if not self.mfcs[0].connected:
#             messagebox.showerror("Connection Error", "MFC 1 is not connected.")
#             return False
#         if not self.mfcs[1].connected:
#             messagebox.showerror("Connection Error", "MFC 2 is not connected.")            
#             return False
#         ##Koeling Uitzetten omdat hij het nog niet doet
#         # # Cooling OFF
#         # if not self.cooling.connected:
#         #     messagebox.showerror("Connection Error", "Cooling is not connected.")
#         #     return False
#         if not self.valve.connected:
#             messagebox.showerror("Connection Error", "Valve is not connected.")            
#             return False
        
#         #switch position valve to open
#         self.valve.switch_position(2)

#         ##Koeling Uitzetten omdat hij het nog niet doet
#         # # Cooling OFF
#         # threading.Thread(
#         #     target=lambda: self.cooling.set_temperature(self.pureflowrate_sel_temp, self.ambient_temp),
#         #     daemon=True
#         # ).start()

#         threading.Thread(
#             target=lambda: self.mfcs[0].set_massflow(self.pureflowrate_sel_flow1),
#             daemon=True
#         ).start()

#         threading.Thread(
#             target=lambda: self.mfcs[1].set_massflow(self.pureflowrate_sel_flow2),
#             daemon=True
#         ).start()
        
#         self.status_var.set(f"Running Constant Flow Rate for Concentration {self.pureflowrate_conc_var.get()} ppm | MFC1: {self.pureflowrate_sel_flow1} mL/min | MFC2 (Nitrogen): {self.pureflowrate_sel_flow2} mL/min | Temp: {self.pureflowrate_sel_temp} °C, | Valve set to position 1 ")
        
#         self.update_run_var()
    
#     def pureflowrate_stop_cnt(self):
#         ##Koeling Uitzetten omdat hij het nog niet doet
#         # # Cooling OFF
#         # self.cooling.set_temperature(self.ambient_temp, self.ambient_temp)
#         self.mfcs[0].set_massflow(0)
#         self.mfcs[1].set_massflow(0)
#         self.valve.switch_position(2)

#         self.status_var.set(f"Stopping Constant Flow Rate Profile | MFC1 set to 0 mL/min, | MFC2 (Nitrogen) set to 0 mL/min | Temperature set to Ambient temperature: {self.ambient_temp} °C, | Valve set to position 2")
        
#     # ###with start time but:     ##elapsed time do not align with the run profile elapsed time
#     # def update_elapsed_time_display(self, start_timestamp, run_time):
#     #     elapsed = time.time() - start_timestamp
#     #     self.elapsed_time_var.set(f"Elapsed Time: {elapsed:.1f} s / {run_time:.1f} s")

#     #     if elapsed < run_time:
#     #         self.root.after(1, lambda: self.update_elapsed_time_display(start_timestamp, run_time))
#     #     else:
#     #         self.elapsed_time_var.set(f"Done: Elapsed Time: {run_time:.1f} s")
            
#     # def pureflowrate_run_onoffprofile(self):
#         self.plot_expected_profile()
#         try:
#             start_time = float(self.start_delay_entry.get())
#             on_time = float(self.on_time_entry.get())
#             off_time = float(self.off_time_entry.get())
#             run_time = float(self.run_time_entry.get())
#         except ValueError:
#             messagebox.showerror("Input Error", "All timing fields must be numbers.")
#             return

#         if not self.mfcs[0].connected:
#             messagebox.showerror("Connection Error", "MFC 1 is not connected.")
#             return False
#         if not self.mfcs[1].connected:
#             messagebox.showerror("Connection Error", "MFC 2 is not connected.")            
#             return False
#         ##Koeling Uitzetten omdat hij het nog niet doet
#         # # Cooling OFF
#         # if not self.cooling.connected:
#         #     messagebox.showerror("Connection Error", "Cooling is not connected.")
#         #     return False
#         if not self.valve.connected:
#             messagebox.showerror("Connection Error", "Valve is not connected.")            
#             return False

#         # check whether ambient temp is set
#         if not isinstance(self.ambient_temp, (int, float)):
#             messagebox.showerror("Error", "Ambient temperature must be set.")
#             return False
    

#         def run_pulse_cycle():
#             self.update_run_var()
#         ##Koeling Uitzetten omdat hij het nog niet doet
#         # # # Cooling OFF
#         #     self.cooling.set_temperature(self.pureflowrate_sel_temp, self.ambient_temp)
#             ###Ik weet nou niet of we eerst moeten wachten totdat deze temp is bereikt of niet tho..
#             pulse_starttime = time.time()
            
#             self.root.after(0, lambda: self.update_elapsed_time_display(pulse_starttime, run_time))
#             self.status_var.set(f" Start Delay Time of {start_time}")
#             time.sleep(start_time)
#             elapsed = time.time() + start_time
#             while elapsed < run_time:
#                 # ON state
#                 self.mfcs[0].set_massflow(self.pureflowrate_sel_flow1)
#                 self.mfcs[1].set_massflow(self.pureflowrate_sel_flow2)
#                 self.valve.switch_position(2)
#                 self.status_var.set(f" ON-state | MFC1 set to {self.pureflowrate_sel_flow1} mL/min | MFC2 (Nitrogen) set to {self.pureflowrate_sel_flow2} mL/min | Temp set to {self.pureflowrate_sel_temp} °C, | Valve set to Position 2")
#                 time.sleep(on_time)
#                 elapsed += on_time

#                 if elapsed >= run_time:
#                     break
#                 # OFF state
#                 self.mfcs[0].set_massflow(0)
#                 self.mfcs[1].set_massflow(2)
#                 self.valve.switch_position(1)
#                 self.status_var.set(f" OFF-state | MFC1 set to 0 mL/min | MFC2 (Nitrogen) set to 0 mL/min | Temp set to {self.pureflowrate_sel_temp} °C | Valve set to Position 1")
#                 time.sleep(off_time)
#                 elapsed += off_time


#             # Final
#             self.mfcs[0].set_massflow(0)
#             self.mfcs[1].set_massflow(0)
#             self.valve.switch_position(1)
#             ##Koeling Uitzetten omdat hij het nog niet doet
#         # # Cooling OFF
#             # self.cooling.set_temperature(self.ambient_temp, self.ambient_temp)
#             self.status_var.set(f" Final Stop | MFC1 set to 0 mL/min | MFC2 (Nitrogen) set to 0 mL/min | Temp set to {self.ambient_temp} °C | Valve set to Position 1")

#         threading.Thread(target=run_pulse_cycle, daemon=True).start()
            
#     ##Without start time
#     def update_elapsed_time_display(self, start_timestamp, run_time):
#         #when the UI is closed then this won't be "updating" (to debug)
#         if not self.root.winfo_exists():
#             return
                
#         #elapsed time
#         elapsed = time.time() - start_timestamp  
#         self.elapsed_time_var.set(f"Elapsed Time: {elapsed:.1f} s / {run_time:.1f} s")

#         if elapsed < run_time:
#             self.root.after(100, lambda: self.update_elapsed_time_display(start_timestamp, run_time))
#         else:
#             self.elapsed_time_var.set(f"Done: Elapsed Time: {run_time:.1f} s / {run_time:.1f} s")

#     def pureflowrate_run_onoffprofile(self):
#         self.plot_expected_profile()
#         try:
#             on_time = float(self.on_time_entry.get())
#             off_time = float(self.off_time_entry.get())
#             run_time = float(self.run_time_entry.get())
#         except ValueError:
#             messagebox.showerror("Input Error", "All timing fields must be numbers.")
#             return

#         if not self.mfcs[0].connected:
#             messagebox.showerror("Connection Error", "MFC 1 is not connected.")
#             return False
#         if not self.mfcs[1].connected:
#             messagebox.showerror("Connection Error", "MFC 2 is not connected.")            
#             return False
#         ##Koeling Uitzetten omdat hij het nog niet doet
#         # # Cooling OFF

#         # if not self.cooling.connected:
#         #     messagebox.showerror("Connection Error", "Cooling is not connected.")
#         #     return False
#         if not self.valve.connected:
#             messagebox.showerror("Connection Error", "Valve is not connected.")            
#             return False

#         # check whether ambient temp is set
#         if not isinstance(self.ambient_temp, (int, float)):
#             messagebox.showerror("Error", "Ambient temperature must be set.")
#             return False
    

#         def run_pulse_cycle():
#             self.update_run_var()

#         ##Koeling Uitzetten omdat hij het nog niet doet
#         # # Cooling OFF
#             # self.cooling.set_temperature(self.pureflowrate_sel_temp, self.ambient_temp)

#             # Obtain the time that the code is start with running
#             pulse_starttime = time.time()
#             self.root.after(0, lambda: self.update_elapsed_time_display(pulse_starttime, run_time))

#             while True:
#                 # Check of tijd op is
#                 if time.time() - pulse_starttime >= run_time:
#                     break

#                 # ON state
#                 self.mfcs[0].set_massflow(self.pureflowrate_sel_flow1)
#                 self.mfcs[1].set_massflow(self.pureflowrate_sel_flow2)
#                 self.valve.switch_position(2)
#                 self.status_var.set(
#                     f" ON-state | MFC1 set to {self.pureflowrate_sel_flow1} mL/min | "
#                     f"MFC2 (Nitrogen) set to {self.pureflowrate_sel_flow2} mL/min | "
#                     f"Temp set to {self.pureflowrate_sel_temp} °C, | Valve set to Position 2"
#                 )
#                 on_start = time.time()

#                 while time.time() - on_start < on_time:
#                     if time.time() - pulse_starttime >= run_time:
#                         break
#                     time.sleep(0.05)
                    
#                 ##When it ends within the on-time
#                 if time.time() - pulse_starttime >= run_time:
#                     break

#                 # OFF state
#                 self.mfcs[0].set_massflow(0)
#                 self.mfcs[1].set_massflow(2)
#                 self.valve.switch_position(1)
#                 self.status_var.set(
#                     f" OFF-state | MFC1 set to 0 mL/min | MFC2 (Nitrogen) set to 0 mL/min | "
#                     f"Temp set to {self.pureflowrate_sel_temp} °C | Valve set to Position 1"
#                 )

#                 off_start = time.time()
#                 while time.time() - off_start < off_time:
#                     if time.time() - pulse_starttime >= run_time:
#                         break
#                     time.sleep(0.05)

#             # Final state after run_time is reached
#             self.mfcs[0].set_massflow(0)
#             self.mfcs[1].set_massflow(0)
#             self.valve.switch_position(1)
#         ##Koeling Uitzetten omdat hij het nog niet doet
#         # # Cooling OFF

#             # self.cooling.set_temperature(self.ambient_temp, self.ambient_temp)
#             self.status_var.set(
#                 f" Final Stop | MFC1 set to 0 mL/min | MFC2 (Nitrogen) set to 0 mL/min | "
#                 f"Temp set to {self.ambient_temp} °C | Valve set to Position 1"
#             )

#         threading.Thread(target=run_pulse_cycle, daemon=True).start()
            
#     def plot_expected_profile(self):
#         #Expected Graph
#         try:
#             # Obtaining time fields
#             # start_time = float(self.start_delay_entry.get())
#             on_time = float(self.on_time_entry.get())
#             off_time = float(self.off_time_entry.get())
#             run_time = float(self.run_time_entry.get())
#             conc = float(self.pureflowrate_conc_var.get())
#         except ValueError:
#             messagebox.showerror("Input Error", "Start Delay Time, On time, Off Time, Run Time and Concentrations must be numbers.")
#             return

#         time_data = []
#         signal_data = []
#         total_time = 0

#         # # Generating the start delay time 
#         # # Keep adding concentration 0 until the start time has reached
#         # for time in range(int(start_time)):
#         #     time_data.append(total_time)
#         #     signal_data.append(0)
#         #     total_time += 1

#         # Generating the on and off pattern
#         while total_time < run_time:
#             for time in range(int(on_time)):
#                 # on pattern: voeg concentration toe aan een lijst voor de tijd dat hij op "ON" moet staan
#                 if total_time >= run_time:
#                     break
#                 time_data.append(total_time)
#                 signal_data.append(conc)
#                 total_time += 1
#                 # off pattern: voeg concentration toe aan een lijst voor de tijd dat hij op "OFF" moet staan
#             for time in range(int(off_time)):
#                 if total_time >= run_time:
#                     break
#                 time_data.append(total_time)
#                 signal_data.append(0)
#                 total_time += 1

#         # Clear previous canvas if exists
#         # https://stackoverflow.com/questions/65544881/clearing-and-plotting-mathplot-figure-on-tkinter
#         for child in self.graph_frame.winfo_children():
#             child.destroy()

#         # Create plot
#         fig, ax = plt.subplots(figsize=(6, 4))
#         ax.plot(time_data, signal_data, linewidth=2)
#         ax.set_xlabel("Time (s)")
#         ax.set_ylabel("Concentration (ppm)")
#         ax.set_title("Expected On/Off Graph")
#         ax.set_xlim(0, time_data[-1] * 1.2 )
#         ax.set_ylim(0, conc * 1.2)
#         ax.grid(True)
#         fig.tight_layout()  

#        # Embed in Tkinter
#         canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
#         canvas.draw()

#         canvas_widget = canvas.get_tk_widget()
#         # Graph size 400 x 300
#         canvas_widget.config(width=500, height=300) 
#         # Prevent Frame Shrinking
#         # https://youtu.be/onIEw70Uw-4
#         canvas_widget.pack_propagate(False)  # prevent auto-resizing
#         canvas_widget.pack(fill='none', expand=False)

###MATLABCODE 
    def create_voccalculator_tab(self):

        ##Make it scrollable
        voccalc_tab = self.create_scrollable_tab(self.notebook, "ON/OFF Profile")
        # self.voccalc_tab = ttk.Frame(self.notebook)
        # self.notebook.add(self.voccalc_tab, text="VOC Flow Calculator")

        ##Make it scrollable
        # profile_tab = self.create_scrollable_tab(self.notebook, "Different Concentration Profile Management")
        ## Split into two frames
        list_frame = ttk.Frame(voccalc_tab)
        list_frame.pack(side= 'left', fill = 'both', expand=True, padx=5, pady=5)
        
        edit_frame = ttk.Frame(voccalc_tab)
        edit_frame.pack(side= 'right', fill= 'both', expand=True, padx=5, pady=5)
        
        ### Left frame / list frame
        ## Profile listbox with scrollbar
        # https://www.pythontutorial.net/tkinter/tkinter-listbox/#adding-a-scrollbar-to-the-listbox
        # Making an empty profile listbox
        self.onoffconcprofile_listbox = tk.Listbox(list_frame, selectmode = tk.SINGLE)
        self.onoffconcprofile_listbox.pack(fill= 'both', expand=True, padx=5, pady=5)
    
        # Putting all the profiles in the profile listbox
        self.update_onoffconcprofile_list()
        
        #Adding a scrollbar to the profile listbox
        v_scrollbar = ttk.Scrollbar(list_frame, orient = tk.VERTICAL, command = self.onoffconcprofile_listbox.yview)
        v_scrollbar.pack(side='right', fill='y')
        
        self.onoffconcprofile_listbox['yscrollcommand'] = v_scrollbar.set
        
        ##Adding the buttons to the left frame (list frame)
        # Profile list buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        load_button = ttk.Button(button_frame, text="New", command=self.new_onoffconcprofile)
        load_button.pack(side='left', padx=3, expand=True)

        load_button = ttk.Button(button_frame, text="Load", command=self.load_onoffconcprofile)
        load_button.pack(side='left', padx=3, expand=True)
        
        save_button = ttk.Button(button_frame, text="Save", command=self.save_onoffconcprofile)
        save_button.pack(side='left', padx=3, expand=True)

        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_onoffconcprofile)
        delete_button.pack(side='left', padx=3, expand=True)
        
        # VOC selection
        ttk.Label(edit_frame, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.onoffconc_namevar = tk.StringVar()
        name_entry = ttk.Entry(edit_frame, textvariable=self.onoffconc_namevar)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        name_entry.config(width=30)
        
        ttk.Label(edit_frame, text="Description:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.onoffconc_desc_var = tk.StringVar()
        desc_entry = ttk.Entry(edit_frame, textvariable=self.onoffconc_desc_var)
        desc_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(edit_frame, text="Select VOC:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.voccalc_voc_var = tk.StringVar()
        self.vocslist = list(self.settings_manager.get_voc_data().keys())
        self.voc_dropdown_voccalculator = ttk.Combobox(edit_frame, textvariable=self.voccalc_voc_var, values=self.vocslist, state="readonly")
        self.voc_dropdown_voccalculator.grid(row=2, column=1, padx=10, pady=10)
        self.voc_dropdown_voccalculator.current(0)

        # Concentration input
        ttk.Label(edit_frame, text="Concentration (ppm):").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.voccalc_concentration_var = tk.DoubleVar()
        concentration_entry = ttk.Entry(edit_frame, textvariable=self.voccalc_concentration_var)
        concentration_entry.grid(row=3, column=1, padx=10, pady=10)

        # Total Flow Rate input
        ttk.Label(edit_frame, text="Total Flow Rate (mL/min):").grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.voccalc_totalflowrate_var = tk.DoubleVar()
        totalflow_entry = ttk.Entry(edit_frame, textvariable=self.voccalc_totalflowrate_var)
        totalflow_entry.grid(row=4, column=1, padx=10, pady=10)

        # Calculate Button
        calc_button = ttk.Button(edit_frame, text="Calculate Flow", command=self.calculate_voc_flow)
        calc_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Result labels
        self.voccalc_flow_label = ttk.Label(edit_frame, text="Required Flow: -")
        self.voccalc_flow_label.grid(row=6, column=0, columnspan=2, pady=5)
        
        self.voccalc_N_label = ttk.Label(edit_frame, text="Required Mass Flow of Nitrogen: -")
        self.voccalc_N_label.grid(row=7, column=0, columnspan=2, pady=5)

        # No need
        # self.voccalc_temp_label = ttk.Label(self.voccalc_tab, text="Required Temperature: -")
        # self.voccalc_temp_label.grid(row=6, column=0, columnspan=2, pady=5)

        self.voccalc_ps_label = ttk.Label(edit_frame, text="Saturated Vapor Pressure (Ps): -")
        self.voccalc_ps_label.grid(row=8, column=0, columnspan=2, pady=5)

        # self.voccalc_run_button = ttk.Button(self.voccalc_tab, text="Run Continuously", command=self.voccalc_run_cnt)
        # self.voccalc_run_button.grid(row=7, column=0, padx=5, pady=10, sticky="ew")

        # self.voccalc_stop_button = ttk.Button(self.voccalc_tab, text="Stop", command=self.voccalc_stop_cnt)
        # self.voccalc_stop_button.grid(row=7, column=1, padx=5, pady=10, sticky="ew")

        ttk.Label(edit_frame, text="On Time (s):").grid(row=9, column=0)
        self.voccalc_on_time_entry = ttk.Entry(edit_frame)
        self.voccalc_on_time_entry.grid(row=9, column=1)

        ttk.Label(edit_frame, text="Off Time (s):").grid(row=10, column=0)
        self.voccalc_off_time_entry = ttk.Entry(edit_frame)
        self.voccalc_off_time_entry.grid(row=10, column=1)

        ttk.Label(edit_frame, text="Run Time (s):").grid(row=11, column=0)
        self.voccalc_run_time_entry = ttk.Entry(edit_frame)
        self.voccalc_run_time_entry.grid(row=11, column=1)
        
        self.voccalc_run_button = ttk.Button(edit_frame, state="disabled", text="Run ON/OFF Graph", command=self.voccalculator_run_onoffprofile)
        self.voccalc_run_button.grid(row=12, column=0, padx=5, pady=10, sticky="ew")
        
        self.voccalc_stop_button = ttk.Button(edit_frame, state="disabled", text="Stop ON/OFF Graph", command=self.stop_onoffconc_run)
        self.voccalc_stop_button.grid(row=12, column=1, padx=5, pady=10, sticky="ew")
                
        self.voccalc_plotgraph_button = ttk.Button(edit_frame,state="disabled", text="Plot ON/OFF Graph", command=self.plot_expected_vocprofile)
        self.voccalc_plotgraph_button.grid(row=13, column=0, padx=5, pady=10, sticky="ew")

        self.voccalc_elapsed_time_var = tk.StringVar(value="Elapsed Time: 0.0 s")
        self.voccalc_elapsed_time_label = ttk.Label(edit_frame, textvariable=self.voccalc_elapsed_time_var)
        self.voccalc_elapsed_time_label.grid(row=14, column=0, columnspan=2, sticky='w')

        # For the graph
        self.voccalc_graph_frame = ttk.LabelFrame(edit_frame, text="Setpoint Concentration On/Off Graph")
        self.voccalc_graph_frame.grid(row=0, column=2, rowspan=10, padx=10, pady=10, sticky="ns")        
        
    def update_voc_elapsed_time_display(self, start_timestamp, run_time):
        #when the UI is closed then this won't be "updating" (to debug)
        try:
            if not self.root.winfo_exists():
                return
            
            #elapsed time
            elapsed = time.time() - start_timestamp  
            self.voccalc_elapsed_time_var.set(f"Elapsed Time: {elapsed:.1f} s / {run_time:.1f} s")

            if elapsed < run_time and not self.stop_onoff_conc_run:
                self.root.after(100, lambda: self.update_voc_elapsed_time_display(start_timestamp, run_time))
            elif self.stop_onoff_conc_run:
                self.voccalc_elapsed_time_var.set(f"Profile Stopped at {elapsed:.1f} s")            
            else:
                self.voccalc_elapsed_time_var.set(f"Done: Elapsed Time: {run_time:.1f} s / {run_time:.1f} s")
        except tk.TclError:
            return

    def voccalculator_run_onoffprofile(self):
        self.plot_expected_vocprofile()
        try:
            on_time = float(self.voccalc_on_time_entry.get())
            off_time = float(self.voccalc_off_time_entry.get())
            run_time = float(self.voccalc_run_time_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "All timing fields must be numbers.")
            return

        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # if not self.mfcs[0].connected or not self.mfcs[1].connected or not self.cooling.connected or not self.valve.connected:
        if not self.mfcs[0].connected or not self.mfcs[1].connected or not self.valve.connected:
            messagebox.showerror("Connection Error", "Ensure all devices are connected.")
            return

        # if not isinstance(self.ambient_temp, (int, float)):
        #     messagebox.showerror("Error", "Ambient temperature must be set.")
        #     return
        
        #Checking whether the temperature has already been set to the filled temperature
        # https://www.pythontutorial.net/tkinter/tkinter-askyesno/
        # print(self.voc_temp)
        # if self.voc_temp is not None:
        #     confirm = messagebox.askyesno(
        #         "Cooling Plate Temperature",
        #         f"Did you set the cooling plate temperature to {self.voc_temp:.1f} °C?"
        #     )
        #     if not confirm:
        #         return  

        # T = 0
        confirm = messagebox.askyesno(
            "Cooling Plate Temperature",
            f"Did you set the cooling plate temperature to 0 °C?"
        )
        if not confirm:
            return  
            
        self.voccalc_stop_button.config(state = 'enabled')
        self.stop_onoff_conc_run = False
        def run_pulse_cycle():
            self.update_run_var()
        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
            # self.cooling.set_temperature(self.voc_temp, self.ambient_temp)
            
            pulse_starttime = time.time()
            self.root.after(0, lambda: self.update_voc_elapsed_time_display(pulse_starttime, run_time))

            while not self.stop_onoff_conc_run:
                if time.time() - pulse_starttime >= run_time:
                    break

                # ON state
                self.mfcs[0].set_massflow(self.voc_flow)
                self.mfcs[1].set_massflow(self.voc_N)
                self.valve.switch_position(2)
                self.status_var.set(f"VOC ON-state | MFC1: {self.voc_flow}, MFC2 (Nitrogen): {self.voc_N}")
                if not self.sleep_with_stop_check(on_time):
                    break

                if time.time() - pulse_starttime >= run_time:
                    break
                
                # OFF state
                self.mfcs[0].set_massflow(0)
                self.mfcs[1].set_massflow(0) #nitrogen max flow rate
                self.valve.switch_position(1)
                self.status_var.set("VOC OFF-state")    
                if not self.sleep_with_stop_check(off_time):
                    break

            if not self.stop_onoff_conc_run:
                # Final reset
                self.mfcs[0].set_massflow(0)
                self.mfcs[1].set_massflow(0)
            ##Koeling Uitzetten omdat hij het nog niet doet
            # # Cooling OFF
                # self.cooling.set_temperature(self.ambient_temp, self.ambient_temp)
                
                self.valve.switch_position(1)
                self.status_var.set("VOC Run complete")

        threading.Thread(target=run_pulse_cycle, daemon=True).start()

    def sleep_with_stop_check(self, duration):
        interval = 0.1  # 100 ms
        end_time = time.time() + duration
        while time.time() < end_time:
            if self.stop_onoff_conc_run:
                return False
            time.sleep(interval)
        return True

    def plot_expected_vocprofile(self):
        #Expected Graph
        try:
            # Obtaining time fields
            # start_time = float(self.start_delay_entry.get())
            on_time = float(self.voccalc_on_time_entry.get())
            off_time = float(self.voccalc_off_time_entry.get())
            run_time = float(self.voccalc_run_time_entry.get())
            conc = float(self.voccalc_concentration_var.get())
        except ValueError:
            messagebox.showerror("Input Error", "Start Delay Time, On time, Off Time, Run Time and Concentrations must be numbers.")
            return

        time_data = []
        signal_data = []
        total_time = 0

        # # Generating the start delay time 
        # # Keep adding concentration 0 until the start time has reached
        # for time in range(int(start_time)):
        #     time_data.append(total_time)
        #     signal_data.append(0)
        #     total_time += 1
        
        step_time = 1e-2
        on_time_steps = on_time / step_time
        off_time_steps = off_time / step_time
        
        # Generating the on and off pattern
        while total_time < run_time:
            for time in range(int(on_time_steps)):
                # on pattern: voeg concentration toe aan een lijst voor de tijd dat hij op "ON" moet staan
                if total_time >= run_time:
                    break
                time_data.append(total_time)
                signal_data.append(conc)
                total_time += step_time
                # off pattern: voeg concentration toe aan een lijst voor de tijd dat hij op "OFF" moet staan
            for time in range(int(off_time_steps)):
                if total_time >= run_time:
                    break
                time_data.append(total_time)
                signal_data.append(0)
                total_time += step_time

        # Clear previous canvas if exists
        # https://stackoverflow.com/questions/65544881/clearing-and-plotting-mathplot-figure-on-tkinter
        for child in self.voccalc_graph_frame.winfo_children():
            child.destroy()

        # Create plot
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(time_data, signal_data, color='red', linewidth=2)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Concentration (ppm)")
        ax.set_title("Setpoint Concentration On/Off Graph")
        ax.set_xlim(0, time_data[-1] * 1.2 )
        ax.set_ylim(0, conc * 1.2)
        ax.grid(True)
        fig.tight_layout()  

        # Om figure te saven        
        # fig.savefig("C:/Users/chant/Downloads/expected_onoffconcentration_plot.png", dpi=300, bbox_inches='tight')

       # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.voccalc_graph_frame)
        canvas.draw()

        canvas_widget = canvas.get_tk_widget()
        # Graph size 400 x 300
        canvas_widget.config(width=500, height=300) 
        # Prevent Frame Shrinking
        # https://youtu.be/onIEw70Uw-4
        canvas_widget.pack_propagate(False)  # prevent auto-resizing
        canvas_widget.pack(fill='none', expand=False)
       
    def calculate_voc_flow(self):
        try:
            voc = self.voccalc_voc_var.get()
            concentration = float(self.voccalc_concentration_var.get())
            total_flow = float(self.voccalc_totalflowrate_var.get())
            print(concentration, total_flow)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers for concentration and total flow rate.")
            return

        ### Standard temperature of 0 degree
        self.voc_flow, self.voc_N, self.voc_Ps = self.calculate_required_flow_0degrees(voc, concentration, total_flow)
        
        # ## Variating temp
        # self.voc_flow, self.voc_N, self.voc_temp, self.voc_Ps = self.calculate_required_flow(voc, concentration, total_flow)
        # print(self.voc_flow, self.voc_N, self.voc_temp, self.voc_Ps)
        
        if self.voc_flow is not None:
            self.voccalc_flow_label.config(text=f"Required Flow: {self.voc_flow} mL/min")
            self.voccalc_N_label.config(text=f"Required Flow of Nitrogen: {self.voc_N} mL/min")
            # self.voccalc_temp_label.config(text=f"Required Temperature: {self.voc_temp} °C")
            self.voccalc_ps_label.config(text=f"Saturated Vapor Pressure (Ps): {self.voc_Ps} mmHg")
            self.voccalc_plotgraph_button.config(state="enabled")
            self.voccalc_run_button.config(state="enabled")
        else:
            self.voccalc_flow_label.config(text="Required Flow: N/A")
            self.voccalc_N_label.config(text=f"Required Flow of Nitrogen: N/A")
            # self.voccalc_temp_label.config(text="Required Temperature: N/A")
            self.voccalc_ps_label.config(text="Saturated Vapor Pressure (Ps): N/A")

    # def calculate_required_flow_variating_temp(self, voc_name, concentration_ppm, total_flow_rate):       
    #     voc_data = self.settings_manager.get_voc_data()
    #     # print("vocdata", voc_data)
    
    #     if voc_name not in voc_data:
    #         return None, None, None, None
       
    #     ##with using the tmin and tmax
    #     A, B, C, Tmin, Tmax = voc_data[voc_name]
    #     # print(A, B, C, Tmin, Tmax)
    #     P = 760  # mmHg; normale atmosferische luchtdruk
    #     min_f = 0.1 #minimum flow rate

    #     if not isinstance(self.ambient_temp, (int, float)):
    #         messagebox.showwarning("Invalid Input", "Ambient Temperature has not been set yet or is an non-numeric value.")
    #         return None, None, None, None
        
    #     # When temperature variates (cooling)
    #     min_T = self.ambient_temp - 30
        
    #     if concentration_ppm == 0:
    #         f = 0
    #         F = 0 
    #         T = self.ambient_temp #It doesn't matter what temperature it is
    #         Ps = 0 #By setting pressure to zero we ensure no flow thus no concentration
    #         return f, F, T, Ps
        
    #     #Range of Torrey Pines XR: -10 to 110 degrees, however also depending on ambient temp
    #     for T in range(-10, 110):
    #         Ps = 10 ** (A - B / (C + T))
    #         f = concentration_ppm * (total_flow_rate * P / Ps) * 1e-6
    #         F = total_flow_rate - f
    #         # print(min_f, f, total_flow_rate)
    #         if min_f <= f <= total_flow_rate: # f should be smaller than the total flow rate but bigger than the minimum flow rate
    #             # print("ambient temp", min_T, f, F, T, Ps)
    #             if T > min_T:
    #                 print("T bigger than minimum temp regarding ambient temp")
    #                 # Regarding the Tmin and Tmax of the Antoine eq table
    #                 if Tmin <= T <= Tmax:
    #                     return f, F, T, Ps

    #     return None, None, None, None

    def calculate_required_flow_0degrees(self, voc_name, concentration_ppm, total_flow_rate):       
        T = 0
        voc_data = self.settings_manager.get_voc_data()
        # print("vocdata", voc_data)
    
        if voc_name not in voc_data:
            return None, None, None, None
       
        ##with using the tmin and tmax
        A, B, C, Tmin, Tmax = voc_data[voc_name]
        # print(A, B, C, Tmin, Tmax)
        P = 760  # mmHg; normale atmosferische luchtdruk
        min_f = 0.1 #minimum flow rate

        if concentration_ppm == 0:
            f = 0
            F = 0 
            Ps = 0 #By setting pressure to zero we ensure no flow thus no concentration
            return f, F, Ps

        Ps = 10 ** (A - B / (C + T))
        f = concentration_ppm * (total_flow_rate * P / Ps) * 1e-6
        F = total_flow_rate - f
        # print(min_f, f, total_flow_rate)
        if min_f <= f <= total_flow_rate: # f should be smaller than the total flow rate but bigger than the minimum flow rate
            if Tmin <= T <= Tmax:
                return f, F, Ps

        return None, None, None
    
    #profile
    def update_onoffconcprofile_list(self):
        """Refresh the list of available profiles"""
        #https://youtu.be/Vm0ivVxNaA8
        
        #Delete all the items from the listbox
        self.onoffconcprofile_listbox.delete(0, tk.END)
        
        #Add all the profiles to the listbox
        for profile in self.onoffconcprofilemanager.get_profiles():
            self.onoffconcprofile_listbox.insert(tk.END, profile)  #listbox.insert(index, element)

    def new_onoffconcprofile(self):
        """Clear fields to create a new ON/OFF concentration profile."""

        self.onoffconc_namevar.set("")
        self.onoffconc_desc_var.set("")
        self.voccalc_voc_var.set("")
        self.voccalc_concentration_var.set(0.0)
        self.voccalc_totalflowrate_var.set(0.0)
        self.voccalc_on_time_entry.delete(0, tk.END)
        self.voccalc_off_time_entry.delete(0, tk.END)
        self.voccalc_run_time_entry.delete(0, tk.END)
        self.status_var.set("Creating new ON/OFF profile.")
  
        # Clear existing plot from the graph frame
        for child in self.voccalc_graph_frame.winfo_children():
            child.destroy()

    def delete_onoffconcprofile(self):
        """Delete selected ON/OFF profile."""
        selection = self.onoffconcprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete.")
            return

        profile_name = self.onoffconcprofile_listbox.get(selection[0])
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{profile_name}'?"):
            if self.onoffconcprofilemanager.delete_profile(profile_name):
                self.update_onoffconcprofile_list()
                self.status_var.set(f"Deleted profile: {profile_name}")
            else:
                messagebox.showerror("Error", f"Could not delete profile: {profile_name}")

    def load_onoffconcprofile(self):
        """Load selected ON/OFF profile into editor, after gathering all values first."""
        self.stop_onoff_conc_run = False
        selection = self.onoffconcprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to load.")
            return

        profile_name = self.onoffconcprofile_listbox.get(selection[0])
        profile = self.onoffconcprofilemanager.load_profile(profile_name)

        if not profile:
            messagebox.showerror("Error", "Failed to load the selected profile.")
            return

        description = profile.get("description", "")
        voc = profile.get("voc", "")
        concentration = profile.get("concentration", 0.0)
        total_flow = profile.get("total_flow", 0.0)
        on_time = profile.get("on_time", "")
        off_time = profile.get("off_time", "")
        run_time = profile.get("run_time", "")
        

        print(profile_name, profile, description, voc)
        
        self.onoffconc_namevar.set(profile.get("name", profile_name))
        self.onoffconc_desc_var.set(description)
        self.voccalc_voc_var.set(voc)
        self.voccalc_concentration_var.set(concentration)
        self.voccalc_totalflowrate_var.set(total_flow)

        self.voccalc_on_time_entry.delete(0, tk.END)
        self.voccalc_on_time_entry.insert(0, on_time)

        self.voccalc_off_time_entry.delete(0, tk.END)
        self.voccalc_off_time_entry.insert(0, off_time)

        self.voccalc_run_time_entry.delete(0, tk.END)
        self.voccalc_run_time_entry.insert(0, run_time)

        self.status_var.set(f"Loaded profile: {profile_name}")
        
        self.calculate_voc_flow()
        self.plot_expected_vocprofile()
        

    def save_onoffconcprofile(self):
        """Save current VOC ON/OFF profile to file."""
        # Fetch all values first (as you requested: first get, then set/save)
        voc = self.voccalc_voc_var.get()
        try:
            concentration = float(self.voccalc_concentration_var.get())
            total_flow = float(self.voccalc_totalflowrate_var.get())
            on_time = float(self.voccalc_on_time_entry.get())
            off_time = float(self.voccalc_off_time_entry.get())
            run_time = float(self.voccalc_run_time_entry.get())
            profile_name = self.onoffconc_namevar.get()
            description = self.onoffconc_desc_var.get()
        except ValueError:
            messagebox.showerror("Input Error", "All numeric fields must be valid numbers.")
            return

        # Package the data
        profile_data = {
            "name": profile_name,
            "description": description,
            "voc": voc,
            "concentration": concentration,
            "total_flow": total_flow,
            "on_time": on_time,
            "off_time": off_time,
            "run_time": run_time
        }

        # Save using profile manager
        success = self.onoffconcprofilemanager.save_profile(profile_name, profile_data)
        if success:
            self.update_onoffconcprofile_list()
            self.status_var.set(f"Saved profile: {profile_name}")
        else:
            messagebox.showerror("Save Error", f"Could not save profile '{profile_name}'.")
    
    def stop_onoffconc_run(self):
        self.stop_onoff_conc_run = True
        self.status_var.set("Stop running the profile.")
        self.voccalc_stop_button.config(state = 'disabled')
        self.mfcs[0].set_massflow(0)
        self.mfcs[1].set_massflow(0) #nitrogen max flow rate
        self.valve.switch_position(1)
    

####Tab different concentration
    def create_diffconc_profile_tab(self):
        # profile_tab = ttk.Frame(self.notebook)
        # profile_tab.pack(fill = 'both', expand = True)
        # self.notebook.add(profile_tab, text = 'Different Concentration Profile Management')
        
                
        ##Make it scrollable
        profile_tab = self.create_scrollable_tab(self.notebook, "Different Concentration Profile Management")
        ## Split into two frames
        list_frame = ttk.Frame(profile_tab)
        list_frame.pack(side= 'left', fill = 'both', expand=True, padx=5, pady=5)
        
        edit_frame = ttk.Frame(profile_tab)
        edit_frame.pack(side= 'right', fill= 'both', expand=True, padx=5, pady=5)
        
        ### Left frame / list frame
        ## Profile listbox with scrollbar
        # https://www.pythontutorial.net/tkinter/tkinter-listbox/#adding-a-scrollbar-to-the-listbox
        # Making an empty profile listbox
        self.diffconcprofile_listbox = tk.Listbox(list_frame, selectmode = tk.SINGLE)
        self.diffconcprofile_listbox.pack(fill= 'both', expand=True, padx=5, pady=5)
    
        # Putting all the profiles in the profile listbox
        self.update_diffconcprofile_list()
        
        #Adding a scrollbar to the profile listbox
        v_scrollbar = ttk.Scrollbar(list_frame, orient = tk.VERTICAL, command = self.diffconcprofile_listbox.yview)
        v_scrollbar.pack(side='right', fill='y')
        
        self.diffconcprofile_listbox['yscrollcommand'] = v_scrollbar.set
        
        ##Adding the buttons to the left frame (list frame)
        # Profile list buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        load_button = ttk.Button(button_frame, text="Load", command=self.load_diffconcprofile)
        load_button.pack(side='left', padx=3, expand=True)
        
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_diffconcprofile)
        delete_button.pack(side='left', padx=3, expand=True)
        
        # Frame for the expected graph
        graph_frame = ttk.Frame(list_frame)
        graph_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.diffconc_fig, self.diffconc_ax = plt.subplots(figsize=(4, 2))
        self.diffconc_ax.set_title("Setpoint Concentration vs Time Graph")
        self.diffconc_ax.set_xlabel("Time (s)")
        self.diffconc_ax.set_ylabel("Concentration (ppm)")
        self.diffconc_ax.grid(True)

        self.diffconc_canvas = FigureCanvasTkAgg(self.diffconc_fig, master=graph_frame)
        self.diffconc_canvas.draw()
        self.diffconc_canvas.get_tk_widget().pack(fill='both', expand=True)
            
        ##Right frame / edit frame
        # Profile info
        info_frame = ttk.Frame(edit_frame)
        info_frame.pack(fill='both', padx=5, pady=5)
        
        firstrow_frame = ttk.Frame(info_frame)
        firstrow_frame.pack(fill='x', pady=2)
        
        ##Showing green text with new profile if new profile made  
        self.new_diffconcprofile_label = ttk.Label(firstrow_frame, text="")
        self.new_diffconcprofile_label.pack(side = 'left', padx=5)
        
        name_frame = ttk.Frame(firstrow_frame)
        name_frame.pack(side='left', fill='x', padx=5)

        ttk.Label(name_frame, text="Name:").pack(side='left')
        self.diffconc_namevar = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=self.diffconc_namevar)
        name_entry.pack(side='left', padx=10)
        name_entry.config(width=30)
        
        desc_frame = ttk.Frame(firstrow_frame)
        desc_frame.pack(side='left', fill='x', expand=True)

        ttk.Label(desc_frame, text="Description:").pack(side='left')
        self.diffconc_desc_var = tk.StringVar()
        desc_entry = ttk.Entry(desc_frame, textvariable=self.diffconc_desc_var)
        desc_entry.pack(side='left', fill='x', expand=True)
        
        secondrow_frame = ttk.Frame(info_frame)
        secondrow_frame.pack(fill='x', pady=2)
        
        # VOC selection
        ttk.Label(secondrow_frame, text="Select VOC:").pack(side='left', padx=5)
        self.diffconc_voc_var = tk.StringVar()
        self.vocslist = list(self.settings_manager.get_voc_data().keys())
        self.voc_dropdown_diffconcprofile = ttk.Combobox(secondrow_frame, textvariable=self.diffconc_voc_var, values=self.vocslist, state="readonly")
        self.voc_dropdown_diffconcprofile.pack(side='left', padx=5)
        self.voc_dropdown_diffconcprofile.current(0)
        self.voc_dropdown_diffconcprofile.config(state = 'enabled')
        
        # Total flow rate
        ttk.Label(secondrow_frame, text="Total Flow Rate (mL/min):").pack(side='left', padx=5)
        self.diffconc_totalflowrate_var = tk.DoubleVar()
        self.totalflow_entry = ttk.Entry(secondrow_frame, textvariable=self.diffconc_totalflowrate_var)
        self.totalflow_entry.pack(side='left', padx=5)
        self.totalflow_entry.config(state = 'enabled')
        
        # temperature always set to 0 degrees
        # ttk.Label(secondrow_frame, text="Temperature (°C)").pack(side='left')
        # self.diffconc_temp_var = tk.DoubleVar()
        # self.temp_entry = ttk.Entry(secondrow_frame, textvariable=self.diffconc_temp_var)
        # self.temp_entry.pack(side='left', padx=5, expand=True, fill='x')
        # self.temp_entry.config(state = 'enabled')
        
        # Select Button, zodat de temperature, voc button enz niet meer kan worden gewijzigd maar nu wel stappen kan toevoegen
        ttk.Button(secondrow_frame, text="Select", command=self.enabling_select_diffconcprofile).pack(side='left', padx=5)

        new_profile_btn = ttk.Button(secondrow_frame, text = 'New Profile', command = self.create_new_diffconcprofile)
        new_profile_btn.pack(side='right', padx=3, expand=True)
        
        # Steps in the right/frame
        steps_frame = ttk.Frame(edit_frame)
        steps_frame.pack(fill = 'both' , expand=True, padx=5, pady=5)
        
        #https://tk-tutorial.readthedocs.io/en/latest/tree/tree.html
        self.diffconc_steps_tree = ttk.Treeview(
            steps_frame, 
            columns=("time", "valve", "concentration", "flow mfc1", "flow mfc2"), 
            show="headings"
        )
        self.diffconc_steps_tree.heading("time", text="Time (s)")
        self.diffconc_steps_tree.heading("valve", text="Valve Position (1 or 2)")
        self.diffconc_steps_tree.heading("concentration", text="Concentration (ppm)")
        self.diffconc_steps_tree.heading("flow mfc1", text="Flow MFC 1 (mL/min)")
        self.diffconc_steps_tree.heading("flow mfc2", text="Flow MFC 2 (mL/min)")

        
        self.diffconc_steps_tree.column("time", width=80, anchor=tk.CENTER)
        self.diffconc_steps_tree.column("valve", width=80, anchor=tk.CENTER)
        self.diffconc_steps_tree.column("concentration", width=100, anchor=tk.CENTER)
        self.diffconc_steps_tree.column("flow mfc1", width=100, anchor=tk.CENTER)
        self.diffconc_steps_tree.column("flow mfc2", width=100, anchor=tk.CENTER)

        
        self.diffconc_steps_tree.pack(fill = 'both' , expand=True)
        
        step_controls_frame = ttk.Frame(edit_frame)
        step_controls_frame.pack(fill='x', padx=5, pady=5)
        
        self.diffconc_profile_time_label = ttk.Label(step_controls_frame, text="Time (s):").pack(side='left')
        self.diffconc_step_time_var = tk.DoubleVar()
        self.step_time_entry = ttk.Entry(step_controls_frame, textvariable=self.diffconc_step_time_var, width=8)
        self.step_time_entry.pack(side='left', padx=2)
        self.step_time_entry.config(state ='disabled')

        self.diffconc_profile_valve_label =  ttk.Label(step_controls_frame, text="Valve Position:").pack(side='left')
        self.diffconc_valve_var = tk.IntVar() #integer variable, since the valve should be position on 1/2
        self.step_valve_combo = ttk.Combobox(
            step_controls_frame, 
            textvariable=self.diffconc_valve_var, 
            values=[1, 2], 
            width=5
        )
        self.step_valve_combo.pack(side='left', padx=2)
        self.step_valve_combo.config(state ='disabled')
        
        self.diffconc_profile_conc_label = ttk.Label(step_controls_frame, text="Concentration (ppm):").pack(side='left')
        self.diffconc_step_conc_var = tk.DoubleVar()
        self.step_conc_entry = ttk.Entry(step_controls_frame, textvariable=self.diffconc_step_conc_var, width=8)
        self.step_conc_entry.pack(side='left', padx=2)
        self.step_conc_entry.config(state ='disabled')

        
        self.diffconc_profile_mfc1_label = ttk.Label(step_controls_frame, text="Flow MFC 1 (mL/min):").pack(side='left')
        self.diffconc_flow1_var = tk.DoubleVar()
        self.step_flow1_entry = ttk.Entry(step_controls_frame, textvariable=self.diffconc_flow1_var, width=25)
        self.step_flow1_entry.pack(side='left', padx=2)
        self.step_flow1_entry.config(state ='disabled')

        self.diffconc_mfc2_label = ttk.Label(step_controls_frame, text="Flow MFC 2 (mL/min):").pack(side='left')
        self.diffconc_flow2_var = tk.DoubleVar()
        self.step_flow2_entry = ttk.Entry(step_controls_frame, textvariable=self.diffconc_flow2_var, width=25)
        self.step_flow2_entry.pack(side='left', padx=2)
        self.step_flow2_entry.config(state ='disabled')
        
        self.calculate_step_button = ttk.Button(step_controls_frame, text="Calculate Flow Rates", command=self.diffconc_calc_step)
        self.calculate_step_button.pack(side='left', padx=2)
        self.calculate_step_button.config(state = 'disabled')

        # Step buttons
        step_buttons_frame = ttk.Frame(edit_frame)
        step_buttons_frame.pack(fill='both')
        
        self.add_step_button = ttk.Button(step_buttons_frame, text="Add Step", command=self.diffconcadd_step)
        self.add_step_button.pack(side='left', padx=2)
        self.add_step_button.config(state = 'disabled')
        
        self.remove_step_button = ttk.Button(step_buttons_frame, text="Remove Step", command=self.diffconcremove_step)
        self.remove_step_button.pack(side='left', padx=2)
        self.remove_step_button.config(state = 'disabled')
                
        self.clear_steps_button = ttk.Button(step_buttons_frame, text="Clear All Steps", command=self.diffconcclear_steps)
        self.clear_steps_button.pack(side='left', padx=2)
        self.clear_steps_button.config(state = 'disabled')
        
        # Save and run buttons
        action_buttons_frame = ttk.Frame(edit_frame)
        action_buttons_frame.pack(fill='both')
        
        self.save_button = ttk.Button(action_buttons_frame, text="Save Profile", command=self.save_diffconcprofile)
        self.save_button.pack(side='left', padx=2)
        self.save_button.config(state = 'disabled')
        
        self.run_button = ttk.Button(action_buttons_frame, text="Run Profile", command=self.run_diffconcprofile)
        self.run_button.pack(side='left', padx=2)
        self.run_button.config(state = 'disabled')
        
        self.diffconc_stop_button = ttk.Button(action_buttons_frame, text="Stop", command=self.stop_diffconcprofile)
        self.diffconc_stop_button.pack(side='left', padx=2)
        self.diffconc_stop_button.config(state=tk.DISABLED)
    
        # Initialize variables
        self.current_loaded_diffconc_profile = None
    
    def enabling_select_diffconcprofile(self):
        ## Lock the VOC dropdown, total flow and temperature entry
        self.voc_dropdown_diffconcprofile.config(state = 'disabled')
        self.totalflow_entry.config(state = 'disabled')
        # self.temp_entry.config(state = 'disabled')
        
        # Enabling all input fields
        self.step_time_entry.config(state ='enabled')
        self.step_conc_entry.config(state ='enabled')
        # self.step_flow1_entry.config(state ='enabled')
        # self.step_flow2_entry.config(state ='enabled')
        self.step_valve_combo.config(state = 'enabled')

        # Enabling all buttons
        self.calculate_step_button.config(state = 'enabled')
        # self.add_step_button.config(state = 'enabled')
        self.remove_step_button.config(state = 'enabled')
        self.clear_steps_button.config(state = 'enabled')
        self.save_button.config(state = 'enabled')
        self.run_button.config(state = 'enabled')
    
    def disabling_select_diffconcprofile(self):
        ## Lock the VOC dropdown, total flow and temperature entry
        self.voc_dropdown_diffconcprofile.config(state = 'enabled')
        self.totalflow_entry.config(state = 'enabled')
        # self.temp_entry.config(state = 'enabled')
        
        # Enabling all input fields
        self.step_time_entry.config(state ='disabled')
        self.step_conc_entry.config(state ='disabled')
        self.step_flow1_entry.config(state ='disabled')
        self.step_flow2_entry.config(state ='disabled')
        self.step_valve_combo.config(state = 'disabled')

        # Enabling all buttons
        self.calculate_step_button.config(state = 'disabled')
        self.add_step_button.config(state = 'disabled')
        self.remove_step_button.config(state = 'disabled')
        self.clear_steps_button.config(state = 'disabled')
        self.save_button.config(state = 'disabled')
        self.run_button.config(state = 'disabled')        
    
    def update_diffconcprofile_list(self):
        """Refresh the list of available profiles"""
        #https://youtu.be/Vm0ivVxNaA8
        
        #Delete all the items from the listbox
        self.diffconcprofile_listbox.delete(0, tk.END)
        
        #Add all the profiles to the listbox
        for profile in self.diffconcprofilemanager.get_profiles():
            self.diffconcprofile_listbox.insert(tk.END, profile)  #listbox.insert(index, element)

    def load_diffconcprofile(self):
        """Load the selected profile into the editor"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.diffconcprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to load")
            return
        
        #To ensure that you only select the first selected
        profile_name = self.diffconcprofile_listbox.get(selection[0])
        profile = self.diffconcprofilemanager.load_profile(profile_name)
        
        self.new_diffconcprofile_label.config(text = "")
        
        if profile:
            self.current_loaded_profile = profile_name
            #Update the name of the profile
            self.diffconc_namevar.set(profile_name)
            
            #Update the description, temp, voc and total flow in the field
            self.diffconc_desc_var.set(profile.get("description", ""))
            # self.diffconc_temp_var.set(profile.get("temperature", ""))
            self.diffconc_voc_var.set(profile.get("voc", "")) 
            self.diffconc_totalflowrate_var.set(profile.get("total_flow", 0)) 
            
            # Clear the existing steps
            for item in self.diffconc_steps_tree.get_children():
                self.diffconc_steps_tree.delete(item)
            
            # Add new steps
            for step in profile.get("steps", []):
                self.diffconc_steps_tree.insert("", tk.END, values=(
                    step["time"],
                    step["valve"],
                    step["concentration"],
                    step["flow mfc1"],
                    step["flow mfc2"]
                ))
            self.update_diffconc_graph(profile.get("steps", []))
            
            self.status_var.set(f"Loaded profile: {profile_name}")
            
        self.enabling_select_diffconcprofile()
        
    def delete_diffconcprofile(self):
        """Delete the selected profile"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        selection = self.diffconcprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete")
            return
            
        profile_name = self.diffconcprofile_listbox.get(selection[0]) #To ensure that you only select the first selected
        
        if messagebox.askyesno("Confirm", f"Delete profile '{profile_name}'?"):
            if self.diffconcprofilemanager.delete_profile(profile_name):
                #Updating the new profile list
                self.update_diffconcprofile_list() 
                #Changing the status
                self.status_var.set(f"Deleted profile: {profile_name}")
            else:
                messagebox.showerror("Error", f"Failed to delete the profile: '{profile_name}'")
                
    def create_new_diffconcprofile(self):
        #Clearing all input fields and steps
        self.diffconc_namevar.set("")
        self.diffconc_desc_var.set("")
        self.diffconc_voc_var.set("")
        self.diffconc_totalflowrate_var.set("") 
    
        self.diffconc_step_time_var.set("")
        self.diffconc_step_conc_var.set("")
        self.diffconc_flow1_var.set("")
        self.diffconc_flow2_var.set("")
        # self.diffconc_temp_var.set("")
        self.diffconc_valve_var.set("")
        
        for item in self.diffconc_steps_tree.get_children():
            self.diffconc_steps_tree.delete(item)
        
        self.new_diffconcprofile_label.config(text = "New profile", foreground = "green")
        self.disabling_select_diffconcprofile()
  
    def diffconcadd_step(self):
        """Add a new step to the current profile with calculated flows"""
        try:
            #Obtain the values
            time_val = float(self.diffconc_step_time_var.get())
            concentration_val = float(self.diffconc_step_conc_var.get())
            f_voc = self.diffconc_flow1_var.get()
            f_n2 = self.diffconc_flow2_var.get()
            valve_val = int(self.diffconc_valve_var.get())

            if time_val < 0:
                raise ValueError("Time cannot be negative")
            if valve_val not in [1, 2]:
                raise ValueError("Valve position must be 1 or 2")

            for child in self.diffconc_steps_tree.get_children():
                if float(self.diffconc_steps_tree.item(child, "values")[0]) == time_val:
                    if not messagebox.askyesno("Confirm", f"Step at time {time_val}s already exists. Overwrite?"):
                        return
                    self.diffconc_steps_tree.delete(child)
                    break

            # Insert met automatisch berekende flows
            self.diffconc_steps_tree.insert("", tk.END, values=(time_val, valve_val, concentration_val, f_voc, f_n2))
            
            self.calculate_step_button.config(state = 'enabled')
            self.add_step_button.config(state = 'disabled')

        except ValueError as error:
            messagebox.showerror("Error", f"Invalid input: {error}")

    def diffconcremove_step(self):
        """Remove the selected step"""
        selection = self.diffconc_steps_tree.selection()
        if selection:
            self.diffconc_steps_tree.delete(selection)
    
    def diffconcclear_steps(self):
        """Clear all steps"""
        if messagebox.askyesno("Confirm", "Clear all the steps?"):
            #Obtain all the steps and delete all the steps
            for item in self.diffconc_steps_tree.get_children():
                self.diffconc_steps_tree.delete(item)
    
    def save_diffconcprofile(self):
        """Save the current profile"""
        #Getting the name
        name = self.diffconc_namevar.get().strip()
        
        #Ensuring that the name isn't empty
        if not name:
            messagebox.showwarning("Warning", "Profile name cannot be empty")
            return
        
        # Collect steps from the profile
        steps = []
        for child in self.diffconc_steps_tree.get_children():
            #To obtain all the values of the steps
            values = self.diffconc_steps_tree.item(child, "values")
            steps.append({
                "time": float(values[0]),
                "valve": int(values[1]),
                "concentration": float(values[2]),
                "flow mfc1": float(values[3]),
                "flow mfc2": float(values[4])

            })
        
        self.update_diffconc_graph(steps)
            
        # Sort steps by time
        #https://docs.python.org/3/howto/sorting.html
        steps = sorted(steps, key=lambda steps: steps["time"])
        
        # Create the profile data
        profile_data = {
            "description": self.diffconc_desc_var.get(),
            # "temperature": float(self.diffconc_temp_var.get()),
            "voc": self.diffconc_voc_var.get(),  
            "total_flow": float(self.diffconc_totalflowrate_var.get()), 
            "steps": steps
        }
        
        if self.diffconcprofilemanager.save_profile(name, profile_data):
            self.update_diffconcprofile_list()
            self.status_var.set(f"Saved profile: {name}")
        else:
            messagebox.showerror("Error", f"Failed to save profile '{name}'")
    
    def run_diffconcprofile(self):
        """Run the current profile"""    

        ##Koeling Uitzetten omdat hij het nog niet doet
        # # Cooling OFF
        # if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected and self.cooling.connected and self.valve.connected):

        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected and self.valve.connected):
            messagebox.showwarning("Error", "One or more devices are not connected")
            return False
          
        #Get the name of the profile without spaces, such that the .json file can be loaded later
        name = self.diffconc_namevar.get().strip()
        
        #Checking whether the name is empty
        if not name:
            messagebox.showwarning("Warning", "Please load or create a profile first")
            return

        # Load the profile that needs to be runned
        profile = self.diffconcprofilemanager.load_profile(name)
        if not profile:
            messagebox.showerror("Error", f"Failed to load profile: '{name}'")
            return
        
        #To check whether the temperature has already been set to the filled temperature
        # and asking whether it is thermal eq
        if not self.diffconcprofile_checkthermaleq_alarm(profile):
            return
            
        self.update_run_var()
        #Enabling the stop button, since you can now stop a running profile
        self.diffconc_stop_button.config(state=tk.NORMAL) 
        
        # Start profile in a separate thread, such that the UI doesn't freeze until it finishes
        # And you'll still be able to see what happens, e.g. popup of not connection
        self.diffconcprofile_thread = threading.Thread(
            target=self.run_diffconcprofile_thread,
            args=(profile,),    
            daemon=True         # Stops threading by pressing an event, e.g. pressing on stop button
        )
        self.diffconcprofile_thread.start()

    def diffconcprofile_checkthermaleq_alarm(self, profile):
        #Checking whether the temperature has already been set to the filled temperature
        # https://www.pythontutorial.net/tkinter/tkinter-askyesno/
        confirm = messagebox.askyesno(
            "Cooling Plate Temperature",
            f"Did you set the cooling plate temperature to 0 °C? And is the temperature constant and stable?"
        )
        if not confirm:
            return confirm
        return True 

    def run_diffconcprofile_thread(self, profile):      
        try:
            def safe_update(status):
                self.root.after(0, lambda: self.update_diffconcprofile_var(status))

            self.status_var.set(f"Running profile: {self.diffconc_namevar.get()}")
            self.diffconcprofilemanager.run_profile(
                # temp_ambient=self.ambient_temp,
                update_callback=safe_update
            )
            self.root.after(0, self.diffconcprofile_complete)

        except Exception as e:
            self.root.after(0, lambda: self.diffconcprofile_error(e))
    
    def diffconcprofile_complete(self):
        """Called when profile completes successfully"""
        self.diffconc_stop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run completed")
    
    def diffconcprofile_error(self, error):
        """Called when profile run encounters an error"""
        self.diffconc_stop_button.config(state=tk.DISABLED)
        messagebox.showerror("Error", f"Profile run failed: {error}")
        self.status_var.set("Profile run failed")
    
    def stop_diffconcprofile(self):
        """Stop the currently running profile"""
        self.diffconcprofilemanager.stop_profile()
        self.diffconc_stop_button.config(state=tk.DISABLED)
        self.status_var.set("Profile run stopped by user")
    
    def update_diffconcprofile_var(self, status):
        #when the UI is closed then this won't be "updating" (to debug)
        try:
            if not self.root.winfo_exists():
                return
            
            self.diffconc_elapsed_label.config(text=f"{status['elapsed_time']:.1f}s")
            self.diffconc_step_label.config(text=f"{status['current_step']}/{status['total_steps']}")
            self.diffconc_value_label.config(text=f"{status['concentration']} (ppm), mfc1: {status['flow mfc1']:.2f}, mfc2: {status['flow mfc2']:.2f}, valve: {status['valve']}")

                
        except tk.TclError:
            return
        

    def diffconc_calc_step(self):
        try:
            concentration_val = float(self.diffconc_step_conc_var.get())
            total_flow = float(self.diffconc_totalflowrate_var.get())
            voc = self.diffconc_voc_var.get()
            valve_position = int(self.diffconc_valve_var.get())
            print(valve_position)

            f_voc, f_n2, P_s = self.calculate_required_flow_0degrees(voc, concentration_val, total_flow)
            if f_voc is None or f_n2 is None:
                messagebox.showerror("Calculation Error", "Flow could not be calculated for this VOC and concentration.")
                return

            ## Set the values to the corresponding labels
            self.diffconc_flow1_var.set(f_voc)
            self.diffconc_flow2_var.set(f_n2)

            self.add_step_button.config(state = 'enabled')

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            
    def update_diffconc_graph(self, steps):
        #when the UI is closed then this won't be "updating" (to debug)
        try:
            if not self.root.winfo_exists():
                return
        
            times = []
            concs = []

            # Sort steps by time to ensure correct plotting
            steps = sorted(steps, key=lambda s: s.get("time", 0))

            for step in steps:
                time = step.get("time", 0)
                conc = step.get("concentration", 0)
                valve = step.get("valve", 1)
                times.append(time)
                concs.append(conc)

            self.diffconc_ax.clear()
            self.diffconc_ax.step(times, concs, where='post', linestyle='-', marker='o', markersize = 3, linewidth=2, color='red' )
            self.diffconc_ax.set_title("Setpoint Concentration Graph")
            self.diffconc_ax.set_xlim(0, max(times))
            self.diffconc_ax.set_ylim(0, max(concs) * 1.5)
            self.diffconc_ax.set_xlabel("Time (s)")
            self.diffconc_ax.set_ylabel("Concentration (ppm)")
            self.diffconc_ax.grid(True)
            self.diffconc_canvas.draw()

            # Om figure te saven        
            # self.diffconc_fig.savefig("C:/Users/chant/Downloads/setpoint_concentration_plot.png", dpi=300, bbox_inches='tight')
            
        except tk.TclError:
                return

###Add VOCs
    def voc_settings(self):
        window = tk.Toplevel(self.root)
        window.title("VOC Manager")

        vocs = self.settings_manager.get_voc_data()

        # VOC list
        list_frame = ttk.LabelFrame(window, text="Existing VOCs")
        list_frame.pack(padx=15, pady=10, fill="x")

        self.voc_listbox = tk.Listbox(list_frame, height=6, width=40)
        self.voc_listbox.pack(padx=10, pady=5)
        for name in sorted(vocs.keys()):
            self.voc_listbox.insert(tk.END, name)

        self.voc_listbox.bind("<<ListboxSelect>>", self.load_voc_to_entries)

        # New VOC entry
        entry_frame = ttk.LabelFrame(window)
        entry_frame.pack(padx=15, pady=10, fill="x")

        # VOC Name veld
        ttk.Label(entry_frame, text = 'VOC Name').grid(row = 0, column = 0)
        self.voc_name_entry = ttk.Entry(entry_frame, width=25)
        self.voc_name_entry.grid(row=0, column=1)

        self.voc_value_entries = []
        labels = ["Antoine A", "Antoine B", "Antoine C", "Tmin", "Tmax"]
        for i, label in enumerate(labels):
            ttk.Label(entry_frame, text=label).grid(row=i+1, column=0)
            entry = ttk.Entry(entry_frame, width=25)
            entry.grid(row=i+1, column=1)
            self.voc_value_entries.append(entry)

        # New VOC button by clearing the field
        new_button = ttk.Button(entry_frame, text="New VOC", command=self.new_voc_fields)
        new_button.grid(row=6, column=0, padx=5, pady=10)
        
        save_button = ttk.Button(entry_frame, text="Save VOC", command=self.save_voc_from_ui)
        save_button.grid(row=6, column=1, padx=5, pady=10)

        # Delete button
        delete_button = ttk.Button(entry_frame, text="Delete VOC", command=self.delete_voc_from_ui)
        delete_button.grid(row=6, column=2, padx=5, pady=10)
        
    def load_voc_to_entries(self, event=None):
        selection = self.voc_listbox.curselection()
        if not selection:
            return

        voc_name = self.voc_listbox.get(selection[0])
        data = self.settings_manager.get_voc_data().get(voc_name)
        print(data)
        if data:
            self.voc_name_entry.delete(0, tk.END)
            self.voc_name_entry.insert(0, voc_name)

            for i in range(5):
                self.voc_value_entries[i].delete(0, tk.END)
                self.voc_value_entries[i].insert(tk.END, str(data[i]))

    def save_voc_from_ui(self):
        try:
            name = self.voc_name_entry.get().strip()
            if not name:
                raise ValueError("VOC name cannot be empty.")

            values = []
            for voc in self.voc_value_entries:
                val = float(voc.get()) 
                values.append(val)

            print(values)
            self.settings_manager.add_voc(name, values)
            messagebox.showinfo("Success", f"VOC '{name}' is saved.")

            self.refresh_voc_list()
            
            self.voc_name_entry.delete(0, tk.END)
            for voc in self.voc_value_entries:
                voc.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def refresh_voc_list(self):
        voc_names = list(self.settings_manager.get_voc_data().keys())

        self.voc_dropdown_diffconcprofile['values'] = voc_names
        self.voc_dropdown_voccalculator['values'] = voc_names

        #Update the listbox
        self.voc_listbox.delete(0, tk.END)
        for name in sorted(voc_names):
            self.voc_listbox.insert(tk.END, name)
            
    def delete_voc_from_ui(self):
        selected = self.voc_listbox.curselection()
        if not selected:
            messagebox.showwarning("No VOC selected", "Please select a VOC to delete.")
            return

        voc_name = self.voc_listbox.get(selected[0])

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{voc_name}'?")
        if confirm:
            self.settings_manager.delete_voc(voc_name)
            self.refresh_voc_list()
            self.voc_name_entry.delete(0, tk.END)
            for entry in self.voc_value_entries:
                entry.delete(0, tk.END)

            messagebox.showinfo("VOC Deleted", f"'{voc_name}' has been deleted.")
            
    def new_voc_fields(self):
        self.voc_name_entry.delete(0, tk.END)
        for entry in self.voc_value_entries:
            entry.delete(0, tk.END)
        self.voc_listbox.selection_clear(0, tk.END) #clear the selection of the list
