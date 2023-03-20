#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jgraves
#
# Created:     05/09/2017
# Copyright:   (c) jgraves 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os


path = r'N:\landrec\Jonathan Graves\Pictures\April20th'


def get_date_taken(path):

    c = 1
    files = os.listdir(path)

    for f in files:

        if ".db" not in f:
            name = os.path.basename(str(f) + ".jpg")
            os.rename(os.path.join(path, f), os.path.join(path, name))


get_date_taken(path)


def nozero(t):
   s = t.replace('0', '', 1)
   return s