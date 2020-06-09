# SOLAR ENERGY IMPORT MODULE
#   This function is aimed at developing all the functions that will be dealing with processing of the solar data. To get
# a better overview, check the first issue in Github.

import glob
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pvlib

def GHIcalc(Gb, Gd, N, lat, sh):

    omega = ((2*math.pi)/24) * sh

    # calculate solar declination
    delta = 23.45*math.sin((360/365)*(284 + N))

    # clculate the cost of the zenith angle
    cosz = math.cos(omega)*cos + math.cos(delta) + math.cos(lat) + math.sin(delta) + math.sin(lat)

    GHI = Gb + Gd*cosz
    return GHI


def getOrientedIrradiation(GHI, location, orientation, angle, panel, type):



    return
