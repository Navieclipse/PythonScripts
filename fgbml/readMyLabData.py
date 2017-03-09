# -*- coding: utf-8 -*-
import os
import re

def readlines(f , fileName, div):
    data = []
    if f.find(fileName) >= 0:
        for line in open(f):
            if line != "":
                items = line.split(div)
                items.pop( len(items)-1 )
                items = [item for item in items if item is not '']
                if len(items) != 0:             
                    data.append([float(i) for i in items if bool(re.compile("^\d+\.?\d*\Z").match(items[0]))])
    return data
              
def readData(fileName):
    data = []
    for path, subdirs, files in os.walk("."):
        for f in files:
            data += readlines(f, fileName, ',')
    return data
    
            