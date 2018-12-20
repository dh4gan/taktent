taktent: a simulator package for testing SETI observational strategies
==============================================
[![DOI](https://zenodo.org/badge/157450057.svg)](https://zenodo.org/badge/latestdoi/157450057)

This Python package allows the user to setup and run an agent-based simulation of a SETI survey.  The package allows the creation of a population of observing and transmitting civilisations.  Each transmitter and observer conducts their activities (pointing and broadcasting) according to an input strategy.  The success of observers and transmitters can then be recorded, and multiple simulations can be run for Monte Carlo Realisation.

This package is therefore a flexible framework in which to simulate and test different SETI strategies, both as an Observer and as a Transmitter.  It is primarily designed with radio SETI in mind, but is sufficiently flexible to simulate all forms of electromagnetic SETI, and potentially neutrino and gravitational wave SETI.

If you want to use this in a publication, please get in touch with me!

![](doc/xymovie.gif)


Features
--------

* Object-oriented, agent-driven simulation of Observers and Transmitters

* Generates agents spatially distributed in random cubes, random spheres and the Galactic Habitable Zone

* Simulates continuous and pulsing broadcasts at a defined beam-size

* Permits transmission/observation strategies as a smooth scan across the sky, or as a series of discrete pointings

* Accounts for Doppler drift due to transmitters/observers orbiting a host star

* Accounts for signal travel time

* Generates maps of the sky as seen from Observers' point of view

* Current presets optimised for electromagnetic signals - can be configured for signals of arbitrary speed and decay behaviour (gravitational waves, neutrinos)


Future Features/Wishlist
------------------------

* Interstellar scintillation/absorption/dispersion, other forms of noise

* Sampling of planetary orbits from exoplanet data

* Plotting library for output MCR data

* Polarisation modelling - parameters included but not implemented in detections


Installation Instructions
--------------------------

This package is hosted on PyPI.  To install with pip:

`> pip install taktent`

The code has been developed in Python 3.6, using numpy 1.14.3 and matplotlib 2.2.2, and hence requires these for basic operation.

If the user wishes to generate all-sky maps for their Observer objects, this will also require `mpl_toolkits.basemap` to be installed.  This is an optional requirement, and the package will function without it (producing field-of-view maps instead).


Examples of Use
-------------------

Examples of how to use `taktent` to set up and conduct SETI simulations can be found in the `examples/` folder.  


Physical Units
-----------------

The "natural" physical units of the package are:

* distance -- parsecs

* time -- years

* speed -- parsecs/year

* frequency -- Hertz

* Power -- Watts

* Flux/Sensitivity -- Watts m^-2


How to Contribute
----------------------

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for details


Package Structure
---------------------

The package contains several modules defining six fundamental classes: 

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


Creating a Simulation
-------------------------

The basic procedure for creating simulations is as follows:

1. Create a `Population` object
2. Create `Strategy` objects for `Transmitter` and `Observer`
3. Generate `Transmitter` objects (either manually or using methods in `Population`)
4. Generate an `Observer` (or multiple `Observer` objects)
5. Run the simulation (with data recorded in the `Population` Object)

Monte Carlo Realisation simulations can then be run by repeating steps 1-5 as many times as necessary.


The Name
---------

The name "taktent" is derived from the Scots phrase "tak tent o' the sma things", which translates as "pay attention to the little things"



 


