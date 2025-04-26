import numpy as np

class VectorOperations:
    @staticmethod
    def validate_coordinates(coord1, coord2, coord3=None):
        coords = [coord1, coord2]
        if coord3 is not None:
            coords.append(coord3)
        for coord in coords:
            if not isinstance(coord, np.ndarray):
                raise ValueError("Coordinates must be numpy arrays.")
            if coord.shape != (3,):
                raise ValueError("Coordinates must be 3D.")

    @staticmethod
    def add(coord1, coord2, type1, type2):
        VectorOperations.validate_coordinates(coord1, coord2)
        if type1 == "Point" and type2 == "Point":
            raise ValueError("Addition not allowed between two points.")
        return coord1 + coord2

    @staticmethod
    def subtract(coord1, coord2, type1, type2):
        VectorOperations.validate_coordinates(coord1, coord2)
        if type1 == "Point" and type2 == "Vector":
            raise ValueError("Cannot subtract vector from point.")
        return coord1 - coord2

    @staticmethod
    def dot_product(coord1, coord2, type1, type2):
        VectorOperations.validate_coordinates(coord1, coord2)
        if type1 == "Point" or type2 == "Point":
            raise ValueError("Dot product requires two vectors.")
        return np.dot(coord1, coord2)

    @staticmethod
    def cross_product(coord1, coord2, type1, type2):
        VectorOperations.validate_coordinates(coord1, coord2)
        if type1 == "Point" or type2 == "Point":
            raise ValueError("Cross product requires two vectors.")
        return np.cross(coord1, coord2)

    @staticmethod
    def plane_equation(coord1, coord2, coord3, type1, type2, type3):
        VectorOperations.validate_coordinates(coord1, coord2, coord3)
        
        # Initialize normal vector
        normal = None
        
        # Case 1: Three points
        if type1 == "Point" and type2 == "Point" and type3 == "Point":
            vec1 = coord2 - coord1
            vec2 = coord3 - coord1
            normal = np.cross(vec1, vec2)
            point = coord1
        # Case 2: One point and two vectors
        elif type1 == "Point" and type2 == "Vector" and type3 == "Vector":
            normal = np.cross(coord2, coord3)
            point = coord1
        elif type2 == "Point" and type1 == "Vector" and type3 == "Vector":
            normal = np.cross(coord1, coord3)
            point = coord2
        elif type3 == "Point" and type1 == "Vector" and type2 == "Vector":
            normal = np.cross(coord1, coord2)
            point = coord3
        else:
            raise ValueError("Plane equation requires three points or one point and two vectors.")

        # Check if normal is zero (collinear points/vectors)
        if np.allclose(normal, 0):
            raise ValueError("Points are collinear or vectors are parallel, cannot define a plane.")

        # Plane equation: ax + by + cz = d, where normal = [a, b, c]
        a, b, c = normal
        d = np.dot(normal, point)
        
        return a, b, c, d