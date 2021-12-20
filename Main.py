from pathlib import Path
from demand_data  import CreateDFwithDemand

folder = 'optPV_data/Data/Consumo segundo/'

# data path goes back to the parent folder of the repository, where optPV_data folder is
currentpath = Path.cwd()
datapath = currentpath.parent / folder

data = CreateDFwithDemand(datapath)



print()

