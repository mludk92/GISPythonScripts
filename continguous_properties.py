#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      jgraves
#
# Created:     28/08/2017
# Copyright:   (c) jgraves 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import time

startTime = time.time()

arcpy.env.overwriteOutput = True

fn = r'M:\geodatabase\appraisers.gdb\contiguous_deedholder_viking'
arcpy.MakeFeatureLayer_management(fn,"parcel_lyr")

dis = arcpy.Dissolve_management("parcel_lyr", "in_memory/parcel_dissolve", ["Deedholder"], [["PIN", "COUNT"]], "SINGLE_PART")

arcpy.MakeFeatureLayer_management(dis,"dissolve_lyr")
sel = arcpy.Select_analysis("dissolve_lyr", r"in_memory/con_parcels", '"COUNT_PIN" > 1')

poop = arcpy.MakeFeatureLayer_management(sel,"select_parcels")

fields = arcpy.ListFields(dis)
for field in fields:
    print field.name

with arcpy.da.SearchCursor(poop, ["COUNT_PIN", "OBJECTID_1"]) as cursor:
    for row in cursor:
        arcpy.SelectLayerByAttribute_management(poop, "NEW_SELECTION", "OBJECTID_1 = {}".format(row[1]))
        arcpy.SelectLayerByLocation_management("parcel_lyr", "HAVE_THEIR_CENTER_IN", poop, "", "NEW_SELECTION")
        pCount = int(arcpy.GetCount_management("parcel_lyr").getOutput(0))
        if pCount > 1:
            with arcpy.da.UpdateCursor("parcel_lyr", ["PIN", "COWNFLAG"]) as cur:
                for row in cur:
                    row[1] = "YES"
                    cur.updateRow(row)

arcpy.Delete_management("in_memory")

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
print "\nCompleted %02d minutes %02d seconds \n" % (m,s)
