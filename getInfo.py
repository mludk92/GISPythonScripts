#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jgraves
#
# Created:     29/12/2017
# Copyright:   (c) jgraves 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import time

startTime = time.time()

arcpy.MakeFeatureLayer_management(r'N:\landrec\Jonathan Graves\GIS\RatioStudy2023\ay2023.gdb\FeedlotAddress_2021', "address_lyr")
arcpy.MakeFeatureLayer_management(r'N:\landrec\Jonathan Graves\GIS\RatioStudy2023\ay2023.gdb\FeedlotLine_2021', "line_lyr")

info_Dict = {}

for point in arcpy.da.SearchCursor("address_lyr", ["OBJECTID"]):
    feedlot_dist = []
    animal_count = []
    feedlot_count = 0

    select_house = arcpy.SelectLayerByAttribute_management("address_lyr", "NEW_SELECTION", "OBJECTID = {}".format(point[0]))
    select_line = arcpy.SelectLayerByLocation_management("line_lyr", "INTERSECT", select_house, "", "NEW_SELECTION")

    for row in arcpy.da.SearchCursor(select_line, ["OBJECTID", "LengthFt", "ANIMAL"]):
        feedlot_dist.append(row[1])
        feedlot_count += 1
        animal_count.append(row[2])
    info_Dict.update({point[0] : (sorted(feedlot_dist)[0], feedlot_count, sum(animal_count) )})

arcpy.SelectLayerByAttribute_management("address_lyr", "CLEAR_SELECTION")

with arcpy.da.UpdateCursor("address_lyr", ["OBJECTID", "fd_close", "fd_count", "ANIMAL" ]) as cur:
    for rows in cur:
        if rows[0] in info_Dict.keys():
            rows[1] = info_Dict[rows[0]][0]
            rows[2] = info_Dict[rows[0]][1]
            rows[3] = info_Dict[rows[0]][2]
            cur.updateRow(rows)

elapsedTime = time.time() - startTime
m ,s = divmod(elapsedTime, 60)
print "\nCompleted %02d minutes %02d seconds \n" % (m,s)
