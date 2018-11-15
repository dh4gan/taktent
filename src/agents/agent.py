# Defines a base class for both transmitters and observers in the simulation

###############
# Attributes:
###############

# self.pos - position (Vector3D)
# self.vel - velocity (Vector3D)
# self.starpos - host star position (Vector3D)
# self.mstar - host star mass
# self.a - semimajor axis of orbit around host star
# self.meananom - mean anomaly
# self.n - target direction vector
# self.openingangle - opening angle along target vector (either transmitting or receiving)



###########
# Methods:
###########

# orbit(time) - move agent in orbit around host star
# plot - return patches suitable for a matplotlib plot

from numpy import sin,cos,pi,sqrt, arctan2
from matplotlib.patches import Circle, Wedge

piby2 = 0.5*pi

class Agent:
    
    def __init__(self, position,velocity,direction_vector, open,starposition,starmass,semimaj,mean_anomaly):
        """Defines a generic Agent in the simulation"""
    
        self.type = "Agent"
        self.pos = position
        self.vel = velocity
        self.n = direction_vector
        self.openingangle = open
        self.starpos = starposition
        self.mstar = starmass
        self.a = semimaj
        self.meananom = mean_anomaly
        
        self.active = True
    
        try:
            self.period = sqrt(self.a*self.a*self.a/self.mstar)
        except ZeroDivisionError:
            self.period = 0.0

    def orbit(self,dt):
        """Moves agent in orbit around host star"""

        inc = piby2 - self.inc

        self.meananom = self.meananom + self.period*dt

        self.pos.x = self.a*sin(inc)*cos(self.meananom)
        self.pos.y = self.a*sin(inc)*sin(self.meananom)
        self.pos.z = self.a*cos(inc)
        
        self.pos = self.pos.add(self.starpos)
        
        unitr = self.pos.unit()

        velmag = sqrt(self.mstar/self.a) # TODO - units of velocity?

        self.vel.x = cos(inc)*cos(self.meananom)
        self.vel.y = cos(inc)*sin(self.meananom)
        self.vel.z = -sin(inc)

        self.vel = self.vel.scalarmult(velmag)

    def plot(self,radius):
        '''Returns a patch for plotting agent's position on a matplotlib figure'''
        return

    def plot(self,radius,wedge_length):
        """return matplotlib.patches for agent's position, and target vector (with opening angle)"""
        
        # Plot circle at location of agent
        
        
        circle = Circle((self.pos.x, self.pos.y), radius)
        
        # Now plot wedge representing width of target vector
        # central angular direction
        thetamid = arctan2(self.n.y,self.n.x)
        
        if(thetamid <0.0):
            thetamid = 2.0*pi + thetamid
    
        if (self.active):
            distance = wedge_length
        else:
            distance = 0
    
        print (self.active, self.pos.x, self.pos.y, radius, distance, 180.0*(thetamid-self.openingangle)/pi, 180.0*(thetamid+self.openingangle)/pi)
        wedge = Wedge((self.pos.x,self.pos.y), distance, 180.0*(thetamid-self.openingangle)/pi, 180.0*(thetamid+self.openingangle)/pi )

        return circle, wedge



