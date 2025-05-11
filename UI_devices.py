import tkinter as tk
from tkinter import messagebox, ttk
import propar   # Bronkhorst MFC
import serial   # Cooling and Valve
import time 

###
#MFC
#connect
mfc1 = propar.instrument('COM1', channel=1)
mfc2 = propar.instrument('COM1', channel=2)
mfc3 = propar.instrument('COM1', channel=3)

#disconnect

#controlfunction, the instrument works as a flow controller or a pressure controller
mfc1.writeParameter(432, 0)


#ensure_units
#sensor type = gas volume
mfc1.writeParameter(22, 3)

#capacity unit index = 2 (mln/min)
mfc1.writeParameter(23, 2)

#get_massflow
mfc1.readParameter(205)

#set_massflow
par1 = 1
mfc1.writeParameter(206, par1)
