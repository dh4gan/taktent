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

# Inherited from agent.py
# orbit(time) - move observer in orbit around host star
# plot(radius,wedge_length) - plot observer and its field of view

# observe_transmitter(time,dt,transmitter) - attempt to detect transmitter
# skymap - generate a field of view image along observer's current target vector

from agents.agent import Agent as Parent
from numpy import sin,cos, arccos, pi, arctan2, round, amin,amax
from agents.vector import Vector3D
import matplotlib.pyplot as plt

piby2 = 0.5*pi
zero_vector = Vector3D(0.0,0.0,0.0)

pc_yr_to_ms = 3.08e16/3.15e7

class Observer(Parent):
    
    def __init__(self,position=zero_vector, velocity=zero_vector, strategy=None, direction_vector=zero_vector, openingangle=piby2, starposition=zero_vector, starvelocity=zero_vector, starmass=1.0, semimajoraxis=1.0, inclination=0.0, longascend=0.0,mean_anomaly=0.0, sensitivity=None, nu_min=1.0e9, nu_max=2.0e9, nchannels=1.0e6):
        
        """Initialises an Observer object"""
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
        """Update Observer position, velocity and other properties"""
        Parent.update(self,time,dt)
    

    def slew_to_target(self,time,dt, newtarget):
        """Move observer to target direction"""
        self.n = newtarget

    def calculate_doppler_drift(self,time,dt,transmitter):
        """Calculate doppler shift of signal received from transmitter object"""
    
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
        """Attempt to observe a transmitter (returns true or false)
            Must take care to account for time delay between transmission and reception"""



        self.colour = self.fail_colour
             
        # Travel time between observer and transmitter location
        separation = self.position.subtract(transmitter.position)
        delay_time = time - separation.mag()/transmitter.broadcastspeed

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
            signal_powerful_enough = transmitter.eirp > self.sensitivity
        
        # Is transmitter actively broadcasting?
        # Must take into account time delays
        
  
        transmitter_broadcasting = transmitter.broadcast(delay_time,dt)
        
        print (transmitter_broadcasting, delay_time, transmitter.broadcast(time,dt))
        
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
    
    
    def generate_skymap(self, time, agentlist):
        """Given a list of agents, produces a skymap"""

        # Skymap - plane with normal=self.n

        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        ax1.set_xlim(-self.openingangle, self.openingangle)
        ax1.set_ylim(-self.openingangle, self.openingangle)

        for agent in agentlist:
            # If self is in the list, don't plot!
            if agent.ID==self.ID: continue

            relative_position = agent.position.subtract(self.position)
            
            # If outside the observer's field of view, skip
            if arccos(relative_position.unit().dot(self.n)) >self.openingangle:
                continue
                        
            # Distance between self and agent
            distance = relative_position.mag()
            
            # Get x,y co-ordinates on plane via projection
            projected_position = agent.position.subtract(self.n.scalarmult(agent.position.dot(self.n)))

            # Angular co-ordinates found via trig
            theta_x = arctan2(projected_position.x, distance)
            theta_y = arctan2(projected_position.y, distance)
            
            ax1.scatter(theta_x,theta_y, color = agent.colour, s=50)
        
        ax1.text(0.9, 0.9,'t = '+str(round(time,2))+' yr', bbox=dict(edgecolor='black', facecolor='none'), horizontalalignment='center', verticalalignment='center', transform = ax1.transAxes)
        outputfile = "skymap_"+self.ID+"_time_00"+str(round(time,2))+".png"
        fig1.savefig(outputfile)
        plt.close()




  

