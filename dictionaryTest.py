#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jgraves
#
# Created:     17/04/2018
# Copyright:   (c) jgraves 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import os
import time

startTime = time.time()
arcpy.env.overwriteOutput = True


def dorDate(d):
    month_dict = {  'JAN' : '1',
                    'FEB' : '2',
                    'MAR' : '3',
                    'APR' : '4',
                    'MAY' : '5',
                    'JUN' : '6',
                    'JUL' : '7',
                    'AUG' : '8',
                    'SEP' : '9',
                    'OCT' : '10',
                    'NOV' : '11',
                    'DEC' : '12'
                    }

    day = d[0:2]
    month = d[2:5]
    year = d[-4:]

    if day[0] == '0':
        day = day[1]

    if month in month_dict:
        month = month_dict.get(month)

    return day + "/" + month + "/" + year

def salesTable(tblDORSales, tblCamaSales, tblCamaDeedholder):

    salesDict = dict()


    tblDORSales_fields =  [     'Primary_Parcel_ID',
                                'Gross_Sale_Price',
                                'Sale_Date'
                                ]

    tblCamaSales_fields =   [   'GIS_Number',
                                'Sale_Date',
                                'Ratio',
                                'Total_Value'
                                ]

    tblCamaDeedholder_fields = [    'GIS_Number',
                                    'Deedholder'
                                    ]

    for row in arcpy.da.SearchCursor(tblCamaSales, tblCamaSales_fields):
        if row[0][0] in ('r', 'R'):
            ratio = round(float(row[2]),2)
            salesDict.update( { (row[0], row[1]) : [round(float(row[2]),2), row[3] ] } )

    key = salesDict.keys()
    test = '7/21/2017'

    if any(k[1] == test for k in key):



##        if row[0] in salesDict:
##            key = row[0]
##            #print salesDict[key]
##            salesDict.setdefault(key, {}).append([round(row[1],2)])
##            salesDict.setdefault(key, {}).append(row[2])
##
##    for row in arcpy.da.SearchCursor(tblDORSales, tblDORSales_fields):
##        dor_date = dorDate(row[2])
##        poop = row[0].replace(".", "")
##        key = (poop, dor_date)
##        salesDict(key).append(row[1])
##
##    for row in arcpy.da.SearchCursor(tblCamaDeedholder, tblCamaDeedholder_fields):
##        key = salesDict.keys()
##        if row[0] in salesDict:
##            key = row[0]
##            salesDict.setdefault(key, {}).append(row[1])

    return salesDict


if __name__ == '__main__':

    dor_sales = r'N:\landrec\Ag Sales Data\Feedlot Proximity\2018 LBAE Feedlot Proximity Review\feedlot_Proximty.gdb\sales'
    cama_sales = r'N:\landrec\Ag Sales Data\Feedlot Proximity\2018 LBAE Feedlot Proximity Review\feedlot_Proximty.gdb\cama_ratio'
    cama_deedholder = r'N:\landrec\Ag Sales Data\Feedlot Proximity\2018 LBAE Feedlot Proximity Review\feedlot_Proximty.gdb\deedholders'

    poop = salesTable( dor_sales, cama_sales, cama_deedholder)

##    for item in poop:
##        print item, poop[item]

    elapsedTime = time.time() - startTime
    m ,s = divmod(elapsedTime, 60)
    print "\nCompleted %02d minutes %02d seconds \n" % (m,s)

