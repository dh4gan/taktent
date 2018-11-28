# Test code runs multiple simulations (Monte Carlo Realisation)

import sys
sys.path.append('..')

from agents import *
from populations.population import *
from strategies import *
from numpy import pi, cos, sin


# MCR parameters

nruns = 3

time = 0
dt = 0.1
nsteps = 100

ndetect_MCR = []

# function to define a scanning strategy (observer or transmitter)
def scan_strategy(time, tinit=0.0, period_xy=12.0, period_yz=None, phase_xy=0.0, phase_yz=None):
    
    omega = 2.0*pi/period_xy
    x_coord = cos(omega*(time-tinit)+phase_xy)
    y_coord = sin(omega*(time-tinit)+phase_xy)
    z_coord = 0.0
    
    return vector.Vector3D(x_coord, y_coord, z_coord).unit()



for irun in range(nruns):
    #
    # 1. Define Observer properties
    #

    observer_dir = vector.Vector3D(1.0,1.0,0.0).unit()



    # scanningStrategy object

    observe_scanperiod = 10.0
    strat_obs = scanningStrategy.scanningStrategy(scan_strategy, tinit=0.0, period_xy = observe_scanperiod, phase_xy=0.0)

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

    # Use same scanning strategy, but with its own period
    scanperiod = 10.0
    scanphase = 1.7*pi
    strat = scanningStrategy.scanningStrategy(scan_strategy, tinit = 0.0, period_xy=scanperiod, phase_xy = scanphase)

    # Have ten transmitters with common broadcast properties
    # But different spatial locations

    N_transmitters=10

    semimajoraxis = 1.0
    inc = 0.0
    mean_anomaly = 0.0
    longascend = 0.0
    freq = 1.0e10
    band = 1.0e10

    solidangle = pi
    power = 100.0

    popn.generate_identical_transmitters(N_transmitters=N_transmitters, strategy=strat,semimajoraxis =None, inclination=None, mean_anomaly=None, longascend=None, nu=freq, bandwidth=band, solidangle=solidangle, power=power, spatial_distribution="random_sphere")


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
    
        popn.update()



    # Collect MCR data - what to collect?

    ndetect_MCR.append(popn.ndetect)




