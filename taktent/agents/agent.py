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

# define_strategy(strategy) - define strategy of Agent
# update(time,dt) - update agent position, velocity and direction vector
# orbit(time) - move agent in orbit around host star
# sample_random(seed,xmin,xmax,ymin,ymax,zmin,zmax,vdisp) - sample position and velocity in uniform cube
# sample_random_sphere(seed, rmin,rmax,vdisp,flatsphere) - sample position and velocity in uniform sphere
# sample_GHZ(): sample position and velocity in Galactic Habitable Zone

# plot(radius,wedge_length) - return patches suitable for a matplotlib plot

from numpy import sin,cos,pi,sqrt, arctan2
from numpy.random import random

from matplotlib.patches import Circle, Wedge
import itertools
from taktent.agents.vector import Vector3D

piby2 = 0.5*pi

GmsolAU = 4.0*pi*pi
AU_to_pc = 1.0/206265.0
AUyr_to_kms = 1.496e8/(3.15e7)
zero_vector = Vector3D(0.0,0.0,0.0)

newID = itertools.count(1)

class Agent:

    def __init__(self, position=zero_vector, velocity=zero_vector,strategy=None,direction_vector=zero_vector, openingangle=piby2,starposition=zero_vector,starvelocity=zero_vector,starmass=1.0,semimajoraxis=1.0,inclination=0.0, longascend = 0.0, mean_anomaly=0.0):
        """
        Initialises a generic Agent object
        
        Keyword Arguments:
        -----------------
        
        position -- cartesian position vector (pc)
        velocity -- cartesian velocity vector (pc yr^-1)
        strategy -- Strategy object defining Agent's pointing behaviour
        direction_vector -- unit vector defining pointing direction of Agent
        openingangle -- opening angle of beam defined by Agent's pointing (radians)
        starposition -- cartesian position vector of host star (pc)
        starvelocity -- cartesian velocity vector of host star (pc yr^-1)
        starmass -- host star mass (solar masses)
        semimajoraxis -- semimajor axis of orbit about host star (AU)
        inclination -- inclination of orbit about host star (radians)
        longascend -- longitude of the ascending node of orbit about host star (radians)
        mean_anomaly -- mean anomaly of orbit about host star (radians)
        
        
        Other defined attributes of Agent:
        ----------------------------------
        
        type -- Description of agent type (string)
        ID -- Identification number (string)
        colour -- colour for plotting
        active -- Is Agent active? (boolean)
        period -- period of Agent's orbit about host star
        
        """
    
        self.type = "Agent"
        self.ID = str(next(newID)).zfill(3)
        
        self.colour = "black"
        
        self.position = position
        self.velocity = velocity
        
        self.strategy=strategy
        self.n = direction_vector
        
        if(self.n.mag()>1.0e-30):
            self.n = self.n.unit()
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
        """
        Define a new Strategy object for the Agent
        
        Keyword Arguments:
        -----------------
        strategy -- Strategy object
        
        """
        self.strategy = strategy

    def update(self,time,dt):
        """
        Update position, velocity and direction vector of Agent
        
        Keyword Arguments:
        ------------------
        time -- current time (years)
        dt -- timestep (years)
        
        """
        
        # Move Agent in orbit around its host star
        self.orbit(time,dt)
        
        # Update its pointing strategy
        
        self.strategy.update(time,dt)
        
        # If checks that a current target is available
        if(self.strategy.current_target != None):
            self.n = self.strategy.current_target

    def orbit(self,time,dt):
        """
        Moves agent in (circular) orbit around host star - necessarily for computing Doppler drift of emitted signals
        
        Keyword Arguments:
        ------------------
        time -- current time (years)
        dt -- timestep (years)
        
        """
        
        # If orbit not defined, then skip this calculation
        if(self.mean_anomaly==None or self.inclination==None or self.semimajoraxis==None):
            return
        
        # Update mean anomaly
        self.mean_anomaly = self.mean_anomaly + 2.0*pi*self.period*dt

        # Compute orbit in the x-y plane
        self.position.x = cos(self.mean_anomaly)
        self.position.y = sin(self.mean_anomaly)
        self.position.z = 0.0
        
        # Rotate orbit according to inclination and longitude of ascending node
        self.position = self.position.rotate_x(self.inclination)
        self.position = self.position.rotate_z(self.longascend)
        
        self.position = self.position.scalarmult(AU_to_pc)  # positions in pc
        self.position = self.position.add(self.starposition)
        
        unitr = self.position.unit()

        # Magnitude of velocity (Keplerian orbit)
        velmag = sqrt(GmsolAU*self.starmass/self.semimajoraxis)*AU_to_pc # velocity in pc yr-1

        # Compute velocity vector (again in x-y plane)
        self.velocity.x = -sin(self.mean_anomaly)
        self.velocity.y = cos(self.mean_anomaly)
        self.velocity.z = 0.0
        
        # Rotate according to inclination and longitude of ascending node
        self.velocity = self.velocity.rotate_x(self.inclination)
        self.velocity = self.velocity.rotate_z(self.longascend)

        self.velocity = self.velocity.scalarmult(velmag)
        self.velocity = self.velocity.add(self.starvelocity)


    def sample_random(self,seed=-45, xmin=-10.0, xmax=10.0, ymin=-10.0, ymax=10.0, zmin=0.0, zmax=0.0, vdisp=0.1):
        """
        Return uniformly sampled position and velocity vectors
        
        Keyword Arguments:
        ------------------
        
        seed -- Random number seed for generating samples
        xmin, xmax -- minimum and maximum x-coordinates (pc)
        ymin, ymax -- minimum and maximum y-coordinates (pc)
        zmin, zmax -- minimum and maximum z-coordinates (pc)
        vdisp -- magnitude of the velocity vector
        
        """
        
        self.starposition = Vector3D(xmin+ (xmax-xmin)*random(), ymin+(ymax-ymin)*random(), zmin+ (zmax-zmin)*random())
        
        self.star_velocity = Vector3D(vdisp*(-1.0+2.0*random()), vdisp*(-1.0+2.0*random()), vdisp*(-1.0+2.0*random()))
    
    
        self.position = self.starposition
        self.velocity = self.starvelocity
    

    def sample_random_sphere(self, seed=-45, rmin = 10.0, rmax = 20.0, vdisp=0.0, flatsphere=True):
        """
        Return position and velocity vectors randomly sampled on a sphere
        
        Keyword Arguments:
        ------------------
        seed -- Random number seed for generating samples
        rmin -- minimum radius from origin (pc)
        rmax -- maximum radius from origin (pc)
        vdisp -- magnitude of the velocity vector
        flatsphere -- generate 2D sphere (True) or 3D sphere (False)
        """
    
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
        """
        Return matplotlib.patches objects for agent's position, and target vector (with opening angle)
        
        Keyword Arguments:
        ------------------
        
        radius - radius of circle to plot
        wedge_length - length of wedge indicating agent beam
        
        Returns:
        --------
        
        circle -- matplotlib.patches.Circle object
        wedge -- matplotlib.patches.Wedge object
            
        """
        
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







