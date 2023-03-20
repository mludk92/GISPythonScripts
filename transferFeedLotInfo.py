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

arcpy.MakeFeatureLayer_management(r'N:\landrec\Jonathan Graves\GIS\RatioStudy2023\ay2023.gdb\FeedlotAddress_2021', "address_lyr")
arcpy.MakeFeatureLayer_management(r'N:\landrec\Jonathan Graves\GIS\RatioStudy2023\ay2023.gdb\TaxParcels', "parcel_lyr")

for point in arcpy.da.SearchCursor("address_lyr", ["OBJECTID", "ParcelNum"]):
    select_house = arcpy.SelectLayerByAttribute_management("address_lyr", "NEW_SELECTION", "OBJECTID = {}".format(point[0]))
    select_parcel = arcpy.SelectLayerByLocation_management("parcel_lyr", "INTERSECT", select_house, "", "NEW_SELECTION")
    for row in arcpy.da.SearchCursor(select_parcel, ["OBJECTID", "PIN"]):
        with arcpy.da.UpdateCursor("address_lyr", ["OBJECTID", "ParcelNum"]) as cur:
            for rows in cur:
                    rows[1] = row[1]
                    cur.updateRow(rows)
