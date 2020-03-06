# PV AND BATTERY DESIGN FOR XUNQUEIRA %
# Pedro Basanta Franco

'''
In this file I am going to design a code for sizing the correct amount of solar PV alone or with batteries for
households considering their energy demand and the solar production in the area.
'''
''' 
I am also going to use this to train classes, methods and attributes. As a reminder, classes are basically python 
objects. They generalize and abstract information. Within them, we can have methods, which are functions that only that
class can perform; and attributes, which are, more or less, variables or data stored within that class.
'''

''' 
Structure:
    - Define a month class where the solar data is store. We could also have more attributes, as average day of the 
    month.
    - The same could be done with the demand. Store it monthly demand classes.
    - Again, with several of the solar panels a class could be created that stores the data for the different fabricants
    - Once this is defined, we want to be able to find out if either only solar pannels or solar + battery is economically
    feasible.
    - The reference month for both the installation and storage should be dediced, as it is not the same a solar system
    based on July or based on January. Maybe an evaluation of cost, % of energy covered and savings can be done per month,
    in order to find the most suitable solution. Within that monthly study, the optimal solution considering only 
    solar and solar and batteries is computed. 
    - Among all the monthly solutions, the reasonable ones are selected based on criteria that could be input from user.
    For example, establishing a limit in cost or a minimum percentage, the solution with most savings, etc...

'''