#-------------------------------------------------------------------------------
# Name:        Solar Farms Sales Analysis based on 1/2 mile proximity
#
# Author:      Jonathan Graves
#
# Created:     2/15/2019
# Copyright:   (c) jgraves 2019
# Licence:     Uselo bajo su propio riesgo
#-------------------------------------------------------------------------------

import xlrd
import re
import arcpy
import time
import pandas as pd

startTime = time.time()

#-------------------------------------------------------------------------------
# Uses DOR Sales Listing excel spreadsheet to extract parcel ida, emv, sale price and sales ratio

def sales_listing(file_location):

    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_name("Sales Listing")

    sales_dict = dict()

    for row in range(1, sheet.nrows):
        parcelID = str(sheet.cell(row, 2).value).replace('.','')
        sales_dict.update({parcelID :  [int(sheet.cell(row, 7).value), int(sheet.cell(row, 19).value), float(sheet.cell(row, 20).value)]})

    return sales_dict

#-------------------------------------------------------------------------------
# Searches through excel file that has the Solar Farm parcel Id, MW, and permit information

def solar_plants(solar_location):

    workbook = xlrd.open_workbook(solar_location)
    sheet = workbook.sheet_by_name("Sheet1")

    solar_dict = dict()
    x = 0

    for row in range(2, sheet.nrows):
        parcelID = str(sheet.cell(row, 9).value).replace('.','')
        mw = str(sheet.cell(row, 7).value)
        permit = str(sheet.cell(row, 0).value)

        if mw == "Unk.":
            mw = 999

        if 'KW' in str(mw) or 'kw' in str(mw):
            mw = re.sub('[ KWkw]', '', mw)
            mw = str(float(mw) / 1000)

        mw = re.sub('[ MW]', '', str(mw))

        if mw == '':
            mw = 999

        if parcelID in solar_dict:
            mw = float(mw) + float(solar_dict.get(parcelID)[0])

        solar_dict.update({parcelID :  [(mw), (permit)]})

    return solar_dict

#-------------------------------------------------------------------------------
# To be developed later to find sales that are within 1/2 mile of multiple solar farms

##def sales_check(sale, sale_dict):
##
##    print sale
##    for item in sale_dict.values():
##        if item == sale:
##            saleID = sale_dict[item]
##            print saleID

#-------------------------------------------------------------------------------
# Does the geographic work of identifing all sales withn 1/2 mile and creating a diction to be passed to the csv output function

def mapping(s, t, u, r):

    solar_site = dict()
    sale_site = dict()

    parcel_site =[]

    spatial_ref = arcpy.Describe(u).spatialReference

    for row in arcpy.da.SearchCursor(u, ['CountyPIN','SHAPE@X', 'SHAPE@Y']):
        if row[0] in t:
            solar_site.update({row[0] : (row[1], row[2])})


    for row in arcpy.da.SearchCursor(r, ['PIN','SHAPE@X', 'SHAPE@Y']):
        if row[0] not in solar_site and row[0] in t:
            solar_site.update({row[0] : (row[1], row[2])})

    fc_solar = arcpy.CreateFeatureclass_management('in_memory', 'SolarPoint', 'POINT', '', '', '', spatial_ref)
    arcpy.AddField_management(fc_solar, 'PIN', 'TEXT')

    with arcpy.da.InsertCursor(fc_solar, ['SHAPE@', 'PIN']) as cur:
        for k, v in solar_site.iteritems():
            solar_point = [v[0], v[1]]
            cur.insertRow([solar_point, k])

    solarPoint_lyr = arcpy.MakeFeatureLayer_management(fc_solar, 'solar_lyr')
    address_lyr = arcpy.MakeFeatureLayer_management(u, 'Address_lyr')
    x = 0
    for row in arcpy.da.SearchCursor(solarPoint_lyr, ['PIN']):
        select_feedlot = arcpy.SelectLayerByAttribute_management(solarPoint_lyr, "NEW_SELECTION", "PIN = '{}'".format(row[0]))
        sales = arcpy.SelectLayerByLocation_management(address_lyr, 'WITHIN_A_DISTANCE', solarPoint_lyr, '2640 FEET', 'NEW_SELECTION')
        for sale in arcpy.da.SearchCursor(sales, ['CountyPIN']):
            if sale[0] in s:
                x += 1
                y = 1
                #sales_check(sale[0], sale_site)
                saleParcel = sale[0]
                solarParcel = row[0]
                solarPerm = t.get(row[0])[1]
                emv2018 = s.get(sale[0])[0]
                adjsale = s.get(sale[0])[1]
                megawatt = t.get(row[0])[0]
                ratio = s.get(sale[0])[2]
                count = y

                sale_site.update({x : [saleParcel, solarParcel, solarPerm, emv2018, adjsale, megawatt, ratio, count]})

    arcpy.Delete_management('in_memory')

    return sale_site

#-------------------------------------------------------------------------------
# Creates CSV file from dictionary created by the def mapping.

def csvOutput(v):
    try:
        df = pd.DataFrame.from_dict(v, orient='index')
        df.to_csv(r'N:\landrec\Jonathan Graves\GIS\RatioStudy2023\text.csv', index_col=0, header=['Parcel ID', 'Solar Farm', 'Permit No', 'EMV 2022', 'Adj Sale 2023', 'MW', 'Ratio', '# of Solar Farms within .5 Miles'])

    except:
        print 'No es bueno escribir en el archivo csv'

#-------------------------------------------------------------------------------

# variables
s = sales_listing(r'N:\landrec\Jonathan Graves\GIS\RatioStudy2023\DOR-CO7-PRELFIN-2022-Sales Listing-20JAN2023.xlsx')  # DOR Sales Listing Spreadsheet
t = solar_plants(r'N:\landrec\Jonathan Graves\GIS\RatioStudy2023\BEC Solar Site12-6-2021 update.xlsx')  # Solar Site Spreadsheet
u = r'N:\landrec\Jonathan Graves\GIS\RatioStudy2023\ay2023.gdb\BEC_Central_SDE_ADDRESSPOINTS'  # GIS address feature class
r = r'N:\landrec\Jonathan Graves\GIS\RatioStudy2023\ay2023.gdb\TaxParcels'  # GIS parcel layer feature class

v = mapping(s, t, u, r)

csvOutput(v)

#-------------------------------------------------------------------------------

elapsedTime = time.time() - startTime
m ,s = divmod(elapsedTime, 60)
print "\nCompleted %02d minutes %02d seconds \n" % (m,s)
