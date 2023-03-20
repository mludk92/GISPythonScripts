#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jgraves
#
# Created:     24/04/2017
# Copyright:   (c) jgraves 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#import Tkinter
import xlrd


file = r'C:\Users\jgraves\Downloads\test.xlsx'

workbook = xlrd.open_workbook(file)

sheet = workbook.sheet_by_index(0)

x = []

for cell in sheet.col_values(0):
    if cell != 'ParcelId':
        x.append(cell)


for item in x:
    p = "."
    x1 = item[0:3]
    x2 = item[3:5]
    x3 = item[5:7]
    x4 = item[7:10]
    x5 = item[10:13]
    #output =  "'" + x1+ p  + x2 + p + x3 + p + x4 + p + x5 + "',"
    output = "'" + item.replace(".", "") + "',"

    print output,




