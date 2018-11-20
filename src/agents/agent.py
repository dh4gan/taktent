# Defines a base class for both transmitters and observers in the simulation

###############
# Attributes:
###############

# self.position - position (Vector3D)               (units: pc)
# self.velocity - velocity (Vector3D)               (units: km s-1)
# self.starpos - host star position (Vector3D)      (units: pc)
# self.mstar - host star mass
# self.a - semimajor axis of orbit around host star  (units: AU)
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
from uuid import uuid4

piby2 = 0.5*pi

AU_to_pc = 1.0/206265.0
AUyr_to_kms = 1.496e8/(3.15e7)

class Agent:
    
    def __init__(self, position=None,velocity=None,strategy=None,direction_vector=None, openingangle=None,starposition=None,starvelocity=None,starmass=None,semimajoraxis=None,inc=None,mean_anomaly=None):
        """Defines a generic Agent in the simulation"""
    
        self.type = "Agent"
        self.ID = str(uuid4())
        self.colour = "black"
        
        self.position = position
        self.velocity = velocity
        
        self.strategy=strategy
        
        self.n = direction_vector
        self.openingangle = openingangle
        self.starposition = starposition
        self.starvelocity = starvelocity
        self.starmass = starmass
        self.semimajoraxis = semimajoraxis
        self.inclination = inc
        self.mean_anomaly = mean_anomaly
        
        self.active = True
    
        try:
            self.period = sqrt(self.semimajoraxis*self.semimajoraxis*self.semimajoraxis/self.starmass)
        except ZeroDivisionError:
            self.period = 0.0


    def define_strategy(self,strategy):
        self.strategy = strategy

    def update(self,time,dt):
        '''Update position, velocity and direction vector of Agent'''
        self.orbit(time,dt)
        
        self.strategy.update(time,dt)
        
        # If checks that a current target is available
        if(self.strategy.current_target != None):
            self.n = self.strategy.current_target

    def orbit(self,time,dt):
        """Moves agent in orbit around host star"""

        # If orbit not defined, then skip
        if(self.mean_anomaly==None or self.inclination==None or self.semimajoraxis==None):
            return
        
        inc = piby2 - self.inclination

        self.mean_anomaly = self.mean_anomaly + self.period*dt

        self.position.x = self.semimajoraxis*sin(inc)*cos(self.mean_anomaly)
        self.position.y = self.semimajoraxis*sin(inc)*sin(self.mean_anomaly)
        self.position.z = self.semimajoraxis*cos(inc)
        
        
        self.position = self.position.scalarmult(AU_to_pc)
        self.position = self.position.add(self.starposition)
        
        unitr = self.position.unit()

        velmag = sqrt(self.starmass/self.semimajoraxis)*AUyr_to_kms

        self.velocity.x = cos(inc)*cos(self.mean_anomaly)
        self.velocity.y = cos(inc)*sin(self.mean_anomaly)
        self.velocity.z = -sin(inc)

        self.velocity = self.velocity.scalarmult(velmag)
        self.velocity = self.velocity.add(self.starvelocity)

    def plot(self,radius,wedge_length):
        """return matplotlib.patches for agent's position, and target vector (with opening angle)"""
        
        # Plot circle at location of agent
        # Colour-coded by agent type (and if agent successful)
        
        circle = Circle((self.position.x, self.position.y), radius, color=self.colour)
        
        # Now plot wedge representing width of target vector
        # central angular direction
        thetamid = arctan2(self.n.y,self.n.x)
        
        if(thetamid <0.0):
            thetamid = 2.0*pi + thetamid
    
        wedge = Wedge((self.position.x,self.position.y), wedge_length, 180.0*(thetamid-self.openingangle)/pi, 180.0*(thetamid+self.openingangle)/pi ,color=self.colour,width=0.75*wedge_length, alpha=0.3)

        return circle, wedge







