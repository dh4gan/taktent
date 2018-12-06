# Class instantiates an object which acts as an observer


###############
# Attributes:
###############

# Inherited from agent.py
# self.position - position (Vector3D)
# self.velocity - velocity (Vector3D)
# self.starposition - host star position (Vector3D)
# self.starmass - host star mass
# self.a - semimajor axis of orbit around host star
# self.inc - inclination of orbit around host star
# self.mean_anomaly - mean anomaly

# self.sensitivity - sensitivity of observation
# self.numin - minimum frequency
# self.numax - maximum frequency
# self.nchannels - number of channels in observation


###########
# Methods:
###########

# Inherited/Extended from agent.py
# define_strategy(strategy) - define strategy of Agent
# update(time,dt) - update Agent position, velocity and direction vector
# orbit(time) - move agent in orbit around host star
# sample_random(seed,xmin,xmax,ymin,ymax,zmin,zmax,vdisp) - sample position and velocity in uniform cube
# sample_random_sphere(seed, rmin,rmax,vdisp,flatsphere) - sample position and velocity in uniform sphere
# sample_GHZ(): sample position and velocity in Galactic Habitable Zones

# plot(radius,wedge_length) - return patches suitable for a matplotlib plot

# Additional Methods:

# calculate_doppler_drift(time,dt,transmitter) - calculate the Doppler drift from a signal emitted by a transmitter
# set_colour() - set the colour of the observer for plotting
# observe_transmitter(time,dt,transmitter) - attempt to detect transmitter
# skymap - generate a field of view image along observer's current target vector

from taktent.agents.agent import Agent as Parent
from numpy import sin,cos, arccos, pi, arctan2, round, amin,amax, zeros,linspace, arange
from taktent.agents.vector import Vector3D
import matplotlib.pyplot as plt

basemap_installed = True

try:
    from mpl_toolkits.basemap import Basemap
except ModuleNotFoundError:
    print ("WARNING: basemap not installed")
    print ("==> Cannot produce all sky maps for Observers")
    print ("==> Will default to field-of-view sky maps")
    basemap_installed = False


def get_circle_outline(x0,y0,r, npoints=100):
    t = linspace(0,2.0*pi, num=npoints)
    
    x = zeros(npoints)
    y = zeros(npoints)
        
    for i in range(npoints):
        x[i] = r*cos(t[i]) + x0
        y[i] = r*sin(t[i]) + y0
            
    return x,y

piby2 = 0.5*pi
zero_vector = Vector3D(0.0,0.0,0.0)

pc_yr_to_ms = 3.08e16/3.15e7

