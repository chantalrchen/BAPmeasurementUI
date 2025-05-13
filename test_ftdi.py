import sys
import time
import ftd2xx

print("Python:", sys.executable, sys.version)
print("Waiting 2 sec for COM to settle…")
time.sleep(2)
print("Library:", ftd2xx.getLibraryVersion())

devs = ftd2xx.listDevices()
print("FTDI listDevices() →", devs)

if devs:
    try:
        d = ftd2xx.open(0)
        print("Opened device 0, serial:", d.getSerialNumber())
        d.close()
    except Exception as e:
        print("Failed to open device:", e)