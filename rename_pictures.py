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

import PIL, os
from PIL import Image

path = r'\\BECFP2\depts\landrec\Jonathan Graves\Pictures\Apr 26'


def get_date_taken(path):

    c = 1
    files = os.listdir(path)

    for f in files:

        if ".db" not in f:
            name = str(Image.open(os.path.join(path, f))._getexif()[36867])[0:10].replace(":", "") + "_" + str(c).zfill(3) + ".JPG"
            os.rename(os.path.join(path, f), os.path.join(path, name))
            c += 1

get_date_taken(path)