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
import agents.vector as vector
from numpy import zeros
import matplotlib.pyplot as plt

class Population:

    def __init__(self,time,dt):
        """Constructor for a group of agents"""

        self.agents = []
        self.time = time
        self.dt = dt

    def add_agent(self, agent):
        """add Agent object to Population"""
        self.agents.append(agent)
    
        self.nagents = len(self.agents)

    def generate_observer_at_origin(self,observe_direction,openangle,strategy):
        """Place a single observer object at co-ordinates (0.0,0.0,0.0)"""
        origin = vector.Vector3D(0.0,0.0,0.0)
        
        self.agents.append(observer.Observer(origin, origin, strategy, observe_direction, openangle, origin, 0.0, 0.0, 0.0))


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

    def conduct_observations(self,time,dt):
        """Loop through all Observers and attempt to observe all Transmitters"""

        success = zeros((self.nagents,self.nagents))
        
        for i in range(self.nagents):
            
            if self.agents[i].type=="Observer":

                for j in range(self.nagents):
                    if (i==j): continue
                
                    if self.agents[j].type=="Transmitter":
                        observed = self.agents[i].observe_transmitter(time,dt,self.agents[j])
                    if(observed):
                            success[i,j]=1

        return success

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

        # Add time to plots TODO
        #ax1.annotate(self.time)
        
        
        if(filename==None):
            plt.show()
        else:
            fig1.savefig(filename)


