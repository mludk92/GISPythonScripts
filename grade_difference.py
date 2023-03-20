#------------------------------------------------------------------------------
# Name: Grade Difference
#
# Author: Jonathan Graves
#
# Created: 6/22/2017
# Updated: 9/1/2017
# Notes:
#------------------------------------------------------------------------------


import arcpy

def addtnCheck(s, yr):

    addtnSqFt = 0

    addtnTable = r'N:\landrec\Jonathan Graves\GIS\Quintile2020.gdb\Check2s'
    fields = ["GIS_Number", "Addtn_Year_Built", "Addtn_Square_Ft"]

    with arcpy.da.SearchCursor(addtnTable, fields) as cursor:
        for row in cursor:
            if row[0] == s:
                if row[1] > (yr + 10):
                    addtnSqFt += row[2]
    return addtnSqFt

def gradeCheck (style, tla):

    if style in ('1 Story Brick', '1 Story Frame', 'Split Foyer Frame', 'Split Level Frame'):
        if tla < 1050:
            return "4"
        if 1050 <= tla <= 1150:
            return "4+5"
        if 1151 <= tla <= 1250:
            return "4+10"
        if 1251 <= tla <= 1350:
            return "3-10"
        if 1351 <= tla <= 1450:
            return "3-5"
        if 1451 <= tla <= 1650:
            return "3"
        if 1651 <= tla <= 1850:
            return "3+5"
        if 1851 <= tla <= 2150:
            return "3+10"
        if 2151 <= tla <= 2350:
            return "2-10"
        if 2351 <= tla <= 2550:
            return "2-5"
        if 2551 <= tla <= 2750:
            return "2"

    if style in ('2 Story Frame', '2 Story Brick'):
        if tla < 1250:
            return "4"
        if 1250 <= tla <= 1350:
            return "4+5"
        if 1351 <= tla <= 1550:
            return "4+10"
        if 1551 <= tla <= 1650:
            return "3-10"
        if 1651 <= tla <= 1750:
            return "3-5"
        if 1751 <= tla <= 1950:
            return "3"
        if 1951 <= tla <= 2150:
            return "3+5"
        if 2151 <= tla <= 2450:
            return "3+10"
        if 2451 <= tla <= 2650:
            return "2-10"
        if 2651 <= tla <= 2850:
            return "2-5"
        if 2851 <= tla <= 3000:
            return "2"
        if tla > 3000:
            return "Custom"
    else:
        return "N/A"

def gradeDiff(corGrade, sugGrade):

    u = {   "6-10"  :   1,
            "6-5"   :   2,
            "6"     :   3,
            "6+5"   :   4,
            "6+10"  :   5,
            "5-10"  :   6,
            "5-5"   :   7,
            "5"     :   8,
            "5+5"   :   9,
            "5+10"  :   10,
            "4-10"  :   11,
            "4-5"   :   12,
            "4"     :   13,
            "4+5"   :   14,
            "4+10"  :   15,
            "3-10"  :   16,
            "3-5"   :   17,
            "3"     :   18,
            "3+5"   :   19,
            "3+10"  :   20,
            "2-10"  :   21,
            "2-5"   :   22,
            "2"     :   23,
            "2+5"   :   24,
            "2+10"  :   25,
            "1-10"  :   26,
            "1-5"   :   27,
            "1"     :   28,
            "1+5"   :   29,
            "1+10"  :   30,
            }

    if corGrade not in (None, "N/A", "Custom"):
        x = u.get(sugGrade) - u.get(corGrade)
        return x
    if corGrade =="Custom":
        return -98
    else:
        return -99

def main():

    gradeTable = r"N:\landrec\Jonathan Graves\GIS\Quintile2020.gdb\Check2s"
    gradeFields = ["GIS_Number", "Main_Style_Desc", "Total_Living_Area", "Main_Year_Built", "CORGRADE", "gradediff", "GradeDescription", "effTLA"]

    with arcpy.da.UpdateCursor(gradeTable, gradeFields) as upd_cur:
        for upd_row in upd_cur:
            if upd_row[3] >= 1970:

                if upd_row[1] in ('1 Story Brick', '1 Story Frame', 'Split Foyer Frame', 'Split Level Frame', '2 Story Frame', '2 Story Brick'):
                    s = addtnCheck(upd_row[0], upd_row[3])
                    if s > 0:
                        gradeArea = upd_row[2] - int(s)
                        print upd_row[0] + " : " + str(upd_row[2]) + " - " + str(gradeArea)
                    else: gradeArea = upd_row[2]

                    suggestedGrade = gradeCheck(upd_row[1], gradeArea)
                    gradeDifference = gradeDiff(suggestedGrade, upd_row[6])
                    upd_row[4] = suggestedGrade
                    upd_row[5] = gradeDifference
                    upd_row[7] = gradeArea
                    upd_cur.updateRow(upd_row)

            else:
                upd_row[4] = "N/A"
                upd_row[5] = -99
                upd_cur.updateRow(upd_row)

main()







