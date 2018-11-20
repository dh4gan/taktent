from agents import *
from populations.population import *
from strategies import *
from numpy import pi, cos, sin

# test code imports key classes, makes a transmitter and an observer object, and plots them

time = 0
dt = 0.1

nsteps = 10

# Define transmitter properties

transmitter_pos = vector.Vector3D(10.0,0.0,0.0)
transmitter_vel = vector.Vector3D(0.0,0.0,0.0)
transmitter_dir = vector.Vector3D(0.0,1.0,0.0)

freq = 1.0e9
band = 1.0e8
openangle = 0.1*pi
solidangle = pi
power = 100.0

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



tran = transmitter.Transmitter(transmitter_pos,transmitter_vel,strat,transmitter_dir,openangle,transmitter_pos.copy(), 1.0,1.0,0.0,1.0,freq,band,solidangle,power)


# Define Observer properties

observer_dir = vector.Vector3D(1.0,0.0,0.0).unit()
strat_obs = strategy.Strategy()


# Define Population and create observer at origin

popn = Population(time,dt)

popn.generate_observer_at_origin(observer_dir,openangle,strat_obs)
popn.add_agent(tran)


# Define plot limits

markersize = 0.5
wedge_length = 5.0
xmax = 20
ymax = 20

time = 0.0
dt = 0.1

# Initialise population ready for run
popn.initialise()

# Test run multiple steps
for i  in range(nsteps):

    print ("Time: ",popn.time)
    success = popn.conduct_observations(time,dt)

    outputfile = 'population_'+str(i).zfill(3)+'.png'
    popn.plot(markersize,wedge_length, xmax,ymax, outputfile)
    popn.update()






