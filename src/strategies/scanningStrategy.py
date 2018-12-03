# This class defines pointing strategies applicable to any Agent in the simulation

# Attributes

# self.targetlist - a list of target direction vectors for pointing (list of Vector3D)
# self.tbegin - when to begin at a target (list)
# self.tend - when to finish at a target (list)
# self.ntargets - Total number of targets

# Methods

# add_target_to_list - add a given target vector to strategy
# convert_locations_to_targets - take a set of 3D position vectors, turn them into direction vectors

from agents import vector
from strategies.strategy import Strategy as Parent
import copy


class scanningStrategy(Parent):

    def __init__(self, targetfunction=None, period_xy=None, period_yz=None, phase_xy = None, phase_yz = None, tinit=None):
        Parent.__init__(self)
        
        self.targetfunction = targetfunction
        self.period_xy = period_xy
        self.period_yz = period_yz
        
        self.phase_xy = phase_xy
        self.phase_yz = phase_yz
    
        self.tinit = tinit
    
    def __copy__(self):
        return scanningStrategy(self.targetfunction, self.period_xy, self.period_yz, self.phase_xy, self.phase_yz, self.tinit)
    
    
    def get_target(self,time,dt):
        '''Get target vector at time time'''
        
        Parent.get_target(self,time,dt)
        
        target_vector = self.targetfunction(time, tinit = self.tinit, period_xy = self.period_xy, period_yz = self.period_yz, phase_xy=self.phase_xy, phase_yz=self.phase_yz)
    
        return target_vector

    
    def update(self,time,dt):
        '''Call scanning function that defines target at time t'''

        Parent.update(self,time,dt)
        
        self.current_target= self.get_target(time,dt)


