
import cplex
import numpy as np
import os
import sys
sys.path.append("..")

class setCS():
    def  __init__(
        self,
        time_increment = None,
        nr_timesteps = None,
        ghg_CO2 = None,
        include_penalty = None,
        penalty_factor = None,
        file_directionary = None,
    ):

        # -------------
        # NOTE: Profiles have a time resolution of 15 minutes and include data of seven days.
        
        # time increment (h)
        self.time_increment = 0.25; # (h)
        
        # number of time steps
        self.nr_timesteps = 24;
        
        # objective function
        # (1 - cost optimized, 2 - CO2 optimized)
        self.objective_function = 1;
        
        # include penalty factor (only for CO2 optimization)
        # (1 - yes, 0 - no)
        self.include_penalty = 1;
        self.penalty_factor = 0.001;
        
        self.file_directionary = os.getcwd()

def getLPFileDirectories(file_directionary: str,filename: str) -> dict:
    ## set objective (Minimize/Maximize)
    
    obj_minmax = 'Minimize'
    
    
    ## get file directories
    
    # main file
    lp= file_directionary + '\\'+'LPfiles\\'+ filename+'.lp'
    
    # temporary file for objective variables
    filename_obj = filename +'_obj'
    obj = file_directionary + '\\'+'LPfiles\\'+ filename_obj+'.lp'
    with open(obj,'w+') as f:
        f.truncate(0)
        f.write(obj_minmax +'\n')

    
    # temporary file for constraints
    filename_cons = filename +'_cons'
    cons = file_directionary + '\\'+'LPfiles\\'+ filename_cons+'.lp'
    with open(cons,'w+') as f:
        f.truncate(0)
        f.write('\nSubject To\n')
    
    # temporary file for boundaries
    filename_bounds = filename +'_bounds'
    bounds = file_directionary + '\\'+'LPfiles\\'+ filename_bounds+'.lp'
    with open(bounds,'w+') as f:
        f.truncate(0)
        f.write( '\nBounds\n')
    
    # temporary file for binaries
    filename_binaries = filename +'_binaries'
    binaries =file_directionary + '\\'+'LPfiles\\'+ filename_binaries+'.lp'
    with open(binaries,'w+') as f:
        f.truncate(0)
        f.write('\nBinaries\n')

    return {'lp':lp,'obj':obj,'cons':cons,'bounds':bounds,'binaries':binaries}


def mergeFiles(filedirectory):
    obj = ''
    cons =''
    binaries =''
    bounds = ''
    with open(filedirectory['obj'],'r') as f:
        obj =f.read()
        f.close()
    with open(filedirectory['cons'],'r') as f:
        cons =f.read()
        f.close()
    with open(filedirectory['binaries'],'r') as f:
        binaries =f.read()
        f.close()
    with open(filedirectory['bounds'],'r') as f:
        bounds =f.read()
        f.close()
    with open(filedirectory['lp'],'a+') as f:
        f.truncate(0)
        f.write(obj)
        f.write(cons)
        f.write(bounds)
        f.write(binaries)
        
        f.write('\nEnd')
        f.close()

