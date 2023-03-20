#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jgraves
#
# Created:     01/09/2017
# Copyright:   (c) jgraves 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import os.path
import xlrd

def address(files, ext):

    d = {   'Avenue'    :   'Ave',
            'Boulevard' :   "Blvd",
            'Circle'    :   "Cir",
            'Court'     :   'Ct',
            'Drive'     :   'Dr',
            'Lane'      :   'ln',
            'Place'     :   'Pl',
            'Street'    :   'St',
            'Trail'     :   'Trl',
            'Road'      :   'Rd'}

    r = files.split(" ", 1)[0]
    s = files.split(" ", 1)[-1]
    s2 = files.split(" ")[-1]

    if s2.capitalize() in d:
        print s
        s = s.rsplit(' ', 1)[0] + ' ' + d.get(s2)
    else:
        s = files.split(" ", 1)[-1]

    if ''.join(n for n in r if n not in "1234567890"):
        return False
    else:
        return r, s, ext

def neighborhood(street, house):

    file = r"N:\landrec\BLUEPRINTS - PERMITS\BLUE PRINTS - BEC\Mankato - BluePrints\!--ROAD_INDEX--!.xls"
    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheet_by_index(0)

    d = "zUNK"
    for r in xrange(sheet.nrows):
        row = sheet.row(r)
        if row[0].value == street:
            if int(house) >= int(row[1].value) and int(house) <= int(row[2].value):
                d = row[3].value
            else:
                d = "zUNK"
    return d

def renamePermit(neigh, street, house, path, files, ext):

    if neigh == "":
        neigh = "zUNK"

    neighborhood = [ "DOLPH", "DOWNTOWN", "E VICTORY", "HILLTOP", "LINCOLN", "MOUND", "N END", "N HWY", "N MADISON", "NW SAKATA", "PRAIRIE", "SE VILLAGE", "TINKOMS", "VIKING", "WEST", "zUNK"]

    name = str(neigh) + " - " + str(street) + " " + str(house) + str(ext)


    if os.path.isfile(os.path.join(path,name)) == True:
        name = str(neigh) + " - " + str(street) + " " + str(house) + "-COPY" + str(ext)
    os.rename(os.path.join(path, files), os.path.join(path, name))

def main():

    path = r"N:\landrec\BLUEPRINTS - PERMITS\BLUE PRINTS - BEC\Mankato - BluePrints"
    files = os.listdir(path)
    c = 0
    n = 0


    for f in files:
        filename, file_extension = os.path.splitext(f)
        if file_extension in ['.pdf', '.msg']:
            permit = address(filename, file_extension)
            if permit != False:
                newName = neighborhood(permit[1], permit[0])
                renamePermit(newName, permit[1], permit[0], path, f, file_extension)
        else:
            pass

main()
