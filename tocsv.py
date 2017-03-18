#!/usr/bin/python

import os
import glob
import numpy as np

#開けたフォルダ順に　前処理は必要

dataname = 'heart'

def outputTxt(data, fileName):

    newFileName = fileName[:-4] + ".csv"

    outc = ""
    for d in data[1:]:
        outc += d[:-2] + "\n"
        print(d[:-2])

    fc = open(newFileName, 'w')
    fc.write(outc)
    fc.close()
    
direc = glob.glob("*" + dataname + "*")

for name in direc:
    f = open(name, 'r')
    data = f.readlines()

    outputTxt(data, name)











