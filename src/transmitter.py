# Defines a class instantiating a transmitting civilisation
# Class built assuming transmission via electromagnetic radiation

###############
# Attributes:
###############


# Inherited from agent.py:

# self.pos - position (Vector3D)
# self.vel - velocity (Vector3D)
# self.starpos - host star position (Vector3D)
# self.mstar - host star mass
# self.a - semimajor axis of orbit around host star
# self.meananom - mean anomaly

# self.nu - central frequency of broadcast
# self.bandwidth - bandwidth of broadcast
# self.openingangle - opening angle of broadcast
# self.solidangle - solid angle of broadcast
# self.n - direction vector of broadcast (Vector3D)

# self.power - broadcast power
# self.eirp - effective isotropic radiated power
# self.polarisation - broadcast polarisation
# self.tzero - broadcast beginning time
# self.pulseduration - pulse duration (if 0, does not transmit)
# self.pulseinterval - pulse interval (if 0, continuous)
# self.tend - broadcast end time

###########
# Methods:
###########

# Inherited from agent.py
# orbit(mstar,a) - move transmitter in orbit around a star at starpos
# plot(self,radius) - plot transmitter and its beam

# set_broadcast_direction - set self.n
# calc_eirp - calculate effective isotropic radiated power
# broadcast(time,dt) - determine if transmitter is transmitting

from numpy import pi,mod,arctan2

fourpi = 4.0*pi

class Transmitter(Agent):

    def __init__(position,velocity,starposition,starmass,semimaj,mean_anomaly)
        Agent.__init__(position,velocity,starposition,starmass,semimaj,mean_anomaly)
        # TODO finish transmitter constructor
        self.type="Transmitter"
        self.broadcast = false
        
        # opening angle = fraction of solid angle (opening angle = pi if solid angle = 4 pi)
        self.openingangle = 0.25*self.solidangle
        
        self.calc_eirp()

    def calc_eirp(self):
        """Calculate effective isotropic radiated power"""

        self.eirp = self.power*(fourpi)/self.solidangle

    def broadcast(time,dt):
        """Is transmitter broadcasting or not?"""

        # period of pulse = pulse duration + pulse interval
        period = self.pulseduration + self.pulseinterval

        # How many pulse cycles have elapsed (real value)
        nperiods = time/period
        
        # fraction of time pulse is on during a cycle
        onfrac = self.pulseduration/period

        # Pulse is on if remainder of nperiods is less than onfrac
        self.broadcast = mod(nperiods) < onfrac


    def plot(self,radius,wedge_length):
        """Plot transmitter and transmitter beam"""

        # Plot circle at location of transmitter
        circle = Agent.plot(radius)

        # Now plot wedge representing beam
        # central angular direction
        thetamid = arctan2(self.n.y,self.n.x)

        if(thetamid <0.0):
            thetamid = 2.0*pi + thetamid
        
        if (self.broadcast):
            broadcast_distance = wedge_length
        else:
            broadcast_distance = 0
        
        wedge = Wedge((self.pos.x,self.pos.y), broadcast_distance, thetamid-self.openingangle, thetamid+self.openingangle )

        return circle, wedge

