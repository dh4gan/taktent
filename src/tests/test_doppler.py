import sys
sys.path.append('..')

from agents import *
from populations.population import *
from strategies import *
from numpy import pi, cos, sin

# test code imports key classes, makes a transmitter and an observer object, and plots them

time = 0.0
tmin = 0.0
tmax = 1.0
dt = 0.01

nsteps = int((tmax - tmin)/dt)
# Define transmitter properties

transmitter_pos = vector.Vector3D(10.0,0.0,0.0)
transmitter_vel = vector.Vector3D(0.0,0.0,0.0)
transmitter_dir = vector.Vector3D(-1.0,0.0,0.0)
transmitter_a = 1.0         # AU
transmitter_starmass = 1.0  # solarmass
transmitter_inc = 0.0

freq = 1.0e9
band = 0.1
openangle = 0.1*pi
solidangle = 4.0*pi
power = 100.0

# Define a scanning transmitter strategy:

# function to define transmitter target vector (constant)
def transmit_strategy(time):
    return vector.Vector3D(-1.0,0.0,0.0).unit()

# scanningStrategy object
strat = scanningStrategy.scanningStrategy(transmit_strategy)



tran = transmitter.Transmitter(transmitter_pos,transmitter_vel,strat,transmitter_dir,openangle,transmitter_pos.copy(), transmitter_vel.copy(),freq=freq,band=band,solidangle=solidangle,power=power)


transmitter.a = transmitter_a
transmitter.inclination = transmitter_inc
transmitter.mean_anomaly = 0.0
transmitter.longascend = 0.0


# Define Observer properties

observer_dir = vector.Vector3D(1.0,0.0,0.0).unit()
strat_obs = strategy.Strategy()

# Define Population and create observer at origin

popn = Population(time,dt)

observerID = popn.generate_observer_at_origin(observer_dir,openangle,strat_obs)

popn.agents[-1].nu_min = tran.nu*(1.0-6.0e-4)
popn.agents[-1].nu_max = tran.nu*(1.0+6.0e-4)
popn.add_agent(tran)


# Define plot limits

markersize = 0.5
wedge_length = 5.0
xmax = 20
ymax = 20

# Initialise population ready for run
popn.initialise()

# Test run multiple steps
for i in range(nsteps):

    print ("Time: ",popn.time)
    popn.conduct_observations()

    outputfile = 'population_'+str(i).zfill(3)+'.png'
    popn.plot(markersize,wedge_length, xmax,ymax, outputfile)
    popn.update()






