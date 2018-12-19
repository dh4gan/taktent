# Example use of taktent for science
# Explore 100 transmitters inside the Galactic Habitable Zone
# All transmitters emit isotropically, with uniform distribution of transmission parameters

import sys
sys.path.append('..')

from taktent.agents import *
from taktent.populations.population import *
from taktent.strategies import *
from numpy import pi, cos, sin, random


iseed = 10
nruns=4
tbegin = 0
tend = 10.0
dt = 0.1

# function to define a scanning strategy for the observer
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


    #
    # Define scanningStrategy object
    #

    observe_scanperiod = 10.0
    strat_obs = scanningStrategy.scanningStrategy(scan_strategy, tinit=0.0, period_xy = observe_scanperiod, phase_xy=0.0)

    openangle = 0.1*pi


    #
    # 2. Define Population and create observer
    #

    popn = Population(tbegin,tend,dt,index=irun,seed=iseed)

    observerID = popn.generate_observer(direction_vector=observer_dir,openingangle=openangle,strategy=strat_obs, spatial_distribution="GHZ", nu_min=1.0e0, nu_max=1.0e11,sensitivity=0.0,semimajoraxis=1.0)


    #
    # 3. Define properties of transmitter population
    #

    N_transmitters=1000
    freq = 1.0e10
    band = 1.0e10
    solidangle = 4.0*pi
    power = 1.0e18

    # Generate identical transmitters spatially distributed
    popn.generate_identical_transmitters(N_transmitters=N_transmitters, strategy=strat_obs,semimajoraxis =None, inclination=None, mean_anomaly=None, longascend=None, nu=freq, bandwidth=band, solidangle=solidangle, power=power, spatial_distribution="GHZ",tbegin=popn.tbegin, tend=popn.tend)

    # Randomly assign broadcast parameters
    popn.assign_uniform_broadcast_parameters(nu_parameters=[1.40e9,1.5e9], bandwidth_parameters=[1.0e0,1.0e1], pulseduration_parameters=[0.1,5.0], pulseinterval_parameters=[0.1,5.0], power_parameters=[1.0e17,1.0e18])

    # Run simulation
    popn.run_simulation(write_detections=True, make_plots=False, allskymap=True,delay_time=False)


    print ("Number of Detections: ",popn.ndetect)
    print ("Mean Distance: ",popn.means["distance"])
    print ("Mean Frequency: ",popn.means["frequency"])
    print ("Mean Pulse Duration: ",popn.means["pulseduration"])
    print ("Mean Pulse Interval: ",popn.means["pulseinterval"])




