#There is no shebang line because this is a PyQGIS script
#run this in the pyQgis python console

#log position from serial to vector layer "waypnts" in pyQgis
#This script will lock up the canvas until you stop entry with ctrl+c or
#when the program finishes. This is a precursor script to one that
#averages a certain number of waypoints and adds them to the map.

#I wrote this to use with the ublox 6 gps unit that I purchased on amazon.com


from PyQt4.QtCore import *  #to try and give us Qvariant types
import serial
import pynmea2              #to parse the NMEA strings
import time



project = QgsProject.instance()

for x in QgsMapLayerRegistry.instance().mapLayers().values():
    if x.name() == 'waypnts':
        layer = x  



ser = serial.Serial('/dev/ttyUSB0',9600) #make sure that you use the right serial port

for var in range(100):  #The range is arbirary, because the final script will count the waypoints
    data = ser.readline()
    if (data.startswith("$GPRMC")):
        msg = pynmea2.parse(data)
        y, x = msg.latitude, msg.longitude
        vpr = layer.dataProvider()
        pnt = QgsGeometry.fromPoint(QgsPoint(x,y))
        f = QgsFeature()
        f.setGeometry(pnt)
        vpr.addFeatures([f])

        #the following line refreshes the canvas
        ser.reset_input_buffer()
        layer.triggerRepaint()  