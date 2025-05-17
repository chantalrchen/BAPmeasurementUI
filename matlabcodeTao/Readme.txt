
E-nose system version 2023.1
together with Matlab Gui code 
29-03-2023 by TS
Edit on 02-10-2024

************************************************************************************************************
*****************       ******** *******      **************************************************************
******************** ********* *** ***** **** **************************************************************
******************** ********       **** **** **************************************************************
******************** ******* ******* *** **** **************************************************************
******************** ****** ********* **      **************************************************************
************************************************************************************************************
************************************************************************************************************

Make sure you are well grounded  when you touch the chips (package also)!!!!!!!!!!!!!!!!!!!!!!

************************************************************************************************************
Before experiment:
	Usb line and a TTL-3V3 line are needed.
	Always check com ports when you first connect the board to your PC. 
	If the com ports on your PC is different from the default ports setting in "cssgui,ini", change it.

************************************************************************************************************
Operating:
	Check if pin 10 of package is already cut
	Put the chip into the socket in the right way (Align PIN 1)
************************************************************************************************************
************************************************************************************************************
************************************************************************************************************
Matlab Gui Code user guide.
	
	*Create file path: "C:\LocalData\css_Data" and "C:\LocalData\CSSa_Run\CSSa_HelperFiles" (folders)

	Open the "cssgui.m" file
		for some PC, make sure the other .m files are opened as functions
	
	1. Click "Init" button in "Basic Settings", and wait several seconds for the setup to read the default
	   parameters.(CHECK COM PORTS, WHICH CAN BE DIFFERENT FOR DIFFERENT PC)
		*Do not change the default unless specifically required.
	2. Go to "Advanced Settings", to successfully start reading the data, you need to
	3. Add a name in the "Experiment Number:" edit box, then click "Create/Choose data folder". If there is
	   already a folder with this name, it will be chosed and the data will be saved here later. Otherwise, 
	   a new folder with this name will be generated and chosed.
	4. Add value in "Temperature" and "Pressure" edit box. And then click "Save setting parameters". Then you
	   will see the message "Ready to start". If the edit box is empty, you will not be allowed to start.
		*Later more parameters will be added, this is to make sure every experiment is conducted under 
                 known situation.
	5. "Signal trace pixel settings" are for real-time trace of some pixels in each array. You can leave it
	   empty or choose 5 pixels at most for each array. But be sure: Click the "Lock" button below, this will
	   disable the edit box of this parts, and only after this you will be allowed to start measurement.
		*Each array have 1024 pixels, please choose a number from 1-1023 to choose a pixel to read real-time.
	6. Every time you want to record something, you can write in the "Notes" box and click "Save", the content 
	   will be saved together with time.
	7. Finally, go to "Data" page.
	8. Select and only select the box "S0" in "Target 1"
		*"Cell Pair" and other settings are not needed in E-nose measurements.
	9. Click "Start Read". It will sometimes give wrong results, just click the "Stop Read" and re-click "Start
	   Read". Otherwise, try to disconnect the PCB and reconnect it again, (and restart the code).
		*A tip: you can check in the "Command Window" of Matlab, if the displayed packet number starting from 
		 a quite large value, normally it means wrong results.
	10. Select on "Auto scale", and select off at a stable reference situation (reference measurement)
	
	Other functions that can try:
	11. Click "Capture 1 image", then the image of the sensor data visualization interface will be saved.
	12. Click "Start Record image", then every image of sensor data cisualization interface will be saved (take time).
		*It will make the whole read-out slower.
	13. After finishing image record, if you click "Video generation", then the recorded image will be
	    deleted and a video will be generated instead.
		*This can only work just after measurement, and before starting a new one.
	14. In "Signal display mode", you can drag the progress bar, and the way the sensor data is displayed will change.
	    The "Linear interpolation" is friendly to human's eyes, and the "Nearest electrode" will show directly
	    electrode shape and obvious change among each pixels.
	15. If you add value in the edit box of "min ADC" and "max ADC", the shown Color bar range and ADC code axis
	    range will be reset to the range you set. It will be helpful if you want to zoo in some parts.
		*You can delete the value during measurement, then it will automatically go back to normal display way.
		*Our ADC output ranged from 0-4095.
	16. If you add value in the edit box of "trace time", the time axis of signal trace image will be limited to
	    [0,the value you set].
		*You can delete the value during measurement, then it will automatically go back to normal display way.
	17. Go back to "Advanced Settings" page, if you click "Restart trace", then the signal trace image will clean
	    the results before and restart recording from now on. This can be down during experiments.
	


Quick operation remind:
filling Temperature, Pressure, Experiment Number box
--> Click Create/Choose data folder
--> Click Save setting parameters
--> Click Lock for the signal trace pixel settings (no matter if you enter mark number or not)
--> Start Read
























	


































