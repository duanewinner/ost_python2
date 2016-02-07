#!/usr/local/bin/python3

import glob
import os
import zipfile



def zipdir_depth1(src, dst):
        zip_object = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
        os.chdir(src)
        for item in glob.glob("*"):
            if os.path.isfile(item):
                zip_object.write(item, os.path.relpath(item, os.path.dirname(src)))
        zip_object.close()
        
    
    