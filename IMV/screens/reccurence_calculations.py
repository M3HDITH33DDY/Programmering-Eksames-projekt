# screens/rekus_calculations.py

import re  # Bruges til regulære udtryk til at parse brugerens input
import numpy as np  # Bruges til matrixberegninger og komplekse tal
from numpy.polynomial import Polynomial  # Bruges til at finde rødder af karakteristiske polynomier

def subscript(i):
    """
    Konverterer et heltal til subscript-tegn (fx 1 -> ₁), bruges til C₁, C₂, ... i løsninger.
    """
    return "".join("₀₁₂₃₄₅₆₇₈₉"[int(d)] for d in str(i))

def pretty_power(base):
    """
    Gør eksponent-notation flottere, især til komplekse tal og negative rødder.
    """
    if isinstance(base, complex):  # Kompleks tal repræsenteres med real + imag i
        base = f"({base.real:.2f} + {base.imag:.2f}i)"
    elif base < 0:  # Negative rødder pakkes i parenteser
        base = f"({base:.0f})"
    else:
        base = f"{base:.0f}"
    return f"{base}ⁿ"

def format_polynomial(coeffs):
    """
    Formaterer en liste af koefficienter som en matematisk polynomiel streng.
    
    """
    terms = []
    degree = len(coeffs) - 1  # Øverste eksponent
    for i, c in enumerate(coeffs):
        power = degree - i
        if c == 0:
            continue  # Spring null-led over
        sign = " + " if c > 0 and i > 0 else ""  # Brug "+" for positive værdier (undtagen første led)
        coeff_str = "" if abs(c) == 1 and power != 0 else f"{abs(c)}"  # Undlad koefficienten hvis 1 og ikke konstantled
        term = f"{coeff_str}r^{power}" if power > 1 else (
            f"{coeff_str}r" if power == 1 else f"{abs(c)}"
        )
        terms.append(f"{sign}{'-' if c < 0 else ''}{term}")
    return "".join(terms)

