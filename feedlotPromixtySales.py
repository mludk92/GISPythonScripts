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

address = r'N:\landrec\Jonathan Graves\GIS\RatioStudy2023\ay2023.gdb\BEC_Central_SDE_ADDRESSPOINTS'
feedlots = r'N:\landrec\Jonathan Graves\GIS\RatioStudy2023\ay2023.gdb\BEC_Central_SDE_Feedlot'

workspace = r'N:\landrec\Jonathan Graves\GIS\RatioStudy2023\ay2023.gdb'
sf = arcpy.Describe(feedlots).spatialReference

yr = "2021" #raw_input("Sales Year: " )
fc_line = raw_input("Line Layer Name: " )
fc_selectAddress =raw_input("Address Layer Name: " )

startTime = time.time()

fields_add = [      ["City", "TEXT"],
                    ["Zipcode", "TEXT"],
                    ["Township", "TEXT"],
                    ["Address", "TEXT"],
                    ["Place", "TEXT"],
                    ["ParcelNum", "TEXT"],
                    ["fd_close", "LONG"],
                    ["fd_count", "LONG"],
                    ["ANIMAL", "LONG"]
                ]

fields_line = [ ["Grouping", "TEXT"],
                ["ANIMAL", "LONG"],
                ["LengthFt", "LONG"]
              ]

lineDict = dict()
addDict = dict()

where_clause = '"YrFirstPer" <= ' + '%s' %yr
x = 1
y = 0
z = 0

# create target layers for lines and address points within 1/2 mile of feedlots
new_Address = arcpy.CreateFeatureclass_management(workspace, fc_selectAddress + "_" + yr,  "POINT", "", "", "", sf )
new_lines = arcpy.CreateFeatureclass_management(workspace, fc_line + "_" + yr,  "POLYLINE", "", "", "", sf )

for item in fields_add:
    arcpy.AddField_management(new_Address, fields_add[y][0], fields_add[y][1] )
    y += 1

for item in fields_line:
    arcpy.AddField_management(new_lines, fields_line[z][0], fields_line[z][1] )
    z += 1

arcpy.MakeFeatureLayer_management(address, "houses_lyr")
arcpy.MakeFeatureLayer_management(feedlots, "feedlots_lyr")

# Finds address points within 1/2 mile of feedlots points based on feedlot permit year
for row in arcpy.da.SearchCursor("feedlots_lyr", ["SHAPE@X", "SHAPE@Y", "OBJECTID", "Permit_Num", "AU_State"], where_clause):
    select_feedlot = arcpy.SelectLayerByAttribute_management("feedlots_lyr", "NEW_SELECTION", "OBJECTID = {}".format(row[2]))
    select_houses = arcpy.SelectLayerByLocation_management("houses_lyr", "WITHIN_A_DISTANCE", select_feedlot, "2640 FEET", "NEW_SELECTION")

    for adds in arcpy.da.SearchCursor(select_houses, ["SHAPE@X", "SHAPE@Y", "POSTCOMM", "ZIP", "CTU_NAME", "ADDRESS", "PLACE_DESC"]):
        # adds x,y coordinates for feedlot and for address points with feedlot permit number and animal units to dictionary
        lineDict.update({x : ( row[0], row[1], adds[0], adds[1],row[3], row[4])})
        addDict.update({x : (adds[0], adds[1], adds[2], adds[3], adds[4], adds[5], adds[6])})
        x += 1

with arcpy.da.InsertCursor(new_lines, ["SHAPE@", "Grouping", "ANIMAL"]) as cur:
    for line in lineDict:
        array = arcpy.Array([arcpy.Point(lineDict[line][0], lineDict[line][1]), arcpy.Point(lineDict[line][2], lineDict[line][3])])
        polyline = [arcpy.Polyline(array), lineDict[line][4], lineDict[line][5]]
        cur.insertRow(polyline)
        array.removeAll()
    del cur

with arcpy.da.UpdateCursor(new_lines, ["SHAPE@", "LengthFt"]) as cur:
    for row in cur:
        length = round(row[0].getLength('PLANAR', 'FEET'), 0)
        row[1] = int(length)
        cur.updateRow(row)
    del cur

with arcpy.da.InsertCursor(new_Address, ["SHAPE@", "City", "Zipcode", "Township", "Address", "Place"]) as cur:
    for point in addDict:
        new_point = [arcpy.Point(addDict[point][0], addDict[point][1]), addDict[point][2], addDict[point][3], addDict[point][4], addDict[point][5], addDict[point][6]]
        cur.insertRow(new_point)
    del cur

elapsedTime = time.time() - startTime
m ,s = divmod(elapsedTime, 60)
print "\nCompleted %02d minutes %02d seconds \n" % (m,s)
