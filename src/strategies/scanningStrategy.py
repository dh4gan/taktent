# This class defines pointing strategies applicable to any Agent in the simulation

# Attributes

# self.targetlist - a list of target direction vectors for pointing (list of Vector3D)
# self.tbegin - when to begin at a target (list)
# self.tend - when to finish at a target (list)
# self.ntargets - Total number of targets

# Methods

# add_target_to_list - add a given target vector to strategy
# convert_locations_to_targets - take a set of 3D position vectors, turn them into direction vectors

from strategies.strategy import Strategy as Parent

class scanningStrategy(Parent):

    def __init__(self, targetfunction=None):
        
        self.targetfunction = targetfunction
    
    def update(self,time):
        '''Call scanning function that defines target at time t'''

        Parent.update(time)

        return self.targetfunction(time)


