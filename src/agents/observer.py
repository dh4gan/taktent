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

class Observer(Parent):
    
    def __init__(self,position,velocity,direction_vector,openangle, starposition,starmass,semimaj,mean_anomaly):
        """Initialises an Observer object"""
        Parent.__init__(self,position,velocity,direction_vector,openangle,starposition,starmass,semimaj,mean_anomaly)
        # TODO finish observer constructor
        self.type = "Observer"

    def slew_to_target(self,time,dt, newtarget):
        """Move observer to target direction"""
        self.n = newtarget


    def observe_transmitter(self,time,dt,transmitter):
        """Attempt to observe a transmitter (returns true or false)"""

        # Is transmitter beam illuminating observer?
        separation = transmitter.pos.subtract(self.pos)
        unitsep = separation.unit()

        nt_dot_r = transmitter.n.dot(unitsep)
        observer_illuminated = nt_dot_r < cos(transmitter.solidangle)

        # Is transmitter in observer field of view?
        no_dot_r = self.n.dot(unitsep)
        in_observer_field = no_dot_r < cos(observer.openingangle)
        
        # Is signal powerful enough?
        signal_powerful_enough = transmitter.eirp > observer.sensitivity
        
        # Is transmitter actively broadcasting?
        # Must take into account time delays
        
        delay_time = time - separation/transmitter.broadcastspeed
        transmitter_broadcasting = transmitter.broadcast(delay_time)

        return observer_illuminated and in_observer_field and signal_powerful_enough

  

