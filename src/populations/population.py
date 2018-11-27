#
# This class instantiates a group of agents, and drives the simulation
#

# Attributes
#
# agents - list of Agent objects
# time - global time of simulation


# Methods

# generate_transmitters - create a population of Transmitter objects TODO
# generate_observer_at_origin - creates a single Observer at origin
# generate_observers - create a population of Observer objects TODO
# define_observation_strategies - defines observation strategy for all Observer objects
# define_transmitter_strategies - defines transmission strategy for all Transmitter objects
# conduct_observations - goes through each Observer object and attempts to observe Transmitters
# plot - plots entire population of Agents (Observers & Transmitters)

import agents.observer as observer
import agents.transmitter as transmitter
import agents.vector as vector
from numpy import zeros
import matplotlib.pyplot as plt

from numpy import round
from numpy.random import random

class Population:

    def __init__(self,time,dt):
        """Constructor for a group of agents"""

        self.agents = []
        self.time = time
        self.dt = dt
    
        self.ndetect = []
    

    def add_agent(self, agent):
        """add Agent object to Population"""
        self.agents.append(agent)
    
        self.nagents = len(self.agents)
    
    # TODO - these probably belong in Agent?
    def sample_random(self,seed=-45, xmin=-100.0,xmax=100.0,ymin=-100.0,ymax=100.0,zmin=-100.0,zmax=100.0):
        """Return randomly sampled position and velocity vectors (vmag = 0.1 posmag)"""
    
        position = vector.Vector3D(xmin+ (xmax-xmin)*random(), ymin+(ymax-ymin)*random(), zmin+ (zmax-zmin)*random())

        velocity = vector.Vector3D(random(), random(), random())

        velocity = velocity.scalarmult(0.1*position.mag())

        return position,velocity
    
    
    def sample_GHZ(self):
        '''Returns position and velocity vector of a star in the GHZ'''
    # TODO copy in GHZ sampler from C++ methods
    
    
    def sample_globular(self):
        '''Returns position and velocity vector of a star in a globular cluster'''
    
    def generate_identical_transmitters(self, N_transmitters, strategy,semimajoraxis,inc,mean_anomaly,freq,band,solidangle,power,polarisation,tbegin,tend,pulseduration,pulseinterval,spatial_distribution=None):
        '''Generate a population of identical transmitters according to some spatial distribution'''

#zeroVector = vector.Vector3D(0.0,0.0,0.0)
        
        # Define a transmitter object with fixed broadcast parameters but no
        agent = transmitter.Transmitter(freq=freq,band=band,solidangle=solidangle,power=power,polarisation=polarisation,tbegin=tbegin,tend=tend,pulseduration=pulseduration,pulseinterval=pulseinterval)
        

        # Set its position and velocity according to a random sampling
        if(distribution=="GHZ"):
            position,velocity = self.sample_GHZ()

        elif(distribution=="globular"):
            position,velocity = self.sample_globular()

        elif(distribution=="random" or distribution==None):
            position, velocity = self.sample_random()

        agent.starposition = position
        agent.star_velocity = velocity

        agent.orbit()

# Add to population

        self.add_agent(agent)


    def generate_observer_at_origin(self,observe_direction,openangle,strategy):
        """Place a single observer object at co-ordinates (0.0,0.0,0.0)"""
        
        
        self.add_agent(observer.Observer(strategy=strategy, direction_vector=observe_direction, openingangle=openangle,semimaj=None))
    
        return self.agents[-1].ID


    def define_agent_strategies(self,strategy,agentType):
        """Define strategies of agents in the population (where they are type agentType)"""
        for agent in self.agents:
            if(agent.type==agentType or agentType==None):
                agent.define_strategy(strategy)

    def define_transmitter_strategies(self,strategy):
        """Define strategies of transmitters"""
        self.define_agent_strategies(self,strategy,"Transmitter")
    
    def define_observation_strategies(self,strategy):
        """Define strategies of observers"""
        self.define_agent_strategies(self,strategy,"Observer")
    
    
    def update(self):
        self.update_agents()
        self.time = self.time+self.dt
    
    def update_agents(self):
        '''Update the properties of all Agent Objects in the Population'''
        
        for agent in self.agents:
            agent.update(self.time,self.dt)

    def initialise(self):
        '''Set time to zero, and ensure all Agents in population are correctly up to date'''
        self.time = 0.0
        self.update_agents()
    
    
    def generate_skymaps(self):
        """Generate a map of the sky as seen by every observer"""
    
        for agent in self.agents:
            if(agent.type=="Observer"):
                agent.generate_skymap(self.time, self.agents)
    

    def conduct_observations(self):
        """Loop through all Observers and attempt to observe all Transmitters"""

        self.success = zeros((self.nagents,self.nagents))
        
        for i in range(self.nagents):
            
            if self.agents[i].type=="Observer":

                for j in range(self.nagents):
                    if (i==j): continue
                
                    if self.agents[j].type=="Transmitter":
                        observed = self.agents[i].observe_transmitter(self.time,self.dt,self.agents[j])
                    if(observed):
                            self.success[i,j]=1

    def plot(self, markersize, wedge_length,xmax,ymax, filename=None):
        """Plot all agents in the system"""
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        ax1.set_xlim(-xmax,xmax)
        ax1.set_ylim(-ymax,ymax)
        
        for agent in self.agents:
            circle, wedge = agent.plot(markersize,wedge_length)
            ax1.add_patch(circle)
            
            # If actively transmitting/receiving, plot transmission/reception beam
            if(agent.active): ax1.add_patch(wedge)

        # Add time to plots
        ax1.text(0.9, 0.9,'t = '+str(round(self.time,2))+' yr', bbox=dict(edgecolor='black', facecolor='none'), horizontalalignment='center', verticalalignment='center', transform = ax1.transAxes)
        
        
        if(filename==None):
            plt.show()
        else:
            fig1.savefig(filename)

        plt.close()


