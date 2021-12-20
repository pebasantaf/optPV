import os
from os.path import isfile, join
import pandas as pd


def getCSVfromdir(mypath):

    onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]

    return onlyfiles

def CreateDFwithDemand(datapath):

    filenames = getCSVfromdir(datapath)
    data = []
    for f in filenames:

        aktdata  = pd.read_excel(datapath / f, header=12)

        # get index first empty row to reduce dataframe 

        emptyrow = aktdata[aktdata.columns[0]].index[aktdata.Fecha.isnull()==True].tolist()[0]

        #limit dataframe until empty row
        aktdata = aktdata.loc[0:emptyrow-1,:]

        if filenames.index(f) == 0:
            data = aktdata

        else:

            data = data.append(aktdata, ignore_index=True)

    return data