class Observer(Parent):
    
    def __init__(self,position=zero_vector, velocity=zero_vector, strategy=None, direction_vector=zero_vector, openingangle=piby2, starposition=zero_vector, starvelocity=zero_vector, starmass=1.0, semimajoraxis=1.0, inclination=0.0, longascend=0.0,mean_anomaly=0.0, sensitivity=None, nu_min=1.0e9, nu_max=2.0e9, nchannels=1.0e6):
        
        """
        Initialises an Observer object
        
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
        
        sensitivity -- the minimum detectable signal power
        nu_min -- the minimum frequency detectable (Hz)
        nu_max -- the maximum frequency detectable (Hz)
        nchannels -- the number of frequency channels in the detector
        
        """
        Parent.__init__(self, position, velocity, strategy, direction_vector, openingangle, starposition, starvelocity,starmass, semimajoraxis, inclination, longascend, mean_anomaly)
        
        self.type = "Observer"
        #self.success_colour = "#377eb8"
        #self.fail_colour = "#ff7f00"
        self.success_colour = "blue"
        self.fail_colour = "red"
        self.colour = self.fail_colour
    
        self.sensitivity = sensitivity
        self.nu_min = nu_min
        self.nu_max = nu_max
        self.nchannels = nchannels
        
        self.detect = {}
    
    def update(self,time,dt):
        """
        Update position, velocity and direction vector of Observer
            
            Keyword Arguments:
            ------------------
            time -- current time (years)
            dt -- timestep (years)
            
        """
        Parent.update(self,time,dt)

    def calculate_doppler_drift(self,time,dt,transmitter):
        """
        Calculate doppler drift of signal received from transmitter object
        
        Keyword Arguments:
        ------------------
        time -- current time (in years)
        dt -- timestep (in years)
        transmitter -- Transmitter object being observed
        
        Returns:
        --------
        delta_freq = change in frequency (Hz)
        
        """
    
        # Calculate relative velocity
        relative_velocity = transmitter.velocity.subtract(self.velocity)
        relative_position = transmitter.position.subtract(self.position)
    
        # radial velocity (in pc yr-1)
        radial_velocity = relative_velocity.dot(relative_position)
        radial_velocity = radial_velocity*pc_yr_to_ms
    
        # frequency shift
        delta_freq = -transmitter.nu*radial_velocity/transmitter.broadcastspeed
 
        return delta_freq
    

    def observe_transmitter(self,time,dt,transmitter):
        """
        Attempt to observe a transmitter, taking into account time delay between transmission and reception, and doppler drift
        
        Keyword Arguments:
        ------------------
        time -- current time (years)
        dt -- timestep (years)
        transmitter -- Transmitter Object
        
        
        Returns:
        --------
        detected -- Is transmitter detected or not? (Boolean)
        
        """

        self.colour = self.fail_colour
             
        # Travel time between observer and transmitter location
        separation = self.position.subtract(transmitter.position)
        distance = separation.mag()
        delay_time = time - distance/transmitter.broadcastspeed
        
        # Cannot detect transmitters before start of run
        if(delay_time <0.0):
            return False

        #
        # 1. Is transmitter beam illuminating observer?
        #
        
        unitsep = separation.unit()

        # Find transmitter target vector given time delay
        
        oldn = transmitter.strategy.get_target(delay_time, dt)
        nt_dot_r = oldn.dot(unitsep)
        observer_illuminated = arccos(nt_dot_r) < transmitter.openingangle

        # Is transmitter in observer field of view?
        no_dot_r = self.n.dot(unitsep.scalarmult(-1.0))
    
        in_observer_field = arccos(no_dot_r) < self.openingangle
        
        # Is signal powerful enough?
        if(self.sensitivity==None):
            signal_powerful_enough =True
        else:
            signal_powerful_enough = transmitter.transmitted_flux(distance,) > self.sensitivity
        
        # Is transmitter actively broadcasting (given time delay)?
        transmitter_broadcasting = transmitter.broadcast(delay_time,dt)
        
        # Is signal in frequency range after Doppler drifting?
        delta_freq = self.calculate_doppler_drift(time,dt,transmitter)
        
        freqmin = transmitter.nu -0.5*transmitter.bandwidth + delta_freq
        freqmax = transmitter.nu +0.5*transmitter.bandwidth + delta_freq

        in_frequency_range = False
        
        if(self.nu_min==None or self.nu_max==None):
            in_frequency_range = True
        else:
            in_frequency_range = freqmin <=self.nu_max and self.nu_min <=freqmax

        detected = observer_illuminated and in_observer_field and signal_powerful_enough and in_frequency_range
        
        if(detected):
            self.colour = self.success_colour
            transmitter.colour = transmitter.success_colour
        
        self.detect[transmitter.ID] = detected
        transmitter.detected[self.ID] = detected

        return detected


    def set_colour(self):
    
        if True in self.detect.values():
            self.colour = self.success_colour
        else:
            self.colour = self.fail_colour
    
    
    def generate_skymap(self, time, agentlist,fullmap=False):
        """
        Given a list of agents, produces a skymap (in standard spherical polar co-ordinates)
        
        Keyword Arguments:
        ------------------
        time -- current time (years)
        dt -- timestep (years)
        fullmap -- Boolean determines type of map:
        
                True - Produce either an all-sky map with observer field of view drawn on. (Requires mpl_toolkits.basemap)
        
                False - Produce a map of observer's field of view only
        """


        # Boolean checks if user wants an all-sky map and has Basemap installed
        plot_fullmap = fullmap and basemap_installed

        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)

        # Set up centre of plot
        # If plotting an all-sky map , get angles in degrees
        # otherwise use radians
        
        r0,theta0,phi0 = self.n.spherical_polars(degrees=plot_fullmap)
        
        # Lists to store agent positions and colours
        thetapoints = []
        phipoints = []
        colourpoints = []

        # If plotting an all-sky map, set up Basemap object and draw parallels/meridians
        if(plot_fullmap):

            parallels = arange(-90,90, 30)
            meridians = arange(-180,180,30)
            parlabels = [True for i in range(len(parallels))]
        
            map = Basemap(projection="moll",lat_0=0, lon_0=0)
            map.drawparallels(parallels, labels=parlabels)
            map.drawmeridians(meridians)
            
        else:

            ax1.set_xlim(phi0-self.openingangle, phi0+self.openingangle)
            ax1.set_ylim(theta0-self.openingangle, theta0+self.openingangle)

        for agent in agentlist:
            # If self is in the list, don't plot!
            if agent.ID==self.ID: continue

            # Find relative position vector (in Cartesian co-ordinates)

            relative_position = agent.position.subtract(self.position)

            # If agent outside the observer's field of view, skip
            if (plot_fullmap==False and arccos(relative_position.unit().dot(self.n)) >self.openingangle):
                continue

            # Convert to spherical polars (if a fullmap, angles will be in degrees)
            r,theta,phi = relative_position.spherical_polars(degrees=plot_fullmap)
            
            # Store data in lists
            thetapoints.append(theta)
            phipoints.append(phi)
            colourpoints.append(agent.colour)
        
        
        # If creating an all-sky map, plot agents and draw a circle representing observer's FoV
        if(plot_fullmap):
            map.scatter(phipoints,thetapoints, color=colourpoints,latlon=True)
            
            xcircle,ycircle = get_circle_outline(phi0, theta0, self.openingangle*180.0/pi)
            xpt,ypt = map(xcircle,ycircle)
            map.scatter(xpt,ypt, color='red', latlon=False, marker='.')
            
            # Note that text location slightly different for all sky maps vs FoV maps
            ax1.text(0.9, 1.3,'Observer '+str(self.ID)+'\nt = '+str(round(time,2))+' yr', bbox=dict(edgecolor='black', facecolor='none'), horizontalalignment='center', verticalalignment='center', transform = ax1.transAxes)
            
        else:
            
            ax1.scatter(phipoints,thetapoints, color=colourpoints)
            ax1.text(0.87, 0.9,'Observer '+str(self.ID)+'\nt = '+str(round(time,2))+' yr', bbox=dict(edgecolor='black', facecolor='none'), horizontalalignment='center', verticalalignment='center', transform = ax1.transAxes)
        
        # save to file
        outputfile = "skymap_"+self.ID+"_time_00"+str(round(time,2))+".png"
        plt.savefig(outputfile)
        plt.close()




  

