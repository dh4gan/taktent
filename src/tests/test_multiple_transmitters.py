# Test code produces a population of transmitters (with an observer at the origin)
# and tests observer detection algorithms

import sys
sys.path.append('..')

from agents import *
from populations.population import *
from strategies import *
from numpy import pi, cos, sin

# test code imports key classes, makes a transmitter and an observer object, and plots them

time = 0
dt = 0.1
nsteps = 100



#
# 1. Define Observer properties
#

observer_dir = vector.Vector3D(1.0,1.0,0.0).unit()

# function to define observer's target vector
def observing_strategy(time, tinit=0.0, period=12.0):
    
    omega = 2.0*pi/period
    x_coord = cos(omega*(time-tinit))
    y_coord = sin(omega*(time-tinit))
    z_coord = 0.0
    
    return vector.Vector3D(x_coord, y_coord, z_coord).unit()

# scanningStrategy object
strat_obs = scanningStrategy.scanningStrategy(observing_strategy)

openangle = 0.1*pi


#
# 2. Define Population and create observer at origin
#

popn = Population(time,dt)

observerID = popn.generate_observer_at_origin(observer_dir,openangle,strat_obs)


popn.agents[-1].nu_min = 1.0e0
popn.agents[-1].nu_max = 1.0e11


#
# 3. Define properties of transmitter population
#

# Define a scanning transmitter strategy:

# function to define transmitter target vector
def transmit_strategy(time, tinit=0.0, period=12.0):

    omega = 2.0*pi/period
    x_coord = cos(omega*(time-tinit))
    y_coord = sin(omega*(time-tinit))
    z_coord = 0.0

    return vector.Vector3D(x_coord, y_coord, z_coord).unit()

# scanningStrategy object
strat = scanningStrategy.scanningStrategy(transmit_strategy)

# Have ten transmitters with common broadcast properties
# But different spatial locations

N_transmitters=10

semimajoraxis = 1.0
inc = 0.0
mean_anomaly = 0.0
longascend = 0.0
freq = 1.0e10
band = 1.0e10

solidangle = 4.0*pi
power = 100.0

popn.generate_identical_transmitters(N_transmitters=N_transmitters, strategy=strat,semimajoraxis =None, inclination=None, mean_anomaly=None, longascend=None, nu=freq, bandwidth=band, solidangle=solidangle, power=power, spatial_distribution="random_sphere")


# Define plot limits

markersize = 0.5
wedge_length = 2.0
xmax = 20
ymax = 20

# Simulation timestep etc
popn.time = 0
tmax = 20
popn.dt = 0.1

# Initialise population ready for run
popn.initialise()

# Test run multiple steps
for i in range(nsteps):

    print ("Time: ",popn.time)
    popn.conduct_observations()
    
    outputfile = 'population_'+str(i).zfill(3)+'.png'
    popn.plot(markersize,wedge_length, xmax,ymax, outputfile)
    popn.update()

    popn.generate_skymaps()





