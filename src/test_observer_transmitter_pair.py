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
freq = 1.0e9
band = 1.0e8
solidangle = pi
power = 100.0

# transmitter strategy: function

def transmit_strategy(time, tinit=0.0, period=12.0):

    omega = 2.0*pi/period
    x_coord = cos(omega*(time-tinit))
    y_coord = sin(omega*(time-tinit))
    z_coord = 0.0
    
    print ("Update: ",time-tinit,period,x_coord, y_coord)

    return vector.Vector3D(x_coord, y_coord, z_coord).unit()


openangle = 0.1*pi

markersize = 0.5
wedge_length = 5.0
xmax = 20
ymax = 20

time = 0.0
dt = 0.1

#strat = scanningStrategy.scanningStrategy(transmit_strategy(time,tinit=0.0,period=10.0))
strat = scanningStrategy.scanningStrategy(transmit_strategy)
strat_obs = strategy.Strategy()

transmitter_dir = vector.Vector3D(0.0,1.0,0.0)
observer_dir = vector.Vector3D(1.0,0.0,0.0).unit()

popn = Population(time)

tran = transmitter.Transmitter(transmitter_pos,transmitter_vel,strat,transmitter_dir,openangle,transmitter_pos.copy(), 1.0,1.0,0.0,1.0,freq,band,solidangle,power)

tran.active = False

popn.generate_observer_at_origin(observer_dir,openangle,strat_obs)
popn.add_agent(tran)




for i  in range(nsteps):

    success = popn.conduct_observations(time,dt)

    popn.plot(markersize,wedge_length, xmax,ymax)
    popn.update_agents(time,dt)

    time = time+dt








