from pathlib import Path
from demand_data  import *
from solar_functions import *
from datetime import datetime
from utils import selectDatabyDate
from models import *
from optimizer import *
import plots as pl

if __name__ == '__main__':

    demandfolder = 'optPV_data/Data/'
    solarfolder = 'optPV_data/Data/solar_data/'
    LPfolder = 'LPfiles/'
    
    # data path goes back to the parent folder of the repository, where optPV_data folder is
    currentpath = Path.cwd()
    demandpath = currentpath.parent / demandfolder
    solarpath = currentpath.parent / solarfolder
    cs = setCS()
    
    initdate = datetime(2022,5,1)
    enddate = datetime(2022,5,31)
    
    demanddata = CreateDFwithDemand(demandpath)
    demanddata = selectDatabyDate(demanddata, initdate, enddate, datecolumn=1)
    
    zones = generateTimeZones(demanddata.shape[0])
    
    initdate = datetime(2019,5,1)
    enddate = datetime(2019,5,31)
    
    solardata = importSolarData(solarpath)
    solardata = selectDatabyDate(solardata, initdate, enddate, dateformat='%Y-%m-%d')
    
    
    pv = pvSystem()
    hh = household()
    em = electricityMarket()
    
    em.constantEMprice(0.14, cs.nr_timesteps)
    em.constantCompensation(0, cs.nr_timesteps)
    
    pv.power = solardata.electricity.values
    hh.power = demanddata.Consumo_kWh.values
    
    
    
    dirs = getLPFileDirectories(str(currentpath),'VPP')
    writeLPem(dirs,cs,em)
    writeLPhh(dirs,cs, hh)
    writeLPpv(dirs, cs, pv)
    writeLPadd(dirs,cs)
    mergeFiles(dirs)
    
    opt = cplexoptimization(dirs)
    
    cpx_sol = opt.solution.get_values()
    cpx_var = opt.variables.get_names()
    
    results = sortResults(cs, cpx_sol, cpx_var)
    
    
    pl.plotResults(cs, results, em)
    
    print()
    