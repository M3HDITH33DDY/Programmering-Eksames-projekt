import numpy as np

class VectorOperations:
    @staticmethod
    def validate_coordinates(coord1, coord2):
        if not (isinstance(coord1, np.ndarray) and isinstance(coord2, np.ndarray)):
            raise ValueError("Coordinates must be numpy arrays.")
        if coord1.shape != (3,) or coord2.shape != (3,):
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