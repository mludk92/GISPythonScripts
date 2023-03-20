#-------------------------------------------------------------------------------
# Name: CPI & CER Comparison
# Purpose: Compare TWP and Section trends in CER and CPI across soil types
# Author:      jgraves
# Created:     11/15/2019
# Copyright:   (c) jgraves 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import time
import os
import csv
import pandas as pd
from arcpy import env

startTime = time.time()
print "Starting Analysis\n" + str(startTime)

def getCPI(cpi, cer):

    dict_cpi = dict()
    dict_cer = dict()

    with open(cpi) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                dict_cpi.update({row[1]: row[3]})
                line_count += 1

    with open(cer) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                dict_cer.update({row[1]: row[3]})
                line_count += 1

    return dict_cpi, dict_cer

def getdata(twp, landuse, soils, cpi, cer):

    dict_all = dict()

    print "getting data"

    fields = 'UniqueID'
    lyr_twp = arcpy.MakeFeatureLayer_management(twp, "twp_lyr")
    lyr_landuse = arcpy.MakeFeatureLayer_management(landuse, "landuse_lyr")
    lyr_soils = arcpy.MakeFeatureLayer_management(soils, "soils_lyr")

    recno = 0
    for row in arcpy.da.SearchCursor(lyr_twp, fields):
        cer_list = []
        cpi_list = []

        twpName = ''.join(n for n in row[0] if n not in " ""!@#$%^&*")

        where_clause = fields + " = '" +  row[0] + "'"
        select_twp = arcpy.SelectLayerByAttribute_management(lyr_twp, "NEW_SELECTION", where_clause)
        clip_twp = arcpy.Clip_analysis(lyr_landuse, select_twp, os.path.join(r'in_memory', str(twpName)))
        clip_soils = arcpy.Clip_analysis(lyr_soils, clip_twp, os.path.join(r'in_memory', str(twpName)+ "x"))
        dissolve_soils = arcpy.Dissolve_management(clip_soils, os.path.join(r'in_memory', str(twpName) + "p"), "MUSYM")

        y = 0
        for rows in arcpy.da.SearchCursor(dissolve_soils, ["Shape@Area"]):
            x = rows[0]
            y += x
        y = round(y/43560,2)
        if y == 0:
            print row[0]

        for rows in arcpy.da.SearchCursor(dissolve_soils, ["MUSYM","Shape@Area"]):
            x = rows[1] / 43560
            z = x / y
            if rows[0] in cer:
                s = cer.get(rows[0])

            p = float(s) * float(z)

            cer_list.append(p)

        for rows in arcpy.da.SearchCursor(dissolve_soils, ["MUSYM","Shape@Area"]):
            x = rows[1] / 43560
            z = x / y
            if rows[0] in cpi:
                s = cpi.get(rows[0])
            if rows[0] == "130":
                s = cpi.get("L85A")

            p = float(s) * float(z)

            cpi_list.append(p)
        recno += 1
        dict_all.update({recno: [row[0],round(sum(cer_list), 2), round(sum(cpi_list), 2), y]})
        arcpy.Delete_management("in_memory")

    return dict_all

def csvOutput(twp):

    df = pd.DataFrame.from_dict(twp, orient='index')
    df.to_csv(r'C:\Users\jgraves\Desktop\SectionCPICER.csv', index_col=0, header=['Section', 'CER', 'CPI', "Tillable Acres"])

if __name__ == '__main__':

    arcpy.env.workspace = r'C:\Users\jgraves\Desktop\CPI\ququscript.gdb'
    arcpy.env.overwriteOutput = True

    fc_twp = r'C:\Users\jgraves\Desktop\CPI\ququscript.gdb\forties'
    fc_lu = r'C:\Users\jgraves\Desktop\CPI\ququscript.gdb\lu'
    fc_soils = r'C:\Users\jgraves\Desktop\CPI\ququscript.gdb\Soil'
    csv_cpi = r'C:\Users\jgraves\Desktop\CPI\2019CPI_ForFarms.csv'
    csv_cer = r'C:\Users\jgraves\Desktop\CPI\soilvaluetableCER.csv'

    cpi = getCPI(csv_cpi, csv_cer)

    twpData = getdata(fc_twp, fc_lu, fc_soils, cpi[0], cpi[1])

    csvOutput(twpData)

    elapsedTime = time.time() - startTime
    m ,s = divmod(elapsedTime, 60)
    print "\nCompleted %02d minutes %02d seconds \n" % (m,s)
