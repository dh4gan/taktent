# This base class instantiates a generic strategy for directing
# either transmission or reception for all Agent objects

#

import itertools
import copy
from taktent.agents.vector import Vector3D

newID = itertools.count(1)

class Strategy:

    def __init__(self):
        """ Creates a new Strategy object"""
    
        self.ID = str(next(newID)).zfill(3)
        self.current_target = Vector3D(1.0,0.0,0.0)
    
    
    def __copy__(self):
        """ Return a copy of the Strategy object"""
        return Strategy()
    
    def get_target(self,time,dt):
        '''Returns target vector at a given time t
            Allows for vector to be retrieved at earlier times
            if signal travel time is long'''
    
    
    def update(self, time,dt):
        '''Update the current strategy to a given time'''
