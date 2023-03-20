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
import os
import time

arcpy.env.overwriteOutput = True

address = r'N:\landrec\Ag Sales Data\Feedlot Proximity\2018 LBAE Feedlot Proximity Review\feedlot_Proximty.gdb\Address1000_2017'
sales = r'N:\landrec\Ag Sales Data\Feedlot Proximity\2018 LBAE Feedlot Proximity Review\feedlot_Proximty.gdb\sales'
ratio = r'N:\landrec\Ag Sales Data\Feedlot Proximity\2018 LBAE Feedlot Proximity Review\feedlot_Proximty.gdb\cama_ratio'

yr = "2018" #raw_input("Sales Year: ")
name = "sales_" + str(yr)

startTime = time.time()
ratio_Dict = {}

for row in arcpy.da.SearchCursor(ratio, ["DOV_or_CRV", "Ratio"]):
    ratio_Dict.update({row[0] : row[1]})

print "Step 1"
for row in arcpy.da.SearchCursor(address, ["ParcelNum", "fd_close", "fd_count", "ANIMAL"]):
    print row[0]
    with arcpy.da.UpdateCursor(sales, ["GISNumber", "close_feedlot", "feedlot_count", "ANIMAL", "eCRV__", "Ratio"]) as cur:
        for rows in cur:
            if rows[0] == row[0]:
                rows[1] = row[1]
                rows[2] = row[2]
                rows[3] = row[3]
                cur.updateRow(rows)

poop = row[0].replace(".", "")

print "Step 2"
new_tbl = arcpy.Copy_management(sales, os.path.join(os.path.dirname(sales), name))

with arcpy.da.UpdateCursor(new_tbl, ["Land_Bldg_Indicator"]) as cur:
    for rows in cur:
        if rows[0] != "Land and Buildings":
            cur.deleteRow()

with arcpy.da.UpdateCursor(new_tbl, ["Sale_Month", "Sale_Year"]) as cur:
    for rows in cur:
        if rows[0] < 10 and rows[1] < 2016:
            cur.deleteRow()

print "Step 3"
with arcpy.da.UpdateCursor(new_tbl, ["eCRV__", "Ratio", "Sale_Month", "Sale_Year"]) as cur:
    for rows in cur:
        if str(rows[0]) in ratio_Dict.keys():
            rows[1] = ratio_Dict[str(rows[0])]
            cur.updateRow(rows)

print "Step 4"
with arcpy.da.UpdateCursor(sales, ["close_feedlot", "feedlot_count", "ANIMAL", "Ratio" ]) as cur:
    for rows in cur:
        rows[0] = None
        rows[1] = None
        rows[2] = None
        rows[3] = None
        cur.updateRow(rows)

print "Step 5"
with arcpy.da.UpdateCursor(new_tbl, ["feedlot_count"]) as cur:
    for rows in cur:
        if rows[0] is None:
            cur.deleteRow()

elapsedTime = time.time() - startTime
m ,s = divmod(elapsedTime, 60)
print "\nCompleted %02d minutes %02d seconds \n" % (m,s)