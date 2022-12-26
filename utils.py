import os
from os.path import isfile, join
import pandas as pd

def getCSVfromdir(mypath):

    onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]

    return onlyfiles

def selectDatabyDate(data, initdate, enddate, datecolumn=0, dateformat='%d/%m/%Y'):
    
    data[data.columns[datecolumn]] = pd.to_datetime(data[data.columns[datecolumn]], format=dateformat)
    
    if not 'Hora' in data.columns:
        
        data.insert(2, 'hour', data[data.columns[datecolumn]].dt.hour)
        data[data.columns[datecolumn]] = data[data.columns[datecolumn]].dt.date
        data[data.columns[datecolumn]] = pd.to_datetime(data[data.columns[datecolumn]])
        
    mask =  (data[data.columns[datecolumn]] >= initdate) & (data[data.columns[datecolumn]] <= enddate)
    
    return data[mask]