#--------------------------------------------------------------------------------------------------------
#   Create Lines between Points and Other Point Features
#   Author: Jonathan Graves
#   email: jonathan.graves@blueearthcountymn.gov
#   Creation Date: 12/27/2016
#   Revised Date:
#   Version 0.1
#   NOTES:
#--------------------------------------------------------------------------------------------------------

import arcpy
import time

startTime = time.time()

arcpy.MakeFeatureLayer_management(r'M:\geodatabase\feedlots.gdb\Address_points', "houses_lyr")
arcpy.MakeFeatureLayer_management(r'M:\geodatabase\feedlots.gdb\Feedlot_test', "feedlots_lyr")
lines = r'M:\geodatabase\feedlots.gdb\linearDistance'
workspace = r'M:\geodatabase\feedlots.gdb'

yr = raw_input("Sales Year: " )

for row in arcpy.da.SearchCursor("feedlots_lyr", ["SHAPE@X", "SHAPE@Y", "OBJECTID", "Permit_Num", "YrFirstPermit", "AU_State"]):
    if row[4] <= int(yr):
        select_feedlot = arcpy.SelectLayerByAttribute_management("feedlots_lyr", "NEW_SELECTION", "OBJECTID = {}".format(row[2]))
        select_houses = arcpy.SelectLayerByLocation_management("houses_lyr", "WITHIN_A_DISTANCE", select_feedlot, "2640 FEET", "NEW_SELECTION")
        for rows in arcpy.da.SearchCursor(select_houses, ["SHAPE@X", "SHAPE@Y"]):
            array = arcpy.Array([arcpy.Point(row[0], row[1]), arcpy.Point(rows[0], rows[1])])
            polyline = [arcpy.Polyline(array), row[3], row[5]]
            with arcpy.da.InsertCursor(lines, ["SHAPE@", "Grouping", "ANIMAL"]) as cur:
                cur.insertRow(polyline)
            array.removeAll()

if "LengthFt" not in [field.name for field in arcpy.ListFields(lines)]:
    arcpy.AddField_management(lines, "LengthFt", "DOUBLE")
    arcpy.CalculateField_management(lines, "LengthFt", "round(!SHAPE.LENGTH@FEET!, 0)", "PYTHON_9.3")
else:
    arcpy.CalculateField_management(lines, "LengthFt", "round(!SHAPE.LENGTH@FEET!, 0)", "PYTHON_9.3")


elapsedTime = time.time() - startTime
m ,s = divmod(elapsedTime, 60)
print "\nCompleted %02d minutes %02d seconds \n" % (m,s)