#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jgraves
#
# Created:     19/09/2018
# Copyright:   (c) jgraves 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

##Database Connections\becgis3.parcels.prod.becnt.sara.sde\Parcels.SDE.Farms
##Database Connections\becgis3.parcels.prod.becnt.sara.sde\Parcels.SDE.Cadastral
##Database Connections\becgis3.parcels.prod.becnt.sara.sde\Parcels.SDE.Farms
##
##Database Connections\becgis3.becnt.sara.BEC_Central.sde
##Database Connections\becgis3.becnt.sara.BEC_Central.sde\BEC_Central.TSSDE.editing
##Database Connections\becgis3.becnt.sara.BEC_Central.sde\BEC_Central.TSSDE.Farms

import os
import arcpy

mxd = arcpy.mapping.MapDocument(r'G:\prj\mn\blue earth\mxd\Maintenance10 - test.mxd') #('CURRENT')
df = arcpy.mapping.ListDataFrames(mxd)

s = 'becgis3.parcels.prod.becnt.sara.sde\Parcels.SDE.Cadastral'
t = 'becgis3.becnt.sara.BEC_Central.sde\BEC_Central.TSSDE.editing'

u = 'becgis3.parcels.prod.becnt.sara.sde\Parcels.SDE.Farms'
v = 'becgis3.becnt.sara.BEC_Central.sde\BEC_Central.TSSDE.Farms'

w = 'becgis3.parcels.prod.becnt.sara.sde'
x = 'becgis3.becnt.sara.BEC_Central.sde'

for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.supports("DATASOURCE"):
        if s in lyr.dataSource:
            #print os.path.dirname(lyr.dataSource)
            lyr.replaceDataSource(r'C:\Users\sara\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\becgis3.becnt.sara.BEC_Central.sde', 'SDE_WORKSPACE', 'BEC_Central.TSSDE.editing', '')
            mxd.save()
            print lyr.name





