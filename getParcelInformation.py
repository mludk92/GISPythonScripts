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

arcpy.env.overwriteOutput = True

address = r'N:\landrec\Jonathan Graves\GIS\RatioStudy2023\ay2023.gdb\FeedlotAddress_2021'
sales = r'N:\landrec\Jonathan Graves\GIS\RatioStudy2023\ay2023.gdb\SalesListing'

yr = raw_input("Sales Year: ")
name = "sales_" + str(yr)

for row in arcpy.da.SearchCursor(address, ["ParcelNum", "fd_close", "fd_count", "ANIMAL"]):
    with arcpy.da.UpdateCursor(sales, ["GISNumber", "close_feedlot", "feedlot_count", "ANIMAL"]) as cur:
        for rows in cur:
            if rows[0] == row[0]:
                rows[1] = row[1]
                rows[2] = row[2]
                rows[3] = row[3]
                cur.updateRow(rows)

new_tbl = arcpy.Copy_management(sales, os.path.join(os.path.dirname(sales), name))

with arcpy.da.UpdateCursor(sales, ["close_feedlot", "feedlot_count", "ANIMAL"]) as cur:
    for rows in cur:
            rows[0] = None
            rows[1] = None
            rows[2] = None
            cur.updateRow(rows)

with arcpy.da.UpdateCursor(new_tbl, ["feedlot_count"]) as cur:
    for rows in cur:
        if rows[0] is None:
            cur.deleteRow()
