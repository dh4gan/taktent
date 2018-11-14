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
# self.openingangle - field of view opening angle
# self.n - target direction vector

###########
# Methods:
###########

# Inherited from agent.py
# orbit(time) - move transmitter in orbit around host star

# slew_to_target(time,dt) - move target direction vector
# observe_transmitter(time,dt,transmitter) - attempt to detect transmitter
# plot - plot observer and its field of view


class Observer(Agent):
    
    def __init__(position,velocity,starposition,starmass,semimaj,mean_anomaly)
        """Initialises an Observer object"""
        Agent.__init__(position,velocity,starposition,starmass,semimaj,mean_anomaly)
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

        nt_dot_r = transmitter.n.dot.(unitsep)
        observer_illuminated = nt_dot_r < cos(transmitter.solidangle)

        # Is transmitter in observer field of view?
        no_dot_r = self.n.dot(unitsep)
        in_observer_field = no_dot_r < cos(observer.openingangle)
        
        # Is signal powerful enough?
        signal_powerful_enough = transmitter.eirp > observer.sensitivity

        return observer_illuminated && in_observer_field && signal_powerful_enough


    def plot(self,radius,wedge_length):
        """Plot observer and observer fov"""
        
        # Plot circle at location of transmitter
        circle = Agent.plot(radius)
        
        # Now plot wedge representing beam
        # central angular direction
        thetamid = arctan2(self.n.y,self.n.x)
        
        if(thetamid <0.0):
            thetamid = 2.0*pi + thetamid
        
        if (self.broadcast):
            beam_distance = wedge_length
        else:
            beam_distance = 0
    
        wedge = Wedge((self.pos.x,self.pos.y), beam_distance, thetamid-self.openingangle, thetamid+self.openingangle )
        
    return circle, wedge

