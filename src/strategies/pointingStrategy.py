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

        Parent.__init__(self)
        self.targetlist = []
        self.tbegin = []
        self.tend = []

        self.ntargets = len(self.targetlist)
    
    
    def update(self,time,dt):
        '''Update pointing'''
        
        Parent.update(self,time,dt)
    
        ibegin = next((t for t in tbegin if t>time), None)
        iend =  next((t for t in tend if t>time),None)

        self.current_target= self.targetlist[ibegin]

    def get_old_target(self,oldtime,dt):
        '''Find pointing at time oldtime'''
        
        Parent.get_old_target(self,oldtime,dt)
        
        ibegin = next((t for t in tbegin if t>oldtime), None)
        iend =  next((t for t in tend if t>oldtime),None)
        
        return self.targetlist[ibegin]

    
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



