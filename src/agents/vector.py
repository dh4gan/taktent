# Class defines a 3D cartesian vector
# along with methods defining basic vector operations

# Attributes:
# self.x = x co-ordinate
# self.y = y co-ordinate
# self.z = z co-ordinate

# Methods
# add - add two vectors
# subtract - subtract two vectors
# scalarmult - multiply by a scalar
# mag - magnitude of a vector
# unit - calculate unit vector
# dot - calculate scalar product
# cross - calculate vector product

import math

class Vector3D(object):
    """3D cartesian vector object"""
# Initialising Function
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        s= '3D Vector ( %f, %f, %f)' % (self.x, self.y, self.z)
        return s

# Vector addition

    def copy(self):
        '''Return a copy of vector3D object'''
        return Vector3D (self.x, self.y, self.z)
            
    def add(self,other):
        """ Adds another vector"""
        return Vector3D (self.x + other.x, self.y + other.y, self.z + other.z)
            
# Vector subtraction
            
    def subtract(self,other):
        """ Subtracts another vector"""
        return Vector3D (self.x - other.x, self.y - other.y, self.z - other.z)
            
    def scalarmult(self, num):
        """ Multiplies vector by scalar"""
        return Vector3D (num*self.x, num*self.y,num*self.z)

# Magnitude of the Vector
    
    def mag(self):
        """ Takes magnitude of the vector"""
        mag = math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        return mag
    
# Unit Vector

    def unit(self):
        """Returns unit vector"""
        return self.scalarmult(1.0/self.mag())

# Scalar Product
            
    def dot(self,other):
        """Returns dot product self.other"""
        dotproduct = 0.0
        dotproduct += self.x*other.x
        dotproduct += self.y*other.y
        dotproduct += self.z*other.z
        return dotproduct
    
# Vector Product

    def cross(self,other):
        """Returns vector product self x other"""
        xcross = self.y*other.z - self.z*other.y
        ycross = -self.x*other.z + self.z*other.x
        zcross = self.x*other.y - self.y*other.x

        return Vector3D(xcross,ycross,zcross)

    
    
