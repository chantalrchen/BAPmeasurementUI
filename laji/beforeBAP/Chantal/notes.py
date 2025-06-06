##MFC
#Connecting the MFC with the dedicated port
MFC_port = 'COM1'
MFC_instrument = propar.instrument(MFC_port)

#Reading the mass flow
MFC_instrument.readParameter(205) #Fmeasure

#Setting the mass flow
MFC_target_massflow = 0.0
MFC_instrument.writeParameter(206, MFC_target_massflow) #Fsetpoint (float)

#########################################
##Cooling: the cooling system can lower the temperature maximum by 30 \textcelsius below the ambient temperature 	
Cooling_port = 'COM2'
Cooling_instrument = serial.Serial(Cooling_port, 9600, timeout=1) #p24: 9600 baud, 1 stop bit, no parity, no hardware handshake, 100ms delay after each command sent (after \r)
#100 ms delay, so a timeout of 1s should be enough

#Reading the temperature
Cooling_instrument.write(b"p\r") #sending a request to read the temperature; The current plate temperature will be returned in a text string terminated by <CR><LF>, e.g. 14.3\r
time.sleep(0.1)  # 100ms delay after each command sent (after \r)
response = Cooling_instrument.read_until(b'\r').decode().strip()  #reads until \r


#Setting the temperature
Cooling_instrument.write(b"n20\r") #setting the temperature to 20 degrees
time.sleep(0.1)  # 100ms delay after each command sent (after \r)

####################################3
##Valve: 4-ports but actually only has 2 directions
#Connecting the valve with the dedicated port
RVM_port = 'COM3'
RVM_instrument = serial.Serial(RVM_port, 9600, 8, None, 1, 1000) # Baudrate = 9600, Data bits = 8, Parity = None, Stop bit = 1, Timeout = 1000 sec!!!!;
##TIMEOUT SHOULD BE CHANGED AFTER WE KNOW WHAT KIND OF RVM IT IS!!!!

#Initializing the valve, Once it is done, the valve is positioned on port 1 (opened)
RVM_instrument.write(b"/1ZR\r")

# Position 1: connects port 1 - port 2 and port 3- port 4
RVM_instrument.write(b"/1b1R\r")
# Position 2: connects port 2 - port 3 and port 1 - port 4
RVM_instrument.write(b"/1b2R\r")


####
##formatting with alt shift F
## documentating using """
