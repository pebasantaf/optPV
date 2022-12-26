from utils import getCSVfromdir
import pandas as pd


def CreateDFwithDemand(datapath):

    filenames = getCSVfromdir(datapath)
    data = []
    for f in filenames:
        
        fextension = f.split('.')[-1]
        
        if fextension == 'csv':
            
            aktdata  = pd.read_csv(datapath / f, sep=';', decimal=',')
            
        elif fextension == 'xlsx':
            
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


def generateTimeZones(length):
    
    
    print()