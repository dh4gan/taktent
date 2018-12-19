# Module holds key constants used by all parts of the taktent package

from taktent.agents.vector import Vector3D
from numpy import pi


twopi = 2.0*pi
fourpi = 4.0*pi
piby2 = 0.5*pi

AU = 1.498e11
pc = 3.08e16
year = 3.15e7
c = 2.99e8

c_pc_yr = c*year/pc
AU_to_pc = AU/pc

GmsolAU = fourpi*pi


zero_vector = Vector3D(0.0,0.0,0.0)