def writeLPem(filedirectory, cs, em):
    tstep = np.array(range(1,cs.nr_timesteps+1))
    """ objective variables"""

    # open temporary optimization file for objective function
    with open(filedirectory['obj'],'a') as f:
    # check objective function
        if (cs.objective_function==1): # cost optimization
        
            # write optimization variable into file for each time step

            for i in range(cs.nr_timesteps):
                cost = em.price_em[i]
                f.write("+ {:g} P_im_em~{} - {:g} P_ex_em~{}\n".format
                    (cost*cs.time_increment, tstep[i], cost*cs.time_increment, tstep[i]))
            
        elif (cs.objective_function==2): # CO2 optimization
           
            # check if penalty factor is activated
            if (cs.include_penalty==1):
                emission_export = em.ghg_CO2_EX + cs.penalty_factor
            else:
                emission_export = em.ghg_CO2_EX

            
            # write optimization variable into file for each time step
            emission_import = em.ghg_CO2_IM
            for i in range(cs.nr_timesteps):       
                f.write("+ {:g} P_im_em~{} + {:g} P_ex_em~{}\n".format
                    (emission_import*cs.time_increment, tstep[i] ,emission_export*cs.time_increment, tstep[i]))
 
        # close temporary optimization file 
        f.close()
    """ constraints"""
    
    # open temporary optimization file for constraints
    with open(filedirectory['cons'],'a') as f:
    
    # write constraints for operation modes (equations 3.19, 3.20, 3.21 and 3.22)
        P_im_min = em.P_im_min
        for i in range(cs.nr_timesteps):
            f.write("{:g} y_em~{} - P_im_em~{} <= 0\n".format
            (P_im_min, tstep[i], tstep[i]))
        P_im_max = em.P_im_max
        for i in range(cs.nr_timesteps):
            f.write(" P_im_em~{} - {:g} y_em~{} <= 0\n".format
        (tstep[i], P_im_max, tstep[i]))
        P_ex_min = em.P_ex_min
        for i in range(cs.nr_timesteps):
            f.write("{:g} y_em~{} + P_ex_em~{} >= {:g}\n".format
            (P_ex_min ,tstep[i], tstep[i] ,P_ex_min))        
        P_ex_max = em.P_ex_max
        for i in range(cs.nr_timesteps):
            f.write(" {:g} y_em~{}  + P_ex_em~{} <= {:g}\n".format
            (P_ex_max ,tstep[i], tstep[i], P_ex_max))
        

        # close temporary optimization file 
        f.close()
    """ boundaries"""
    
    # open temporary optimization file for boundary conditions
    with open(filedirectory['bounds'],'a') as f:
    
    # write boundary conditions for market imports into file for each time step
        lb = em.P_im_min
        ub = em.P_im_max
        for i in range(cs.nr_timesteps):
            f.write("{:g} <= P_im_em~{} <= {:g}\n".format( lb ,tstep[i] ,ub))
        
        # write boundary conditions for market exports into file for each time step
        lb = em.P_ex_min
        ub = em.P_ex_max
        for i in range(cs.nr_timesteps):
            f.write("{:g} <= P_ex_em~{} <= {:g}\n".format( lb, tstep[i] ,ub))
        
        # close temporary optimization file 
        f.close()
    
    """ binaries"""
    
    # open temporary optimization file for binaries according to slide 45
    with open(filedirectory['binaries'],'a') as f:
    
        # write binary into file for each time step
        for i in range(cs.nr_timesteps):
            f.write("y_em~{}\n".format(tstep[i]))
        
        # close temporary optimization file 
        f.close()


def writeLPpv(filedirectory:dict, cs, pv):


    """
    objective variables
    """
    filedirectory
    # open temporary optimization file for objective function
    with open(filedirectory['obj'],'a') as f:
    
    # check objective function
        if (cs.objective_function==1): # cost optimization
        
            # write optimization variable into file for each time step
            cost = pv.cost
            tstep = np.array(range(1,cs.nr_timesteps+1))
            for i in range(cs.nr_timesteps):
                str = '+ {:g} P_g_pv~{}\n'.format( cost * cs.time_increment,tstep[i])
                f.write(str)
        
        elif (cs.objective_function==2): # CO2 optimization
            
            # write optimization variable into file for each time step
            emission = pv.ghg_CO2
            for i in range(cs.nr_timesteps):
               f.write("+ {:g} P_g_pv~{}\n".format(emission*cs.time_increment,tstep[i]))
       # close temporary optimization file 
        f.close() 
    
    """ 
    constraints
    """
    # open temporary optimization file for constraints
    with open(filedirectory['cons'],'a') as f:
    
    # write profile given constraints into file for each time step
        tstep = np.array(range(1,cs.nr_timesteps+1))
        for i in range(cs.nr_timesteps):
            f.write("P_g_pv~{} = {:g}\n".format(tstep[i],pv.power[i]));
    
        # close temporary optimization file 
        f.close()
    """
    boundaries
    """ 
    
    # open temporary optimization file for boundary conditions
    with open(filedirectory['bounds'],'a') as f:
    
    # write boundary conditions for power generation into file for each time step
        tstep = np.array(range(1,cs.nr_timesteps+1))
        lb = pv.P_g_min
        ub = pv.P_g_max
        for i in range(cs.nr_timesteps):
            f.write("{:g} <= P_g_pv~{} <= {}\n".format(lb,tstep[i],ub))
        # close temporary optimization file 
        f.close()



