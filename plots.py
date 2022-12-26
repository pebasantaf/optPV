import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
import os

def plotResults(cs, results, em):
    """## create electrical power matrices"""

    
    print(datetime.now().strftime("%H:%M:%S") + ': Plotting results')
    
    #set plotting style
    
    plt.style.use('classic')
    mpl.rc('lines', linewidth=2)
    mpl.rcParams['patch.edgecolor'] = "none"
    
    
    #calculate cumulative energy of the result for checking validity of results
    
         
    fig, ax1 = plt.subplots()
    
    ax1.bar(range(cs.nr_timesteps), -results['hh']['P_d'], label='Household demand')
    ax1.bar(range(cs.nr_timesteps), -results['em']['P_ex'],bottom=-results['hh']['P_d'],
            label='Market exports')
    
    # Market imports
    
    ax1.bar(range(cs.nr_timesteps), results['em']['P_im'], bottom=results['pv']['P_g'], label='Market imports')
    ax1.bar(range(cs.nr_timesteps), results['pv']['P_g'], label='Solar PV generation')
    
    #generation
    
    
    #prices
    
    ax2 = ax1.twinx()
    
    ax2.plot(range(cs.nr_timesteps), em.price_em, label='DA market price', color='black')

    
    ax1.set_xlabel('Time (h)')
    ax1.set_ylabel('Power (kW)')
    ax2.set_ylabel('Market price (€/kWh)')
    ax1.margins(0.05)
    ax2.margins(0.05)
    ax1.grid()
    
    ax1.legend(loc='upper left', framealpha=0.5)
    ax2.legend(loc='upper right', framealpha=0.5)
    
    fig.set_size_inches(18.5, 10.5)
    plt.show()
    
    #plt.savefig(r'results/' + fleet.id + '/market_allocation_' + figname + '.png', dpi=100)
    
