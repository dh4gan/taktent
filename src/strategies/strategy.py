# This base class instantiates a generic strategy for directing
# either transmission or reception for all Agent objects

#

from uuid import uuid4

class Strategy:

    def __init__(self):
    
        self.ID = str(uuid4())

    def update(self, time,dt):
        '''Update the strategy to its current time'''



