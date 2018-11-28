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
from numpy.random import random

from matplotlib.patches import Circle, Wedge
import itertools
from agents.vector import Vector3D

piby2 = 0.5*pi

GmsolAU = 4.0*pi*pi
AU_to_pc = 1.0/206265.0
AUyr_to_kms = 1.496e8/(3.15e7)
zero_vector = Vector3D(0.0,0.0,0.0)

newID = itertools.count(1)

class Agent:

    def __init__(self, position=zero_vector, velocity=zero_vector,strategy=None,direction_vector=zero_vector, openingangle=piby2,starposition=zero_vector,starvelocity=zero_vector,starmass=1.0,semimajoraxis=1.0,inclination=0.0, longascend = 0.0, mean_anomaly=0.0):
        """Defines a generic Agent in the simulation"""
    
        self.type = "Agent"
        self.ID = str(next(newID)).zfill(3)
        
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
        self.inclination = inclination
        self.longascend = longascend
        self.mean_anomaly = mean_anomaly
        
        self.active = True
    
        if self.semimajoraxis !=None:
            try:
                self.period = sqrt(self.semimajoraxis*self.semimajoraxis*self.semimajoraxis/(self.starmass))
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

        self.mean_anomaly = self.mean_anomaly + 2.0*pi*self.period*dt

        self.position.x = cos(self.mean_anomaly)
        self.position.y = sin(self.mean_anomaly)
        self.position.z = 0.0
        
        self.position = self.position.rotate_x(self.inclination)
        self.position = self.position.rotate_z(self.longascend)
        
        self.position = self.position.scalarmult(AU_to_pc)  # positions in pc
        self.position = self.position.add(self.starposition)
        
        unitr = self.position.unit()

        velmag = sqrt(GmsolAU*self.starmass/self.semimajoraxis)*AU_to_pc # velocity in pc yr-1

        self.velocity.x = -sin(self.mean_anomaly)
        self.velocity.y = cos(self.mean_anomaly)
        self.velocity.z = 0.0
        
        self.velocity = self.velocity.rotate_x(self.inclination)
        self.velocity = self.velocity.rotate_z(self.longascend)

        self.velocity = self.velocity.scalarmult(velmag)
        self.velocity = self.velocity.add(self.starvelocity)


    def sample_random(self,seed=-45, xmin=-10.0, xmax=10.0, ymin=-10.0, ymax=10.0, zmin=0.0, zmax=0.0, vdisp=0.1):
        """Return randomly sampled position and velocity vectors (vmag = 0.1 posmag)"""
        
        self.starposition = Vector3D(xmin+ (xmax-xmin)*random(), ymin+(ymax-ymin)*random(), zmin+ (zmax-zmin)*random())
        
        self.star_velocity = Vector3D(vdisp*(-1.0+2.0*random()), vdisp*(-1.0+2.0*random()), vdisp*(-1.0+2.0*random()))
    

    def sample_random_sphere(self, seed=-45, rmin = 10.0, rmax = 20.0, vdisp=0.0, flatsphere=False):
    
        r = rmin+ (rmax-rmin)*random()
        theta = pi*random()
        phi = 2.0*pi*random()
        
        if(flatsphere):
            self.starposition = Vector3D(r*cos(phi), r*sin(phi),0.0)
            self.starvelocity = Vector3D(vdisp*(-1.0+2.0*random()), vdisp*(-1.0+2.0*random()), 0.0)        
        else:
            self.starposition = Vector3D(r*sin(theta)*cos(phi), r*sin(theta)*sin(phi), r*cos(theta))
            self.starvelocity = Vector3D(vdisp*(-1.0+2.0*random()), vdisp*(-1.0+2.0*random()), vdisp*(-1.0+2.0*random()))
        
        self.position = self.starposition
        self.velocity = self.starvelocity
                

    def sample_GHZ(self):
        '''Returns position and velocity vector of a star in the GHZ'''
        # TODO copy in GHZ sampler from C++ methods

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







