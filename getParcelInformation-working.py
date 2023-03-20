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

arcpy.env.overwriteOutput = True

startTime = time.time()

address = r'N:\landrec\Ag Sales Data\Feedlot Proximity\2018 LBAE Feedlot Proximity Review\feedlot_Proximty.gdb\Address2640_2017'
parcels = r'N:\landrec\Ag Sales Data\Feedlot Proximity\2018 LBAE Feedlot Proximity Review\feedlot_Proximty.gdb\Parcels'


arcpy.MakeFeatureLayer_management(address, "houses_lyr")
arcpy.MakeFeatureLayer_management(parcels, "parcels_lyr")

parcel_Dict = {}

for row in arcpy.da.SearchCursor("houses_lyr", ["OBJECTID"]):
    select_address = arcpy.SelectLayerByAttribute_management("houses_lyr", "NEW_SELECTION", "OBJECTID = {}".format(row[0]))
    select_parcels = arcpy.SelectLayerByLocation_management("parcels_lyr", "INTERSECT", select_address, "", "NEW_SELECTION")
    for rows in arcpy.da.SearchCursor(select_parcels, ["PIN"]):
        parcel_Dict.update({row[0] : rows[0]})

arcpy.SelectLayerByAttribute_management("houses_lyr", "CLEAR_SELECTION")

with arcpy.da.UpdateCursor("houses_lyr", ["OBJECTID", "ParcelNum" ]) as cur:
    for rows in cur:
        if rows[0] in parcel_Dict.keys():
            rows[1] = parcel_Dict[rows[0]]
            cur.updateRow(rows)


elapsedTime = time.time() - startTime
m ,s = divmod(elapsedTime, 60)
print "\nCompleted %02d minutes %02d seconds \n" % (m,s)