class RecurrenceSolver:
    """
    Klasse til løsning af lineære rekursive ligninger som:
    a(n) = 2a(n-1) - 3a(n-2), med givne startværdier a(0), a(1), ...
    """

    def __init__(self, equation_str, initial_values_str):
        self.equation_str = equation_str.replace(" ", "")  # Fjern mellemrum
        self.initial_values_str = initial_values_str.replace(" ", "")
        self.coefficients = {}  # Dictionary til koefficienter som {delay: coeff}
        self.order = 0  # Ordenen af rekursionsligningen (højeste n-k)
        self.roots = []  # Liste af rødder til karakteristisk ligning
        self.initial_values = {}  # Dictionary over startværdier

    def parse_equation(self):
        """
        Parser rekursionsligningen og udtrækker koefficienterne til a(n-k).
        """
        match = re.match(r'a\(n\)=(.+)', self.equation_str)  # Finder RHS af ligningen
        if not match:
            raise ValueError("Forkert format. Brug fx: a(n) = 2*a(n-1) - 3*a(n-2)")
        rhs = match.group(1)  # Højreside af ligningen

        # Finder alle forekomster af fx 2*a(n-1), -3a(n-2), a(n-3), osv.
        terms = re.findall(r'([+-]?\d*)\*?a\(n-(\d+)\)', rhs)
        if not terms:
            raise ValueError("Kun støtte for lineære rekursive ligninger af formen a(n-k)")
        self.coefficients = {}
        for coeff, delay in terms:
            # Behandler koefficienter som "", "+" eller "-" og konverterer dem til +1 eller -1
            coeff = int(coeff) if coeff not in ["", "+", "-"] else int(coeff + "1")
            delay = int(delay)
            self.coefficients[delay] = coeff
        self.order = max(self.coefficients)

    def build_characteristic_equation(self):
        """
        Bygger koefficientlisten for den karakteristiske ligning, fx [1, -2, 1] for r² - 2r + 1.
        """
        coeffs = [0] * (self.order + 1)
        coeffs[self.order] = 1  # r^order har altid koefficient 1
        for delay, c in self.coefficients.items():
            coeffs[self.order - delay] -= c  # Flyt alle led over på venstresiden
        return coeffs

    def solve_roots(self, coeffs):
        """
        Finder rødderne til det karakteristiske polynomium vha. numpy's Polynomial.
        """
        p = Polynomial(coeffs)  # Opret et polynomium
        self.roots = p.roots()  # Find alle rødder (kan være komplekse)
        return self.roots

    def parse_initial_values(self):
        """
        Parser input som fx: a(0)=1\na(1)=2 og gemmer som {0:1, 1:2}.
        """
        lines = self.initial_values_str.strip().splitlines()
        for line in lines:
            match = re.match(r'a\((\d+)\)=([-+]?\d+)', line)
            if not match:
                raise ValueError("Forkert startværdi. Brug fx: a(0)=1")
            idx = int(match.group(1))
            val = int(match.group(2))
            self.initial_values[idx] = val
        if len(self.initial_values) < self.order:
            raise ValueError(f"Der skal angives mindst {self.order} startværdier.")

    def solve_general_only(self):
        """
        Løser og returnerer den generelle løsning uden at beregne konstanterne.
        """
        self.parse_equation()
        coeffs = self.build_characteristic_equation()
        self.solve_roots(coeffs)
        general = self.general_solution_str()
        return coeffs, self.roots, general

    def general_solution_str(self):
        """
        Genererer streng for generel løsning, fx:
        C₁·2ⁿ + C₂·n·2ⁿ ved multiple rødder, eller komplekse rødder som:
        C₁·Re(rⁿ) + C₂·Im(rⁿ)
        """
        terms = []
        counted = {}
        for r in self.roots:
            key = (round(r.real, 10), round(r.imag, 10))  # Rund for at håndtere numerisk støj
            counted[key] = counted.get(key, 0) + 1
        c_index = 1
        for (real, imag), mult in counted.items():
            r = complex(real, imag)
            if imag == 0:
                # Reel rod med evt. multiplicitet (n^m·rⁿ)
                for m in range(mult):
                    terms.append(f"C{subscript(c_index)}·n^{m}·{pretty_power(real)}")
                    c_index += 1
            else:
                # Komplekse rødder – omformes til reelle led med sinus/cosinus
                terms.append(f"C{subscript(c_index)}·Re({pretty_power(r)}) + C{subscript(c_index+1)}·Im({pretty_power(r)})")
                c_index += 2
        return " + ".join(terms).replace("·n^0·", "·")  # Fjern unødvendig n^0 faktor

    def solve_constants(self):
        """
        Bygger og løser lineært ligningssystem Ax = b for at finde konstanterne.
        """
        funcs = []
        counted = {}
        for r in self.roots:
            key = (round(r.real, 10), round(r.imag, 10))
            counted[key] = counted.get(key, 0) + 1
        for (real, imag), mult in counted.items():
            r = complex(real, imag)
            if imag == 0:
                # Funktioner af formen n^m * r^n
                for m in range(mult):
                    funcs.append(lambda n, r=r, m=m: (n**m) * (r**n))
            else:
                # Reelle og imaginære dele af komplekse potenser
                funcs.append(lambda n, r=r: np.real(r**n))
                funcs.append(lambda n, r=r: np.imag(r**n))

        # Opsætning af matrixsystem A·C = b
        A = []
        b = []
        indices = sorted(self.initial_values.keys())[:len(funcs)]
        for i in indices:
            A.append([f(i) for f in funcs])  # Evaluer hver funktion i punktet i
            b.append(self.initial_values[i])  # Tilhørende kendt værdi
        A = np.array(A)
        b = np.array(b)
        C = np.linalg.solve(A, b)  # Løs med NumPy's lineære solver
        return C, funcs

    def full_solution_str(self, C_vals):
        """
        Returnerer en strengrepræsentation af den fulde løsning, inkl. beregnede konstanter.
        """
        terms = []
        for i, (C, r) in enumerate(zip(C_vals, self.roots), start=1):
            real_c = round(C.real, 3)
            if abs(C.imag) > 1e-10:
                # Kompleks konstant
                terms.append(f"({C})·{pretty_power(r)}")
            else:
                # Reel konstant
                terms.append(f"{real_c}·{pretty_power(r)}")
        return " + ".join(terms)

    def solve(self):
        """
        Løser hele rekursive ligning inkl. generel og specifik løsning.
        Returnerer:
            - Koefficienter til karakteristisk ligning
            - Rødder
            - Generel løsning (symbolsk)
            - Fuld løsning med indsatte konstanter
        """
        self.parse_equation()
        coeffs = self.build_characteristic_equation()
        self.solve_roots(coeffs)
        self.parse_initial_values()
        general = self.general_solution_str()
        C_vals, _ = self.solve_constants()
        full = self.full_solution_str(C_vals)
        return coeffs, self.roots, general, full
