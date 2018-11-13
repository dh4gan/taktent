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
# self.solidangle - solid angle of broadcast
# self.n - direction vector of broadcast (Vector3D)

# self.power - broadcast power
# self.eirp - effective isotropic radiated power
# self.polarisation - broadcast polarisation
# self.tzero - broadcast beginning time
# self.pulsefreq - pulse frequency (if 0, continuous)
# self.tend - broadcast end time

###########
# Methods:
###########

# Inherited from agent.py
# orbit(mstar,a) - move transmitter in orbit around a star at starpos

# set_broadcast_direction - set self.n
# calc_eirp - calculate effective isotropic radiated power
# broadcast(time,dt) - determine if transmitter is transmitting


class Transmitter(Agent):

    def __init__(position,velocity,starposition,starmass,semimaj,mean_anomaly)
        Agent.__init__(position,velocity,starposition,starmass,semimaj,mean_anomaly)

        self.type="Transmitter"



