#
# This class instantiates a group of agents, and drives the simulation
#

# Attributes
#
# agents - list of Agent objects
# time - global time of simulation


# Methods

# add_agent -- add an agent to the Population
# assign_Gaussian_broadcast_parameters -- randomly sample broadcast parameters from Gaussians
# assign_uniform_broadcast_parameters -- randomly sample broadcast parameters from uniform distributions

# assign_Gaussian_strategy_parameters -- randomly sample strategy parameters from Gaussians

# generate_identical_transmitters - create a population of Transmitter objects
# generate_observer_at_origin - creates a single Observer at origin

# define_agent_strategies - set strategies for all agents
# define_observation_strategies - defines observation strategy for all Observer objects
# define_transmitter_strategies - defines transmission strategy for all Transmitter objects
# update -- update the Population object's attributes
# update_agents -- update all Agents in the Population
# initialise - initialise the Population ready for running simulations

# generate_skymaps -- generate sky maps for all observers in the simulation

# conduct_observations - goes through each Observer object and attempts to observe Transmitters
# plot - plot entire population of Agents (Observers & Transmitters)

import taktent.agents.observer as observer
import taktent.agents.transmitter as transmitter
import taktent.agents.vector as vector
from numpy import zeros, sum, round, random, pi, where, amax, savetxt, vstack, transpose
import matplotlib.pyplot as plt

import itertools

newID = itertools.count(1)

def gaussian_sample(params):
    '''Return sample from a Gaussian distribution with params=[mu,sigma]'''
    return params[1]*random.randn() + params[0]

def uniform_sample(params):
    '''Return sample from a uniform distribution in range given by params=[min,max]'''
    return params[0]+ random.random()*(params[1]-params[0])


