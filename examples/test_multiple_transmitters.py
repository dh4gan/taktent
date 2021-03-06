# Test code produces a population of transmitters (with an observer at the origin)
# and tests observer detection algorithms

import sys
sys.path.append('..')

from taktent.agents import *
from taktent.populations.population import *
from taktent.strategies import *
from numpy import pi, cos, sin, random

# test code imports key classes, makes a transmitter and an observer object, and plots them

iseed = 10
tbegin = 0
tend = 1.0
dt = 0.1

# function to define a scanning strategy (observer or transmitter)
def scan_strategy(time, tinit=0.0, period_xy=12.0, period_yz=None, phase_xy=0.0, phase_yz=None):
    
    omega = 2.0*pi/period_xy
    x_coord = cos(omega*(time-tinit)+phase_xy)
    y_coord = sin(omega*(time-tinit)+phase_xy)
    z_coord = 0.0
    
    return vector.Vector3D(x_coord, y_coord, z_coord).unit()

#
# 1. Define Observer properties
#

observer_dir = vector.Vector3D(1.0,1.0,0.0).unit()



# scanningStrategy object

observe_scanperiod = 10.0
strat_obs = scanningStrategy.scanningStrategy(scan_strategy, tinit=0.0, period_xy = observe_scanperiod, phase_xy=0.0)

openangle = 0.1*pi


#
# 2. Define Population and create observer
#

popn = Population(tbegin,tend,dt,seed=iseed)

observerID = popn.generate_observer(direction_vector=observer_dir,openingangle=openangle,strategy=strat_obs,semimajoraxis=1.0, nu_min=1.0e0, nu_max=1.0e11, sensitivity=1.0e-23)


#
# 3. Define properties of transmitter population
#

# Use same scanning strategy, but with its own period
scanperiod = 10.0
scanphase = 1.7*pi
strat = scanningStrategy.scanningStrategy(scan_strategy, tinit = 0.0, period_xy=scanperiod, phase_xy = scanphase)

# Have ten transmitters with common broadcast properties
# But different spatial locations

N_transmitters=1000

semimajoraxis = 1.0
inc = 0.0
mean_anomaly = 0.0
longascend = 0.0
freq = 1.0e10
band = 1.0e10

solidangle = 4.0*pi
power = 1.0e18

popn.generate_identical_transmitters(N_transmitters=N_transmitters, strategy=strat,semimajoraxis =None, inclination=None, mean_anomaly=None, longascend=None, nu=freq, bandwidth=band, solidangle=solidangle, power=power, spatial_distribution="GHZ",tbegin=popn.tbegin, tend=popn.tend)

popn.assign_Gaussian_broadcast_parameters(nu_parameters=[1.42e9,1.0e9], solidangle_parameters=[pi,0.5*pi])

popn.assign_Gaussian_strategy_parameters()

# Run simulation
popn.run_simulation(write_detections=True, make_plots=False, allskymap=True)


print ("Distance: ",popn.means["distance"])
print (popn.means["frequency"])
print (popn.means["pulseinterval"])
print (popn.means["pulseduration"])




