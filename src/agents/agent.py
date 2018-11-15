# Defines a base class for both transmitters and observers in the simulation

###############
# Attributes:
###############

# self.position - position (Vector3D)
# self.velocity - velocity (Vector3D)
# self.starpos - host star position (Vector3D)
# self.mstar - host star mass
# self.a - semimajor axis of orbit around host star
# self.mean_anomaly - mean anomaly
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
    
    def __init__(self, position=None,velocity=None,direction_vector=None, openingangle=None,starposition=None,starmass=None,semimaj=None,mean_anomaly=None):
        """Defines a generic Agent in the simulation"""
    
        self.type = "Agent"
        
        self.position = position
        self.velocity = velocity
        self.n = direction_vector
        self.openingangle = openingangle
        self.starpos = starposition
        self.mstar = starmass
        self.a = semimaj
        self.mean_anomaly = mean_anomaly
        
        self.active = True
    
        try:
            self.period = sqrt(self.a*self.a*self.a/self.mstar)
        except ZeroDivisionError:
            self.period = 0.0

    def orbit(self,dt):
        """Moves agent in orbit around host star"""

        inc = piby2 - self.inc

        self.mean_anomaly = self.mean_anomaly + self.period*dt

        self.position.x = self.a*sin(inc)*cos(self.mean_anomaly)
        self.position.y = self.a*sin(inc)*sin(self.mean_anomaly)
        self.position.z = self.a*cos(inc)
        
        self.position = self.position.add(self.starpos)
        
        unitr = self.position.unit()

        velmag = sqrt(self.mstar/self.a) # TODO - units of velocity?

        self.velocity.x = cos(inc)*cos(self.mean_anomaly)
        self.velocity.y = cos(inc)*sin(self.mean_anomaly)
        self.velocity.z = -sin(inc)

        self.velocity = self.velocity.scalarmult(velmag)

    def plot(self,radius,wedge_length):
        """return matplotlib.patches for agent's position, and target vector (with opening angle)"""
        
        # Plot circle at location of agent
        # Colour-coded by agent type
        
        if self.type=="Transmitter":
            colour = 'blue'
        elif self.type=="Observer":
            colour='green'
        else:
            colour='black'
        
        circle = Circle((self.position.x, self.position.y), radius, color=colour)
        
        # Now plot wedge representing width of target vector
        # central angular direction
        thetamid = arctan2(self.n.y,self.n.x)
        
        if(thetamid <0.0):
            thetamid = 2.0*pi + thetamid
    
        wedge = Wedge((self.position.x,self.position.y), wedge_length, 180.0*(thetamid-self.openingangle)/pi, 180.0*(thetamid+self.openingangle)/pi ,color=colour,width=0.75*wedge_length, alpha=0.3)

        return circle, wedge



