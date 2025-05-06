import numpy as np

class VectorOperations:
    @staticmethod
    def validate_coordinates(coord1, coord2, coord3=None):
        coords = [coord1, coord2]
        if coord3 is not None:
            coords.append(coord3)
        for coord in coords:
            if not isinstance(coord, np.ndarray):
                raise ValueError("Koordinater skal være et nparray")
            if coord.shape != (3,):
                raise ValueError("Alle 3 koordinater skal udfyldes")

    @staticmethod
    def add(coord1, coord2, type1, type2):
        VectorOperations.validate_coordinates(coord1, coord2)
        if type1 == "Point" and type2 == "Punkt":
            raise ValueError("Addition kan ikke foretages mellem to punkter")
        return coord1 + coord2

    @staticmethod
    def subtract(coord1, coord2, type1, type2):
        VectorOperations.validate_coordinates(coord1, coord2)
        if type1 == "Punkt" and type2 == "Vektor":
            raise ValueError("Kan ikke fratrække punkt fra vektor")
        return coord1 - coord2

    @staticmethod
    def dot_product(coord1, coord2, type1, type2):
        VectorOperations.validate_coordinates(coord1, coord2)
        if type1 == "Punkt" or type2 == "Punkt":
            raise ValueError("Skalar produkt kræver to vektorer")
        return np.dot(coord1, coord2)

    @staticmethod
    def cross_product(coord1, coord2, type1, type2):
        VectorOperations.validate_coordinates(coord1, coord2)
        if type1 == "Punkt" or type2 == "Punkt":
            raise ValueError("Kryds produkt kræver to vektorer")
        return np.cross(coord1, coord2)

    @staticmethod
    def plane_equation(coord1, coord2, coord3, type1, type2, type3):
        VectorOperations.validate_coordinates(coord1, coord2, coord3)
        
        # Initialisering af normalvektor
        normal = None
        
        # Udkast 1: 3 punkter
        if type1 == "Punkt" and type2 == "Punkt" and type3 == "Punkt":
            vec1 = coord2 - coord1
            vec2 = coord3 - coord1
            normal = np.cross(vec1, vec2)
            point = coord1
        # Udkast 2: 1 punkt og 2 vektorer
        elif type1 == "Punkt" and type2 == "Vektor" and type3 == "Vektor":
            normal = np.cross(coord2, coord3)
            point = coord1
        elif type2 == "Punkt" and type1 == "Vektor" and type3 == "Vektor":
            normal = np.cross(coord1, coord3)
            point = coord2
        elif type3 == "Punkt" and type1 == "Vektor" and type2 == "Vektor":
            normal = np.cross(coord1, coord2)
            point = coord3
        else:
            raise ValueError("Planens ligning kræver 3 punkter eller 2 vektorer og 1 punkt")

        # Tjekker om normalvektoren er lig 0
        if np.allclose(normal, 0):
            raise ValueError("Vektorer er parallele eller rammer hinanden, planens ligning kan ikke fremstilles")

        # Planens ligning
        a, b, c = normal
        d = np.dot(normal, point)
        
        return a, b, c, d
    