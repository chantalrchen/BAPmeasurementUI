import os
import numpy as np
import time
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

class DataHandler:
    def init(self, gui):
        self.gui = gui
    
    #DataPortBytesAvailableHandler.m
    def DataPortBytesAvailableHandler(self, obj, event):
        #obj:      serial port object
        #event:    event information
        #handles:  handles

        #Get the folder name that the user entered in the GUI (edit box #19)
        i_foldername = self.edit19_foldername.get()
        path = os.path.join('experiment', i_foldername)
        settingfilename = os.path.join(path, 'setting_information.txt')
        timefilename = os.path.join(path, 'time.dat')
        
        if not os.path.exists(settingfilename):
            print('Information record incomplete')
            messagebox.showwarning('Warning','Information record incomplete')
            return
        
        if self.AutoScale.get() == 1:
            print("Auto-Scaling on")
        else:
            print("Auto-Scaling off")
        #Autoscale = 0
        Autoscale = self.AutoScale.get()
        
        tensmode = self.radiobutton12_tensmode.get()
        minADC = self.edit26_minADC.get()
        maxADC = self.edit27_maxADC.get()
        
        RefPackets = [3,8] #enter negative number if no reference frame (under construction)
        tNow = time.time() #record event time
        
        try:
            if self.datacom_s['UserData']['CaptureData']:
                
            
    
        

   