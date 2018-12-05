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
from numpy import cos,sin,arccos,arctan2, pi, sign

class Vector3D(object):
    """3D cartesian vector object"""
    
    def __init__(self,x,y,z):
        """
        Constructs 3D cartesian vector
        Keyword Arguments:
        ------------------
        x -- x co-ordinate
        y -- y co-ordinate
        z -- z co-ordinate
        """
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        """
        Print vector as a string
        """
        
        s= '3D Vector ( %f, %f, %f)' % (self.x, self.y, self.z)
        return s

# Vector addition

    def copy(self):
        """
        Return a copy of Vector3D object
        """
        return Vector3D (self.x, self.y, self.z)
            
    def add(self,other):
        """
        Returns self + other
        
        Keyword Arguments:
        ------------------
        other -- Vector3D
        
        Returns:
        --------
        self+other
        """
        return Vector3D (self.x + other.x, self.y + other.y, self.z + other.z)
            
# Vector subtraction
            
    def subtract(self,other):
        """
        Returns self - other
        
        Keyword Arguments:
        ------------------
        other -- Vector3D
        
        Returns:
        --------
        self-other
        """
        
        return Vector3D (self.x - other.x, self.y - other.y, self.z - other.z)
            
    def scalarmult(self, num):
        """
        Returns self*num
            
        Keyword Arguments:
        ------------------
        num -- Scalar
            
        Returns:
        --------
        self*num
        """
 
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


# Rotate about x-axis

    def rotate_x(self, angle):
        """Returns vector rotated by angle radians around x axis"""

        xnew = self.x
        ynew = self.y*cos(angle) - self.z*sin(angle)
        znew = self.y*sin(angle) + self.z*cos(angle)

        return Vector3D(xnew, ynew, znew)

# Rotate about y-axis

    def rotate_y(self, angle):
        """Returns vector rotated by angle radians around y axis"""
        
        xnew = self.x*cos(angle) + self.y*sin(angle)
        ynew = self.y
        znew = -self.x*sin(angle) + self.z*cos(angle)
        
        return Vector3D(xnew, ynew, znew)

# Rotate about z-axis

    def rotate_z(self, angle):
        """Returns vector rotated by angle radians around z axis"""
        
        xnew = self.x*cos(angle) - self.y*sin(angle)
        ynew = self.x*sin(angle) + self.y*cos(angle)
        znew = self.z
        
        return Vector3D(xnew, ynew, znew)

# Get spherical polar coordinates

    def spherical_polars(self,degrees=False):
        """ Return vector components in spherical polars
            
            Keyword Arguments:
            ------------------
            degrees -- return angles in degrees? (boolean)
            

            Returns:
            --------
            r - r component
            theta - theta component
            phi - phi component
        """

        r = self.mag()
        
        # Theta in range [-pi/2,pi/2]
        theta = arccos(self.z/r) - 0.5*pi
    
        # Phi in range [-pi,pi]
        phi = arctan2(self.y,self.x)
        
        if(degrees):
            theta = theta*180.0/pi
            phi = phi*180.0/pi

        return r,theta,phi



    
    
