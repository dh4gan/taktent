# Test code runs multiple simulations (Monte Carlo Realisation)

import sys
sys.path.append('..')

from taktent.agents import *
from taktent.populations.population import *
from taktent.strategies import *
from numpy import pi, cos, sin, sum


# MCR parameters

nruns = 3
runseed = 4
tbegin = 0
tend = 20
dt = 0.1

ndetect_MCR = []
ntotal_MCR = []

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

    runseed = runseed + irun
    observer_dir = vector.Vector3D(1.0,1.0,0.0).unit()


    # scanningStrategy object

    observe_scanperiod = 10.0
    strat_obs = scanningStrategy.scanningStrategy(scan_strategy, tinit=0.0, period_xy = observe_scanperiod, phase_xy=0.0)

    openangle = 0.1*pi


    #
    # 2. Define Population and create observer at origin
    #

    popn = Population(tbegin,tend,dt,seed=runseed)

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

    N_transmitters=100

    semimajoraxis = 1.0
    inc = 0.0
    mean_anomaly = 0.0
    longascend = 0.0
    freq = 1.0e10
    band = 1.0e10

    solidangle = 4.0*pi
    power = 100.0

    popn.generate_identical_transmitters(N_transmitters=N_transmitters, strategy=strat,semimajoraxis =None, inclination=None, mean_anomaly=None, longascend=None, nu=freq, bandwidth=band, solidangle=solidangle, power=power, spatial_distribution="random_sphere",tbegin=popn.tbegin, tend=popn.tend)

    # Initialise population ready for run
    popn.initialise()

    # Test run multiple steps
    for i in range(popn.nsteps):

        print ("Time: ",popn.time)
        popn.conduct_observations()
        popn.update()

    # Collect MCR data - what to collect?

    ndetect_MCR.append(popn.ndetect)
    ntotal_MCR.append(sum(popn.ndetect))


# End of MCR runs

print (ntotal_MCR)
print (ndetect_MCR)




