# Class instantiates an object which acts as an observer


###############
# Attributes:
###############

# Inherited from agent.py
# self.pos - position (Vector3D)
# self.vel - velocity (Vector3D)
# self.starpos - host star position (Vector3D)
# self.mstar - host star mass
# self.a - semimajor axis of orbit around host star
# self.meananom - mean anomaly

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

# slew_to_target(time,dt) - move target direction vector
# observe_transmitter(time,dt,transmitter) - attempt to detect transmitter

from agents.agent import Agent as Parent
from numpy import sin,cos, arccos

class Observer(Parent):
    
    def __init__(self,position=None,velocity=None,strategy=None, direction_vector=None,openingangle=None, starposition=None,starmass=None,semimaj=None,mean_anomaly=None, sensitivity=None, nu_min=None, nu_max=None, nchannels=None):
        """Initialises an Observer object"""
        Parent.__init__(self,position,velocity,strategy,direction_vector,openingangle,starposition,starmass,semimaj,mean_anomaly)
        
        self.type = "Observer"
    
        self.sensitivity = sensitivity
        self.nu_min = nu_min
        self.nu_max = nu_max
        self.nchannels = nchannels
    

    def slew_to_target(self,time,dt, newtarget):
        """Move observer to target direction"""
        self.n = newtarget

    def calculate_doppler_drift(self,time,dt,transmitter):
        """Calculates doppler shift of signal"""
    
        # Calculate relative velocity
        relative_velocity = transmitter.velocity.subtract(self.velocity)
    
        relative_position = transmitter.position.subtract(self.position)
    
        # radial velocity
        radial_velocity = relative_velocity.dot(relative_position)
    
        # frequency shift
        delta_freq = -transmitter.nu*radial_velocity/transmitter.broadcastspeed

        return delta_freq
    

    def observe_transmitter(self,time,dt,transmitter):
        """Attempt to observe a transmitter (returns true or false)"""

        # Is transmitter beam illuminating observer?
        separation = transmitter.position.subtract(self.position)
        unitsep = separation.unit()

        nt_dot_r = transmitter.n.dot(unitsep)
        observer_illuminated = arccos(nt_dot_r) < transmitter.openingangle

        # Is transmitter in observer field of view?
        no_dot_r = self.n.dot(unitsep)
        print(self.n)
        print(unitsep)
        print (arccos(no_dot_r), self.openingangle)
        in_observer_field = arccos(no_dot_r) < self.openingangle
        
        # Is signal powerful enough?
        if(self.sensitivity==None):
            signal_powerful_enough =True
        else:
            signal_powerful_enough = transmitter.eirp > self.sensitivity
        
        # Is transmitter actively broadcasting?
        # Must take into account time delays
        
        delay_time = time - separation.mag()/transmitter.broadcastspeed
        transmitter_broadcasting = transmitter.broadcast(delay_time,dt)
        
        # Is signal in frequency range after Doppler drifting?
        delta_freq = self.calculate_doppler_drift(time,dt,transmitter)
        
        freqmin = transmitter.nu -0.5*transmitter.bandwidth + delta_freq
        freqmax = transmitter.nu +0.5*transmitter.bandwidth + delta_freq

        if(self.nu_min==None or self.nu_max==None):
            in_frequency_range = True
        else:
            in_frequency_range = freqmin> self.nu_min or freqmax < self.nu_max

        print (observer_illuminated, in_observer_field, signal_powerful_enough)
        return observer_illuminated and in_observer_field and signal_powerful_enough

  

