import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import threading
from profilemanager import MFCProfileManager, RVMProfileManager, MFCandRVMProfileManager, DiffConcProfileManager, OnOffConcProfileManager
from settingsmanager import SettingsManager
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AutomatedSystemUI:
    """GUI class for the automated system
    """
    def __init__(self, root):
        """Initializing the GUI
        """
        # Window for the Automated System
        self.root = root
        self.root.title("Automated System")
        self.root.geometry("1400x800")
                        
        # Load the profile paths and com ports for all devices
        self.settings_manager = SettingsManager()
        settings_path = self.settings_manager.get_profiles_path()
        saved_ports = self.settings_manager.get_com_ports()

        # Initialize the MFC and Valve profile managers with the loaded COM port settings
        self.mfcprofilemanager = MFCProfileManager(saved_ports["mfc1"], saved_ports["mfc2"], saved_ports["mfc3"], profiles_dir=settings_path)
        self.valveprofilemanager = RVMProfileManager(saved_ports["valve1"], saved_ports["valve2"], profiles_dir=settings_path)

        # Initialize the MFCs and valves
        self.mfcs = self.mfcprofilemanager.mfcs
        self.valve = self.valveprofilemanager.valve

        # Initialize the profile managers with the loaded COM port settings
        self.mfcandrvmprofilemanager = MFCandRVMProfileManager(UImfcs=self.mfcs, UIvalve=self.valve, profiles_dir=settings_path)
        self.diffconcprofilemanager = DiffConcProfileManager(UImfcs=self.mfcs, UIvalve=self.valve, profiles_dir=settings_path)
        self.onoffconcprofilemanager = OnOffConcProfileManager(UImfcs=self.mfcs, UIvalve=self.valve, profiles_dir=settings_path)

        ############################################## HEADER ##############################################
        # Header frame for connection and status
        header_frame = ttk.Frame(self.root)
        header_frame.pack(side='top', fill='x', padx=5, pady=5)
        
        ######## Connection status frame ########
        connection_frame = ttk.Frame(header_frame)
        connection_frame.pack(side='right', padx=10)
        
        ttk.Label(connection_frame, text="Device Connections", font=("Arial", 10, "bold")).pack(fill = 'both', expand = True)
        #### Connection status labels ####
        self.connection_mfc1_port_label = ttk.Label(connection_frame, 
                                                 text=f"MFC 1 Port: {self.mfcs[0].port}, Connected: {self.mfcs[0].connected}")
        self.connection_mfc1_port_label.pack(fill='both', expand=True)
        
        self.connection_mfc2_port_label = ttk.Label(connection_frame, 
                                                 text=f"MFC 2 Port: {self.mfcs[1].port}, Connected: {self.mfcs[1].connected}")
        self.connection_mfc2_port_label.pack(fill='both', expand=True)
        
        self.connection_mfc3_port_label = ttk.Label(connection_frame, 
                                                 text=f"MFC 3 Port: {self.mfcs[2].port}, Connected: {self.mfcs[2].connected}")
        self.connection_mfc3_port_label.pack(fill='both', expand=True)
        
        self.connection_valve1_port_label = ttk.Label(connection_frame, 
                                                  text=f"RVM 1 Port: {self.valve[0].port}, Connected: {self.valve[0].connected}")
        self.connection_valve1_port_label.pack(fill='both', expand=True)
        
        self.connection_valve2_port_label = ttk.Label(connection_frame, 
                                                  text=f"RVM 2 Port: {self.valve[1].port}, Connected: {self.valve[1].connected}")
        self.connection_valve2_port_label.pack(fill='both', expand=True)
        
        connect_all_button = ttk.Button(connection_frame, text = "Connect all devices", command = self.connect_all_devices)
        connect_all_button.pack(side='right', fill = 'both', expand = 'true')
        
        ######## Frame for status and profile updates ########
        othervar_frame  = ttk.Frame(header_frame)
        othervar_frame.pack(side='right', padx=10)

        #### Status Bar ####
        self.status_var = tk.StringVar() 
        self.status_var.set("Status:")
        status_bar = ttk.Label(header_frame, text='Status', textvariable=self.status_var)
        status_bar.pack(fill='both', padx=5, pady=5)

        # Information Bar with live values, such as mass flow rates and valve positions
        self.running_var_bar = tk.Label(header_frame, text="", anchor="w", relief="sunken")
        self.running_var_bar.pack(side='top', fill='x')
        
        ######### PROFILE STATUS OVERVIEW #########
        overview_profile = ttk.Frame(self.root)
        overview_profile.pack(fill="x", padx=10, pady=5)
        
        # Frae to display current running profiles
        self.profile_status_frame = ttk.LabelFrame(overview_profile, text="Profile Overview")
        self.profile_status_frame.pack(side = "left", padx=10, pady=5)

        # Labels for profile status
        ttk.Label(self.profile_status_frame, text="Profile", font=("Arial", 8, "bold")).grid(row=0, column=0, padx=5, sticky="w")
        ttk.Label(self.profile_status_frame, text="Elapsed Time", font=("Arial", 8, "bold")).grid(row=0, column=1, padx=5, sticky="w")
        ttk.Label(self.profile_status_frame, text="Step", font=("Arial", 8, "bold")).grid(row=0, column=2, padx=5, sticky="w")
        ttk.Label(self.profile_status_frame, text="Value", font=("Arial", 8, "bold")).grid(row=0, column=3, padx=5, sticky="w")

        # Labels for profile status of MFC
        ttk.Label(self.profile_status_frame, text="MFC Running Profile").grid(row=1, column=0, padx=5, sticky="w")
        self.mfc_elapsed_label = ttk.Label(self.profile_status_frame, text="-")
        self.mfc_elapsed_label.grid(row=1, column=1, padx=5, sticky="w")
        self.mfc_step_label = ttk.Label(self.profile_status_frame, text="-")
        self.mfc_step_label.grid(row=1, column=2, padx=5, sticky="w")
        self.mfc_value_label = ttk.Label(self.profile_status_frame, text="-")
        self.mfc_value_label.grid(row=1, column=3, padx=5, sticky="w")

        # Labels for profile status of RVM
        ttk.Label(self.profile_status_frame, text="RVM Running Profile").grid(row=3, column=0, padx=5, sticky="w")
        self.valve_elapsed_label = ttk.Label(self.profile_status_frame, text="-")
        self.valve_elapsed_label.grid(row=3, column=1, padx=5, sticky="w")
        self.valve_step_label = ttk.Label(self.profile_status_frame, text="-")
        self.valve_step_label.grid(row=3, column=2, padx=5, sticky="w")
        self.valve_value_label = ttk.Label(self.profile_status_frame, text="-")
        self.valve_value_label.grid(row=3, column=3, padx=5, sticky="w")

        # Labels for profile status of MFC and RVM Profile
        ttk.Label(self.profile_status_frame, text="MFC and RVM Running Profile").grid(row=4, column=0, padx=5, sticky="w")
        self.mfcvalve_profile_elapsed_label = ttk.Label(self.profile_status_frame, text="-")
        self.mfcvalve_profile_elapsed_label.grid(row=4, column=1, padx=5, sticky="w")
        self.mfcvalve_profile_step_label = ttk.Label(self.profile_status_frame, text="-")
        self.mfcvalve_profile_step_label.grid(row=4, column=2, padx=5, sticky="w")
        self.mfcvalve_profile_value_label = ttk.Label(self.profile_status_frame, text="-")
        self.mfcvalve_profile_value_label.grid(row=4, column=3, padx=5, sticky="w")
        
        # Labels for profile status of Pure Gas Different Concentration Running Profile
        ttk.Label(self.profile_status_frame, text="Pure Gas Different Concentration Running Profile").grid(row=5, column=0, padx=5, sticky="w")
        self.diffconc_elapsed_label = ttk.Label(self.profile_status_frame, text="-")
        self.diffconc_elapsed_label.grid(row=5, column=1, padx=5, sticky="w")
        self.diffconc_step_label = ttk.Label(self.profile_status_frame, text="-")
        self.diffconc_step_label.grid(row=5, column=2, padx=5, sticky="w")
        self.diffconc_value_label = ttk.Label(self.profile_status_frame, text="-")
        self.diffconc_value_label.grid(row=5, column=3, padx=5, sticky="w")
        
        #### Multiple Profile Runner ####
        selectprofiles_frame = ttk.LabelFrame(overview_profile, text="Multiple Profile Runner")
        selectprofiles_frame.pack(side="right")
        
        # Labels for listboxes of MFC profiles and Valve Profiles
        ttk.Label(selectprofiles_frame, text="MFC Profiles").grid(row=0, column=0)
        ttk.Label(selectprofiles_frame, text="Valve Profiles").grid(row=0, column=1)

        ## Multiple Profile: MFC Profile Listbox ##
        # Frame for listbox of MFC profile
        mfc_listbox_frame = ttk.Frame(selectprofiles_frame)
        mfc_listbox_frame.grid(row=1, column=0, padx=5, pady=5)
        
        # Create a listbox to display the available MFC profiles
        # # https://www.pythontutorial.net/tkinter/tkinter-listbox/#adding-a-scrollbar-to-the-listbox
        # # Making an empty profile listbox
        # Exportseleciton = False, such that when you select another listbox you still can have your selection
        self.selprof_mfc_listbox = tk.Listbox(mfc_listbox_frame, height=2, exportselection=False)
        self.selprof_mfc_listbox.pack(side='left', fill='y')
        
        # Add vertical scrollbar to MFC listbox
        mfc_v_scrollbar = ttk.Scrollbar(mfc_listbox_frame, orient=tk.VERTICAL, command=self.selprof_mfc_listbox.yview)
        mfc_v_scrollbar.pack(side='right', fill='y')
        
        # Link the scrollbar to the MFC listbox
        self.selprof_mfc_listbox.config(yscrollcommand=mfc_v_scrollbar.set)

        # Add profiles to the MFC listboxes
        for profile in self.mfcprofilemanager.get_profiles():
            self.selprof_mfc_listbox.insert(tk.END, profile)

        ## Multiple Profile: Valve Profile Listbox ##
        
        # Create a listbox to display the available Valve profiles    
        # Frame for listbox of Valve profile
        valve_listbox_frame = ttk.Frame(selectprofiles_frame)
        valve_listbox_frame.grid(row=1, column=1, padx=5, pady=5)
        self.selprof_valve_listbox = tk.Listbox(valve_listbox_frame, height=2, exportselection=False)
        self.selprof_valve_listbox.pack(side='left', fill='y')
        
        # Add vertical scrollbar to RVM listbox
        valve_v_scrollbar = ttk.Scrollbar(valve_listbox_frame, orient=tk.VERTICAL, command=self.selprof_valve_listbox.yview)
        valve_v_scrollbar.pack(side='right', fill='y')
        
        # Link the scrollbar to the RVM listbox
        self.selprof_valve_listbox.config(yscrollcommand=valve_v_scrollbar.set)
        ##

        # Add profiles to the RVM listboxes
        for profile in self.valveprofilemanager.get_profiles():
            self.selprof_valve_listbox.insert(tk.END, profile)

        # Run Button to run the selected profiles of the MFC and RVM listboxes
        ttk.Button(selectprofiles_frame, text="Run Selected Profiles", command=self.run_selected_profiles).grid(row=1, column=3, padx=10)

        # Stop Button to stop the selected profiles of the MFC and RVM listboxes
        self.stop_all_button = ttk.Button(selectprofiles_frame, text="Stop Selected Profiles", command=self.stop_all_profiles)
        self.stop_all_button.grid(row=2, column=3, padx=10, pady= 5)  
        self.stop_all_button.config(state='disabled')

        ######### Notebook for tabs #########
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Add all tabs
        self.create_menu()
        self.create_device_tab()
        self.create_puregas_onoff_profile()
        self.create_diffconc_profile_tab()
        self.create_mfcandvalveprofile_tab()
        self.create_mfcprofile_tab()
        self.create_valveprofile_tab()


    def create_scrollable_tab(self, notebook, tab_name):
        """Create a scrollable tab

        Args:
            notebook: Parent notebook at which the tab will be added
            tab_name (str): The name of the tab

        Returns:
            scrollable_frame: Tab that supports vertical scrolling
        """
        # Create a new tab and add it to the notebook
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=tab_name)

        # Create a canvas inside the tab 
        canvas = tk.Canvas(tab)
        
        # Add vertical scollbar to the canvas
        v_scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=v_scrollbar.set)
        v_scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Create a frame inside the canvas for the widgets
        scrollable_frame = ttk.Frame(canvas)
        
        # Top left corner place a scrollable frame
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Update the scroll region
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        # Bind configure_scroll_region to configure events
        # Such that everytime the scrollable_frame changes it size, the canvas updates its scrollable frame
        scrollable_frame.bind("<Configure>", configure_scroll_region)

        return scrollable_frame
    
    def update_run_var(self):
        """Updates the UI with live readings from the connected MFCs and RVMs
        """
        try:
            # When the UI is closed then this function stops with 'updating'
            if not self.root.winfo_exists():
                return
        
            ######## Update MFCs mass flow rates ########
            massflows = []
            
            # For each MFC
            for i in range(3):
                if self.mfcs[i].connected:
                    # When connected to the real devices
                    # flow = self.mfcs[i].get_massflow()[0]['data']
            
                    # To simulate, so connected to the simulated devices
                    flow = self.mfcs[i].get_massflow()
                    flow_str = f"{flow} mL/min"
                    
                else:
                    # If MFC not connected, display "-"
                    flow = None
                    flow_str = "-"
                # Store the massflow to the list 
                massflows.append(flow_str)
                # Update label in the device tab
                self.current_massflow_labels[i].config(text=f"Current mass flow rate: {flow_str}")

            ######## Update RVM positions ########
            valveposition = []
            
            # For each RVM
            for i in range(2):
                if self.valve[i].connected:
                    # Get the current valve posiiton
                    pos = self.valve[i].get_position()

                else:
                    # If RVM not connected, display "-"
                    pos = "-"
                # Store valve position to the list
                valveposition.append(pos)
                # Update label in the device tab
                self.current_position_labels[i].config(text=f"Current position of the valve: {pos}")

            ######## Update Information bar with live values ########
            self.running_var_bar.config(
                text=(
                    f"Reading Values   : "
                    f"MFC 1 (N2) Mass Flow Rate: {massflows[0]} | "
                    f"MFC 2 Mass Flow Rate: {massflows[1]} | "
                    f"MFC 3 Mass Flow Rate: {massflows[2]} | "
                    f"RVM 1 Position: {valveposition[0]} | "
                    f"RVM 2 Position: {valveposition[1]} | "
                )
            )
            
            # Run this function after 1000 ms (1s)
            self.root.after(1000, self.update_run_var)
        
        # To avoid crashing if the function is called after the UI is already closed
        except tk.TclError:
            return

    def create_menu(self):
        """Creates menu bar in the main window
        
        Add a Settings dropdown in the menu bar with:
        - Configuration settings: to set COM-Ports and profile directory path
        - VOC Settings: configuration of the VOCs with the corresponding Antoine coefficients A, B, C and corresponding Tmin and Tmax
        """
        # Create a top-level menu bar
        menu = tk.Menu(self.root)
        
        # Create "Settings" submenu
        settings_menu = tk.Menu(menu, tearoff=0)
        # Add Configuration Settings to the dropdown submenu
        settings_menu.add_command(label="Configuration Settings", command=self.com_settings)
        # Add Configuration Settings to the dropdown submenu
        settings_menu.add_command(label="VOC settings", command=self.voc_settings)
        
        # Add the Settings menu to the menubar
        menu.add_cascade(label="Settings", menu=settings_menu)

        # Attach the menu to the main window
        self.root.config(menu=menu)
    
    def create_device_tab(self):
        """Creates Device Control tab in the GUI to manually manage the MFCs and RVMs.
        """
        # Create scrollable tab with the name 'Device Control'
        device_tab = self.create_scrollable_tab(self.notebook, "Device Control")

        ###########################	MFC	###########################
        # Frame for all MFC frames
        all_mfc_frame = ttk.LabelFrame(device_tab)
        all_mfc_frame.pack(fill='x', padx=10, pady=5)
        
        # lists to store the widgets for each MFC
        self.mfc_frames = []
        self.massflow_vars = []
        self.current_massflow_labels = []
        self.target_massflow_labels = []
        
        # Creating 3 MFC frames
        for i in range(len(self.mfcs)):
            self.create_mfc_frame(all_mfc_frame, i)
        
        ###########################	RVM	###########################
        # Frame for all RVM frames
        all_valve_frame = ttk.LabelFrame(device_tab)
        all_valve_frame.pack(fill='x', padx=10, pady=5)

        # lists to store the widgets for each RVM
        self.valve_frames = []
        self.position_vars = []
        self.current_position_labels = []
        self.target_position_labels = []

        # Creating 2 RVM frames
        for i in range(len(self.valve)):
            self.create_valve_frame(all_valve_frame, i)
    
    def create_valve_frame(self, parent, index):
        """Creates the frame for the RVM with widgets

        Args:
            parent: The widget frame where this RVM frame should be placed
            index (int): The index of the RVM for which this frame is
        """
        
        # Retrieve the valve object
        valve = self.valve[index]
        
        # Label frame such that the user can see which index this valve frame is meant for
        frame = ttk.LabelFrame(parent, text=f'RVM {index + 1}')
        frame.grid(row=0, column=index, padx=10, pady=5)

        # Combobox such that the user can select what the desired valve position is for the valve object
        tk.Label(frame, text="RVM Position").grid(row=0, column=0, padx=10, pady=10)
        var = tk.IntVar()
        entry = ttk.Combobox(frame, textvariable=var, values=[1, 2], width=5, state="readonly")
        entry.grid(row=0, column=1, padx=10, pady=10)
        entry.current(0) #Assign a standard value
        self.position_vars.append(var)

        # Button the set the selected valve position
        tk.Button(frame, text="Set RVM Position", command=lambda i=index: self.set_valve(i)).grid(
            row=1, column=0, columnspan=2, pady=10)

        # Label to display the current valve position
        current_label = tk.Label(frame, text="Current RVM position: Not available")
        current_label.grid(row=2, column=0, padx=10, pady=10)
        self.current_position_labels.append(current_label)

        # Lavel to display the desired/target valve posiiton
        target_label = tk.Label(frame, text=f"Target RVM position: Not available")
        target_label.grid(row=2, column=1, padx=10, pady=10)
        self.target_position_labels.append(target_label)

        # Button to connect the valve
        tk.Button(frame, text="Connect", command=lambda i=index: self.connect_valve(i)).grid(row=3, column=0, padx=10, pady=10)
        # Button to disconnect the valve
        tk.Button(frame, text="Disconnect", command=lambda i=index: self.disconnect_valve(i)).grid(row=3, column=1, padx=10, pady=10)
        
    def create_mfc_frame(self, parent, index):
        """Creates the frame for the MFC with widgets

        Args:
            parent: The widget frame where this MFC frame should be placed
            index (int): The index of the MFC for which this frame is
        """
        
        # Retrieve the MFC object
        mfc = self.mfcs[index]
        
        # Label frame such that the user can see which index this valve frame is meant for
        frame = ttk.LabelFrame(parent, text=f'MFC {index + 1}')
        frame.grid(row=0, column=index, padx=10, pady=5)

        # Label and entry field to set the desired mass flow rate
        tk.Label(frame, text="Mass flow rate (mL/min):").grid(row=0, column=0, padx=10, pady=10)
        var = tk.DoubleVar()
        entry = tk.Entry(frame, textvariable=var)
        entry.grid(row=0, column=1, padx=10, pady=10)
        self.massflow_vars.append(var)

        # Button to set the mass flow rate to the MFC
        tk.Button(frame, text="Set mass flow rate", command=lambda i=index: self.set_MFCmassflow(i)).grid(
            row=1, column=0, columnspan=2, pady=10)

        # Label to show the current mass flow rate
        current_label = tk.Label(frame, text="Current mass flow rate: Not available", width=35, anchor="w")
        current_label.grid(row=2, column=0, padx=10, pady=10)
        self.current_massflow_labels.append(current_label)

        # Label to show the target mass flow rate
        target_label = tk.Label(frame, text=f"Target mass flow rate: {mfc.targetmassflow:.2f} mL/min", width=35, anchor="w")
        target_label.grid(row=2, column=1, padx=10, pady=10)
        self.target_massflow_labels.append(target_label)

        # Button to connect to the MFC
        tk.Button(frame, text="Connect", command=lambda i=index: self.connect_MFC(i)).grid(row=3, column=0, columnspan=2, pady=10)
        
    def connect_all_devices(self):
        """Connect all MFCs and RVMs
        """
        # Connect all MFCs and RVMs
        self.connect_MFC(index = 0)
        self.connect_MFC(index = 1)
        self.connect_MFC(index = 2)
        self.connect_valve(index = 0)
        self.connect_valve(index = 1)

        # Show in the status bar that all MFCs and RVMs are disconnected
        self.status_var.set(f"MFC1, MFC2, MFC3, RVM 1 and RVM2 are connected")
   
    def update_connection_devices(self):
        """Update the GUI labels at the top interface showing connection status and COM ports of each device
        """
        #Labels at the header for MFCs with the COM ports and connection status
        self.connection_mfc1_port_label.config (text=f"MFC 1 Port: {self.mfcs[0].port}, Connected: {self.mfcs[0].connected}")
        self.connection_mfc2_port_label.config (text=f"MFC 2 Port: {self.mfcs[1].port}, Connected: {self.mfcs[1].connected}")
        self.connection_mfc3_port_label.config (text=f"MFC 3 Port: {self.mfcs[2].port}, Connected: {self.mfcs[2].connected}")
        self.connection_valve1_port_label.config(text=f"RVM 1 Port: {self.valve[0].port}, Connected: {self.valve[0].connected}")
        self.connection_valve2_port_label.config(text=f"RVM 2 Port: {self.valve[1].port}, Connected: {self.valve[1].connected}")

    def com_settings(self):
        """Settings window where the user can configure COM ports and select the directory path to save the profile.
        """
        # Creates top level window for settings
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Connection Settings")
        settings_window.geometry("400x400")
        
        # Forcing the focus on the top level until the toplevel is closed
        settings_window.grab_set()
        
        ############ Bronkhorst MFC settings ############
        MFC_frame = ttk.LabelFrame(settings_window, text="Bronkhorst MFC")
        MFC_frame.pack(fill="both", padx=10, pady=10)
        
        # Label and entry field for MFC1 Port
        ttk.Label(MFC_frame, text="MFC 1 Port:").grid(row=0, column=0, padx=5, pady=5)
        self.MFC1_port_var = tk.StringVar(value=self.mfcs[0].port)
        MFC1_port_entry = ttk.Entry(MFC_frame, textvariable=self.MFC1_port_var)
        MFC1_port_entry.grid(row=0, column=1, padx=5, pady=5)

        # Label and entry field for MFC2 Port
        ttk.Label(MFC_frame, text="MFC 2 Port:").grid(row=1, column=0, padx=5, pady=5)
        self.MFC2_port_var = tk.StringVar(value=self.mfcs[1].port)
        MFC2_port_entry = ttk.Entry(MFC_frame, textvariable=self.MFC2_port_var)
        MFC2_port_entry.grid(row=1, column=1, padx=5, pady=5)

        # Label and entry field for MFC3 Port
        ttk.Label(MFC_frame, text="MFC 3 Port:").grid(row=2, column=0, padx=5, pady=5)
        self.MFC3_port_var = tk.StringVar(value=self.mfcs[2].port)
        MFC3_port_entry = ttk.Entry(MFC_frame, textvariable=self.MFC3_port_var)
        MFC3_port_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ############ RVM settings ############
        valve_frame = ttk.LabelFrame(settings_window, text="RVM Industrial Microfluidic Rotary valve ")
        valve_frame.pack(fill="both", padx=10, pady=10)

        # Label and entry field for RVM1 Port
        ttk.Label(valve_frame, text="RVM 1 Port:").grid(row=4, column=0, padx=5, pady=5)
        self.valve1_port_var = tk.StringVar(value=self.valve[0].port)
        valve1_port_entry = ttk.Entry(valve_frame, textvariable=self.valve1_port_var)
        valve1_port_entry.grid(row=4, column=1, padx=5, pady=5)

        # Label and entry field for RVM2 Port
        ttk.Label(valve_frame, text="RVM 2 Port:").grid(row=5, column=0, padx=5, pady=5)
        self.valve2_port_var = tk.StringVar(value=self.valve[1].port)
        valve2_port_entry = ttk.Entry(valve_frame, textvariable=self.valve2_port_var)
        valve2_port_entry.grid(row=5, column=1, padx=5, pady=5)
        
        ############ Directory path for profiles settings ############
        profile_frame = ttk.LabelFrame(settings_window, text="Directory Path for Profiles")
        profile_frame.pack(fill="both", padx=10, pady=10)

        # Label for the path
        path_label = ttk.Label(profile_frame, text="Path:")
        path_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.settings_path_var = tk.StringVar(value=self.settings_manager.get_profiles_path())
        ttk.Entry(profile_frame, textvariable=self.settings_path_var, width=35).grid(row=0, column=1, padx=5, pady=5)

        # Function for opening a directory browser dialog
        def browse_profile_path():
            path = filedialog.askdirectory()
            if path:
                self.settings_path_var.set(path)

        # Button to browse for a profile directory
        browse_button = ttk.Button(profile_frame, text="Bladeren...", command=browse_profile_path)
        browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Button to save the settings
        save_button = ttk.Button(settings_window, text="Save", command=self.save_settings)
        save_button.pack(pady=10)
        
    def save_settings(self):
        """Saves the updated COM port and directory path for profiles
        """
        # Gather the current COM port entries from the UI into a dictionary
        com_ports = {
            "mfc1": self.MFC1_port_var.get(),
            "mfc2": self.MFC2_port_var.get(),
            "mfc3": self.MFC3_port_var.get(),
            "valve1": self.valve1_port_var.get(),
            "valve2": self.valve2_port_var.get()
        }
        
        # Save COM port in settingsmanager
        self.settings_manager.set_com_ports(com_ports)     
        
        # Get updated profile path from the UI
        new_path = self.settings_path_var.get()
        
        # Save the profile path
        self.settings_manager.set_profiles_path(new_path)
        
        # Reload all devices and apply the new settings
        self.reload_all_devices()   
        
        # Update status bar showing that settings are updated
        self.status_var.set("The settings are updated.")
        
        # Asks the user to restart the GUI, since the MFC can't be disconnected, but the connection status is set to failed, which can occur errors
        messagebox.showwarning("Restart", "Please restart the GUI")
        return

    def reload_all_devices(self):    
        """ Reload all MFCs and RVMs using the current settings
        """       
        # Obtain the assigned comports
        saved_ports = self.settings_manager.get_com_ports()
        # Get the profile directory path
        new_path = self.settings_path_var.get()

        # Reinitialize the settings manager with new base directory
        self.settings_manager = SettingsManager(base_dir = new_path)
        
        # Create new profile mamagers with updated COM ports and paths
        self.mfcprofilemanager = MFCProfileManager(saved_ports["mfc1"], saved_ports["mfc2"], saved_ports["mfc3"], new_path)
        self.valveprofilemanager = RVMProfileManager(saved_ports["valve1"],saved_ports["valve2"], new_path)

        # Update the MFC and valve objects
        self.mfcs = self.mfcprofilemanager.mfcs
        self.valve = self.valveprofilemanager.valve

        # Update the MFCandRVMProfileManager, DiffConcProfileManager and OnOffConcProfileManager
        self.mfcandrvmprofilemanager = MFCandRVMProfileManager(UImfcs=self.mfcs, UIvalve=self.valve, profiles_dir=new_path)
        self.diffconcprofilemanager = DiffConcProfileManager(UImfcs=self.mfcs, UIvalve=self.valve, profiles_dir=new_path)
        self.onoffconcprofilemanager = OnOffConcProfileManager(UImfcs=self.mfcs, UIvalve=self.valve, profiles_dir=new_path)

        # Update the labels about the COM ports and connection status
        self.connection_mfc1_port_label.config(text=f"MFC 1 Port: {self.mfcs[0].port}, Connected: {self.mfcs[0].connected}")
        self.connection_mfc2_port_label.config(text=f"MFC 2 Port: {self.mfcs[1].port}, Connected: {self.mfcs[1].connected}")
        self.connection_mfc3_port_label.config(text=f"MFC 3 Port: {self.mfcs[2].port}, Connected: {self.mfcs[2].connected}")
        self.connection_valve1_port_label.config(text=f"RVM 1 Port: {self.valve[0].port}, Connected: {self.valve[0].connected}")
        self.connection_valve2_port_label.config(text=f"RVM 2 Port: {self.valve[1].port}, Connected: {self.valve[1].connected}")

   ######################### MFC PROFILE  #########################
    def create_mfcprofile_tab(self):
        """Creates a tab for MFC Management
        """
        # Create scrollable frame with the name 'MFCs Profile Management'
        profile_tab = self.create_scrollable_tab(self.notebook, "MFCs Profile Management")        
        
        ## Split into two frames: list_frame and edit_frame
        
        # List frame displaying the list with the available profiles
        list_frame = ttk.Frame(profile_tab, width = 400)
        list_frame.pack(side= 'left', fill = 'both', expand=True, padx=10, pady=10)
        list_frame.pack_propagate(False)

        # Edit frame where the user can edit the profile and fill in the daa for new profiles
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
        # Frame for the profile list buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', padx=5, pady=5)

        # Button to load the profile
        load_button = ttk.Button(button_frame, text="Load", command=self.load_mfcprofile)
        load_button.pack(side='left', padx=3, expand=True)

        # Button to delete the profile
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_mfcprofile)
        delete_button.pack(side='left', padx=3, expand=True)
        
        ############# Right frame / edit frame #############
        # Edit frame where the user can edit the profile and fill in the daa for new profiles
        info_frame = ttk.Frame(edit_frame)
        info_frame.pack(fill='both', padx=5, pady=5)

        # Label to display the text 'new profile' when the user want to add a new profile 
        self.new_mfcprofile_label = ttk.Label(info_frame, text="")
        self.new_mfcprofile_label.pack(side = 'left', padx=5, expand=True, fill='x')

        # Label and entry field for profile name
        ttk.Label(info_frame, text="Name:").pack(side='left')
        self.mfcname_var = tk.StringVar()
        name_entry = ttk.Entry(info_frame, textvariable=self.mfcname_var)
        name_entry.pack(side='left', padx=5, expand=True, fill='x')

        # Label and entry field for profile description  
        ttk.Label(info_frame, text="Description:").pack(side='left')
        self.mfcdesc_var = tk.StringVar()
        desc_entry = ttk.Entry(info_frame, textvariable=self.mfcdesc_var)
        desc_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        # Button to add a new profile
        new_profile_btn = ttk.Button(info_frame, text = 'New Profile', command = self.create_new_mfcprofile)
        new_profile_btn.pack(side='right', padx=3, expand=True)

        # Frame to show the steps
        steps_frame = ttk.Frame(edit_frame)
        steps_frame.pack(fill = 'both' , expand=True, padx=5, pady=5)

        # Tree to show steps in the right frame
        #https://tk-tutorial.readthedocs.io/en/latest/tree/tree.html
        self.mfcsteps_tree = ttk.Treeview(
            steps_frame, 
            columns=("time", "flow mfc1", "flow mfc2", "flow mfc3", "valve"), 
            show="headings"
        )
        self.mfcsteps_tree.heading("time", text="Time (s)")
        self.mfcsteps_tree.heading("flow mfc1", text="Flow N2 (mL/min)")
        self.mfcsteps_tree.heading("flow mfc2", text="Flow MFC 2 (mL/min)")
        self.mfcsteps_tree.heading("flow mfc3", text="Flow MFC 3 (mL/min)")
        
        self.mfcsteps_tree.column("time", width=250, anchor=tk.CENTER)
        self.mfcsteps_tree.column("flow mfc1", width=250, anchor=tk.CENTER)
        self.mfcsteps_tree.column("flow mfc2", width=250, anchor=tk.CENTER)
        self.mfcsteps_tree.column("flow mfc3", width=250, anchor=tk.CENTER)
        
        self.mfcsteps_tree.pack(fill = 'both' , expand=True)

        # Frame for the entry field of the steps
        step_controls_frame = ttk.Frame(edit_frame)
        step_controls_frame.pack(fill='x', padx=5, pady=5)

        # Label and entry field for the time of the step
        self.mfcprofile_time_label = ttk.Label(step_controls_frame, text="Time (s):").pack(side='left')
        self.mfcstep_time_var = tk.DoubleVar()
        step_time_entry = ttk.Entry(step_controls_frame, textvariable=self.mfcstep_time_var, width=8)
        step_time_entry.pack(side='left', padx=5)
        
        # Label and entry field for the flow of N2 (MFC1) of the step
        self.mfcprofile_mfc1_label = ttk.Label(step_controls_frame, text="Flow N2 (mL/min):").pack(side='left')
        self.mfcstep_flow1_var = tk.DoubleVar()
        step_flow1_entry = ttk.Entry(step_controls_frame, textvariable=self.mfcstep_flow1_var, width=8)
        step_flow1_entry.pack(side='left', padx=5)

        # Label and entry field for the flow of MFC2 of the step
        self.mfcprofile_mfc2_label = ttk.Label(step_controls_frame, text="Flow MFC 2 (mL/min):").pack(side='left')
        self.mfcstep_flow2_var = tk.DoubleVar()
        step_flow2_entry = ttk.Entry(step_controls_frame, textvariable=self.mfcstep_flow2_var, width=8)
        step_flow2_entry.pack(side='left', padx=5)

        # Label and entry field for the flow of MFC3 of the step
        self.mfcprofile_mfc3_label = ttk.Label(step_controls_frame, text="Flow MFC 3 (mL/min):").pack(side='left')
        self.mfcstep_flow3_var = tk.DoubleVar()
        step_flow3_entry = ttk.Entry(step_controls_frame, textvariable=self.mfcstep_flow3_var, width=8)
        step_flow3_entry.pack(side='left', padx=5)
        
        ########## Buttons for the step ##########
        ## Frame to add and remove a step, and clear all steps ##
        step_buttons_frame = ttk.Frame(edit_frame)
        step_buttons_frame.pack(fill='both')

        # Button to add a new step        
        add_step_button = ttk.Button(step_buttons_frame, text="Add Step", command=self.add_mfcstep)
        add_step_button.pack(side='left', padx=2)
        
        # Button to remove a step        
        remove_step_button = ttk.Button(step_buttons_frame, text="Remove Step", command=self.remove_mfcstep)
        remove_step_button.pack(side='left', padx=2)
        
        # Button to clear all steps
        clear_steps_button = ttk.Button(step_buttons_frame, text="Clear All Steps", command=self.clear_mfcsteps)
        clear_steps_button.pack(side='left', padx=2)
        
        ## Frame for actions such as save, run and stop profile ##
        action_buttons_frame = ttk.Frame(edit_frame)
        action_buttons_frame.pack(fill='both')

        # Button to save the profile
        save_button = ttk.Button(action_buttons_frame, text="Save Profile", command=self.save_mfcprofile)
        save_button.pack(side='left', padx=2)
                
        ## Button to run the profile
        run_button = ttk.Button(action_buttons_frame, text="Run Profile", command=self.run_mfcprofile)
        run_button.pack(side='left', padx=2)
                
        ## Button to stop running the profile
        self.mfcstop_button = ttk.Button(action_buttons_frame, text="Stop", command=self.stop_mfcprofile)
        self.mfcstop_button.pack(side='left', padx=2)
        self.mfcstop_button.config(state='disabled')
    
    def connect_MFC(self, index):
        """Connect to specific MFC by index.
        If successful, update the UI.

        Args:
            index (int): The index of the MFC, indicating which MFC
        """
        # Trying to connect with the MFC
        if self.mfcs[index].connect():
            # Update the device statuses in the GUI
            self.update_connection_devices()
            
            # Show in the status bar that the MFC is connected
            self.status_var.set(f"MFC {index + 1} connected")
            
            # Enabling automatic updates in function update_massflow
            self.keep_updating_mfc = True
        else:
            # Show error message when connection fails
            messagebox.showinfo("Connection Failed", f"MFC {index + 1} is not connected")

    def set_MFCmassflow(self, index):
        """Sets the target mass flow rate for the specific MFC by index

        Args:
            index (int): index of the MF
        """
        # Get the desired mass flow rate entered by the user
        massflowrate = self.massflow_vars[index].get()
        
        # Set the massflow rate to the device
        if self.mfcs[index].set_massflow(massflowrate):
            # If settings is successfull, update the corresponding target label
            self.target_massflow_labels[index].config(text=f"Target mass flow rate: {self.mfcs[index].targetmassflow} mL/min")
            
            # Enabling that the massflow will continously updated
            self.update_massflow(index)
        else:
            # Messagebox if setting the massflow fails.
            messagebox.showerror("Error", f"Failed to set mass flow rate to {massflowrate} for MFC {index + 1}.")
                    
    def update_massflow(self, index):
        """ Updating the current mass flow rate reading for a specific MFC

        Args:
            index (int): the index of the MFC to update (0-based)
        """
        try:
            # When the UI is closed then this function won't be "updating"
            if not self.root.winfo_exists():
                return

            # Stop updating if flag is turned off
            if not self.keep_updating_mfc:
                return
            
            # When connected to the real device
            # current_flow = self.mfcs[index].get_massflow()[0]['data']
            
            # When simulating the devices
            current_flow = self.mfcs[index].get_massflow()
            
            # Ensuring that the values will be updates in the GUI
            self.update_run_var()
            
            # If obtained massflow has a value, update the label
            if current_flow is not None:
                self.current_massflow_labels[index].config(text=f"Current mass flow rate: {current_flow:.2f} mL/min")
            else:
                messagebox.showerror("Read Error", f"Failed to read mass flow rate from MFC {index + 1}.")
            
            # Passing the index to the function by using lambda
            # Lambda are anonymous function means that the function is without a name
            # https://www.geeksforgeeks.org/using-lambda-in-gui-programs-in-python/
            # Updating the MFC flow rate reading each 1s
            self.root.after(1000, lambda: self.update_massflow(index)) 
            
        except tk.TclError:
            return
        
    def update_mfcprofile_list(self):
        """Refresh the list of available MFC profiles"""
        #https://youtu.be/Vm0ivVxNaA8
        
        #Delete all the items from the listbox
        self.mfcprofile_listbox.delete(0, tk.END)
        
        #Add all the profiles to the listbox
        for profile in self.mfcprofilemanager.get_profiles():
            #Append the profiles at the end
            self.mfcprofile_listbox.insert(tk.END, profile) 

    def load_mfcprofile(self):
        """Load the selected MFC profile"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        # Get the currently selected item in the listbox
        selection = self.mfcprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to load")
            return
        
        # Get the name of the selected profile (first selected item)
        profile_name = self.mfcprofile_listbox.get(selection[0])
        
        # Load the profile with MFC profile manager
        profile = self.mfcprofilemanager.load_profile(profile_name)

        # Clear label for new profiles
        self.new_mfcprofile_label.config(text = "")
        
        if profile:
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
                
            # Update the status bar to update the user that profile is loaded
            self.status_var.set(f"Loaded profile: {profile_name}")
        
    def delete_mfcprofile(self):
        """Delete the selected MFC profile"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        
        # Get selected item from the listbox
        selection = self.mfcprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete")
            return

        # Get the name of the selected profile (first selected item)
        profile_name = self.mfcprofile_listbox.get(selection[0]) #To ensure that you only select the first selected

        # Ask for user confirmation before deleting the profile
        if messagebox.askyesno("Confirm", f"Delete profile '{profile_name}'?"):
            if self.mfcprofilemanager.delete_profile(profile_name):
                #Updating the new profile list
                self.update_mfcprofile_list() 
                #Changing the status
                self.status_var.set(f"Deleted profile: {profile_name}")
            else:
                # If profile deleting fails, show error message
                messagebox.showerror("Error", f"Failed to delete the profile: '{profile_name}'")
                
    def create_new_mfcprofile(self):
        """Clear all fields for new MFC profile
        """
        #Clearing all input fields and steps
        self.mfcname_var.set("")
        self.mfcdesc_var.set("")
        self.mfcstep_time_var.set("0.0")
        self.mfcstep_flow1_var.set("0.0")
        self.mfcstep_flow2_var.set("0.0")
        self.mfcstep_flow3_var.set("0.0")

        # Clear all entries of the existing steps in the tree
        for item in self.mfcsteps_tree.get_children():
            self.mfcsteps_tree.delete(item)
        
        # Show the user that a new profile is made, with the text new profile
        self.new_mfcprofile_label.config(text = "New profile", foreground = "green")
        
    def add_mfcstep(self):
        """Add a new step to the current MFC profile"""
        try:
            # Get input values from the entry fields
            time_val = float(self.mfcstep_time_var.get())
            flow1_val = float(self.mfcstep_flow1_var.get())
            flow2_val = float(self.mfcstep_flow2_var.get())
            flow3_val = float(self.mfcstep_flow3_var.get())
            
            # Time should not be negative
            if time_val < 0:
                raise ValueError("Time cannot be negative")
            
            # Check if the time already exists
            for child in self.mfcsteps_tree.get_children():
                if float(self.mfcsteps_tree.item(child, "values")[0]) == time_val:
                    # Ask user to confirm if they want to overwrite the existing step
                    if not messagebox.askyesno("Confirm", f"Step at time {time_val}s already exists. Overwrite?"):
                        #if True, thus User selects 'NO' then return
                        return 
                    # Remove the existing step
                    self.mfcsteps_tree.delete(child) 
                    break
 
            # Insert the new step to the tree
            self.mfcsteps_tree.insert("", tk.END, values=(time_val, flow1_val, flow2_val, flow3_val)) 
            
        except ValueError as error:
            # If invalid input values, show error messagebox
            messagebox.showerror("Error", f"Invalid input: {error}")
    
    def remove_mfcstep(self):
        """Remove the selected step from the MFC profile"""
        # Get the selected item
        selection = self.mfcsteps_tree.selection()
        # Delete the selected item
        if selection:
            self.mfcsteps_tree.delete(selection)
    
    def clear_mfcsteps(self):
        """Clear all steps from the MFC profile"""
        # Ask the user for confirmation before clearing all the steps
        if messagebox.askyesno("Confirm", "Clear all the steps?"):
            #Loop through all the steps and delete them
            for item in self.mfcsteps_tree.get_children():
                self.mfcsteps_tree.delete(item)
    
    def save_mfcprofile(self):
        """Save the current MFC profile"""
        # Get the profile name
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
            })
        
        # Sort steps by time
        #https://docs.python.org/3/howto/sorting.html
        steps = sorted(steps, key=lambda steps: steps["time"])
        
        # Create the profile data
        profile_data = {
            "description": self.mfcdesc_var.get(),
            "steps": steps
        }
        
        # Save the profile use the profile manager
        if self.mfcprofilemanager.save_profile(name, profile_data):
            # Update the list and show it in the status bar
            self.update_mfcprofile_list()
            self.status_var.set(f"Saved profile: {name}")
        else:
            # If saving failed, show error message
            messagebox.showerror("Error", f"Failed to save profile '{name}'")
    
    def run_mfcprofile(self):
        """Run the current MFC profile"""    
        
        # Check that all 3 MFCs devices are connected
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected): 
            messagebox.showwarning("Error", "One or more devices are not connected")
            return False
          
        # Get the name of the profile without spaces, such that the .json file can be loaded later
        name = self.mfcname_var.get().strip()
        
        # Checking whether the name is empty
        if not name:
            messagebox.showwarning("Warning", "Please load or create a profile first")
            return

        # Load the profile that needs to be runned
        profile = self.mfcprofilemanager.load_profile(name)
        if not profile:
            messagebox.showerror("Error", f"Failed to load profile: '{name}'")
            return
        
        # Update the status bar with the realtime values
        self.update_run_var()
        
        # Enabling the stop button, since you can now stop a running profile
        self.mfcstop_button.config(state=tk.NORMAL) 
        
        # Start profile in a separate thread, such that the UI doesn't freeze until it finishes

        self.mfcprofile_thread = threading.Thread(
            target=self.run_mfcprofile_thread,  
            daemon=True         # Stops threading by pressing an event, e.g. pressing on stop button
        )
        self.mfcprofile_thread.start()
    
    def run_mfcprofile_thread(self):
        """Thread function to run the MFC profile in the background"""
        
        try:
            # Displaying which MFC profile is running in the status bar
            self.status_var.set(f"Running profile: {self.mfcname_var.get()}")
            
            # Run the MFC profile in the profile manager
            self.mfcprofilemanager.run_profile(update_callback=self.update_mfcprofile_var)

            self.root.after(0, lambda: self.mfcprofile_complete)

        except Exception as e:
            self.root.after(0, lambda: self.mfcprofile_error(e))
    
    def mfcprofile_complete(self):
        """Called when mfc profile completes successfully"""
        self.mfcstop_button.config(state='disabled')
        # Update status bar with profile run is completed
        self.status_var.set("Profile run completed")
    
    def mfcprofile_error(self, error):
        """Called when profile run encounters an error"""
        self.mfcstop_button.config(state='disabled')
        # Update status bar with profile run is failed
        messagebox.showerror("Error", f"Profile run failed: {error}")
        self.status_var.set("Profile run failed")
    
    def stop_mfcprofile(self):
        """Stop the currently running profile"""
        self.mfcprofilemanager.stop_profile()
        self.mfcstop_button.config(state='disabled')
        # Update status bar with profile run is stopped
        self.status_var.set("Profile run stopped by user")

    def update_mfcprofile_var(self, status):
        """Update the GUI with the current status of the running MFC profile

        Args:
            status (dict): Dictionary with the value fo the current step of the running profile
        """
        try:
            # When the UI is closed then this won't be "updating" (to debug)
            if not self.root.winfo_exists():
                return

            # Update the status of the running MFC profile in the UI
            self.mfc_elapsed_label.config(text=f"{status['elapsed_time']:.1f}s")
            self.mfc_step_label.config(text=f"{status['current_step']}/{status['total_steps']}")
            self.mfc_value_label.config(text=f"{status['flow mfc1']:.2f}, {status['flow mfc2']:.2f}, {status['flow mfc3']:.2f} mL/min")
                
            # Schedule the next update, per 1s
            self.root.after(1000, lambda: self.update_mfcprofile_var)
            
        except tk.TclError:
            return
        
    ######################### RVM PROFILE #########################

    def create_valveprofile_tab(self):
        """Create tab for RVMs Profile Management
        """
        #Create scrollable tab with the name 'Valve Profile Management'
        profile_tab = self.create_scrollable_tab(self.notebook, "Valve Profile Management")      
                
        ## Split into two frames: list_frame and edit_frame
        # List frame displaying the list with the available profiles
        list_frame = ttk.Frame(profile_tab, width = 400)
        list_frame.pack(side= 'left', fill = 'both', expand=True, padx=10, pady=10)
        list_frame.pack_propagate(False)

        # Edit frame where the user can edit the profile and fill in the daa for new profiles
        edit_frame = ttk.Frame(profile_tab)
        edit_frame.pack(side= 'right', fill= 'both', expand=True, padx=10, pady=10)
        
        ############# Left frame / list frame #############
        # List frame displaying the list with the available profiles
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
        # Frame for the profile list buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        # Button to load the profile
        load_button = ttk.Button(button_frame, text="Load", command=self.load_valveprofile)
        load_button.pack(side='left', padx=3, expand=True)
        
        # Button to delete the profile
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_valveprofile)
        delete_button.pack(side='left', padx=3, expand=True)

        ############# Right frame / edit frame #############
        # Edit frame where the user can edit the profile and fill in the daa for new profiles
        info_frame = ttk.Frame(edit_frame)
        info_frame.pack(fill='both', padx=5, pady=5)
        
        # Label to display the text 'new profile' when the user want to add a new profile 
        self.new_valveprofile_label = ttk.Label(info_frame, text="")
        self.new_valveprofile_label.pack(side = 'left', padx=5, expand=True, fill='x')
        
        # Label and entry field for profile name
        ttk.Label(info_frame, text="Name:").pack(side='left')
        self.valvename_var = tk.StringVar()
        name_entry = ttk.Entry(info_frame, textvariable=self.valvename_var)
        name_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        # Label and entry field for profile description
        ttk.Label(info_frame, text="Description:").pack(side='left')
        self.valvedesc_var = tk.StringVar()
        desc_entry = ttk.Entry(info_frame, textvariable=self.valvedesc_var)
        desc_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        # Button to add a new profile
        new_profile_btn = ttk.Button(info_frame, text = 'New Profile', command = self.create_new_valveprofile)
        new_profile_btn.pack(side='right', padx=3, expand=True)

        # Frame to show the steps
        steps_frame = ttk.Frame(edit_frame)
        steps_frame.pack(fill = 'both' , expand=True, padx=5, pady=5)

        # Tree to show steps in the right frame        
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
        
        # Frame for the entry field of the steps
        step_controls_frame = ttk.Frame(edit_frame)
        step_controls_frame.pack(fill='x', padx=5, pady=5)
        
        # Label and entry field for the time of the step
        self.valveprofile_time_label = ttk.Label(step_controls_frame, text="Time (s):").pack(side='left')
        self.valvestep_time_var = tk.DoubleVar()
        step_time_entry = ttk.Entry(step_controls_frame, textvariable=self.valvestep_time_var, width=8)
        step_time_entry.pack(side='left', padx=5)
        
        # Label and combobox for the position RVM 1 of the step
        self.valveprofile_valve1_label =  ttk.Label(step_controls_frame, text="Valve 1 Position:").pack(side='left')
        self.valvestep_valve1_var = tk.IntVar() #integer variable, since the valve should be position on 1/2
        self.step_valve1_combo = ttk.Combobox(
            step_controls_frame, 
            textvariable=self.valvestep_valve1_var, 
            values=[1, 2], 
            width=5,
            state="readonly"
        )
        self.step_valve1_combo.pack(side='left', padx=2)
        self.step_valve1_combo.current(0) # set the first one as standard chosen one

        # Label and combobox for the position RVM 1 of the step
        self.valveprofile_valve2_label =  ttk.Label(step_controls_frame, text="Valve 2 Position:").pack(side='left')
        self.valvestep_valve2_var = tk.IntVar() #integer variable, since the valve should be position on 1/2
        self.step_valve2_combo = ttk.Combobox(
            step_controls_frame, 
            textvariable=self.valvestep_valve2_var, 
            values=[1, 2], 
            width=5,
            state="readonly"
        )
        self.step_valve2_combo.pack(side='left', padx=2)
        self.step_valve2_combo.current(0) # set the first one as standard chosen one
        
        ########## Buttons for the step ##########
        ## Frame to add and remove a step, and clear all steps ##
        step_buttons_frame = ttk.Frame(edit_frame)
        step_buttons_frame.pack(fill='both')
                
        # Button to add a new step
        add_step_button = ttk.Button(step_buttons_frame, text="Add Step", command=self.add_valvestep)
        add_step_button.pack(side='left', padx=2)
        
        # Button to remove a step
        remove_step_button = ttk.Button(step_buttons_frame, text="Remove Step", command=self.remove_valvestep)
        remove_step_button.pack(side='left', padx=2)
        
        # Button to clear all steps
        clear_steps_button = ttk.Button(step_buttons_frame, text="Clear All Steps", command=self.clear_valvesteps)
        clear_steps_button.pack(side='left', padx=2)
        
        ## Frame for actions such as save, run and stop profile ##
        action_buttons_frame = ttk.Frame(edit_frame)
        action_buttons_frame.pack(fill='both')
        
        # Button to save the profile
        save_button = ttk.Button(action_buttons_frame, text="Save Profile", command=self.save_valveprofile)
        save_button.pack(side='left', padx=2)
        
        ## Button to run the profile
        run_button = ttk.Button(action_buttons_frame, text="Run Profile", command=self.run_valveprofile)
        run_button.pack(side='left', padx=2)
        
        ## Button to stop running the profile
        self.valvestop_button = ttk.Button(action_buttons_frame, text="Stop", command=self.stop_valveprofile)
        self.valvestop_button.pack(side='left', padx=2)
        self.valvestop_button.config(state='disabled')

    def connect_valve(self, index):  
        """Connect to specific RVM by index
        If successfull, update the UI.

        Args:
            index (int): The index of the RVM, indicating which RVM
        """
        # Trying to connect with the RVM
        if self.valve[index].connect():
            # Update the device statuses in the GUI
            self.update_connection_devices()
            
            #initializing the home position of the valve
            self.currentposition = 1

            # Show in the status bar that the RVM is connected
            self.status_var.set(f"RVM {index + 1} connected and set to home position {self.currentposition}")
            # Enabling automatic updates in function update_valve
            self.keep_updating_valve = True
        else:
            # Show error message when connection fails
            messagebox.showinfo("Connection Failed", "RVM is not connected")
         
    def disconnect_valve(self, index):
        """Disconnect the specific RVM by index. If successful update the UI.

        Args:
            index (int):  The index of the RVM, indicating which RVM
        """
        # Disconnect the valve
        self.valve[index].disconnect()
        
        # Stop updating the valve status
        self.keep_updating_valve = False
        
        # Update the UI which shows the connection and the com-port of each device
        self.update_connection_devices()
        
        # Show in the status bar that the RVM is disconnected
        self.status_var.set(f"RVM {index} disconnected")

    def set_valve(self, index):
        """Sets the position of a specific RVM by index

        Args:
            index (int): index of the valve (0-based)
        """
        # Get the selected valve position from the dropdown (1 or 2)
        position = self.position_vars[index].get()
          
        # Switch the valve to the desired position
        if self.valve[index].switch_position(position):
            # Update the label with the new target position
            self.target_position_labels[index].config(text=f"Target position of the valve: {position}")
            # Start with updating the valve's actual position
            self.update_valve(index)
        else:
            # Show error message if the valve failed to switch
            messagebox.showerror("Valve Error", f"Failed to set position {position} for RVM {index + 1}.")

    def update_valve(self, index):
        """Updating the valve's current position in the UI

        Args:
            index (int): Index of the valve to update
        """
        try:
            # When the UI is closed then this function won't be "updating"
            if not self.root.winfo_exists():
                return
            
            # Stop updating if flag is turned off
            if not self.keep_updating_valve:
                return
            
            # Getting the current target position from the RVM
            new_current_position = self.valve[index].get_position()
            
            # Ensuring that the values will be updates in the GUI
            self.update_run_var()
            
            # Check if the valve has returned 
            if new_current_position is not None:
                # If the position has changed, update the label and store it
                if self.currentposition != new_current_position:                
                    self.current_position_labels[index].config(text=f"Current position of the valve: {new_current_position}")
                    self.status_var.set(f"The position is set to {new_current_position}.")
                else:
                    self.status_var.set(f"The target position is the current position, position {new_current_position}.")
            else:
                messagebox.showerror("Valve Error", f"Failed to read position of RVM {index + 1}.")
                
        except tk.TclError:
            return
   
    def update_valveprofile_list(self):
        """Refresh the list of available RVM profiles"""
        #https://youtu.be/Vm0ivVxNaA8
        
        #Delete all the items from the listbox
        self.valveprofile_listbox.delete(0, tk.END)
        
        #Add all the profiles to the listbox
        for profile in self.valveprofilemanager.get_profiles():
            self.valveprofile_listbox.insert(tk.END, profile)  

    def load_valveprofile(self):
        """Load the selected RVM profile """
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        # Get the currently selected item in the listbox
        selection = self.valveprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to load")
            return
        
        # Get the name of the selected profile (first selected item)
        profile_name = self.valveprofile_listbox.get(selection[0])
        # Load the profile with MFC profile manager
        profile = self.valveprofilemanager.load_profile(profile_name)
        # Clear label for new profiles
        self.new_valveprofile_label.config(text = "")
        
        if profile:
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

            # Update the status bar to update the user that profile is loaded            
            self.status_var.set(f"Loaded profile: {profile_name}")
        
    def delete_valveprofile(self):
        """Delete the selected profile"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/

        # Get selected item from the listbox
        selection = self.valveprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete")
            return

        # Get the name of the selected profile (first selected item)
        profile_name = self.valveprofile_listbox.get(selection[0]) #To ensure that you only select the first selected

        # Ask for user confirmation before deleting the profile
        if messagebox.askyesno("Confirm", f"Delete profile '{profile_name}'?"):
            if self.valveprofilemanager.delete_profile(profile_name):
                #Updating the new profile list
                self.update_valveprofile_list() 
                #Changing the status
                self.status_var.set(f"Deleted profile: {profile_name}")
            else:
                # If profile deleting fails, show error message
                messagebox.showerror("Error", f"Failed to delete the profile: '{profile_name}'")
                
    def create_new_valveprofile(self):
        """Clear all fields for new RVM profile
        """
        #Clearing all input fields and steps
        self.valvename_var.set("")
        self.valvedesc_var.set("")
        self.valvestep_time_var.set("0.0")
        self.step_valve1_combo.current(0)
        self.step_valve2_combo.current(0)
        
        # Clear all entries of the existing steps in the tree
        for item in self.valvesteps_tree.get_children():
            self.valvesteps_tree.delete(item)

        # Show the user that a new profile is made, with the text new profile
        self.new_valveprofile_label.config(text = "New profile", foreground = "green")
        
    def add_valvestep(self):
        """Add a new step to the current RVM profile"""
        try:
            # Get input values from the entry fields
            time_val = float(self.valvestep_time_var.get())
            valve1_val = int(self.valvestep_valve1_var.get())
            valve2_val = int(self.valvestep_valve2_var.get())
            
            # Time should not be negative
            if time_val < 0:
                raise ValueError("Time cannot be negative")
            
            # Position of the RVM of 1 or 2
            if (valve1_val not in [1, 2]) and (valve2_val not in [1, 2]) :
                raise ValueError("Position of the valve must be 1 or 2")
            
            # Check if the time already exists
            for child in self.valvesteps_tree.get_children():
                if float(self.valvesteps_tree.item(child, "values")[0]) == time_val:
                    if not messagebox.askyesno("Confirm", f"Step at time {time_val}s already exists. Overwrite?"):
                        #if True, thus User selects 'NO' then return
                        return 
                    # Remove the existing step
                    self.valvesteps_tree.delete(child)
                    break
                
            # Insert the new step to the tree
            self.valvesteps_tree.insert("", tk.END, values=(time_val, valve1_val, valve2_val))
            
        except ValueError as error:
            # If invalid input values, show error messagebox
            messagebox.showerror("Error", f"Invalid input: {error}")
    
    def remove_valvestep(self):
        """Remove the selected step from the RVM profile"""
        # Get the selected item
        selection = self.valvesteps_tree.selection()
        # Delete the selected item
        if selection:
            self.valvesteps_tree.delete(selection)
    
    def clear_valvesteps(self):
        """Clear all steps from the RVM profile"""
        # Ask the user for confirmation before clearing all the steps
        if messagebox.askyesno("Confirm", "Clear all the steps?"):
            #Obtain all the steps and delete all the steps
            for item in self.valvesteps_tree.get_children():
                self.valvesteps_tree.delete(item)
    
    def save_valveprofile(self):
        """Save the current RVM profile"""
        # Get the profile name
        name = self.valvename_var.get().strip()
        
        # Ensuring that the name isn't empty
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

        # Save the profile use the profile manager
        if self.valveprofilemanager.save_profile(name, profile_data):
            self.update_valveprofile_list()
            self.status_var.set(f"Saved profile: {name}")
        else:
            # If saving failed, show error message
            messagebox.showerror("Error", f"Failed to save profile '{name}'")
    
    def run_valveprofile(self):
        """Run the current RVM profile"""    
        
        # Check that the RVM devices are connected
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

        # Update the status bar with the realtime values
        self.update_run_var()
        
        #Enabling the stop button, since you can now stop a running profile
        self.valvestop_button.config(state=tk.NORMAL) 
        
        # Start profile in a separate thread, such that the UI doesn't freeze until it finishes

        self.valveprofile_thread = threading.Thread(
            target=self.run_valveprofile_thread,  
            daemon=True         # Stops threading by pressing an event, e.g. pressing on stop button
        )
        self.valveprofile_thread.start()
    
    def run_valveprofile_thread(self):
        """Thread function to run the RVM profile in the background"""
        
        try:
            # Displaying which RVM profile is running in the status bar
            self.status_var.set(f"Running profile: {self.valvename_var.get()}")
            # Run the RVM profile in the profile manager
            self.valveprofilemanager.run_profile(update_callback=self.update_valveprofile_var)
            self.root.after(0, lambda: self.valveprofile_complete)

        except Exception as e:
            self.root.after(0, lambda: self.valveprofile_error(e))
    
    def valveprofile_complete(self):
        """Called when profile completes successfully"""
        self.valvestop_button.config(state='disabled')
        # Update status bar with profile run is completed
        self.status_var.set("Profile run completed")
    
    def valveprofile_error(self, error):
        """Called when profile run encounters an error"""
        self.valvestop_button.config(state='disabled')
        # Update status bar with profile run is failed
        messagebox.showerror("Error", f"Profile run failed: {error}")
        self.status_var.set("Profile run failed")
    
    def stop_valveprofile(self):
        """Stop the currently running profile"""
        self.valveprofilemanager.stop_profile()
        self.valvestop_button.config(state='disabled')
        # Update status bar with profile run is stopped
        self.status_var.set("Profile run stopped by user")

    def update_valveprofile_var(self, status):
        """Update the GUI with the current status of the running RVM profile

        Args:
            status (dict): Dictionary with the value fo the current step of the running profile
        """
        try:
            # When the UI is closed then this won't be "updating" (to debug)
            if not self.root.winfo_exists():
                return

            # Update the status of the running RVM profile in the UI  
            self.valve_elapsed_label.config(text=f"{status['elapsed_time']:.1f}s")
            self.valve_step_label.config(text=f"{status['current_step']}/{status['total_steps']}")
            self.valve_value_label.config(text=f"RVM 1: Position {status['valve1']}, RVM 2: Position {status['valve2']}")
            
            # Schedule the next update, per 1s
            self.root.after(1000, lambda: self.update_valveprofile_var)
            
        except tk.TclError:
            return

    ################### Multiple Profile Runner ###################
    def run_selected_profiles(self):
        """Run the selected MFC and RVM profiles in parallel
        """
        # Get the selection from the listboxes from the MFC and RVM
        mfc_sel = self.selprof_mfc_listbox.curselection()
        valve_sel = self.selprof_valve_listbox.curselection()
        
        # Ensure that MFC and RVM is selected
        if not mfc_sel or not valve_sel:
            messagebox.showwarning("Selection Error", "Please select a profile from each list.")
            return

        # Extract the selected profile names
        mfc_name = self.selprof_mfc_listbox.get(mfc_sel[0])
        valve_name = self.selprof_valve_listbox.get(valve_sel[0])

        # Load the selected MFC profile
        if not self.mfcprofilemanager.load_profile(mfc_name):
            messagebox.showerror("Error", f"Failed to load MFC profile '{mfc_name}'")
            return

        # Load the selected RVM profile
        if not self.valveprofilemanager.load_profile(valve_name):
            messagebox.showerror("Error", f"Failed to load Valve profile '{valve_name}'")
            return

        # Check whether MFCs are connected
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected):
            messagebox.showerror("Connection Error", "One or more MFCs not connected.")
            return
        
        # Check whether RVMs are connected
        if not (self.valve[0].connected and self.valve[1].connected):
            messagebox.showerror("Connection Error", "Valve not connected.")
            return

        # Update read values in the GUI
        self.update_run_var()
        
        # Enable stop button to allow user to stop the profiles
        self.stop_all_button.config(state=tk.NORMAL)
        
        # Run both MFC and RVM profiles in threads to keep UI responsive
        threading.Thread(target=self.run_mfcprofile_thread, daemon=True).start()
        threading.Thread(target=self.run_valveprofile_thread, daemon=True).start()

        # Show the user with status bar which profiles are running
        self.status_var.set(f"Running MFC: {mfc_name}, Valve: {valve_name}")

    def stop_all_profiles(self):
        """Stop all profiles running from run_selected_profiles"""
        # Stopping all profiles
        self.mfcprofilemanager.stop_profile()
        self.valveprofilemanager.stop_profile()
        # Updating status bar with the information that all profiles is stopped by the user
        self.status_var.set("All profiles stopped by user")
        
    ######################### MFC and Valve Profile #########################
    def create_mfcandvalveprofile_tab(self):
        """Creates tab for MFCs and RVMs Profile management
        """
        #Create scrollable tab with the name 'MFCs and RVMs Profile Management'
        profile_tab = self.create_scrollable_tab(self.notebook, "MFCs and RVMs Profile Management")

        ## Split into two frames: list_frame and edit_frame
        # List frame displaying the list with the available profiles
        list_frame = ttk.Frame(profile_tab)
        list_frame.pack(side= 'left', fill = 'both', expand=True, padx=5, pady=5)

        # Edit frame where the user can edit the profile and fill in the daa for new profiles
        edit_frame = ttk.Frame(profile_tab)
        edit_frame.pack(side= 'right', fill= 'both', expand=True, padx=5, pady=5)
        
        ############# Left frame / list frame #############
        # List frame displaying the list with the available profiles
        ## Profile listbox with scrollbar
        # https://www.pythontutorial.net/tkinter/tkinter-listbox/#adding-a-scrollbar-to-the-listbox
        # Making an empty profile listbox
        self.mfcandvalveprofile_listbox = tk.Listbox(list_frame, selectmode = tk.SINGLE)
        self.mfcandvalveprofile_listbox.pack(fill= 'both', expand=True, padx=5, pady=5)
    
        # Putting all the profiles in the profile listbox
        self.update_mfcandvalve_profile_list()
        
        #Adding a scrollbar to the profile listbox
        v_scrollbar = ttk.Scrollbar(self.mfcandvalveprofile_listbox, orient = tk.VERTICAL, command = self.mfcandvalveprofile_listbox.yview)
        self.mfcandvalveprofile_listbox['yscrollcommand'] = v_scrollbar.set
        v_scrollbar.pack(side='right', fill='y')
        
        ##Adding the buttons to the left frame (list frame)
        # Frame for the profile list buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        # Button to load the profile
        load_button = ttk.Button(button_frame, text="Load", command=self.load_mfcandvalveprofile)
        load_button.pack(side='left', padx=3, expand=True)
        
        # Button to delete the profile
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_mfcandvalveprofile)
        delete_button.pack(side='left', padx=3, expand=True)

        ############# Right frame / edit frame #############
        # Edit frame where the user can edit the profile and fill in the daa for new profiles
        info_frame = ttk.Frame(edit_frame)
        info_frame.pack(fill='both', padx=5, pady=5)
        
        # Label to display the text 'new profile' when the user want to add a new profile 
        self.new_mfcandvalveprofile_label = ttk.Label(info_frame, text="")
        self.new_mfcandvalveprofile_label.pack(side = 'left', padx=5, expand=True, fill='x')
        
        # Label and entry field for profile name
        ttk.Label(info_frame, text="Name:").pack(side='left')
        self.mfcandvalveprofile_name_var = tk.StringVar()
        name_entry = ttk.Entry(info_frame, textvariable=self.mfcandvalveprofile_name_var)
        name_entry.pack(side='left', padx=5, expand=True, fill='x')

        # Label and entry field for profile description
        ttk.Label(info_frame, text="Description:").pack(side='left')
        self.mfcandvalveprofile_desc_var = tk.StringVar()
        desc_entry = ttk.Entry(info_frame, textvariable=self.mfcandvalveprofile_desc_var)
        desc_entry.pack(side='left', padx=5, expand=True, fill='x')
        
        # Button to add a new profile
        new_profile_btn = ttk.Button(info_frame, text = 'New Profile', command = self.create_new_mfcandvalveprofile)
        new_profile_btn.pack(side='right', padx=3, expand=True)

        # Frame to show the steps
        steps_frame = ttk.Frame(edit_frame)
        steps_frame.pack(fill = 'both' , expand=True, padx=5, pady=5)

        # Tree to show steps in the right frame
        #https://tk-tutorial.readthedocs.io/en/latest/tree/tree.html
        self.mfcandvalveprofile_steps_tree = ttk.Treeview(
            steps_frame, 
            columns=("time", "flow mfc1", "flow mfc2", "flow mfc3", "valve1", "valve2"), 
            show="headings"
        )
        self.mfcandvalveprofile_steps_tree.heading("time", text="Time (s)")
        self.mfcandvalveprofile_steps_tree.heading("flow mfc1", text="Flow N2 (mL/min)")
        self.mfcandvalveprofile_steps_tree.heading("flow mfc2", text="Flow MFC 2 (mL/min)")
        self.mfcandvalveprofile_steps_tree.heading("flow mfc3", text="Flow MFC 3 (mL/min)")
        self.mfcandvalveprofile_steps_tree.heading("valve1", text="RVM 1 Position (1 or 2)")
        self.mfcandvalveprofile_steps_tree.heading("valve2", text="RVM 2 Position (1 or 2)")
               
        self.mfcandvalveprofile_steps_tree.column("time", width=80, anchor=tk.CENTER)
        self.mfcandvalveprofile_steps_tree.column("flow mfc1", width=100, anchor=tk.CENTER)
        self.mfcandvalveprofile_steps_tree.column("flow mfc2", width=100, anchor=tk.CENTER)
        self.mfcandvalveprofile_steps_tree.column("flow mfc3", width=100, anchor=tk.CENTER)
        self.mfcandvalveprofile_steps_tree.column("valve1", width=80, anchor=tk.CENTER)
        self.mfcandvalveprofile_steps_tree.column("valve2", width=80, anchor=tk.CENTER)
        
        self.mfcandvalveprofile_steps_tree.pack(fill = 'both' , expand=True)
        
        # Frame for the entry field of the steps
        step_controls_frame = ttk.Frame(edit_frame)
        step_controls_frame.pack(fill='x', padx=5, pady=5)
        
        # Label and entry field for the time of the step
        ttk.Label(step_controls_frame, text="Time (s):").pack(side='left')
        self.mfcandvalveprofile_time_var = tk.DoubleVar(value = 0.0)
        step_time_entry = ttk.Entry(step_controls_frame, textvariable=self.mfcandvalveprofile_time_var, width=8)
        step_time_entry.pack(side='left', padx=2)
        
        # Label and entry field for the flow of N2 (MFC1) of the step
        ttk.Label(step_controls_frame, text="Flow N2 (mL/min):").pack(side='left')
        self.mfcandvalveprofile_step_flow1_var = tk.DoubleVar(value = 0.0)
        step_flow1_entry = ttk.Entry(step_controls_frame, textvariable=self.mfcandvalveprofile_step_flow1_var, width=8)
        step_flow1_entry.pack(side='left', padx=2)

        # Label and entry field for the flow of MFC2 of the step
        ttk.Label(step_controls_frame, text="Flow MFC 2 (mL/min):").pack(side='left')
        self.mfcandvalveprofile_step_flow2_var = tk.DoubleVar(value = 0.0)
        step_flow2_entry = ttk.Entry(step_controls_frame, textvariable=self.mfcandvalveprofile_step_flow2_var, width=8)
        step_flow2_entry.pack(side='left', padx=2)

        # Label and entry field for the flow of MFC3 of the step
        ttk.Label(step_controls_frame, text="Flow MFC 3 (mL/min):").pack(side='left')
        self.mfcandvalveprofile_step_flow3_var = tk.DoubleVar(value = 0.0)
        step_flow3_entry = ttk.Entry(step_controls_frame, textvariable=self.mfcandvalveprofile_step_flow3_var, width=8)
        step_flow3_entry.pack(side='left', padx=2)
    
        # Label and combobox for the position RVM 1 of the step
        ttk.Label(step_controls_frame, text="RVM 1 Position:").pack(side='left')
        self.mfcandvalveprofile_step_valve1_var = tk.IntVar() #integer variable, since the valve should be position on 1/2
        self.step_mfcvalve1_combo = ttk.Combobox(
            step_controls_frame, 
            textvariable=self.mfcandvalveprofile_step_valve1_var, 
            values=[1, 2], 
            width=5,
            state="readonly"
        )
        self.step_mfcvalve1_combo.pack(side='left', padx=2)
        self.step_mfcvalve1_combo.current(0) # select the first as standard
        
        # Label and combobox for the position RVM 1 of the step
        ttk.Label(step_controls_frame, text="RVM 2 Position:").pack(side='left')
        self.mfcandvalveprofile_step_valve2_var = tk.IntVar() #integer variable, since the valve should be position on 1/2
        self.step_mfcvalve2_combo = ttk.Combobox(
            step_controls_frame, 
            textvariable=self.mfcandvalveprofile_step_valve2_var, 
            values=[1, 2], 
            width=5,
            state="readonly"
        )
        self.step_mfcvalve2_combo.pack(side='left', padx=2)
        self.step_mfcvalve2_combo.current(0) # select the first as standard
        
        
        ########## Buttons for the step ##########
        ## Frame to add and remove a step, and clear all steps ##
        step_buttons_frame = ttk.Frame(edit_frame)
        step_buttons_frame.pack(fill='both')
        
        # Button to add a new step
        add_step_button = ttk.Button(step_buttons_frame, text="Add Step", command=self.mfcandvalve_add_step)
        add_step_button.pack(side='left', padx=2)
        
        # Button to remove a step
        remove_step_button = ttk.Button(step_buttons_frame, text="Remove Step", command=self.mfcandvalve_remove_step)
        remove_step_button.pack(side='left', padx=2)
        
        # Button to clear all steps
        clear_steps_button = ttk.Button(step_buttons_frame, text="Clear All Steps", command=self.mfcandvalve_clear_step)
        clear_steps_button.pack(side='left', padx=2)
        
        ## Frame for actions such as save, run and stop profile ##
        action_buttons_frame = ttk.Frame(edit_frame)
        action_buttons_frame.pack(fill='both')
        
        # Button to save the profile
        save_button = ttk.Button(action_buttons_frame, text="Save Profile", command=self.mfcandvalve_saveprofile)
        save_button.pack(side='left', padx=2)
        
        ## Button to run the profile
        run_button = ttk.Button(action_buttons_frame, text="Run Profile", command=self.mfcandvalve_runprofile)
        run_button.pack(side='left', padx=2)
        
        ## Button to stop running the profile
        self.mfcandvalveprofile_stop_button_label = ttk.Button(action_buttons_frame, text="Stop Running", command=self.stop_mfcandvalveprofile)
        self.mfcandvalveprofile_stop_button_label.pack(side='left', padx=2)
        self.mfcandvalveprofile_stop_button_label.config(state='disabled')
         
    def update_mfcandvalve_profile_list(self):
        """Refresh the list of available MFC and RVM profiles"""
        #https://youtu.be/Vm0ivVxNaA8
        
        #Delete all the items from the listbox
        self.mfcandvalveprofile_listbox.delete(0, tk.END)
        
        #Add all the profiles to the listbox
        for profile in self.mfcandrvmprofilemanager.get_profiles():
            self.mfcandvalveprofile_listbox.insert(tk.END, profile)  #listbox.insert(index, element)

    def load_mfcandvalveprofile(self):
        """Load the selected MFC and RVM profile """
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        # Get the currently selected item in the listbox
        selection = self.mfcandvalveprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to load")
            return
        
        # Get the name of the selected profile (first selected item)
        profile_name = self.mfcandvalveprofile_listbox.get(selection[0])
        # Load the profile with MFC profile manager
        profile = self.mfcandrvmprofilemanager.load_profile(profile_name)
        # Clear label for new profiles        
        self.new_mfcandvalveprofile_label.config(text = "")
        
        if profile:
            #Update the name of the profile
            self.mfcandvalveprofile_name_var.set(profile_name)
            #Update the description in the field
            self.mfcandvalveprofile_desc_var.set(profile.get("description", ""))
            
            # Clear the existing steps
            for item in self.mfcandvalveprofile_steps_tree.get_children():
                self.mfcandvalveprofile_steps_tree.delete(item)
            
            # Add new steps
            for step in profile.get("steps", []):
                self.mfcandvalveprofile_steps_tree.insert("", tk.END, values=(
                    step["time"],
                    step["flow mfc1"],
                    step["flow mfc2"],
                    step["flow mfc3"],
                    step["valve1"],
                    step["valve2"]
                ))
            # Update the status bar to update the user that profile is loaded           
            self.status_var.set(f"Loaded profile: {profile_name}")
        
    def delete_mfcandvalveprofile(self):
        """Delete the selected profile"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        
        # Get selected item from the listbox
        selection = self.mfcandvalveprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete")
            return

        # Get the name of the selected profile (first selected item)
        profile_name = self.mfcandvalveprofile_listbox.get(selection[0]) #To ensure that you only select the first selected

        # Ask for user confirmation before deleting the profile
        if messagebox.askyesno("Confirm", f"Delete profile '{profile_name}'?"):
            if self.mfcandrvmprofilemanager.delete_profile(profile_name):
                #Updating the new profile list
                self.update_mfcandvalve_profile_list() 
                #Changing the status
                self.status_var.set(f"Deleted profile: {profile_name}")
            else:
                # If profile deleting fails, show error message
                messagebox.showerror("Error", f"Failed to delete the profile: '{profile_name}'")
                
    def create_new_mfcandvalveprofile(self):
        """Create MFC and RVM profile
        """
        #Clearing all input fields and steps
        self.mfcandvalveprofile_name_var.set("")
        self.mfcandvalveprofile_desc_var.set("")
        self.mfcandvalveprofile_time_var.set("0.0")
        self.mfcandvalveprofile_step_flow1_var.set("0.0")
        self.mfcandvalveprofile_step_flow2_var.set("0.0")
        self.mfcandvalveprofile_step_flow3_var.set("0.0")
        self.step_mfcvalve1_combo.current(0)
        self.step_mfcvalve2_combo.current(0)

        # Clear all entries of the existing steps in the tree
        for item in self.mfcandvalveprofile_steps_tree.get_children():
            self.mfcandvalveprofile_steps_tree.delete(item)

        # Show the user that a new profile is made, with the text new profile
        self.new_mfcandvalveprofile_label.config(text = "New profile", foreground = "green")
        
    def mfcandvalve_add_step(self):
        """Add a new step to the current profile"""
        try:
            # Get input values from the entry fields
            time_val = float(self.mfcandvalveprofile_time_var.get())
            flow1_val = float(self.mfcandvalveprofile_step_flow1_var.get())
            flow2_val = float(self.mfcandvalveprofile_step_flow2_var.get())
            flow3_val = float(self.mfcandvalveprofile_step_flow3_var.get())

            valve1_val = int(self.mfcandvalveprofile_step_valve1_var.get())
            valve2_val = int(self.mfcandvalveprofile_step_valve2_var.get())

            # Time should not be negative
            if time_val < 0:
                raise ValueError("Time cannot be negative")

            # Position of the RVM of 1 or 2
            if valve1_val not in [1, 2]:
                raise ValueError("Position of the RVM 1 must be 1 or 2")
            if valve2_val not in [1, 2]:
                raise ValueError("Position of the RVM 2 must be 1 or 2")
            
            # Check if the time already exists
            for child in self.mfcandvalveprofile_steps_tree.get_children():
                if float(self.mfcandvalveprofile_steps_tree.item(child, "values")[0]) == time_val:
                    if not messagebox.askyesno("Confirm", f"Step at time {time_val}s already exists. Overwrite?"):
                        #if True, thus User selects 'NO' then return
                        return 
                    # Remove the existing step
                    self.mfcandvalveprofile_steps_tree.delete(child)
                    break
                
            # Insert the new step to the tree
            self.mfcandvalveprofile_steps_tree.insert("", tk.END, values=(time_val, flow1_val, flow2_val, flow3_val, valve1_val, valve2_val))
            
        except ValueError as error:
            # If invalid input values, show error messagebox
            messagebox.showerror("Error", f"Invalid input: {error}")
    
    def mfcandvalve_remove_step(self):
        """Remove the selected step from the MFC and Valve profile"""
        # Get the selected item
        selection = self.mfcandvalveprofile_steps_tree.selection()
        # Delete the selected item
        if selection:
            self.mfcandvalveprofile_steps_tree.delete(selection)
    
    def mfcandvalve_clear_step(self):
        """Clear all steps from the MFC and Valve profile"""
        # Ask the user for confirmation before clearing all the steps
        if messagebox.askyesno("Confirm", "Clear all the steps?"):
            #Obtain all the steps and delete all the steps
            for item in self.mfcandvalveprofile_steps_tree.get_children():
                self.mfcandvalveprofile_steps_tree.delete(item)
    
    def mfcandvalve_saveprofile(self):
        """Save the current MFC and Valve profile"""
        # Get the profile name
        name = self.mfcandvalveprofile_name_var.get().strip()
        
        #Ensuring that the name isn't empty
        if not name:
            messagebox.showwarning("Warning", "Profile name cannot be empty")
            return
        
        # Collect steps from the profile
        steps = []
        for child in self.mfcandvalveprofile_steps_tree.get_children():
            #To obtain all the values of the steps
            values = self.mfcandvalveprofile_steps_tree.item(child, "values")
            steps.append({
                "time": float(values[0]),
                "flow mfc1": float(values[1]),
                "flow mfc2": float(values[2]),
                "flow mfc3": float(values[3]),
                "valve1": int(values[4]),
                "valve2": int(values[5])
            })
        
        # Sort steps by time
        #https://docs.python.org/3/howto/sorting.html
        steps = sorted(steps, key=lambda steps: steps["time"])
        
        # Create the profile data
        profile_data = {
            "description": self.mfcandvalveprofile_desc_var.get(),
            "steps": steps
        }

        # Save the profile use the profile manager
        if self.mfcandrvmprofilemanager.save_profile(name, profile_data):
            self.update_mfcandvalve_profile_list()
            self.status_var.set(f"Saved profile: {name}")
        else:
            # If saving failed, show error message
            messagebox.showerror("Error", f"Failed to save profile '{name}'")
    
    def mfcandvalve_runprofile(self):
        """Run the current MFC and RVM profile"""    
    
        # Check that the MFC and RVM devices are connected
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected and self.valve[0].connected and self.valve[1].connected):
            messagebox.showwarning("Error", "One or more devices are not connected")
            return False
          
        #Get the name of the profile without spaces, such that the .json file can be loaded later
        name = self.mfcandvalveprofile_name_var.get().strip()
        
        #Checking whether the name is empty
        if not name:
            messagebox.showwarning("Warning", "Please load or create a profile first")
            return

        # Load the profile that needs to be runned
        profile = self.mfcandrvmprofilemanager.load_profile(name)
        if not profile:
            messagebox.showerror("Error", f"Failed to load profile: '{name}'")
            return

        # Update the status bar with the realtime values
        self.update_run_var()
        
        #Enabling the stop button, since you can now stop a running profile
        self.mfcandvalveprofile_stop_button_label.config(state=tk.NORMAL) 
        
        # Start profile in a separate thread, such that the UI doesn't freeze until it finishes

        self.mfcandvalveprofile_thread = threading.Thread(
            target=self.mfcandvalve_runprofile_thread,
            daemon=True         # Stops threading by pressing an event, e.g. pressing on stop button
        )
        self.mfcandvalveprofile_thread.start()
    
    def mfcandvalve_runprofile_thread(self):      
        """Thread function to run the MFC and RVM profile in the background"""
        try:
            def safe_update(status):
                self.root.after(0, lambda: self.update_mfcandvalveprofile_var(status))
            # Displaying which MFC and RVM profile is running in the status bar
            self.status_var.set(f"Running profile: {self.mfcandvalveprofile_name_var.get()}")
            # Run the MFC and RVM profile in the profile manager
            self.mfcandrvmprofilemanager.run_profile(update_callback=safe_update)
            self.root.after(0, self.mfcandvalveprofile_complete)

        except Exception as e:
            self.root.after(0, lambda: self.mfcandvalveprofile_error(str(e)))

    def mfcandvalveprofile_complete(self):
        """Called when profile completes successfully"""
        self.mfcandvalveprofile_stop_button_label.config(state='disabled')
        # Update status bar with profile run is completed
        self.status_var.set("Profile run completed")
    
    def mfcandvalveprofile_error(self, error):
        """Called when profile run encounters an error"""
        self.mfcandvalveprofile_stop_button_label.config(state='disabled')
        # Update status bar with profile run is failed
        messagebox.showerror("Error", f"Profile run failed: {error}")
        self.status_var.set("Profile run failed")
    
    def stop_mfcandvalveprofile(self):
        """Stop the currently running profile"""
        self.mfcandrvmprofilemanager.stop_profile()
        self.mfcandvalveprofile_stop_button_label.config(state='disabled')
        # Update status bar with profile run is stopped
        self.status_var.set("Profile run stopped by user")
    
    def update_mfcandvalveprofile_var(self, status):
        """Update the GUI with the current status of the running MFC and RVM profile

        Args:
            status (dict): Dictionary with the value fo the current step of the running profile
        """
        try:
            #when the UI is closed then this won't be "updating" 
            if not self.root.winfo_exists():
                return

            # Update the status of the running RVM profile in the UI  
            self.mfcvalve_profile_elapsed_label.config(text=f"{status['elapsed_time']:.1f}s")
            self.mfcvalve_profile_step_label.config(text=f"{status['current_step']}/{status['total_steps']}")
            self.mfcvalve_profile_value_label.config(text=f"MFC 1: {status['flow mfc1']:.2f} ml/min, MFC 2: {status['flow mfc2']:.2f} ml/min, MFC 3: {status['flow mfc3']:.2f} ml/min, RVM 1: Position {status['valve1']}, RVM 2: Position {status['valve2']}")
        except tk.TclError:
            return

    ######################### Pure Gas ON/OFF Profile #########################
    def create_puregas_onoff_profile(self):
        """Creates tab for Pure Gas ON/OFF Profile Management
        """
        #Create scrollable tab with the name "Pure Gas ON/OFF Profile Management"
        puregas_onoff_tab = self.create_scrollable_tab(self.notebook, "Pure Gas ON/OFF Profile Management")

        ## Split into two frames: list_frame and edit_frame
        # List frame displaying the list with the available profiles
        list_frame = ttk.Frame(puregas_onoff_tab)
        list_frame.pack(side= 'left', fill = 'both', expand=True, padx=5, pady=5)
        
        # Edit frame where the user can edit the profile and fill in the data for new profiles
        edit_frame = ttk.Frame(puregas_onoff_tab)
        edit_frame.pack(side= 'right', fill= 'both', expand=True, padx=5, pady=5)
        
        ############# Left frame / list frame #############
        # List frame displaying the list with the available profiles
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
        # Frame for the profile list buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', padx=5, pady=5)

        # Button to load the profile        
        load_button = ttk.Button(button_frame, text="New", command=self.new_onoffconcprofile)
        load_button.pack(side='left', padx=3, expand=True)

        # Button to delete the profile
        load_button = ttk.Button(button_frame, text="Load", command=self.load_onoffconcprofile)
        load_button.pack(side='left', padx=3, expand=True)
        
        # Button to save the profile
        save_button = ttk.Button(button_frame, text="Save", command=self.save_onoffconcprofile)
        save_button.pack(side='left', padx=3, expand=True)

        # Button to delete the profile
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_onoffconcprofile)
        delete_button.pack(side='left', padx=3, expand=True)

        ############# Right frame / edit frame #############
        # Edit frame where the user can edit the profile and fill in the daa for new profiles
        profile_info_frame = ttk.LabelFrame(edit_frame, text="Profile Information")
        profile_info_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        # Label and entry field for profile name
        ttk.Label(profile_info_frame, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.onoffconc_namevar = tk.StringVar()
        name_entry = ttk.Entry(profile_info_frame, textvariable=self.onoffconc_namevar)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        name_entry.config(width=30)

        # Label and entry field for profile description
        ttk.Label(profile_info_frame, text="Description:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.onoffconc_desc_var = tk.StringVar()
        desc_entry = ttk.Entry(profile_info_frame, textvariable=self.onoffconc_desc_var)
        desc_entry.grid(row=1, column=1, padx=10, pady=5)
        desc_entry.config(width=30)
        
        # Combobox for the selected MFC which contains the VOC
        ttk.Label(profile_info_frame, text="Select VOC1 (MFC2) or VOC2 (MFC3):").grid(row=3, column=0, padx=10, pady=5)
        self.onoffconc_voc_mfc_choice = ttk.Combobox(profile_info_frame, values=["VOC1 (MFC2)", "VOC2 (MFC3)"], state="readonly")
        self.onoffconc_voc_mfc_choice.grid(row=3, column=1, padx=5, pady=5)
        self.onoffconc_voc_mfc_choice.current(0)  # default to MFC 2

        # Combobox to select which VOC type it is
        ttk.Label(profile_info_frame, text="Select VOC:").grid(row=3, column=2, padx=10, pady=10, sticky='e')
        self.onoffconc_voc_var = tk.StringVar()
        self.onoffconc_voc_list = list(self.settings_manager.get_voc_data().keys())
        self.onoffconc_typevoc_dropdown = ttk.Combobox(profile_info_frame, textvariable=self.onoffconc_voc_var, values=self.onoffconc_voc_list, state="readonly")
        self.onoffconc_typevoc_dropdown.grid(row=3, column=3, padx=10, pady=10)
        self.onoffconc_typevoc_dropdown.current(0)

        # Label and entry field for concentration
        ttk.Label(profile_info_frame, text="Concentration (ppm):").grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.onoffconc_conc_var = tk.DoubleVar(value=0.0)
        concentration_entry = ttk.Entry(profile_info_frame, textvariable=self.onoffconc_conc_var)
        concentration_entry.grid(row=4, column=1, padx=10, pady=10)

        # Label and entry field for total Flow Rate input
        ttk.Label(profile_info_frame, text="Total Flow Rate (mL/min):").grid(row=5, column=0, padx=10, pady=10, sticky='e')
        self.onoffconc_totflowrate_var = tk.DoubleVar(value=0.0)
        totalflow_entry = ttk.Entry(profile_info_frame, textvariable=self.onoffconc_totflowrate_var)
        totalflow_entry.grid(row=5, column=1, padx=10, pady=10)

        # Button to calculate the flow
        calc_button = ttk.Button(profile_info_frame, text="Calculate Flow", command=self.calculate_voc_flow)
        calc_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Label to display the required flow of Nitrogen
        self.onoffconc_N_label = ttk.Label(profile_info_frame, text="Required Flow of Nitrogen: -")
        self.onoffconc_N_label.grid(row=7, column=0, columnspan=2, pady=5)

        # Label to display the required flow of the VOC
        self.onoffconc_flow_label = ttk.Label(profile_info_frame, text="Required Flow of VOC: -")
        self.onoffconc_flow_label.grid(row=8, column=0, columnspan=2, pady=5)
        
        # Label to display the required saturated vapor pressure
        self.onoffconc_ps_label = ttk.Label(profile_info_frame, text="Saturated Vapor Pressure (Ps): -")
        self.onoffconc_ps_label.grid(row=9, column=0, columnspan=2, pady=5)

        # Label and entry field for the ON Time
        ttk.Label(profile_info_frame, text="ON Time (s):").grid(row=10, column=0)
        self.onoffconc_on_time_entry = ttk.Entry(profile_info_frame)
        self.onoffconc_on_time_entry.grid(row=10, column=1)
        self.onoffconc_on_time_entry.insert(0, "0.0")         
    
        # Label and entry field for the OFF Time
        ttk.Label(profile_info_frame, text="OFF Time (s):").grid(row=11, column=0)
        self.onoffconc_off_time_entry = ttk.Entry(profile_info_frame)
        self.onoffconc_off_time_entry.grid(row=11, column=1)
        self.onoffconc_off_time_entry.insert(0, "0.0")     
        
        # Label and entry field for the Run Time
        ttk.Label(profile_info_frame, text="Run Time (s):").grid(row=12, column=0)
        self.onoffconc_run_time_entry = ttk.Entry(profile_info_frame)
        self.onoffconc_run_time_entry.grid(row=12, column=1)
        self.onoffconc_run_time_entry.insert(0, "0.0")     
        
        # Button to run the ON/OFF graph
        self.onoffconc_run_button = ttk.Button(profile_info_frame, state="disabled", text="Run ON/OFF Profile", command=self.puregas_onoff_runprofile)
        self.onoffconc_run_button.grid(row=13, column=0, padx=5, pady=10, sticky="ew")
 
        # Button to plot the ON/OFF graph
        self.onoffconc_plotgraph_button = ttk.Button(profile_info_frame,state="disabled", text="Plot ON/OFF Graph", command=self.plot_expected_vocprofile)
        self.onoffconc_plotgraph_button.grid(row=13, column=1, padx=5, pady=10, sticky="ew")
               
        # Button to stop the ON/OFF graph running
        self.onoffconc_stop_button = ttk.Button(profile_info_frame, state="disabled", text="Stop Running the ON/OFF Profile", command=self.stop_onoffconc_run)
        self.onoffconc_stop_button.grid(row=13, column=2, padx=5, pady=10, sticky="ew")
        
        # Label to display the elapsed time
        self.onoffconc_elapsed_time_var = tk.StringVar(value="Elapsed Time: 0.0 s")
        onoffconc_elapsed_time_label = ttk.Label(profile_info_frame, textvariable=self.onoffconc_elapsed_time_var)
        onoffconc_elapsed_time_label.grid(row=14, column=0, columnspan=2, sticky='w')

        # Label for the Setpoint concentration ON/OFF graph
        self.onoffconc_graph_frame = ttk.LabelFrame(profile_info_frame, text="Setpoint Concentration On/Off Graph")
        self.onoffconc_graph_frame.grid(row=0, column=4, rowspan=10, padx=10, pady=10, sticky="ns")        
        
        # Create plot
        self.onoff_fig, self.onoff_ax = plt.subplots(figsize=(6, 4))
        self.onoff_ax.set_xlabel("Time (s)")
        self.onoff_ax.set_ylabel("Concentration (ppm)")
        self.onoff_ax.set_title(f"Setpoint Concentration On/Off Graph")
        self.onoff_ax.grid(True)

       # Insert the plot in Tkinter
        self.onoff_canvas = FigureCanvasTkAgg(self.onoff_fig, master=self.onoffconc_graph_frame)
        self.onoff_canvas.draw()
        self.onoff_canvas.get_tk_widget().pack(fill = 'both', expand = True)

        canvas_widget = self.onoff_canvas.get_tk_widget()
        # Graph size 400 x 300
        canvas_widget.config(width=500, height=300) 
        # Prevent Frame Shrinking
        # https://youtu.be/onIEw70Uw-4
        canvas_widget.pack_propagate(False)  # prevent auto-resizing
        canvas_widget.pack(fill='none', expand=False)
        
    def update_puregasonoff_Telapsed_display(self, start_timestamp, run_time):
        """Updates the display of the elapsed time the Pure Gas ON/OFF profile

        Args:
            start_timestamp (float): the timestamp when the profile starts running
            run_time (float): the total time that the profile should run
        """
        try:
            #when the UI is closed then this won't be "updating" (to debug)
            if not self.root.winfo_exists():
                return
            
            # Calculate the elapsed time
            elapsed = time.time() - start_timestamp  
            
            # Update the label showing current elapsed time / total time
            self.onoffconc_elapsed_time_var.set(f"Elapsed Time: {elapsed:.1f} s / {run_time:.1f} s")

            if elapsed < run_time and not self.stop_onoff_conc_run:
                # Update the same function after 100 ms (0.1 s)
                self.root.after(100, lambda: self.update_puregasonoff_Telapsed_display(start_timestamp, run_time))
            # User stopped the profile
            elif self.stop_onoff_conc_run:
                self.onoffconc_elapsed_time_var.set(f"Profile Stopped at {elapsed:.1f} s")            
            # Profile completed
            else:
                self.onoffconc_elapsed_time_var.set(f"Done: Elapsed Time: {run_time:.1f} s / {run_time:.1f} s")
                
        except tk.TclError:
            return

    def puregas_onoff_runprofile(self):
        """ Run the Pure gas ON/OFF profile
        """
        # Plot the expected graph
        self.plot_expected_vocprofile()
        try:
            # Obtaining values from the entries
            on_time = float(self.onoffconc_on_time_entry.get())
            off_time = float(self.onoffconc_off_time_entry.get())
            run_time = float(self.onoffconc_run_time_entry.get())
            self.onoffconc_voc_index = self.onoffconc_voc_mfc_choice.current()
            self.tot_flow = self.onoffconc_totflowrate_var.get()
            
        except ValueError:
            messagebox.showerror("Input Error", "All timing fields must be numbers.")
            return

        # MFC and RVM objects
        voc_mfc = self.mfcs[self.onoffconc_voc_index  + 1]  # index 0 = MFC2 , index 1 = MFC3
        n2_mfc = self.mfcs[0]                               # nitrogen is always MFC1
        
        # Check whether the MFCs and RVMs are connected
        if not voc_mfc.connected or not n2_mfc.connected or not self.valve[0].connected or not self.valve[1].connected:
            messagebox.showerror("Connection Error", "Ensure all devices are connected.")
            return
        
        # Ensuring that the selected VOC exists
        if self.onoffconc_voc_index  not in [0, 1]:
            messagebox.showerror("MFC Selection Error", "Select either VOC1 (MFC2) or VOC2 (MFC3).")
            return 
            
        # Cooling plate temperature should before be set to 0
        confirm = messagebox.askyesno(
            "Cooling Plate Temperature",
            f"Did you set the cooling plate temperature to 0 °C?"
        )
        if not confirm: # When user selected 'No'
            return  
        
        # Enable the stop button
        self.onoffconc_stop_button.config(state = 'enabled')
        self.stop_onoff_conc_run = False
        
        # Start profile execution in a seperate threade, to avoid freezing the UI
        threading.Thread(target=self.puregas_onfoff_run_thread, args = (voc_mfc, n2_mfc, on_time, off_time, run_time), daemon=True).start()
        
    def puregas_onfoff_run_thread(self, voc_mfc, n2_mfc, on_time, off_time, run_time):
        """Thread to run the ON/OFF profile

        # Overview of valve positions, where valve[0] is the valve connected to VOC 1 and valve[1] is the valve connected to VOC2
        # Valve VOC 1, Valve_VOC 2: Gas that goes into the inlet from the chamber
        # POS 1, POS 1 -> VOC2
        # POS 1, POS 2 -> ONLY NITROGEN
        # POS 2, POS 1 -> VOC1 with VOC2
        # POS 2, POS 2 -> VOC1

        Args:
            voc_mfc: The MFC that handles the VOC gas
            n2_mfc: The MFC that handles N2
            on_time: Duration in seconds for VOC to flow in the chamber
            off_time: Duration in seconds for N2 to flow in the chamber
            run_time: Total time the profile should run
        """
        
        # Update the read value from the devices and update it in the GUI
        self.update_run_var()

        # Obtain the starting time
        pulse_starttime = time.time()
        
        # Update the display elapsed time on the GUI
        self.root.after(0, lambda: self.update_puregasonoff_Telapsed_display(pulse_starttime, run_time))
        
        # When VOC1 in MFC 2 is selected
        if self.onoffconc_voc_index  == 0:
            
            # Check whether the user already had stopped the profile running
            while not self.stop_onoff_conc_run:
                # Check if total runtime has been exceeded
                if time.time() - pulse_starttime >= run_time:
                    break

                ############ ON state: VOC and N2 is flowing ############
                voc_mfc.set_massflow(self.voc_flow)
                n2_mfc.set_massflow(self.voc_N)
                self.valve[0].switch_position(2)
                self.valve[1].switch_position(2)
                self.status_var.set(f"VOC ON-state | MFC 1 with N2: {self.voc_N} ml/min, MFC {self.onoffconc_voc_index + 2} with VOC: {self.voc_flow}, RVM 1: Position 2, RVM2: Position 2")
                
                # Wait till off state time is exceeded but also continues checking for stop signal
                if not self.sleep_with_stop_check(on_time):
                    break

                # Check if total runtime has been exceeded
                if time.time() - pulse_starttime >= run_time:
                    break
                
                ############ OFF state: Only N2 is flowing ############
                voc_mfc.set_massflow(0)
                n2_mfc.set_massflow(self.tot_flow) #nitrogen max flow rate
                self.valve[0].switch_position(1)
                self.valve[1].switch_position(2)
                self.status_var.set(f"VOC OFF-state | MFC 1 with N2: 0 ml/min, MFC {self.onoffconc_voc_index  + 2} with VOC: 0, RVM 1: Position 1, RVM2: Position 2")   
                
                # Wait till off state time is exceeded but also continues checking for stop signal
                if not self.sleep_with_stop_check(off_time):
                    break

            # Check whether the user already had stopped the profile running
            if not self.stop_onoff_conc_run:
                # Final reset, so setting all massflow rates to 0
                voc_mfc.set_massflow(0)
                n2_mfc.set_massflow(0)                   
                self.valve[0].switch_position(1)
                self.valve[1].switch_position(2)
                self.status_var.set("VOC Run complete")

        # When VOC2 in MFC3 is selected
        elif self.onoffconc_voc_index  == 1:
            # Check whether the user already had stopped the profile running
            while not self.stop_onoff_conc_run:
                # Check if total runtime has been exceeded
                if time.time() - pulse_starttime >= run_time:
                    break

                ############ ON state: VOC and N2 is flowing ############
                voc_mfc.set_massflow(self.voc_flow)
                n2_mfc.set_massflow(self.voc_N)
                ##verschil zit hier
                self.valve[0].switch_position(1)
                self.valve[1].switch_position(1)
                self.status_var.set(f"VOC ON-state | MFC 1 with N2: {self.voc_N} ml/min, MFC {self.onoffconc_voc_index  + 2} with VOC: {self.voc_flow}, RVM 1: Position 1, RVM2: Position 1")
                
                # Wait till off state time is exceeded but also continues checking for stop signal
                if not self.sleep_with_stop_check(on_time):
                    break

                # Check if total runtime has been exceeded
                if time.time() - pulse_starttime >= run_time:
                    break
                
                ############ OFF state: Only N2 is flowing ############
                voc_mfc.set_massflow(0)
                n2_mfc.set_massflow(0) #nitrogen max flow rate
                self.valve[0].switch_position(1)
                self.valve[1].switch_position(2)
                self.status_var.set(f"VOC OFF-state | MFC 1 with N2: 0 ml/min, MFC {self.onoffconc_voc_index  + 2} with VOC: 0, RVM 1: Position 1, RVM2: Position 2")

                # Wait till off state time is exceeded but also continues checking for stop signal
                if not self.sleep_with_stop_check(off_time):
                    break

            # Check whether the user already had stopped the profile running
            if not self.stop_onoff_conc_run:
                # Final reset, so setting all massflow rates to 0
                voc_mfc.set_massflow(0)
                n2_mfc.set_massflow(0)
                self.valve[0].switch_position(1)
                self.valve[1].switch_position(2)
                self.status_var.set("VOC Run complete")
                
    def sleep_with_stop_check(self, duration):
        """Sleep in small intervals while checking whether the stop flag is triggered by the user

        Args:
            duration (float): Total duration to sleep

        Returns:
            boolean: If run was stopped while sleeping, return False, else True
        """
        # Check every 0.01 s for a stop request
        interval = 0.01  
        # Calculate the end time that it should stop with sleeping
        end_time = time.time() + duration
        
        # Check whether the time exceed the end time
        while time.time() < end_time:
            # Check whether the stop flag has been raised
            if self.stop_onoff_conc_run:
                return False
            # Sleep some short interval
            time.sleep(interval)
        return True

    def plot_expected_vocprofile(self):
        """Plot the expected ON/OFF concentration profile
        """
        try:
            # Obtain inputs from the entries
            on_time = float(self.onoffconc_on_time_entry.get())
            off_time = float(self.onoffconc_off_time_entry.get())
            total_run_time = float(self.onoffconc_run_time_entry.get())
            conc = float(self.onoffconc_conc_var.get())
            self.onoffconc_voc_index = self.onoffconc_voc_mfc_choice.current()
            voc = self.onoffconc_voc_var.get()
        except ValueError:
            messagebox.showerror("Input Error", "Start Delay Time, On time, Off Time, Run Time and Concentrations must be numbers.")
            return

        # Initialize data arrays for plotting
        time_data = []
        signal_data = []
        current_run_time = 0
        
        # Small step times to simulate a continuous graph
        step_time = 1e-2
        on_time_steps = on_time / step_time
        off_time_steps = off_time / step_time
        
        # Generating the on and off pattern
        while current_run_time < total_run_time:
            # ON-time: add the signal and time to a list for the duration that it should be ON (ensured by calculating the #steps) 
            for time in range(int(on_time_steps)):
                if current_run_time >= total_run_time:
                    break
                time_data.append(current_run_time)
                signal_data.append(conc)
                current_run_time += step_time
                
            # OFF-time: add the signal and time to a list for the duration that it should be OFF (ensured by calculating the #steps) 
            for time in range(int(off_time_steps)):
                if current_run_time >= total_run_time:
                    break
                time_data.append(current_run_time)
                # add signal value 0
                signal_data.append(0)
                current_run_time += step_time
                
        # Clear previous canvas if exists
        # https://stackoverflow.com/questions/65544881/clearing-and-plotting-mathplot-figure-on-tkinter
        for child in self.onoffconc_graph_frame.winfo_children():
            child.destroy()

        # Create plot
        self.onoff_fig, self.onoff_ax = plt.subplots(figsize=(6, 4))
        self.onoff_ax.plot(time_data, signal_data, color='red', linewidth=2)
        self.onoff_ax.set_xlabel("Time (s)")
        self.onoff_ax.set_ylabel("Concentration (ppm)")
        self.onoff_ax.set_title(f"Setpoint MFC {self.onoffconc_voc_index + 2} with {voc} On/Off Graph")
        self.onoff_ax.set_xlim(0, time_data[-1] * 1.2 )
        self.onoff_ax.set_ylim(0, conc * 1.2)
        self.onoff_ax.grid(True)
        self.onoff_fig.tight_layout()  

       # Insert the plot in Tkinter
        self.onoff_canvas = FigureCanvasTkAgg(self.onoff_fig, master=self.onoffconc_graph_frame)
        self.onoff_canvas.draw()

        canvas_widget = self.onoff_canvas.get_tk_widget()
        # Graph size 400 x 300
        canvas_widget.config(width=500, height=300) 
        # Prevent Frame Shrinking
        # https://youtu.be/onIEw70Uw-4
        canvas_widget.pack_propagate(False)  # prevent auto-resizing
        canvas_widget.pack(fill='none', expand=False)
       
    def calculate_voc_flow(self):
        """Calculate the required flow of VOC and nitrogen based on the selected concentration and type of VOC and total flow rate
        """
        try:
            # Get the inputs from the entries
            voc = self.onoffconc_voc_var.get()
            concentration = float(self.onoffconc_conc_var.get())
            total_flow = float(self.onoffconc_totflowrate_var.get())
            self.onoffconc_voc_index = self.onoffconc_voc_mfc_choice.current()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers for concentration and total flow rate.")
            return

        # Calculate the required flow of VOC and nitrogen based on the type of VOC and the concentration
        ### Standard temperature of 0 degree
        self.voc_flow, self.voc_N, self.voc_Ps = self.calculate_required_flow_0degrees(voc, concentration, total_flow)
        
        # If calculation was successful, update GUI with results
        if self.voc_flow is not None:
            self.onoffconc_flow_label.config(text=f"Required Flow of VOC {self.onoffconc_voc_index + 1} of MFC {self.onoffconc_voc_index + 2}: {self.voc_flow} mL/min")
            self.onoffconc_N_label.config(text=f"Required Flow of Nitrogen: {self.voc_N} mL/min")
            self.onoffconc_ps_label.config(text=f"Saturated Vapor Pressure (Ps): {self.voc_Ps} mmHg")
            self.onoffconc_plotgraph_button.config(state="enabled")
            self.onoffconc_run_button.config(state="enabled")
        # If calculation failed, display N/A 
        else:
            self.onoffconc_flow_label.config(text="Required Flow: N/A")
            self.onoffconc_N_label.config(text=f"Required Flow of Nitrogen: N/A")
            self.onoffconc_ps_label.config(text="Saturated Vapor Pressure (Ps): N/A")

    def calculate_required_flow_0degrees(self, voc_name, concentration_ppm, total_flow_rate):       
        """Calculate the required flow rates for VOC and nitrogen at 0 degrees, based on the selected concentration and VOC type and total flow rate

        Args:
            voc_name (str): Name of the selected VOC
            concentration_ppm (float): Target concentration in ppm
            total_flow_rate (float): Desired total gas flow rate in ml/min

        Returns:
            tuple: tuple containing the VOC flow in ml/min, N2 flow in ml/min, saturated vapor pressure in mmHg
        """
        # Standard temperature of 0 degrees
        T = 0
        
        # Get the VOC Antoine coefficients and valid temperature range from the settings
        voc_data = self.settings_manager.get_voc_data()
        
        # If VOC name is not in the VOC data list   
        if voc_name not in voc_data:
            return None, None, None, None
       
        A, B, C, Tmin, Tmax = voc_data[voc_name]
        # Atmospheric pressure in mmHg
        P = 760 
        # Minimum allowed VOC flow rate
        min_f = 0.1 

        # Special case when concentration is 0 ppm, the flow rate of N2 should be total_flow_rate
        if concentration_ppm == 0:
            f = 0
            F = total_flow_rate
            Ps = 0               
            return f, F, Ps

        # Antoine Equation where Ps is in mmHg
        Ps = 10 ** (A - B / (C + T))
        
        # Concentration of an analyte
        f = concentration_ppm * (total_flow_rate * P / Ps) * 1e-6

        # Calculate N2 flow rate by subtracting VOC flow from total flow
        F = total_flow_rate - f

        # Check that the VOC flow is smaller than the total_flow rate but bigger than the minimum flow rate
        if min_f <= f <= total_flow_rate: 
            # Check that for the calculated flow rates the Antoine coefficients holds
            if Tmin <= T <= Tmax:
                return f, F, Ps
            
        return None, None, None
    
    def update_onoffconcprofile_list(self):
        """Refresh the list of available profiles"""
        #https://youtu.be/Vm0ivVxNaA8
        
        #Delete all the items from the listbox
        self.onoffconcprofile_listbox.delete(0, tk.END)
        
        #Add all the profiles to the listbox
        for profile in self.onoffconcprofilemanager.get_profiles():
            self.onoffconcprofile_listbox.insert(tk.END, profile)  
            
    def new_onoffconcprofile(self):
        """Clear new Pure Gas ON/OFF concentration profile."""

        self.onoffconc_namevar.set("")
        self.onoffconc_desc_var.set("")
        self.onoffconc_voc_mfc_choice.current(0)  # Reset default to VOC1 in MFC2
        self.onoffconc_voc_var.set("0.0")
        self.onoffconc_conc_var.set("0.0")
        self.onoffconc_totflowrate_var.set("0.0")
        self.onoffconc_on_time_entry.delete(0, tk.END)
        self.onoffconc_on_time_entry.insert(0, "0.0")

        self.onoffconc_off_time_entry.delete(0, tk.END)
        self.onoffconc_off_time_entry.insert(0, "0.0")

        self.onoffconc_run_time_entry.delete(0, tk.END)
        self.onoffconc_run_time_entry.insert(0, "0.0")
        self.onoffconc_typevoc_dropdown.current(0)
        self.status_var.set("Creating new ON/OFF profile.")
  
        # Clear existing plot from the graph frame
        for child in self.onoffconc_graph_frame.winfo_children():
            child.destroy()

        # Create plot
        self.onoff_fig, self.onoff_ax = plt.subplots(figsize=(6, 4))
        self.onoff_ax.set_xlabel("Time (s)")
        self.onoff_ax.set_ylabel("Concentration (ppm)")
        self.onoff_ax.set_title(f"Setpoint Concentration On/Off Graph")
        self.onoff_ax.grid(True)

       # Insert the plot in Tkinter
        self.onoff_canvas = FigureCanvasTkAgg(self.onoff_fig, master=self.onoffconc_graph_frame)
        self.onoff_canvas.draw()
        self.onoff_canvas.get_tk_widget().pack(fill = 'both', expand = True)

        canvas_widget = self.onoff_canvas.get_tk_widget()
        # Graph size 400 x 300
        canvas_widget.config(width=500, height=300) 
        # Prevent Frame Shrinking
        # https://youtu.be/onIEw70Uw-4
        canvas_widget.pack_propagate(False)  # prevent auto-resizing
        canvas_widget.pack(fill='none', expand=False)
        
    def delete_onoffconcprofile(self):
        """Delete selected Pure Gas ON/OFF profile."""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        
        # Get selected item from the listbox
        selection = self.onoffconcprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete.")
            return

        # Get the name of the selected profile (first selected item)
        profile_name = self.onoffconcprofile_listbox.get(selection[0])

        # Ask for user confirmation before deleting the profile
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{profile_name}'?"):
            if self.onoffconcprofilemanager.delete_profile(profile_name):
                #Updating the new profile list
                self.update_onoffconcprofile_list()
                #Changing the status
                self.status_var.set(f"Deleted profile: {profile_name}")
            else:
                # If profile deleting fails, show error message
                messagebox.showerror("Error", f"Could not delete profile: {profile_name}")

    def load_onoffconcprofile(self):
        """Load selected Pure Gas ON/OFF profile"""
        self.stop_onoff_conc_run = False
        
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        # Get the currently selected item in the listbox
        selection = self.onoffconcprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to load.")
            return

        # Get the name of the selected profile (first selected item)
        profile_name = self.onoffconcprofile_listbox.get(selection[0])
        # Load the profile with ON/OFF profile manager
        profile = self.onoffconcprofilemanager.load_profile(profile_name)

        # Profile can not be found
        if not profile:
            messagebox.showerror("Error", "Failed to load the selected profile.")
            return

        # Obtain all values stored in the profile
        description = profile.get("description", "")
        mfc_index = profile.get("selectedmfcindex", 0)

        voc = profile.get("voc", "")
        concentration = profile.get("concentration", 0.0)
        total_flow = profile.get("total_flow", 0.0)
        on_time = profile.get("on_time", "")
        off_time = profile.get("off_time", "")
        run_time = profile.get("run_time", "")

        # Set all the values in the input fields with the loaded values
        self.onoffconc_namevar.set(profile.get("name", profile_name))
        self.onoffconc_desc_var.set(description)
        self.onoffconc_voc_mfc_choice.current(mfc_index)

        self.onoffconc_voc_var.set(voc)
        self.onoffconc_conc_var.set(concentration)
        self.onoffconc_totflowrate_var.set(total_flow)

        self.onoffconc_on_time_entry.delete(0, tk.END)
        self.onoffconc_on_time_entry.insert(0, on_time)

        self.onoffconc_off_time_entry.delete(0, tk.END)
        self.onoffconc_off_time_entry.insert(0, off_time)

        self.onoffconc_run_time_entry.delete(0, tk.END)
        self.onoffconc_run_time_entry.insert(0, run_time)

        # Update the status bar with that the profile is loaded
        self.status_var.set(f"Loaded profile: {profile_name}")
        
        # Calculate the VOC and N2 flow rates based on the loaded data
        self.calculate_voc_flow()
        
        # Plot the expected concenration graph based on the loaded profile
        self.plot_expected_vocprofile()
        
    def save_onoffconcprofile(self):
        """Save current VOC ON/OFF profile"""
        try:
            # Obtain all values from the input fields from the GUI
            voc = self.onoffconc_voc_var.get()
            selected_mfc = self.onoffconc_voc_mfc_choice.current()
            concentration = float(self.onoffconc_conc_var.get())
            total_flow = float(self.onoffconc_totflowrate_var.get())
            on_time = float(self.onoffconc_on_time_entry.get())
            off_time = float(self.onoffconc_off_time_entry.get())
            run_time = float(self.onoffconc_run_time_entry.get())
            profile_name = self.onoffconc_namevar.get()
            description = self.onoffconc_desc_var.get()
            
        except ValueError:
            messagebox.showerror("Input Error", "All numeric fields must be valid numbers.")
            return

        # Package the data into a dictionary such that it can be saved
        profile_data = {
            "name": profile_name,
            "description": description,
            "selectedmfcindex": selected_mfc,
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
            # Update the profile list
            self.update_onoffconcprofile_list()
            
            # Update status bar that saving was succesful
            self.status_var.set(f"Saved profile: {profile_name}")
        else:
            messagebox.showerror("Save Error", f"Could not save profile '{profile_name}'.")
    
    def stop_onoffconc_run(self):
        """Stop running the Pure Gas On/Off concentration profile and set the valve position to let the N2 in the gas inlet, and set the mass flow rate of VOC and MFC to 0
        """
        # Set stop flag to True
        self.stop_onoff_conc_run = True
        
        # Update the status bar that profile will be stopped
        self.status_var.set("Stop running the profile.")
        
        # Disable the stop button
        self.onoffconc_stop_button.config(state = 'disabled')
        
        # Set the flow rates of VOC en N2 both to 0
        self.mfcs[self.onoffconc_voc_index + 1].set_massflow(0)
        self.mfcs[0].set_massflow(0) 
        
        # Valve position is such that only N2 fows into the chamber.
        self.valve[0].switch_position(1)
        self.valve[1].switch_position(2)
    
    ################## Different Pure Gas Concentration Profile Management ###########################
    def create_diffconc_profile_tab(self):
        """Creates tab for Different Pure Gas Concentration Profile Management 
        """
        #Create scrollable tab with the name 'Different Pure Gas Concentration Profile Management'        
        profile_tab = self.create_scrollable_tab(self.notebook, "Different Pure Gas Concentration Profile Management")
        
        ## Split into two frames: list_frame and edit_frame
        # List frame displaying the list with the available profiles
        list_frame = ttk.Frame(profile_tab)
        list_frame.pack(side= 'left', fill = 'both', expand=True, padx=5, pady=5)
        
        # Edit frame where the user can edit the profile and fill in the daa for new profiles
        edit_frame = ttk.Frame(profile_tab)
        edit_frame.pack(side= 'right', fill= 'both', expand=True, padx=5, pady=5)
        
        ############# Left frame / list frame #############
        # List frame displaying the list with the available profiles
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
        # Frame for the profile list buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', padx=5, pady=5)

        # Button to load the profile
        load_button = ttk.Button(button_frame, text="Load", command=self.load_diffconcprofile)
        load_button.pack(side='left', padx=3, expand=True)
        
        # Button to delete the profile
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_diffconcprofile)
        delete_button.pack(side='left', padx=3, expand=True)
        
        # Frame for the concentration setpoint graph
        graph_frame = ttk.Frame(list_frame)
        graph_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.diffconc_fig, self.diffconc_ax = plt.subplots(figsize=(4, 2))
        self.diffconc_ax.set_title("Setpoint Concentration vs Time Graph")
        self.diffconc_ax.set_xlabel("Time (s)")
        self.diffconc_ax.set_ylabel("Concentration (ppm)")
        self.diffconc_ax.grid(True)

        # Insert the plot in Tkinter
        self.diffconc_canvas = FigureCanvasTkAgg(self.diffconc_fig, master=graph_frame)
        self.diffconc_canvas.draw()
        self.diffconc_canvas.get_tk_widget().pack(fill='both', expand=True)

        ############# Right frame / edit frame #############
        # Edit frame where the user can edit the profile and fill in the daa for new profiles
        info_frame = ttk.Frame(edit_frame)
        info_frame.pack(fill='both', padx=5, pady=5)
        
        firstrow_frame = ttk.Frame(info_frame)
        firstrow_frame.pack(fill='x', pady=2)
        
        # Label to display the text 'new profile' when the user want to add a new profile
        self.new_diffconcprofile_label = ttk.Label(firstrow_frame, text="")
        self.new_diffconcprofile_label.pack(side = 'left', padx=5)
        
        # Frame for the profile name
        name_frame = ttk.Frame(firstrow_frame)
        name_frame.pack(side='left', fill='x', padx=5)

        # Label and entry field for profile name
        ttk.Label(name_frame, text="Name:").pack(side='left')
        self.diffconc_namevar = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=self.diffconc_namevar)
        name_entry.pack(side='left', padx=10)
        name_entry.config(width=30)
        
        # Frame for the description
        desc_frame = ttk.Frame(firstrow_frame)
        desc_frame.pack(side='left', fill='x', expand=True)

        # Label and entry field for profile description
        ttk.Label(desc_frame, text="Description:").pack(side='left')
        self.diffconc_desc_var = tk.StringVar()
        desc_entry = ttk.Entry(desc_frame, textvariable=self.diffconc_desc_var)
        desc_entry.pack(side='left', fill='x', expand=True)
        
        secondrow_frame = ttk.Frame(info_frame)
        secondrow_frame.pack(fill='x', pady=2)

        # Combobox for the selected MFC which contains the VOC
        ttk.Label(secondrow_frame, text="Select VOC1 (MFC2) or VOC2 (MFC3):").pack(side='left', padx=5)
        self.diffconc_voc_mfc_choice = ttk.Combobox(secondrow_frame, values=["VOC1 (MFC2)", "VOC2 (MFC3)"], state="readonly")
        self.diffconc_voc_mfc_choice.pack(side='left', padx=5)
        self.diffconc_voc_mfc_choice.current(0)  # default to MFC 2
        
        # Combobox to select the VOC type
        ttk.Label(secondrow_frame, text="Select VOC type:").pack(side='left', padx=5)
        self.diffconc_voc_var = tk.StringVar()
        self.onoffconc_voc_list = list(self.settings_manager.get_voc_data().keys())
        self.diffconcprofile_voc_type_combobox = ttk.Combobox(secondrow_frame, textvariable=self.diffconc_voc_var, values=self.onoffconc_voc_list, state="readonly")
        self.diffconcprofile_voc_type_combobox.pack(side='left', padx=5)
        self.diffconcprofile_voc_type_combobox.current(0)
        
        # Label and entry field for the total flow rate
        ttk.Label(secondrow_frame, text="Total Flow Rate (mL/min):").pack(side='left', padx=5)
        self.diffconc_totalflowrate_var = tk.DoubleVar()
        self.totalflow_entry = ttk.Entry(secondrow_frame, textvariable=self.diffconc_totalflowrate_var)
        self.totalflow_entry.pack(side='left', padx=5)
        self.totalflow_entry.config(state = 'enabled')
        
        # Select Button to activate step input fields and deactivate the selected MFC which contains the VOC, the VOC type, total flow rate
        ttk.Button(secondrow_frame, text="Select", command=self.enabling_select_diffconcprofile).pack(side='left', padx=5)

        # Button to make a new profile
        new_profile_btn = ttk.Button(secondrow_frame, text = 'New Profile', command = self.create_new_diffconcprofile)
        new_profile_btn.pack(side='right', padx=3, expand=True)
        
        # Frame to show the steps
        steps_frame = ttk.Frame(edit_frame)
        steps_frame.pack(fill = 'both' , expand=True, padx=5, pady=5)

        # Tree to show steps in the right frame
        #https://tk-tutorial.readthedocs.io/en/latest/tree/tree.html
        self.diffconc_steps_tree = ttk.Treeview(
            steps_frame, 
            columns=("time", "gas_inlet", "concentration", "flow mfc1", "flow mfc2"), 
            show="headings"
        )
        self.diffconc_steps_tree.heading("time", text="Time (s)")
        self.diffconc_steps_tree.heading("gas_inlet", text="Gas Inlet of Chamber (VOC/N2)")
        self.diffconc_steps_tree.heading("concentration", text="Concentration (ppm)")
        self.diffconc_steps_tree.heading("flow mfc1", text="Flow N2 (mL/min)")
        self.diffconc_steps_tree.heading("flow mfc2", text="Flow MFC 2 (mL/min)")

        self.diffconc_steps_tree.column("time", width=80, anchor=tk.CENTER)
        self.diffconc_steps_tree.column("gas_inlet", width=80, anchor=tk.CENTER)
        self.diffconc_steps_tree.column("concentration", width=100, anchor=tk.CENTER)
        self.diffconc_steps_tree.column("flow mfc1", width=100, anchor=tk.CENTER)
        self.diffconc_steps_tree.column("flow mfc2", width=100, anchor=tk.CENTER)

        self.diffconc_steps_tree.pack(fill = 'both' , expand=True)

        # Frame for the entry field of the steps
        step_controls_frame = ttk.Frame(edit_frame)
        step_controls_frame.pack(fill='x', padx=5, pady=5)

        # Label and entry field for the time of the step
        self.diffconc_profile_time_label = ttk.Label(step_controls_frame, text="Time (s):").pack(side='left')
        self.diffconc_step_time_var = tk.DoubleVar()
        self.step_time_entry = ttk.Entry(step_controls_frame, textvariable=self.diffconc_step_time_var, width=8)
        self.step_time_entry.pack(side='left', padx=2)
        self.step_time_entry.config(state ='disabled')

        # Combobox to select what gas the user want in the gas inlet of the chamber
        self.diffconc_profile_valve_label =  ttk.Label(step_controls_frame, text="Gas Inlet of Chamber:").pack(side='left')
        self.diffconc_valve_var = tk.StringVar() #integer variable, since the valve should be position on 1/2
        self.diffconc_step_valve_combo = ttk.Combobox(
            step_controls_frame, 
            textvariable=self.diffconc_valve_var, 
            values=["VOC", "N2"], 
            width=5,
            state="readonly"
        )
        self.diffconc_step_valve_combo.bind("<<ComboboxSelected>>", self.diffconc_gas_inlet_selected)
        self.diffconc_step_valve_combo.pack(side='left', padx=2)
        self.diffconc_step_valve_combo.config(state ='disabled')
        self.diffconc_step_valve_combo.current(0)  # Selects "VOC"

        # Label and entry for the desired concentration in ppm
        self.diffconc_profile_conc_label = ttk.Label(step_controls_frame, text="Concentration (ppm):").pack(side='left')
        self.diffconc_step_conc_var = tk.DoubleVar()
        self.step_conc_entry = ttk.Entry(step_controls_frame, textvariable=self.diffconc_step_conc_var, width=8)
        self.step_conc_entry.pack(side='left', padx=2)
        self.step_conc_entry.config(state ='disabled')

        # Label and entry field for the flow rate of nitrogen
        self.diffconc_profile_mfc1_label = ttk.Label(step_controls_frame, text="Flow N2 (mL/min):").pack(side='left')
        self.diffconc_flowN2_var = tk.DoubleVar()
        self.diffconc_step_flow1_entry = ttk.Entry(step_controls_frame, textvariable=self.diffconc_flowN2_var, width=25)
        self.diffconc_step_flow1_entry.pack(side='left', padx=2)
        self.diffconc_step_flow1_entry.config(state ='disabled')

        # Label and entry field for the flow rate of the VOC
        self.diffconc_mfc2_label = ttk.Label(step_controls_frame, text="Flow VOC (mL/min):").pack(side='left')
        self.diffconc_flowVOC_var = tk.DoubleVar()
        self.diffconc_step_flow2_entry = ttk.Entry(step_controls_frame, textvariable=self.diffconc_flowVOC_var, width=25)
        self.diffconc_step_flow2_entry.pack(side='left', padx=2)
        self.diffconc_step_flow2_entry.config(state ='disabled')
        
        # Button to calculate the flow rates of N2 and VOC based on the desired concentration
        self.calculate_step_button = ttk.Button(step_controls_frame, text="Calculate Flow Rates", command=self.diffconc_calc_step)
        self.calculate_step_button.pack(side='left', padx=2)
        self.calculate_step_button.config(state = 'disabled')

        ########## Buttons for the step ##########
        ## Frame to add and remove a step, and clear all steps ##
        step_buttons_frame = ttk.Frame(edit_frame)
        step_buttons_frame.pack(fill='both')

        # Button to add a new step
        self.add_step_button = ttk.Button(step_buttons_frame, text="Add Step", command=self.diffconcadd_step)
        self.add_step_button.pack(side='left', padx=2)
        self.add_step_button.config(state = 'disabled')
                
        # Button to remove a step
        self.remove_step_button = ttk.Button(step_buttons_frame, text="Remove Step", command=self.diffconcremove_step)
        self.remove_step_button.pack(side='left', padx=2)
        self.remove_step_button.config(state = 'disabled')
                
        # Button to clear all steps
        self.clear_steps_button = ttk.Button(step_buttons_frame, text="Clear All Steps", command=self.diffconcclear_steps)
        self.clear_steps_button.pack(side='left', padx=2)
        self.clear_steps_button.config(state = 'disabled')
                
        ## Frame for actions such as save, run and stop profile ##
        action_buttons_frame = ttk.Frame(edit_frame)
        action_buttons_frame.pack(fill='both')
        
        # Button to save the profile
        self.save_button = ttk.Button(action_buttons_frame, text="Save Profile", command=self.save_diffconcprofile)
        self.save_button.pack(side='left', padx=2)
        self.save_button.config(state = 'disabled')
        
        ## Button to run the profile
        self.run_button = ttk.Button(action_buttons_frame, text="Run Profile", command=self.run_diffconcprofile)
        self.run_button.pack(side='left', padx=2)
        self.run_button.config(state = 'disabled')
        
        ## Button to stop running the profile
        self.diffconc_stop_button = ttk.Button(action_buttons_frame, text="Stop", command=self.stop_diffconcprofile)
        self.diffconc_stop_button.pack(side='left', padx=2)
        self.diffconc_stop_button.config(state='disabled')
    
    def enabling_select_diffconcprofile(self):
        """Enable all input fields and buttons needed to define the steps and lock the selection of type VOC, total flow and dropdown of the selection of the VOC MFC
        """
        try:
            # Try to convert the value to float
            total_flow = float(self.totalflow_entry.get())
            
            ## Lock the selection of type VOC, total flow and dropdown of the selection of the VOC MFC
            self.diffconcprofile_voc_type_combobox.config(state = 'disabled')
            self.totalflow_entry.config(state = 'disabled')
            self.diffconc_voc_mfc_choice.config(state = 'disabled')
            
            # Enabling all input fields
            self.step_time_entry.config(state ='enabled')
            self.step_conc_entry.config(state ='enabled')
            self.diffconc_step_valve_combo.config(state='readonly')
            
            # Enabling all buttons
            self.calculate_step_button.config(state = 'enabled')
            self.remove_step_button.config(state = 'enabled')
            self.clear_steps_button.config(state = 'enabled')
            self.save_button.config(state = 'enabled')
            self.run_button.config(state = 'enabled')
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for total flow.")
            return

    def disabling_select_diffconcprofile(self):
        """Disable all step input fields and buttons and enable the selection of type VOC, total flow and dropdown of the selection of the VOC MFC
        """
        
        #  selection of type VOC, total flow and dropdown of the selection of the VOC MFC
        self.diffconcprofile_voc_type_combobox.config(state = 'readonly')
        self.totalflow_entry.config(state = 'enabled')
        self.diffconc_voc_mfc_choice.config(state = 'readonly')
        
        # Disabling all input fields
        self.step_time_entry.config(state ='disabled')
        self.step_conc_entry.config(state ='disabled')
        self.diffconc_step_flow1_entry.config(state ='disabled')
        self.diffconc_step_flow2_entry.config(state ='disabled')
        self.diffconc_step_valve_combo.config(state = 'disabled')

        # Disabling all buttons
        self.calculate_step_button.config(state = 'disabled')
        self.add_step_button.config(state = 'disabled')
        self.remove_step_button.config(state = 'disabled')
        self.clear_steps_button.config(state = 'disabled')
        self.save_button.config(state = 'disabled')
        self.run_button.config(state = 'disabled')        
    
    def update_diffconcprofile_list(self):
        """Update the list of available profiles"""
        #https://youtu.be/Vm0ivVxNaA8
        
        #Delete all the items from the listbox
        self.diffconcprofile_listbox.delete(0, tk.END)
        
        #Add all the profiles to the listbox
        for profile in self.diffconcprofilemanager.get_profiles():
            self.diffconcprofile_listbox.insert(tk.END, profile) 

    def load_diffconcprofile(self):
        """Load the selected profile """
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        # Get the currently selected item in the listbox
        selection = self.diffconcprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to load")
            return
        
        # Get the name of the selected profile (first selected item)
        profile_name = self.diffconcprofile_listbox.get(selection[0])
        # Load the profile with Diff conc profile manager
        profile = self.diffconcprofilemanager.load_profile(profile_name)
        # Clear label for new profiles   
        self.new_diffconcprofile_label.config(text = "")
        
        if profile:
            #Update the name of the profile
            self.diffconc_namevar.set(profile_name)
            
            #Update the description, temp, voc and total flow in the field
            self.diffconc_desc_var.set(profile.get("description", ""))
            # self.diffconc_temp_var.set(profile.get("temperature", ""))
            self.diffconc_voc_var.set(profile.get("voc", "")) 
            self.diffconc_totalflowrate_var.set(profile.get("total_flow", 0)) 
            self.diffconc_voc_mfc_choice.set(profile.get("mfcchoice", ""))
            
            # Clear the existing steps
            for item in self.diffconc_steps_tree.get_children():
                self.diffconc_steps_tree.delete(item)
            
            # Add new steps
            for step in profile.get("steps", []):
                self.diffconc_steps_tree.insert("", tk.END, values=(
                    step["time"],
                    step["gas_inlet"],
                    step["concentration"],
                    step["flow mfc1"],
                    step["flow mfc2"]
                ))
            self.update_diffconc_graph(profile.get("steps", []))

            # Update the status bar to update the user that profile is loaded   
            self.status_var.set(f"Loaded profile: {profile_name}")
        
        # Enable all input fields and buttons needed to define the steps and lock the selection of type VOC, total flow and dropdown of the selection of the VOC MFC
        self.enabling_select_diffconcprofile()

    def diffconc_gas_inlet_selected(self, event=None):
        """Function that is triggered when a gas inlet option is selected (N2 or VOC)
        It fills and clears the flow and concentration fields dependent on the selected gas inlet option 
        """
        
        # Get the selected gas inlet (N2 or VOC)
        gas_inlet = self.diffconc_valve_var.get()
        
        if gas_inlet == "N2":
            try:
                # Get the total flow from the GUI
                total_flow = float(self.diffconc_totalflowrate_var.get())
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid total flow rate first.")
                return

            # Automatically fill in the fields for N2
            # Concentration to 0 ppm
            self.diffconc_step_conc_var.set(0.0)  
            
            # mass flow rate of N2 is the total flow
            self.diffconc_flowN2_var.set(total_flow) 
            
            # mass flow rate of VOC is 0 ml/min
            self.diffconc_flowVOC_var.set(0.0) 
            
            # Enable the add step button
            self.add_step_button.config(state='enabled')
    
        elif gas_inlet == "VOC":
            # Clear the previous filled values
            self.diffconc_step_conc_var.set("")
            self.diffconc_flowN2_var.set("")
            self.diffconc_flowVOC_var.set("")
            
            # Disable the add step button
            # The user first need to fill in the desired concentration and calculate the corresponding flow
            self.add_step_button.config(state='disabled')
        else:
            messagebox.showerror("Selection Error", "Unknown gas inlet selection. Please choose 'N2' or 'VOC'")
            
    def delete_diffconcprofile(self):
        """Delete the selected profile"""
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        
        # Get selected item from the listbox
        selection = self.diffconcprofile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a profile to delete")
            return
        
        # Get the name of the selected profile (first selected item)
        profile_name = self.diffconcprofile_listbox.get(selection[0]) #To ensure that you only select the first selected
        
        # Ask for user confirmation before deleting the profile
        if messagebox.askyesno("Confirm", f"Delete profile '{profile_name}'?"):
            if self.diffconcprofilemanager.delete_profile(profile_name):
                #Updating the new profile list
                self.update_diffconcprofile_list() 
                #Changing the status
                self.status_var.set(f"Deleted profile: {profile_name}")
            else:
                # If profile deleting fails, show error message
                messagebox.showerror("Error", f"Failed to delete the profile: '{profile_name}'")
                
    def create_new_diffconcprofile(self):
        """Create Pure gas diff concentration profile
        """
        #Clearing all input fields and steps
        self.diffconc_namevar.set("")
        self.diffconc_desc_var.set("")
        self.diffconc_totalflowrate_var.set("2.0") 
        self.diffconc_step_time_var.set("0.0")
        self.diffconc_step_conc_var.set("0.0")
        self.diffconc_flowN2_var.set("0.0")
        self.diffconc_flowVOC_var.set("0.0")
        
        self.diffconcprofile_voc_type_combobox.current(0)
        self.diffconc_voc_mfc_choice.current(0)
        self.diffconcprofile_voc_type_combobox.current(0)
        self.diffconc_step_valve_combo.current(0)
        
        # Clear all entries of the existing steps in the tree
        for item in self.diffconc_steps_tree.get_children():
            self.diffconc_steps_tree.delete(item)
        
        # Clear the graph as well
        self.diffconc_ax.clear()
        self.diffconc_ax.set_title("Setpoint Concentration vs Time Graph")
        self.diffconc_ax.set_xlabel("Time (s)")
        self.diffconc_ax.set_ylabel("Concentration (ppm)")
        self.diffconc_ax.grid(True)
        self.diffconc_canvas.draw()
        
        # Show the user that a new profile is made, with the text new profile
        self.new_diffconcprofile_label.config(text = "New profile", foreground = "green")
        
        #Disable all step input fields and buttons and enable the selection of type VOC, total flow and dropdown of the selection of the VOC MFC
        self.disabling_select_diffconcprofile()
  
    def diffconcadd_step(self):
        """Add a new step to the current profile with calculated flows"""
        try:
            # Get input values from the entry fields
            time_val = float(self.diffconc_step_time_var.get())
            concentration_val = float(self.diffconc_step_conc_var.get())
            f_n2 = self.diffconc_flowN2_var.get()
            f_voc = self.diffconc_flowVOC_var.get()
            gas_inlet_vocn2 = self.diffconc_valve_var.get()

            # Time should not be negative
            if time_val < 0:
                raise ValueError("Time cannot be negative")
            
            # Gas inlet should be VOC or N2
            if gas_inlet_vocn2 not in ["VOC", "N2"]:
                raise ValueError("Gas Inlet of Chamber should be VOC or N2")

            # Check if the time already exists
            for child in self.diffconc_steps_tree.get_children():
                if float(self.diffconc_steps_tree.item(child, "values")[0]) == time_val:
                    if not messagebox.askyesno("Confirm", f"Step at time {time_val}s already exists. Overwrite?"):
                        #if True, thus User selects 'NO' then return
                        return
                    # Remove the existing step
                    self.diffconc_steps_tree.delete(child)
                    break

            # Insert the new step to the tree
            self.diffconc_steps_tree.insert("", tk.END, values=(time_val, gas_inlet_vocn2, concentration_val, f_voc, f_n2))
            
            # Enable the calculate step button, the user should fill in the next values of the step
            self.calculate_step_button.config(state = 'enabled')
            
            # Disable the add step button, the user should first calculate before adding the next step
            self.add_step_button.config(state = 'disabled')

        except ValueError as error:
            messagebox.showerror("Error", f"Invalid input: {error}")

    def diffconcremove_step(self):
        """Remove the selected step"""
        # Get the selected item
        selection = self.diffconc_steps_tree.selection()
        # Delete the selected item
        if selection:
            self.diffconc_steps_tree.delete(selection)
    
    def diffconcclear_steps(self):
        """Clear all steps"""
        # Ask the user for confirmation before clearing all the steps
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
                "gas_inlet": values[1],
                "concentration": float(values[2]),
                "flow mfc1": float(values[3]),
                "flow mfc2": float(values[4])

            })
        
        # Update the graph with the steps
        self.update_diffconc_graph(steps)
            
        # Sort steps by time
        #https://docs.python.org/3/howto/sorting.html
        steps = sorted(steps, key=lambda steps: steps["time"])
        
        # Create the profile data
        profile_data = {
            "description": self.diffconc_desc_var.get(),
            "mfcchoice": self.diffconc_voc_mfc_choice.get(),
            "voc": self.diffconc_voc_var.get(),  
            "total_flow": float(self.diffconc_totalflowrate_var.get()), 
            "steps": steps
        }

        # Save the profile use the profile manager
        if self.diffconcprofilemanager.save_profile(name, profile_data):
            self.update_diffconcprofile_list()
            self.status_var.set(f"Saved profile: {name}")
        else:
            # If saving failed, show error message
            messagebox.showerror("Error", f"Failed to save profile '{name}'")
    
    def run_diffconcprofile(self):
        """Run the current profile"""    

        # Check that the MFC and RVM devices are connected
        if not (self.mfcs[0].connected and self.mfcs[1].connected and self.mfcs[2].connected and self.valve[0].connected and self.valve[1].connected):
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
        if not self.diffconcprofile_checkthermaleq_alarm():
            return
            
        # Update the status bar with the realtime values
        self.update_run_var()
        
        #Enabling the stop button, since you can now stop a running profile
        self.diffconc_stop_button.config(state=tk.NORMAL) 
        
        # Start profile in a separate thread, such that the UI doesn't freeze until it finishes

        self.diffconcprofile_thread = threading.Thread(
            target=self.run_diffconcprofile_thread,
            daemon=True         # Stops threading by pressing an event, e.g. pressing on stop button
        )
        self.diffconcprofile_thread.start()

    def diffconcprofile_checkthermaleq_alarm(self):
        """
        Checks whether the user has confirmed the cooling plate is set to 0 °C and stable.
        Ensuring that there is thermal equilibrium before running the concentration profile

        Returns:
            boolean: True if user confirms the temperature is 0 degrees and stable, else False
        """
        #Checking whether the temperature has already been set to the filled temperature
        # https://www.pythontutorial.net/tkinter/tkinter-askyesno/
        confirm = messagebox.askyesno(
            "Cooling Plate Temperature",
            f"Did you set the cooling plate temperature to 0 °C? And is the temperature constant and stable?"
        )
        
        # If user clicks "No", return False
        if not confirm:
            return False
        return True 

    def run_diffconcprofile_thread(self):
        """Thread function to run  profile in the background
        """      
        try:
            def safe_update(status):
                self.root.after(0, lambda: self.update_diffconcprofile_var(status))
                
            # Displaying which profile is running in the status bar
            self.status_var.set(f"Running profile: {self.diffconc_namevar.get()}")

            # Run the profile in the profile manager
            self.diffconcprofilemanager.run_profile(
                update_callback=safe_update
            )
            self.root.after(0, self.diffconcprofile_complete)

        except Exception as e:
            self.root.after(0, lambda e=e: self.diffconcprofile_error(e))

    def diffconcprofile_complete(self):
        """Called when profile completes successfully"""
        self.diffconc_stop_button.config(state='disabled')
        # Update status bar with profile run is completed
        self.status_var.set("Profile run completed")
    
    def diffconcprofile_error(self, error):
        """Called when profile run encounters an error"""
        self.diffconc_stop_button.config(state='disabled')
        # Update status bar with profile run is failed
        messagebox.showerror("Error", f"Profile run failed: {error}")
        self.status_var.set("Profile run failed")
    
    def stop_diffconcprofile(self):
        """Stop the currently running profile"""
        self.diffconcprofilemanager.stop_profile()
        # Update status bar with profile run is stopped
        self.diffconc_stop_button.config(state='disabled')
        self.status_var.set("Profile run stopped by user")
    
    def update_diffconcprofile_var(self, status):
        """Update the GUI with the current status of the running the Diff Conc profile

        Args:
            status (dict): Dictionary with the value fo the current step of the running profile
        """
        try:
            #when the UI is closed then this won't be "updating" 
            if not self.root.winfo_exists():
                return

            # Update the status of the running Diff Conc profile in the UI  
            self.diffconc_elapsed_label.config(text=f"{status['elapsed_time']:.1f}s")
            self.diffconc_step_label.config(text=f"{status['current_step']}/{status['total_steps']}")
            self.diffconc_value_label.config(text=f"Concentration: {status['concentration']} (ppm), Gas Inlet of Chamber: {status['gas_inlet']}, MFC N2: {status['flow mfc1']:.2f} ml/min, MFC VOC: {status['flow mfc2']:.2f} ml/min")
                
        except tk.TclError:
            return
        
    def diffconc_calc_step(self):
        """Calculate the required VOC and N2 flow rates based on the entered concentration and total flow rates
        """
        try:
            # Get the input values from the GUI
            concentration_val = float(self.diffconc_step_conc_var.get())
            total_flow = float(self.diffconc_totalflowrate_var.get())
            voc = self.diffconc_voc_var.get()

            # Calculate the required flows for VOC and N2
            f_voc, f_n2, P_s = self.calculate_required_flow_0degrees(voc, concentration_val, total_flow)
            if f_voc is None or f_n2 is None:
                messagebox.showerror("Calculation Error", "Flow could not be calculated for this VOC and concentration. Please enter another concentration.")
                return

            ## Set the values to the corresponding input fields
            self.diffconc_flowN2_var.set(f_n2)
            self.diffconc_flowVOC_var.set(f_voc)

            # Enable add step button
            self.add_step_button.config(state = 'enabled')

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            
    def update_diffconc_graph(self, steps):
        """Update the setpoint differention concentration graph

        Args:
            steps: list of dictionaries where each dictionary represent one step
        """
        try:
            #when the UI is closed then this won't be "updating" (to debug)
            if not self.root.winfo_exists():
                return
            
            voc = self.diffconc_voc_var.get()

            # Initialize lists to store time and concentration for the graph
            times = []
            concs = []

            # Sort steps by time to ensure correct plotting
            steps = sorted(steps, key=lambda s: s.get("time", 0))

            # Obtain from each step the time and concentration
            for step in steps:
                time = step.get("time", 0)
                conc = step.get("concentration", 0)
                times.append(time)
                concs.append(conc)

            self.diffconc_ax.clear()
            self.diffconc_ax.step(times, concs, where='post', linestyle='-', marker='o', markersize = 3, linewidth=2, color='red' )
            self.diffconc_ax.set_title(f"Setpoint Concentration Graph of {voc}")
            self.diffconc_ax.set_xlim(0, max(times) * 1.2)
            self.diffconc_ax.set_ylim(0, max(concs) * 1.5)
            self.diffconc_ax.set_xlabel("Time (s)")
            self.diffconc_ax.set_ylabel("Concentration (ppm)")
            self.diffconc_ax.grid(True)
            
            # Draw the graph in the GUI
            self.diffconc_canvas.draw()

            # Om figure te saven        
            # self.diffconc_fig.savefig("C:/Users/chant/Downloads/setpoint_concentration_plot.png", dpi=300, bbox_inches='tight')
            
        except tk.TclError:
                return

    ################### VOC Settings ###########################
    def voc_settings(self):
        """Create window that manages the VOC type with its variables, where the user can view, add, edit and delete the VOC types
        """
        window = tk.Toplevel(self.root)
        window.title("VOC Manager")

        # Get all the VOC data from the settings manager
        vocs = self.settings_manager.get_voc_data()

        # Frame for existing VOCs
        list_frame = ttk.LabelFrame(window, text="Existing VOCs")
        list_frame.pack(padx=15, pady=10, fill="x")

        # Listbox to display VOCs
        self.voc_listbox = tk.Listbox(list_frame, height=6, width=40)
        self.voc_listbox.pack(padx=10, pady=5)
        for name in sorted(vocs.keys()):
            self.voc_listbox.insert(tk.END, name)

        # Whenever the user select the listbox, the VOC data is loaded
        self.voc_listbox.bind("<<ListboxSelect>>", self.load_voc_to_entries)

        # Frame for VOC data entry fields
        entry_frame = ttk.LabelFrame(window)
        entry_frame.pack(padx=15, pady=10, fill="x")

        # Input field for VOC name
        ttk.Label(entry_frame, text = 'VOC Name').grid(row = 0, column = 0)
        self.voc_name_entry = ttk.Entry(entry_frame, width=25)
        self.voc_name_entry.grid(row=0, column=1)
        
        # Input fields for Antoine equation values and temperature range
        self.voc_value_entries = []
        labels = ["Antoine A", "Antoine B", "Antoine C", "Tmin", "Tmax"]
        for i, label in enumerate(labels):
            ttk.Label(entry_frame, text=label).grid(row=i+1, column=0)
            entry = ttk.Entry(entry_frame, width=25)
            entry.grid(row=i+1, column=1)
            self.voc_value_entries.append(entry)

        # Button for New VOC by clearing the field
        new_button = ttk.Button(entry_frame, text="New VOC", command=self.new_voc_fields)
        new_button.grid(row=6, column=0, padx=5, pady=10)
        
        # Button to save the VOC
        save_button = ttk.Button(entry_frame, text="Save VOC", command=self.save_voc_from_ui)
        save_button.grid(row=6, column=1, padx=5, pady=10)

        # Button to delete the VOC
        delete_button = ttk.Button(entry_frame, text="Delete VOC", command=self.delete_voc_from_ui)
        delete_button.grid(row=6, column=2, padx=5, pady=10)
        
    def load_voc_to_entries(self, event=None):
        """Load the selected VOC data from the listbox into the entry fields
        """
        #https://pythonassets.com/posts/listbox-in-tk-tkinter/
        # Get the currently selected item in the listbox
        selection = self.voc_listbox.curselection()
        if not selection:
            return

        # Get the name of the selected VOC (first selected item)
        voc_name = self.voc_listbox.get(selection[0])
        # Obtain the data from the selected VOC from the settingsmanager
        data = self.settings_manager.get_voc_data().get(voc_name)

        if data:
            # Set the VOC name in the name entry field
            self.voc_name_entry.delete(0, tk.END)
            self.voc_name_entry.insert(0, voc_name)

            # Fill Antoine A, B, C, Tmin, Tmax values into their respective entry fields
            for i in range(5):
                self.voc_value_entries[i].delete(0, tk.END)
                self.voc_value_entries[i].insert(tk.END, str(data[i]))

    def save_voc_from_ui(self):
        """Save VOC data to the settingsmanager
        """
        try:
            # Obtain the VOC name of the entry field
            name = self.voc_name_entry.get().strip()
            if not name:
                raise ValueError("VOC name cannot be empty.")

            # Collect the values (A, B, C, Tmin, Tmax) from the entry fields
            values = []
            for voc in self.voc_value_entries:
                # Convert the input to float
                val = float(voc.get()) 
                values.append(val)

            # Add VOC to settingsmanager
            self.settings_manager.add_voc(name, values)
            messagebox.showinfo("Success", f"VOC '{name}' is saved.")

            # Refresh the VOC list
            self.refresh_voc_list()
            
            # Clear the entry field after saving
            self.voc_name_entry.delete(0, tk.END)
            for voc in self.voc_value_entries:
                voc.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def refresh_voc_list(self):
        """Refresh the VOC list in the UI
        """
        # Get all VOC names from the settingsmanager
        voc_names = list(self.settings_manager.get_voc_data().keys())

        # Update the values of the comboboxes of the onoff conc and diff conc profiles
        self.diffconcprofile_voc_type_combobox['values'] = voc_names
        self.onoffconc_typevoc_dropdown['values'] = voc_names

        #Update the listbox of the VOC settings
        self.voc_listbox.delete(0, tk.END)
        for name in sorted(voc_names):
            self.voc_listbox.insert(tk.END, name)
            
    def delete_voc_from_ui(self):
        """Delete the selected VOC from the VOC settings
        """
        # Get the currently selected VOC in the listbox
        selected = self.voc_listbox.curselection()
        if not selected:
            messagebox.showwarning("No VOC selected", "Please select a VOC to delete.")
            return

        # Get the VOC same from the selected VOC
        voc_name = self.voc_listbox.get(selected[0])

        # Ask user to confirm the deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{voc_name}'?")
        if confirm:
            # Delete the VOC from settings
            self.settings_manager.delete_voc(voc_name)
            # Refresh the VOC lists
            self.refresh_voc_list()
            # Clear all entry fields
            self.voc_name_entry.delete(0, tk.END)
            for entry in self.voc_value_entries:
                entry.delete(0, tk.END)

            messagebox.showinfo("VOC Deleted", f"'{voc_name}' has been deleted.")
            
    def new_voc_fields(self):
        """Clear VOC input fields to add a new VOC
        """
        # Clear all entry fields
        self.voc_name_entry.delete(0, tk.END)
        for entry in self.voc_value_entries:
            entry.delete(0, tk.END)
        
        # Deselect a selected item
        self.voc_listbox.selection_clear(0, tk.END)
