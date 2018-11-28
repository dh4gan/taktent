# This base class instantiates a generic strategy for directing
# either transmission or reception for all Agent objects

#

import itertools

newID = itertools.count(1)

class Strategy:

    def __init__(self):
    
        self.ID = str(next(newID)).zfill(3)
        self.current_target = None
    

    def update(self, time,dt):
        '''Update the strategy to its current time'''



