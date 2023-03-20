#-------------------------------------------------------------------------------
# Name:        ReportLab Owner Index Gen
# Purpose:     Generate owner index for county plat book
#
# Author:      NFlatgard
#
# Created:     30/08/2017
# Copyright:   (c) NFlatgard 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, arcpy, reportlab, time
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Frame , PageTemplate, BaseDocTemplate
from reportlab.lib.units import inch
from reportlab.lib.colors import black, white, gray, maroon

startTime = time.time()

# Setting doc parameters, size, Platypus Doc Template and Frames
    # Frame 1: NW_Cor = 0.4375* inch, 10.5* inch
    #          NE_Cor = 2.875* inch, 10.5* inch
    #          SW_Cor = 0.4375* inch, 0.62* inch
    #          SE_Cor = 2.875* inch, 0.62* inch
    # Frame 2: NW_Cor = 3.125* inch, 10.5* inch
    #          NE_COR = 5.4375* inch, 10.5* inch
    #          SW_Cor = 3.125* inch, 0.62* inch
    #          SE_Cor = 5.4375* inch, 0.62* inch
    # Frame 3: NW_Cor = 5.6875* inch, 10.5* inch
    #          NE_Cor = 8.125* inch, 10.5* inch
    #          SW_Cor = 5.6875* inch, 0.62* inch
    #          SE_Cor = 8.125* inch, 0.62* inch

pdfreport = "Poop.pdf"
canvas = Canvas(pdfreport, pagesize = letter)
doc = BaseDocTemplate(pdfreport, pagesize = letter)
frame1 = Frame(0.4375* inch, 0.62* inch, height = 9.88*inch, width = 2.4375* inch, id='col1')
frame2 = Frame(3.0625* inch, 0.62* inch, height = 9.88*inch, width = 2.4375* inch, id='col2')
frame3 = Frame(5.6875* inch, 0.62* inch, height = 9.88*inch, width = 2.4375* inch, id='col3')
doc.addPageTemplates([PageTemplate(id='threeCol',frames=[frame1,frame2, frame3 ] )])

# container for the "Flowable" objects
elements = []

# Make heading for each column and start data list
column1Heading = "Name"
column2Heading = "Sec"
column3Heading = "Initials"
column4Heading = "LC"
column5Heading = "Pg #"

# Assemble data for each column
data = [[column1Heading, column2Heading, column3Heading, column4Heading, column5Heading ]]
fc = outFeature = "SteeleData.gdb/polygons/PB_Parcels"
whereClause = """(SHAPE_Area <= 2744280 AND SHAPE_Area > 43560)"""
table = arcpy.MakeTableView_management(fc, "fcview", whereClause)
fields = ["SteeleMNTaxData_dbo_tblParcelJoin_OWNAME", "FIRST_SteeleMNTaxData_dbo_tblParcelJoin_APSECT", "FIRST_ShortLabel", "FIRST_LetterCode", "FIRST_Page" ]
with arcpy.da.SearchCursor(table, fields)as cursor:
    for row in cursor:
         data.append([row [0], row[1], row[2], row[3], row[4]])

# Set Table and Tabel Style Parameters
ownerIndex = Table(data, [1.34375 * inch, 0.1875 * inch, 0.34375* inch, 0.21875 * inch, 0.28125 * inch], rowHeights=0.125*inch, repeatRows=1)
tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1), black),
                       ('ALIGN', (1,1), (-1,-1), 'CENTER'),
                       ('FONT', (0,0), (-1,-1),'Times-Roman', 5),
                       ('VALIGN',(0,0),(-1,-1),'TOP'),
                       ('LINEBELOW',(0,0),(-1,-1),0.4, gray),
                       ('BOX',(0,0),(0,-1),.5, gray),
                       ('BOX',(1,0),(1,-1),.5, gray),
                       ('BOX',(2,0),(2,-1),.5, gray),
                       ('BOX',(3,0),(3,-1),.5, gray),
                       ('BOX',(4,0),(4,-1),.5, gray),
                       ('BOX',(5,0),(5,-1),.5, gray)])
tblStyle.add('BACKGROUND',(0,0),(-1,0), maroon)
tblStyle.add('BACKGROUND',(0,1),(-1,-1), white)
tblStyle.add('TEXTCOLOR',(0,0),(-1,-0), white)
tblStyle.add('ALIGN', (0,0), (-1, 0), 'CENTER')
ownerIndex.setStyle(tblStyle)

# Append the Flowable objects and generate PDF
elements.append(ownerIndex)
doc.build(elements)

# Print Completion Time
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
print "\n   |..|    YOU JUST KILLED IT WITH PYTHON IN: %02d minutes %02d seconds \n" % (m,s)