tak-tent: a simulator for (radio) SETI
======================================

This Python code (in development) runs an agent-based simulation of a SETI survey.  A population of observing and transmitting civilisations is created, and the success of observers in detecting transmitters can be measured. The intention is to develop a flexible code capable of Monte Carlo Realisation.  This will allow observation strategies to be tested, and to determine what types of transmitter can be detected for a given survey mode.

The Code
--------

The code contains several packages defining six fundamental classes: 

### `agents/`

`Vector3D` - a 3D cartesian vector class

`Agent` - a generic agent base class

        `Transmitter(Agent)` - a transmitting civilisation

        `Observer(Agent)` - an observing civilisation
 
### `strategies/`

`Strategy` - a base class that defines generic targeting behaviour of an agent as a function of time

               `PointingStrategy(Strategy)` - A discrete pointing strategy (defined by a list of target vectors)
               `scanningStrategy(Strategy)` - A continuous pointing strategy (defined by a target vector function)

### `population/`

`Population` - a class that defines the combined population of Transmitters and Observers, and drives the simulation

Code dependencies
-----------------

The code has been developed in Python 3.6, using numpy 1.14.3 and matplotlib 2.2.2

The Name
---------

The name "tak-tent" is derived from the Scots phrase "tak tent o' the sma things", which translates as "pay attention to the little things"



 


