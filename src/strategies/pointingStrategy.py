# This class defines pointing strategies applicable to any Agent in the simulation

# Attributes

# self.targetlist - a list of target direction vectors for pointing (list of Vector3D)
# self.tbegin - when to begin at a target (list)
# self.tend - when to finish at a target (list)
# self.ntargets - Total number of targets

# Methods

# add_target_to_list - add a given target vector to strategy
# convert_locations_to_targets - take a set of 3D position vectors, turn them into direction vectors

import agents.vector
from strategies.strategy import Strategy as Parent

class pointingStrategy(Parent):

    def __init__(self):
        """
        Generate a pointingStrategy Object
        
        Attributes:
        -----------
        
        targetlist -- list of target vectors (vector3D objects)
        ntargets -- total number of targets in list
        tbegin -- beginning time of strategy (years)
        tend -- ending time of strategy (years)
        """

        Parent.__init__(self)
        self.targetlist = []
        self.tbegin = []
        self.tend = []

        self.ntargets = len(self.targetlist)
    
    def get_target(self,time,dt):
        '''Find pointing at given time'''
        
        Parent.get_target(self,time,dt)
        
        ibegin = next((t for t in tbegin if t>time), None)
        iend =  next((t for t in tend if t>time),None)
        
        return self.targetlist[ibegin]
    
    
    def update(self,time,dt):
        '''Update pointing'''
        
        Parent.update(self,time,dt)
        self.current_target = self.get_target(time,dt)

    
    def add_target(self, targetvector, tbegin, tend):
        """Add a target vector to strategy"""
        
        self.targetlist.append(targetvector)
        self.tbegin.append(tbegin)
        self.tend.append(tend)

        self.ntargets = len(self.targetlist)


    def convert_locations_to_targets(self, position, locations, tbegins, tends):
        """Take a set of locations, and convert them into target vectors relative to given position"""
        
        for location in locations:
            targetvector = location.subtract(position).unit()

            self.add_target(targetvector, tbegins[i],tends[i])



