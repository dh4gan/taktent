#
# Test code creates an observer and transmitter pair
# Observer has a fixed pointing
# Transmitter sweeps its beam with a given period
# Simulation is plotted to file
#

import sys
sys.path.append('..')

from taktent.agents import *
from taktent.populations.population import *
from taktent.strategies import *
from numpy import pi, cos, sin

# Simulation timestep etc
tbegin = 0.0
tend = 20
dt = 0.1
iseed = 20

#
# 1. Define transmitter properties
#

transmitter_pos = vector.Vector3D(10.0,0.0,0.0)
transmitter_vel = vector.Vector3D(0.0,0.0,0.0)
transmitter_dir = vector.Vector3D(0.0,1.0,0.0)

freq = 1.0e9
band = 1.0e8
openangle = 0.1*pi
solidangle = pi
power = 100.0

# Define a scanning transmitter strategy:
# First, function to define transmitter target vector (sweeps x-y plane with a given period)

def transmit_strategy(time, tinit=0.0, period_xy=12.0, period_yz=None, phase_xy = 0.0, phase_yz=None):

    omega = 2.0*pi/period_xy
    x_coord = cos(omega*(time-tinit))
    y_coord = sin(omega*(time-tinit))
    z_coord = 0.0

    return vector.Vector3D(x_coord, y_coord, z_coord).unit()


# Create scanningStrategy object
scanperiod = 5.0
strat = scanningStrategy.scanningStrategy(transmit_strategy, tinit = 0.0, period_xy=scanperiod, phase_xy=0.0)


# Create transmitter object
tran = transmitter.Transmitter(position=transmitter_pos,velocity=transmitter_vel,strategy=strat,direction_vector=transmitter_dir,starposition=transmitter_pos.copy(), starvelocity = transmitter_vel.copy(),nu=freq,bandwidth=band,solidangle=solidangle,power=power, tbegin=0.0, tend = 10.0, pulseduration = 0.1, pulseinterval=0.7)



#
# 2. Define Observer properties
#


# Observer points along x-direction

observer_dir = vector.Vector3D(1.0,0.0,0.0).unit()

# Blank strategy = pointing fixed
strat_obs = strategy.Strategy()

#
# 3. Define Population object and create observer at origin
#

popn = Population(tbegin,tend,dt,seed =iseed)

observerID = popn.generate_observer(direction_vector=observer_dir,openingangle=openangle,strategy=strat_obs)

# Add a single agent
popn.add_agent(tran)


#
# 4. Run simulation
#

# Run simulation
popn.run_simulation(write_detections=True, make_plots=False, allskymap=True)










