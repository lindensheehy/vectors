import math
from Vec2 import Vec2

class Vec3:
    '''
    Class used for 3 dimensional vectors or positions
    Contains functions which allow it to be treated similar to a tuple but with attributes x y z for readability
    '''

    # Constructor
    def __init__(self, x: float, y: float, z: float):
        '''
        Creates an object with a given (x, y, z) as well as a magnitude (length)
        '''

        try:
            self.x = float(x)
            self.y = float(y)
            self.x = float(z)
        except ValueError:
            raise Exception(f"Cannot create Vec3 object with x = {x} ({type(x)}), y = {y} ({type(y)}), and z = {z} ({type(z)})")

        self.magnitude = math.sqrt((x ** 2) + (y ** 2) + (z ** 2))

    # Built in function overrides
    def __repr__(self) -> str:
        '''
        Returns a string representing the Vec3 object
        Runs by default when a Vec3 object gets printed
        '''
        return f"Vec3({self.x}, {self.y}, {self.z})"

    def __hash__(self):
        '''
        Allows sets to properly use Vec3 objects
        '''
        return hash(self.__repr__())

    def __eq__(self, other):
        '''
        Allows Vec3 objects to be compared. If all x, y and z components are the same between the two vectors, it will return True
        '''
        try:
            return (self.x == other.x) and (self.y == other.y) and(self.z == other.z)
        except AttributeError:
            return False

    def __add__(self, other):
        '''
        (Vec3, Vec3) -> Vec3
        Allows Vec3 objects to perform vector addition
        '''
        try:
            x = self.x + other.x
            y = self.y + other.y
            z = self.z + other.z
        except AttributeError:
            raise Exception(f"Cannot add type {type(self)} and type {type(other)} (other should be type Vec3)")
        
        return Vec3(x, y, z)

    def __sub__(self, other):
        '''
        (Vec3, Vec3) -> Vec3
        Allows Vec3 objects to perform vector subtraction
        '''
        try:
            x = self.x - other.x
            y = self.y - other.y
            z = self.z - other.z
        except AttributeError:
            raise Exception(f"Cannot subtract type {type(self)} and type {type(other)} (other should be type Vec3)")

        return Vec3(x, y, z)

    def __mul__(self, other):
        '''
        (Vec3, float) -> Vec3
        Overrides python multiplication to do the vector scale function
        '''

        try:
            factor = float(other)
        except ValueError:
            raise Exception(f"Cannot multiply Vec3 by {other} (type {type(other)}) (should be type int or float)")

        return self.copy().scale(other)

    def __truediv__(self, other: float):
        '''
        (Vec2, float) -> Vec2
        Overrides python division to do vector scale by 1/other
        '''
        try:
            factor = 1 / float(other)
        except ValueError:
            raise Exception(f"Cannot divide Vec2 by {other} (type {type(other)}) (should be type int or float)")
        
        return self.copy().scale(factor)

    def __iter__(self):
        '''
        This function allows the Vec3 object to be treated as a tuple (x, y, z)
        '''
        yield self.x
        yield self.y
        yield self.z

    # Class functions
    def copy(self):
        '''
        Returns a vector with the same components in a new memory location
        '''
        return Vec3(self.x, self.y, self.z)

    def scale(self, factor: float):
        '''
        (Vec3, float) -> Vec3
        Scales the vector by a given factor
        '''

        try:
            self.x *= float(factor)
            self.y *= float(factor)
            self.z *= float(factor)
        except ValueError:
            raise Exception(f"Cannot scale Vec3 by factor of {factor} (type {type(factor)}) (should be type int or float)")
        return self

    def normalise(self, magnitude: float = 1):
        '''
        Changes the magnitude of the vector while keeping the porportions of each component
        '''

        try:
            self.scale( magnitude / self.magnitude )
        except ValueError:
            raise Exception(f"Cannot normalise Vec3 to a magnitude of {magnitude} (type {type(magnitude)}) (should be type int or float)")
        
        return

    def distance_to(self, other):
        '''
        Returns the distance between one position and another
        '''

        if (type(other) != Vec3):
            raise Exception(f"Cannot get distance when other is not a Vec3 object")

        return math.sqrt(((self.x - other.x) ** 2) + ((self.y - other.y) ** 2) + ((self.z - other.z) ** 2))

    def in_bounds(self, bounds: tuple) -> bool:
        '''
        (Vec3, (Vec3, Vec3)) -> bool
        Bounds is given as a tuple of 2 points serving as a min and then max respectively
        Returns True if the given point lies within the bounding box specified
        Returns False otherwise
        '''

        if (len(bounds) != 2):
            raise Exception(f"the list 'bounds' is not of length 2: bounds = {bounds}")

        low = bounds[0]
        high = bounds[1]

        if (type(low) != Vec3) or (type(high) != Vec3):
            raise Exception(f"({low} - {high}) is not a valid set of bounds (both endpoints must be Vec3 objects)")
        
        if (low.x > high.x) or (low.y > high.y) or (low.z > high.z):
            raise Exception(f"Each coordinate of the low endpoint must be less than its high endpoint counterpart. low = {low} , high = {high}")

        return (
            self.x > low.x and
            self.y > low.y and
            self.z > low.z and
            self.x < high.x and
            self.y < high.y and
            self.z < high.z
        )

    def dot_product(self, other) -> float:
        '''
        (Vec3, Vec3) -> float
        Returns the dot product of two vectors
        '''

        if (type(other) != Vec3):
            raise Exception(f"Cannot find dot product of Vec3 and {type(other)}")

        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)
    
    def cross_product(self, other):
        '''
        (Vec3, Vec3) -> Vec3
        Returns the cross product of self and other which will be a vector perpendicular to the given ones
        '''

        if (type(other) != Vec3):
            raise Exception(f"Cannot find dot product of Vec3 and {type(other)}")
        
        x = (self.y * other.z) - (self.z * other.y)
        y = (self.z * other.x) - (self.x * other.z)
        z = (self.x * other.y) - (self.y * other.x)
        return Vec3(x, y, z)

    def angle_to(self, other) -> float:
        '''
        (Vec3, Vec3) -> float
        Returns the angle between 2 vectors in 3d space (along the plane they share)
        '''

        if (type(other) != Vec3):
            raise Exception(f"Cannot find dot product of Vec3 and {type(other)}")
    
        try:
            return math.degrees(math.acos((self.dot_product(other)) / (self.magnitude * other.magnitude)))
        except ZeroDivisionError:
            print("divided by zero")
            return 0

    def rotate(self, yaw: float = 0, pitch: float = 0, around = None):
        '''
        (Vec3, float, float, Vec3) -> Vec3
        Rotates self by a yaw and pitch around some point and returns the new location
        '''

        try:

            if around == None:
                around = Vec3(0, 0, 0)

            if yaw != 0:
                self.x, self.z = Vec2(self.x, self.z).rotate(yaw, Vec2(around.x, around.z))

            # If pitch is not 0, rotate point along the plane shared between the vector and the y axis
            if pitch != 0:

                dist_from_y_axis = math.sqrt((self.x - around.x) ** 2 + (self.z - around.z) ** 2)

                pitch_vec = Vec2(dist_from_y_axis, self.y)
                pitch_vec.rotate(pitch)

                self.x *= pitch_vec.x / dist_from_y_axis
                self.z *= pitch_vec.x / dist_from_y_axis
                self.y = pitch_vec.y

            return self

        except TypeError:
            raise Exception(f"\n{self}.rotate2d(yaw = {yaw}, pitch = {pitch}, around = {around})\nInvalid Arguments")