def writeLPhh(filedirectory, cs, hh):

    """
    objective variables
    """
    
    # open temporary optimization file for objective function
    with open(filedirectory['obj'],'a') as f:
    # check objective function
        if (cs.objective_function==1):# cost optimization
        
           # write optimization variable into file for each time step
            cost = hh.cost
            tstep = np.array(range(1,cs.nr_timesteps+1))
            for i in range(cs.nr_timesteps):
                str = '- {:g} P_d_hh~{}\n'.format( cost * cs.time_increment,tstep[i])
                f.write(str)
        
        elif (cs.objective_function==2):# CO2 optimization          
           # write optimization variable into file for each time step
            emission = hh.ghg_CO2 
            tstep = np.array(range(1,cs.nr_timesteps+1))           
            for i in range(cs.nr_timesteps):
                str = '+ {:g} P_d_hh~{}\n'.format( emission * cs.time_increment,tstep[i])
                f.write(str)
        # close temporary optimization file 
        f.close()
        
    """ 
    constraints
    """
    
   # open temporary optimization file for constraints
    with open(filedirectory['cons'],'a') as f:
    
        # write profile given constraints into file for each time step
        for i in range(cs.nr_timesteps):
            f.write("P_d_hh~{} = {:g}\n".format(tstep[i],hh.power[i]));
    
        # close temporary optimization file 
        f.close()
    """
    boundaries
    """ 
    
   # open temporary optimization file for boundary conditions
    with open(filedirectory['bounds'],'a') as f:
        
   # write boundary conditions for power demand into file for each time step
        lb = hh.P_d_min 
        ub = hh.P_d_max    
        tstep = np.array(range(1,cs.nr_timesteps+1))
        for i in range(cs.nr_timesteps):
            f.write("{:g} <= P_d_hh~{} <= {}\n".format(lb,tstep[i],ub))
        # close temporary optimization file 
        f.close()


def writeLPadd(filedirectory, cs):


    tstep = np.array(range(1,cs.nr_timesteps+1))
    """ power equilibrium constraints"""
     
    # open temporary optimization file for constraints
    with open(filedirectory['cons'],'a') as f:
    
    # write power equilibrium constraint into file for each time step
        power_eqa ='P_g_pv~{} + P_im_em~{} - P_ex_em~{} - P_d_hh~{} = 0\n'
        for i in range(cs.nr_timesteps):
            f.write( power_eqa.format(tstep[i], tstep[i], tstep[i], tstep[i]))

        f.close()



def cplexoptimization(filedirectory):
    ## run optimization 
    
    # initialize CPLEX object
    cpx = cplex.Cplex()
    
    # read optimization model
    cpx.read(filedirectory['lp'])
    
    # deactivate creation of log-file
    cpx.parameters.output.clonelog.Cur = 4
    
    # choose LP method
    # 0 - Automatic: Let Cplex choose
    # 1 - Primal Simplex
    # 2 - Dual Simplex
    # 3 - Network Simplex
    # 4 - Barrier
    # 5 - Sifting
    # 6 - Concurrent (Dual, Barrier and Primal in opportunistic parallel mode)
    cpx.parameters.lpmethod.Cur = 0
    
    # solve optimization problem
    cpx.solve()
    
    # get variable names and respective solution vector
    """if (isfield(cpx.Solution,'x')):
        cpx_sol = cpx.Solution.x
        cpx_var = cpx.Model.colname
    else:
        error(sprintf(['\nNo optimal soluation available, please adjust optimization model and check command window output for more info!']))
    """
    return cpx

def sortResults(cs, cpx_sol, cpx_var):
   
    
    results = {'em': {'P_im':[],
                         'P_ex':[],

                         }, 
               'hh': {'P_d':[],
                },
               
               'pv': {'P_g':[]},
                }
    
    for key1 in results:
        
        for key2 in results[key1]:
            
            name = key2 + '_' + key1
            mask = [name in var for var in cpx_var]
            
            results[key1][key2] = np.array(cpx_sol)[mask]
            assert len(results[key1][key2]) == cs.nr_timesteps
    
    return results   