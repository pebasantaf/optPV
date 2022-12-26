
class household():
    def __init__(
        self,
        P_d_max = None,
        P_d_min = None,
        ghg_CO2 = None,
        timezones = None,
        cost = None,
        power = None
    ):
        
        """
        Info
        ----
        This class provides a model with the basic attributes of a
        household load.
        """
        # max. generation (kW)
        self.P_d_max = 5000;
        
        # min. generation (kW)
        self.P_d_min = 0;
        
        # variable generation cost (EUR/kWh)
        self.cost = 0;
        
        # greenhouse gas emissions (gCO2/kWh)
        self.ghg_CO2 = 0.001;
        
        self.timezones = None
        
        #get load power profiles
        self.power = None


class pvSystem():
    def __init__(
        self,
        P_g_max = None,
        P_g_min = None,
        ghg_CO2 = None,
        cost = None,
        power = None,
    ):
        
        """
        Info
        ----
        This class provides a model with the basic attributes of a
        photovoltaic power plant.
        """
        # max. generation (kW)
        self.P_g_max = 5000;
        
        # min. generation (kW)
        self.P_g_min = 0;
        
        # variable generation cost (EUR/kWh)
        self.cost = 0.048;
        
        # greenhouse gas emissions (gCO2/kWh)
        self.ghg_CO2 = 0.001;
        
        #get load power profiles
        self.power = None
        
class electricityMarket():
    def __init__(
        self,
        P_im_min = None,
        P_im_max = None,
        P_ex_min = None,
        P_ex_max = None,
        ghg_CO2_IM = None,
        ghg_CO2_EX = None,
        price_em = None
    ):
        
        """
        Info
        ----
        This class provides a model with the basic attributes of a
        energy market.
        """
        # min. power import (kW)
        self.P_im_min = 0;
        
        # max. power import (kW)
        self.P_im_max = 1000000;
        
        # min. power export (kW)
        self.P_ex_min = 0;
        
        # max. power export (kW)
        self.P_ex_max = 1000000;
        
        # greenhouse gas emissions for market import (gCO2/kWh)
        self.ghg_CO2_IM = 559;
        
        # greenhouse gas emissions for market export (gCO2/kWh)
        self.ghg_CO2_EX = 0.001;

        self.price_em =  None
        
    def constantEMprice(self, value, length):
        
        self.price_em = [value]*length
        