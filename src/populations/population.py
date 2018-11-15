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
# generate_observers - generate a population of Observer objects TODO
# define_observation_strategies - defines observation survey for all Observer objects TODO
# define_transmitter_strategies - defines transmissions for all Transmitter objects TODO
# conduct_observations - goes through each Observer object and attempts to observe Transmitters
# plot - plots entire population of Agents (Observers & Transmitters)

import agents.observer as observer
import agents.vector as vector
from numpy import zeros
import matplotlib.pyplot as plt

class Population:

    def __init__(self,t):
        """Constructor for a group of agents"""

        self.agents = []
        self.time = t

    def add_agent(self, agent):
        """add Agent object to Population"""
        self.agents.append(agent)
    
        self.nagents = len(self.agents)

    def generate_observer_at_origin(self,observe_direction,openangle ):
        """Place a single observer object at co-ordinates (0.0,0.0,0.0)"""
        origin = vector.Vector3D(0.0,0.0,0.0)
        
        self.agents.append(observer.Observer(origin,origin,observe_direction,openangle,origin,0.0,0.0,0.0))


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

    def plot(self, markersize, wedge_length,xmax,ymax):
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

        plt.show()


