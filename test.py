#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jgraves
#
# Created:     01/02/2018
# Copyright:   (c) jgraves 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import arcpy

fc = r'N:\landrec\Jonathan Graves\GIS\ratiostudy_2017.gdb\CommLand_history'

fields_add = [      ["Rate2013", "LONG"],
                    ["Type2013", "TEXT"],
                    ["Rate2014", "LONG"],
                    ["Type2014", "TEXT"],
                    ["Rate2015", "LONG"],
                    ["Type2015", "TEXT"],
                    ["Rate2016", "LONG"],
                    ["Type2016", "TEXT"],
                    ["Rate2017", "LONG"],
                    ["Type2017", "TEXT"],
                    ["Rate2018", "LONG"],
                    ["Type2018", "TEXT"]
                ]
y = 0

for item in fields_add:
    arcpy.AddField_management(fc, fields_add[y][0], fields_add[y][1] )
    y += 1