# This class defines pointing strategies applicable to any Agent in the simulation

# Attributes

# targetfunction -- function that defines direction vector
# period_xy -- period of motion in x-y plane (years)
# period_yz -- period of motion in y-z plane (years)
# phase_xy -- phase of motion in x-y plane
# phase_yz -- phase of motion in y-z plane
# tinit -- time of strategy initiation (years)

# Methods

# __copy__ -- return a copy of the object
# get_target(time,dt) -- get target at given time
# update(time,dt) -- update to the current target

from agents import vector
from strategies.strategy import Strategy as Parent
import copy

class scanningStrategy(Parent):

    def __init__(self, targetfunction=None, period_xy=None, period_yz=None, phase_xy = None, phase_yz = None, tinit=None):
        
        """
        Define scanningStrategy Object
        
        Keyword Arguments:
        ------------------
        
        targetfunction -- function that defines direction vector
        period_xy -- period of motion in x-y plane (years)
        period_yz -- period of motion in y-z plane (years)
        phase_xy -- phase of motion in x-y plane
        phase_yz -- phase of motion in y-z plane
        tinit -- time of strategy initiation (years)
        
        """
        
        Parent.__init__(self)
        
        self.targetfunction = targetfunction
        self.period_xy = period_xy
        self.period_yz = period_yz
        
        self.phase_xy = phase_xy
        self.phase_yz = phase_yz
    
        self.tinit = tinit
    
    def __copy__(self):
        """ Return a copy of the scanningStrategy Object"""
        return scanningStrategy(self.targetfunction, self.period_xy, self.period_yz, self.phase_xy, self.phase_yz, self.tinit)
    
    
    def get_target(self,time,dt):
        '''
        Get target vector at a given time
        
        Keyword Arguments:
        ------------------
        time -- current time (years)
        dt -- timestep (years)
        
        Returns:
        --------
        
        target_vector -- the target vector at a given time
        '''
        
        Parent.get_target(self,time,dt)
        
        target_vector = self.targetfunction(time, tinit = self.tinit, period_xy = self.period_xy, period_yz = self.period_yz, phase_xy=self.phase_xy, phase_yz=self.phase_yz)
    
        return target_vector

    
    def update(self,time,dt):
        """
        Define current target vector
        
        Keyword Arguments:
        ------------------
        time -- current time (years)
        dt -- timestep (years)
        
        """
        
        Parent.update(self,time,dt)
        
        self.current_target= self.get_target(time,dt)


