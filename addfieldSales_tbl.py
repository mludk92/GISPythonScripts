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

sales_tbl = r'N:\landrec\Jonathan Graves\GIS\RatioStudy2023\ay2023.gdb\SalesListing'

arcpy.AddField_management(sales_tbl, "GISNumber", "TEXT")
arcpy.AddField_management(sales_tbl, "close_feedlot", "LONG")
arcpy.AddField_management(sales_tbl, "feedlot_count", "LONG")
arcpy.AddField_management(sales_tbl, "ANIMAL", "TEXT")
arcpy.AddField_management(sales_tbl, "Ratio", "DOUBLE")


arcpy.CalculateField_management(sales_tbl, "GISNumber", '!Primary_Parcel_ID!.replace(".", "") ', "PYTHON_9.3")

elapsedTime = time.time() - startTime
m ,s = divmod(elapsedTime, 60)
print "\nCompleted %02d minutes %02d seconds \n" % (m,s)
