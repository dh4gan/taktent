#
# This class instantiates a group of agents, and drives the simulation
#

# Attributes
#
# agents - list of Agent objects
# time - global time of simulation


# Methods

# generate_transmitters - create a population of Transmitter objects TODO
# generate_observer_at_origin - creates a single Observer at origin TODO
# generate_observers - generate a population of Observer objects TODO
# define_observation_strategies - defines observation survey for all Observer objects TODO
# define_transmitter_strategies - defines transmissions for all Transmitter objects TODO
# conduct_observations - goes through each Observer object and attempts to observe Transmitters TODO
# plot - plots entire population of Agents (Observers & Transmitters)

class Population(Object):

    def __init__(self,t):
        """Constructor for a group of agents"""

        self.agents = []
        self.time = t


    def generate_observer_at_origin(self):
        """Place a single observer object at co-ordinates (0.0,0.0,0.0)"""
        origin = vector.Vector3D(0.0,0.0,0.0)
        
        self.agents.append(Observer(origin,origin)

    def plot(self, markersize, wedge_length):
        """Plot all agents in the system"""
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        
        for agent in self.agents:

            circle, wedge = agent.plot(self,wedge_length)
            ax1.add_patch(circle)
            ax1.add_patch(wedge)

        plt.show()


