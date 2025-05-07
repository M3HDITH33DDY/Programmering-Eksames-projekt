import math
import numpy as np

class TriangleCalculations:
    """Klasse til beregning af trekants egenskaber baseret på sider og/eller vinkler."""

    @staticmethod
    def validate_triangle_sides(a, b, c):
        """Validerer, om tre sider kan danne en trekant."""
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Sider skal være positive tal.")
        if (a + b <= c) or (b + c <= a) or (a + c <= b):
            raise ValueError("Summen af to sider skal være større end den tredje.")
        return True

    @staticmethod
    def validate_triangle_angles(A, B, C):
        """Validerer, om tre vinkler kan danne en trekant."""
        if A <= 0 or B <= 0 or C <= 0:
            raise ValueError("Vinkler skal være positive.")
        if abs(A + B + C - 180) > 1e-10:  # Tillad lille numerisk fejl
            raise ValueError("Summen af vinkler skal være 180 grader.")
        return True

    @staticmethod
    def calculate_from_sides(a, b, c, angles=None):
        """Beregn areal, omkreds og vinkler baseret på tre sider, valider mod vinkler hvis angivet."""
        TriangleCalculations.validate_triangle_sides(a, b, c)
        
        # Omkreds
        perimeter = a + b + c
        
        # Areal ved Herons formel
        s = perimeter / 2  # Semi-omkreds
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        
        # Vinkler ved cosinusrelation
        A = math.degrees(math.acos((b**2 + c**2 - a**2) / (2 * b * c)))
        B = math.degrees(math.acos((a**2 + c**2 - b**2) / (2 * a * c)))
        C = math.degrees(math.acos((a**2 + b**2 - c**2) / (2 * a * b)))
        
        # Hvis vinkler er angivet, valider konsistens
        if angles is not None:
            input_A, input_B, input_C = angles
            TriangleCalculations.validate_triangle_angles(input_A, input_B, input_C)
            # Tjek om beregnede vinkler matcher inputvinkler inden for en tolerance
            if (abs(A - input_A) > 1 or abs(B - input_B) > 1 or abs(C - input_C) > 1):
                raise ValueError("Angivne vinkler stemmer ikke overens med siderne.")
        
        return {
            "perimeter": perimeter,
            "area": area,
            "angles": {"A": A, "B": B, "C": C},
            "sides": {"a": a, "b": b, "c": c}
        }

    @staticmethod
    def calculate_from_side_angles(known_side, known_side_label, A, B, C):
        """Beregn resterende sider, areal og omkreds baseret på én kendt side og tre vinkler."""
        import math
        TriangleCalculations.validate_triangle_angles(A, B, C)

        # Brug sinusrelation: a/sin(A) = b/sin(B) = c/sin(C)
        angles = {'A': A, 'B': B, 'C': C}
        sides = {}

        # Udregn skalar: known_side / sin(known_angle)
        angle_opposite_known = {'a': 'A', 'b': 'B', 'c': 'C'}[known_side_label]
        scale = known_side / math.sin(math.radians(angles[angle_opposite_known]))

        # Beregn alle sider med skalaen
        for side, angle in zip(['a', 'b', 'c'], ['A', 'B', 'C']):
            sides[side] = scale * math.sin(math.radians(angles[angle]))

        # Areal ved formel: (1/2)*ab*sin(C), her bruger vi a, b og vinkel C
        area = (sides['a'] * sides['b'] * math.sin(math.radians(angles['C']))) / 2
        perimeter = sides['a'] + sides['b'] + sides['c']

        return {
            "perimeter": perimeter,
            "area": area,
            "angles": angles,
            "sides": sides
        }