class Population:

    def __init__(self, tbegin, tend, dt,index=1,seed=10):
        """
        Constructor for a Population object (group of agents in a simulation)
            
        Keyword Arguments:
        ------------------
        
        index -- a numerical identifier for this simulation (to distinguish multiple simulations)
        tbegin -- beginning time of simulation (years)
        tend -- ending time of simulation (years)
        dt -- timestep (years)
        
        Other Attributes:
        -----------------
        agents -- list of Agent objects in the simulation
        nsteps -- number of simulation timesteps
        istep -- current simulation step
        ndetect -- number of transmission detections at a given timestep (numpy array)
        
        """

        self.ID = str(index).zfill(3)
        self.agents = []
        
        self.tbegin = tbegin
        self.tend = tend
        self.dt = dt
        self.time = tbegin
        self.seed = seed
        random.seed(self.seed)
        
        self.nsteps = int((self.tend-self.tbegin)/self.dt)
        self.istep = 0
        
        self.ndetect = zeros(self.nsteps)
    
        self.means = {}
        self.means["time"] = zeros(self.nsteps)
        self.means["distance"] = zeros(self.nsteps)
        self.means["frequency"] = zeros(self.nsteps)
        self.means["bandwidth"] = zeros(self.nsteps)
        self.means["power"] = zeros(self.nsteps)
        self.means["pulseinterval"] = zeros(self.nsteps)
        self.means["pulseduration"] = zeros(self.nsteps)

    def add_agent(self, agent):
        """
        Add Agent object to Population
        
        Keyword Arguments:
        ------------------
        agent -- Agent object to be added
        
        """
        self.agents.append(agent)
        self.nagents = len(self.agents)
    

    def find_agent(self, ID):
        """
        Search for an agent by its ID, and return it
        
        Keyword Arguments:
        ------------------
        ID - ID number to be returned
        
        Returns:
        --------
        agent - agent corresponding to this ID
        """
    
        targetID = where([a.ID==ID for a in self.agents])[0][0]
        return self.agents[targetID]
    
    
    def calculate_means(self):
        """
        Calculate mean properties of detected Transmitters
    
        Mean properties calculated:
        Distance
        Frequency
        Bandwidth
        Pulse Duration
        Pulse Interval
        
        """
        
        for a in self.agents:
            if a.type=="Observer":
                # Loop over detected transmitters in Observer list
                for key in a.detect.keys():
                    transmitter = self.find_agent(key)
                    
                    self.means["time"][self.istep] = self.time
                    
                    self.means["distance"][self.istep] += transmitter.position.subtract(a.position).mag()/float(self.ndetect[self.istep])

                    self.means["frequency"][self.istep] +=transmitter.nu/float(self.ndetect[self.istep])
                    self.means["bandwidth"][self.istep] +=transmitter.bandwidth/float(self.ndetect[self.istep])
                    self.means["power"][self.istep] +=transmitter.power/float(self.ndetect[self.istep])
                    self.means["pulseduration"][self.istep]+=transmitter.pulseduration/float(self.ndetect[self.istep])
                    self.means["pulseinterval"][self.istep]+=transmitter.pulseinterval/float(self.ndetect[self.istep])





                
    
    
    def assign_Gaussian_broadcast_parameters(self, nu_parameters=[1.42e9,1.0e9], bandwidth_parameters=[1.0e9,1.0e8], solidangle_parameters=[0.1*pi, 0.01*pi], power_parameters=[1.0e20,1.0e15], tbegin_parameters = [0.0, 0.0], tend_parameters=[100.0,0.0], pulseduration_parameters = [1.0,0.1], pulseinterval_parameters=[1.0,0.1] ):
        '''
        Assign broadcast parameters to all transmitters assuming Gaussian distributions
        Each argument contains [mean,stdev] for each broadcast parameter
            
        Keyword Arguments:
        ------------------
        nu_parameters - frequency [mean,stdev]
        bandwidth_parameters - bandwidth [mean,stdev]
        solidangle_parameters - solidangle [mean,stdev]
        power_parameters - power [mean,stdev]
        tbegin_parameters - beginning time [mean,stdev]
        tend_parameters - ending time [mean,stdev]
        pulseduration_parameters - pulse duration [mean,stdev]
        pulseinterval_parameters - pulse interval [mean,stdev]
        '''
    
        for agent in self.agents:
            if(agent.type=="Observer"):
                continue
            agent.nu = gaussian_sample(nu_parameters)
            agent.bandwidth = gaussian_sample(bandwidth_parameters)
            agent.solidangle = gaussian_sample(solidangle_parameters)
            if(agent.solidangle>4.0*pi):
                agent.solidangle = 4.0*pi
            agent.openingangle = 0.25*agent.solidangle
            agent.power = gaussian_sample(power_parameters)
            agent.tbegin = gaussian_sample(tbegin_parameters)
            agent.tend = gaussian_sample(tend_parameters)
            agent.pulseduration = gaussian_sample(pulseduration_parameters)
            agent.pulseinterval = gaussian_sample(pulseinterval_parameters)
                
                
    def assign_Gaussian_strategy_parameters(self,period_xy_parameters=[1.0,0.1], period_yz_parameters=[1.0,0.1], phase_xy_parameters=[pi,0.5*pi], phase_yz_parameters=[pi,0.5*pi]):
        '''
        Assign parameters to scanningStrategy objects belonging to Transmitters in Population
            
        Keyword Arguments:
        -----------------
        period_xy_parameters -- period_xy [mean,stdev]
        period_yz parameters -- period_yz [mean,stdev]
        phase_xy_parameters -- phase_xy [mean,stdev]
        phase_yz parameters -- phase_yz [mean,stdev]
        '''
    
        for agent in self.agents:
            if(agent.type=="Observer"):
                continue
            agent.strategy.period_xy = gaussian_sample(period_xy_parameters)
            agent.strategy.period_yz = gaussian_sample(period_yz_parameters)
            agent.strategy.phase_xy = gaussian_sample(phase_xy_parameters)
            agent.strategy.phase_yz = gaussian_sample(phase_yz_parameters)

    def assign_uniform_broadcast_parameters(self, nu_parameters=[1.0e9,5.0e9], bandwidth_parameters=[1.0e8,1.0e9], solidangle_parameters=[0.0, 4*pi], power_parameters=[1.0e15,1.0e20], tbegin_parameters = [0.0, 0.0], tend_parameters=[100.0,100.0], pulseduration_parameters = [0.1,1.0], pulseinterval_parameters=[0.1,1.0] ):
        '''
        Assign broadcast parameters to all transmitters assuming uniform distributions
        Each argument contains [min,max] for each broadcast parameter
        
        Keyword Arguments:
        ------------------
        nu_parameters - frequency [min,max]
        bandwidth_parameters - bandwidth [min,max]
        solidangle_parameters - solidangle [min,max]
        power_parameters - power [min,max]
        tbegin_parameters - beginning time [min,max]
        tend_parameters - ending time [min,max]
        pulseduration_parameters - pulse duration [min,max]
        pulseinterval_parameters - pulse interval [min,max]
        
        '''
            
        for agent in self.agents:
            if(agent.type=="Observer"):
                continue
            agent.nu = uniform_sample(nu_parameters)
            agent.bandwidth = uniform_sample(bandwidth_parameters)
            agent.solidangle = uniform_sample(solidangle_parameters)
            agent.power = uniform_sample(power_parameters)
            agent.tbegin = uniform_sample(tbegin_parameters)
            agent.tend = uniform_sample(tend_parameters)
            agent.pulseduration = uniform_sample(pulseduration_parameters)
            agent.pulseinterval = uniform_sample(pulseinterval_parameters)
    
    
    def generate_identical_transmitters(self, N_transmitters, strategy,semimajoraxis,inclination,longascend, mean_anomaly, nu, bandwidth, solidangle, power, polarisation=None, tbegin=0.0, tend=100.0, pulseduration=0.0, pulseinterval=0.0, spatial_distribution=None):
        '''
        Generate a population of transmitters with identical broadcast properties,
        distributed in space according to a defined distribution
        
        Keyword Arguments:
        ------------------
        N_transmitters -- number of transmitters
        strategy -- Strategy Object
        semimajoraxis -- orbital semimajor axis (AU)
        inclination -- orbital inclination (radians)
        longascend -- longitude of the ascending node (radians)
        mean_anomaly -- mean anomaly (radians)
        nu -- frequency (Hz)
        bandwidth -- bandwidth (Hz)
        solidangle -- solid angle (radians)
        power -- transmission  power
        polarisation -- signal polarisation
        tbegin -- beginning time of broadcast (years)
        tend -- ending time of broadcast (years)
        pulseduration -- pulse duration (years)
        pulseinterval -- pulse interval (years)
        spatial_distribution -- choice of distribution of transmitters: "GHZ", "random_sphere", "random"
        
        '''
        
        for i in range(N_transmitters):
            # Define a transmitter object with fixed broadcast parameters but no initial position
            agent = transmitter.Transmitter(semimajoraxis = semimajoraxis, inclination=inclination, longascend=longascend, mean_anomaly=mean_anomaly, nu=nu, strategy=strategy.__copy__(), bandwidth=bandwidth, solidangle=solidangle, power=power, polarisation=polarisation, tbegin=tbegin, tend=tend, pulseduration=pulseduration, pulseinterval=pulseinterval)
        
            # Set its position and velocity according to a random sampling
            if(spatial_distribution=="GHZ"):
                agent.sample_GHZ()

            elif(spatial_distribution=="random_sphere"):
                agent.sample_random_sphere()
            
            elif(spatial_distribution=="random" or spatial_distribution==None):
                agent.sample_random()

            agent.orbit(self.time,self.dt)

            # Add to population

            self.add_agent(agent)

    def generate_observer(self, observe_direction, openangle, strategy, spatial_distribution="random_sphere"):
        """Place a single observer object according to a spatial distribution"""
    
        agent = observer.Observer(strategy=strategy, direction_vector=observe_direction, openingangle=openangle,semimajoraxis=None)
    
        # Set its position and velocity according to a random sampling
        if(spatial_distribution=="GHZ"):
            agent.sample_GHZ()
            
        elif(spatial_distribution=="random_sphere"):
            agent.sample_random_sphere()
            
        elif(spatial_distribution=="random" or spatial_distribution==None):
            agent.sample_random()

        self.add_agent(agent)

    def generate_observer_at_origin(self,observe_direction,openangle,strategy):
        """Place a single observer object at co-ordinates (0.0,0.0,0.0)"""
        
        self.add_agent(observer.Observer(strategy=strategy, direction_vector=observe_direction, openingangle=openangle,semimajoraxis=None))
    
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

    
    def run_simulation(self, write_detections=False, make_plots=False, fullskymap=False):
        """
        Run Population detection simulation from beginning to end
        
        Keyword Arguments:
        ------------------
        write_detections - record individual detections to file?
        make_plots       - Plot xy position and skymaps for all Observers?
        fullskymap       - Plot all sky maps for each Observer?
        """
        
        self.initialise()
        for i in range(self.nsteps):
            
            print ("Simulation ID ",self.ID, "Time: ",str(round(self.time,2)))
            self.update(write_detections,make_plots,fullskymap)


        self.write_means_to_file()
    
    def initialise(self):
        """
        Set time to zero, and ensure all Agents in population are correctly up to date
        """
        self.time = 0.0
        self.update_agents()
    
    
    def update(self, write_detections=False, make_plots=False, fullskymap=False):
        """ Update Population attributes"""
        
        self.conduct_observations()
        
        if(write_detections):
            self.record_detections()
        
        if(make_plots):
            outputfile = 'xy_'+str(self.istep).zfill(3)+'.png'
            self.plot(outputfile)
            self.generate_skymaps(fullmap=fullskymap)
    
        self.calculate_means()
        self.update_agents()
        
        self.time = self.time+self.dt
        self.istep = self.istep+1
    
    def update_agents(self):
        """Update the properties of all Agent Objects in the Population"""
        
        self.xmin = 1.0e30
        self.xmax = -1.0e30
        self.ymin = 1.0e30
        self.ymax = -1.0e30
        
        for agent in self.agents:
            agent.update(self.time,self.dt)
            
            if agent.position.x > self.xmax:
                self.xmax = agent.position.x
            
            if agent.position.x < self.xmin:
                self.xmin = agent.position.x
                    
            if agent.position.y > self.ymax:
                self.ymax = agent.position.y

            if agent.position.y < self.ymin:
                self.ymin = agent.position.y


    
    
    def generate_skymaps(self,fullmap=False):
        """
        Generate a map of the sky as seen by every observer
            
        Keyword Arguments:
        ------------------
        fullmap -- Boolean determines type of map:
        
        True - Produce either an all-sky map with observer field of view drawn on. (Requires mpl_toolkits.basemap)
        
        False - Produce a map of observer's field of view only
        """
    
        for agent in self.agents:
            if(agent.type=="Observer"):
                agent.generate_skymap(self.time, self.agents,fullmap=fullmap)
    

    def conduct_observations(self):
        """Loop through all Observers and attempt to observe all Transmitters"""

        self.success = zeros((self.nagents,self.nagents))
        
        for i in range(self.nagents):
            
            if self.agents[i].type=="Observer":
                self.agents[i].detect ={}

                for j in range(self.nagents):
                    if (i==j): continue
                
                    if self.agents[j].type=="Transmitter":
                        observed = self.agents[i].observe_transmitter(self.time,self.dt,self.agents[j])
                        if(observed):
                            self.success[i,j]=1
                            
        self.ndetect[self.istep] = sum(self.success)
        
        for i in range(self.nagents):
            self.agents[i].set_colour()

    def plot(self,filename=None):
        """Plot all agents in the system"""
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        ax1.set_xlim(self.xmin,self.xmax)
        ax1.set_ylim(self.ymin,self.ymax)
        
        
        rmax =amax([self.xmax,self.ymax])
        markersize = 0.03*rmax
        wedge_length = 0.15*rmax
        
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


    def record_detections(self):
        """
        For each Observer, write a file containing all detected Transmitters
        """
            
        for a in self.agents:
            if a.type=="Observer":
                
                outputfile = "Observer_"+a.ID+"_time_00"+str(round(self.time,2))+".detections"
                
                f_obj = open(outputfile, 'w')
                
                f_obj.write("# Type ID x y z nx ny nz nu bandwidth power openingangle pulseduration pulseinterval\n")
                
                for key in a.detect.keys():
                    transmitter = self.find_agent(key)
                    
                    f_obj.write(transmitter.write_to_file())
                        
                f_obj.close()

    def write_means_to_file(self):
        """Write mean population data to file"""

        outputfile = "Population_"+self.ID.zfill(3)+"_meandata.dat"

        header = ""
        first_time = True
        for key,value in self.means.items():
            header = header + " " +key.ljust(10)
            if first_time:
                data = value.transpose()
                first_time=False
            else:
                data = vstack((data, value))
            
        print (data[:,0])
        data = transpose(data)
        print (data[:,0])
        savetxt(outputfile, data, fmt="%10.4e",header=header)
  






