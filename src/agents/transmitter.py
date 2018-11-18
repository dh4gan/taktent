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
# self.tbegin - broadcast beginning time
# self.tend - broadcast end time
# self.pulseduration - pulse duration (if 0, does not transmit)
# self.pulseinterval - pulse interval (if 0, continuous)


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
from agents.agent import Agent as Parent

fourpi = 4.0*pi
c = 2.99e8 # speed of light in ms-1

class Transmitter(Parent):

    def __init__(self,position=None,velocity=None,strategy=None,direction_vector=None, openangle=None, starposition=None,starmass=None,semimaj=None,inc=None,mean_anomaly=None, freq=None,band=None, solidangle=None, power=None, polarisation=None, tbegin=None, tend=None, pulseduration=None,pulseinterval=None):
        Parent.__init__(self,position,velocity,strategy,direction_vector,openangle,starposition,starmass,semimaj,inc,mean_anomaly)
        
        self.type="Transmitter"
        
        self.nu = freq
        self.bandwidth = band
        self.solidangle = solidangle
        self.power = power
        self.polarisation = polarisation
        self.tbegin = tbegin
        self.tend = tend
        self.pulseduration = pulseduration
        self.pulseinterval = pulseinterval
        
        self.broadcastspeed = c # assume transmissions move at lightspeed by default
        
        # opening angle = fraction of solid angle (opening angle = pi if solid angle = 4 pi)
        self.openingangle = 0.25*self.solidangle
        
        self.calc_eirp()

    def update(self,time,dt): Parent.update(self,time,dt)

    def calc_eirp(self):
        """Calculate effective isotropic radiated power"""

        self.eirp = self.power*(fourpi)/self.solidangle

    def broadcast(self,time,dt):
        """Is transmitter broadcasting or not?"""


        # If pulse interval not defined or zero, pulse always on

        if(self.pulseinterval==None or self.pulseinterval==0):
            self.active=True
        else:
            # period of pulse = pulse duration + pulse interval
            period = self.pulseduration + self.pulseinterval

            # How many pulse cycles have elapsed (real value)
            nperiods = time/period
        
            # fraction of time pulse is on during a cycle
            onfrac = self.pulseduration/period

            # Pulse is on if remainder of nperiods is less than onfrac
            self.active = mod(nperiods) < onfrac



