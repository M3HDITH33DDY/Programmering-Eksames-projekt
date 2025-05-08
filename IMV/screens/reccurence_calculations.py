# screens/rekus_calculations.py

import re  # Importerer regulære udtryk til parsing af brugerinput
import numpy as np  # Importerer NumPy til matrixberegninger og komplekse tal
from numpy.polynomial import Polynomial  # Importerer Polynomial til at finde rødder af karakteristiske polynomier

def subscript(i):
    """
    Konverterer et heltal til subscript-tegn (fx 1 -> ₁).
    Bruges til at formatere konstanter som C₁, C₂ i løsninger.
    """
    # Omdanner hver ciffer i tallet til dets subscript-ækvivalent
    return "".join("₀₁₂₃₄₅₆₇₈₉"[int(d)] for d in str(i))

def pretty_power(base):
    """
    Formaterer eksponent-notation for at gøre den mere læselig.
    Håndterer både komplekse tal og negative rødder korrekt.
    """
    if isinstance(base, complex):  # Hvis basen er et komplekst tal
        # Formater som (real + imag i) med to decimaler
        base = f"({base.real:.2f} + {base.imag:.2f}i)"
    elif base < 0:  # Hvis basen er negativ
        # Sæt parenteser omkring for at undgå forvirring
        base = f"({base:.0f})"
    else:
        # Formater som heltal uden decimaler
        base = f"{base:.0f}"
    # Returnerer basen efterfulgt af eksponent-symbolet ⁿ
    return f"{base}ⁿ"

def format_polynomial(coeffs):
    """
    Formaterer en liste af koefficienter som en matematisk polynomiel streng.
    Eksempel: [1, -2, 1] bliver r^2 - 2r + 1.
    """
    terms = []  # Liste til at gemme led i polynomiet
    degree = len(coeffs) - 1  # Bestemmer polynomiets grad
    for i, c in enumerate(coeffs):
        power = degree - i  # Beregner eksponenten for det aktuelle led
        if c == 0:
            continue  # Spring over led med koefficient 0
        # Bestem fortegn: "+" for positive koefficienter (undtagen første led)
        sign = " + " if c > 0 and i > 0 else ""
        # Udelad koefficient 1 eller -1, undtagen for konstantleddet
        coeff_str = "" if abs(c) == 1 and power != 0 else f"{abs(c)}"
        # Formater led baseret på eksponenten
        term = f"{coeff_str}r^{power}" if power > 1 else (
            f"{coeff_str}r" if power == 1 else f"{abs(c)}"
        )
        # Tilføj fortegn og led til listen
        terms.append(f"{sign}{'-' if c < 0 else ''}{term}")
    # Sammensæt alle led til en streng
    return "".join(terms)

class RecurrenceSolver:
    """
    Klasse til at løse lineære rekursive ligninger af formen:
    a(n) = c₁a(n-1) + c₂a(n-2) + ..., med givne startværdier.
    """

    def __init__(self, equation_str, initial_values_str):
        # Fjerner alle mellemrum fra inputstrengene for konsistens
        self.equation_str = equation_str.replace(" ", "")
        self.initial_values_str = initial_values_str.replace(" ", "")
        self.coefficients = {}  # Dictionary til at gemme koefficienter {forsinkelse: koefficient}
        self.order = 0  # Ordenen af rekursionen (højeste n-k)
        self.roots = []  # Liste til rødder af karakteristisk ligning
        self.initial_values = {}  # Dictionary til startværdier {indeks: værdi}

    def parse_equation(self):
        """
        Parser rekursionsligningen og udtrækker koefficienter for a(n-k).
        Eksempel: a(n)=2*a(n-1)-3*a(n-2) giver {1: 2, 2: -3}.
        """
        # Matcher højresiden af ligningen med regulært udtryk
        match = re.match(r'a\(n\)=(.+)', self.equation_str)
        if not match:
            # Kast fejl hvis formatet er ugyldigt
            raise ValueError("Forkert format. Brug fx: a(n) = 2*a(n-1) - 3*a(n-2)")
        rhs = match.group(1)  # Uddrag højresiden

        # Finder alle led som ±c*a(n-k) ved hjælp af regex
        terms = re.findall(r'([+-]?\d*)\*?a\(n-(\d+)\)', rhs)
        if not terms:
            # Kast fejl hvis ingen gyldige led findes
            raise ValueError("Kun støtte for lineære rekursive ligninger af formen a(n-k)")
        self.coefficients = {}
        for coeff, delay in terms:
            # Konverter koefficient: "", "+" eller "-" bliver ±1
            coeff = int(coeff) if coeff not in ["", "+", "-"] else int(coeff + "1")
            delay = int(delay)
            self.coefficients[delay] = coeff
        # Sæt ordenen til den højeste forsinkelse
        self.order = max(self.coefficients)

    def build_characteristic_equation(self):
        """
        Konstruerer koefficientlisten for den karakteristiske ligning.
        Eksempel: For a(n) = 2a(n-1) - a(n-2) bliver det [1, -2, 1] for r² - 2r + 1 = 0.
        """
        coeffs = [0] * (self.order + 1)  # Initialiser liste med nuller
        coeffs[self.order] = 1  # Sæt koefficienten for r^order til 1
        for delay, c in self.coefficients.items():
            # Træk koefficienterne fra for at flytte led til venstresiden
            coeffs[self.order - delay] -= c
        return coeffs

    def solve_roots(self, coeffs):
        """
        Finder rødderne til det karakteristiske polynomium ved hjælp af NumPy.
        Gemmer rødderne i self.roots.
        """
        p = Polynomial(coeffs)  # Opretter polynomium fra koefficienterne
        self.roots = p.roots()  # Finder alle rødder (reelle og komplekse)
        return self.roots

    def parse_initial_values(self):
        """
        Parser startværdier som fx a(0)=1\na(1)=2 og gemmer dem i {0:1, 1:2}.
        """
        lines = self.initial_values_str.strip().splitlines()  # Opdel i linjer
        for line in lines:
            # Matcher formatet a(k)=v med regulært udtryk
            match = re.match(r'a\((\d+)\)=([-+]?\d+)', line)
            if not match:
                # Kast fejl hvis formatet er ugyldigt
                raise ValueError("Forkert startværdi. Brug fx: a(0)=1")
            idx = int(match.group(1))  # Uddrag indeks
            val = int(match.group(2))  # Uddrag værdi
            self.initial_values[idx] = val
        # Tjek om der er nok startværdier
        if len(self.initial_values) < self.order:
            raise ValueError(f"Der skal angives mindst {self.order} startværdier.")

    def solve_general_only(self):
        """
        Beregner den generelle løsning uden at finde specifikke konstanter.
        Returnerer koefficienter, rødder og generel løsning som streng.
        """
        self.parse_equation()  # Parser ligningen
        coeffs = self.build_characteristic_equation()  # Bygger karakteristisk ligning
        self.solve_roots(coeffs)  # Finder rødder
        general = self.general_solution_str()  # Genererer generel løsning
        return coeffs, self.roots, general

    def general_solution_str(self):
        """
        Opretter en strengrepræsentation af den generelle løsning.
        Håndterer multiplicitet og komplekse rødder korrekt.
        Eksempel: C₁·2ⁿ + C₂·n·2ⁿ for en rod med multiplicitet 2.
        """
        terms = []  # Liste til at gemme led i løsningen
        counted = {}  # Tæller multiplicitet af rødder
        for r in self.roots:
            # Rund real- og imaginærdel for at undgå numerisk støj
            key = (round(r.real, 10), round(r.imag, 10))
            counted[key] = counted.get(key, 0) + 1
        c_index = 1  # Tæller for konstanter (C₁, C₂, ...)
        for (real, imag), mult in counted.items():
            r = complex(real, imag)
            if imag == 0:
                # Reel rod: tilføj led af formen C_m·n^m·rⁿ for hver multiplicitet
                for m in range(mult):
                    terms.append(f"C{subscript(c_index)}·n^{m}·{pretty_power(real)}")
                    c_index += 1
            else:
                # Kompleks rod: tilføj reelle og imaginære dele
                terms.append(f"C{subscript(c_index)}·Re({pretty_power(r)}) + C{subscript(c_index+1)}·Im({pretty_power(r)})")
                c_index += 2
        # Sammensæt led og fjern unødvendig n^0
        return " + ".join(terms).replace("·n^0·", "·")

    def solve_constants(self):
        """
        Løser for konstanterne i den specifikke løsning ved at opsætte og løse et lineært ligningssystem.
        Returnerer konstanterne og de tilhørende funktioner.
        """
        funcs = []  # Liste til at gemme basisløsninger
        counted = {}  # Tæller multiplicitet af rødder
        for r in self.roots:
            key = (round(r.real, 10), round(r.imag, 10))
            counted[key] = counted.get(key, 0) + 1
        for (real, imag), mult in counted.items():
            r = complex(real, imag)
            if imag == 0:
                # Reel rod: tilføj funktioner af formen n^m·r^n
                for m in range(mult):
                    funcs.append(lambda n, r=r, m=m: (n**m) * (r**n))
            else:
                # Kompleks rod: tilføj reelle og imaginære dele af r^n
                funcs.append(lambda n, r=r: np.real(r**n))
                funcs.append(lambda n, r=r: np.imag(r**n))

        # Byg matrixsystem A·C = b
        A = []  # Matrix til evaluering af funktioner
        b = []  # Vektor af kendte værdier
        indices = sorted(self.initial_values.keys())[:len(funcs)]  # Brug de første startværdier
        for i in indices:
            A.append([f(i) for f in funcs])  # Evaluer hver funktion i punktet i
            b.append(self.initial_values[i])  # Tilføj tilhørende startværdi
        A = np.array(A)  # Konverter til NumPy-array
        b = np.array(b)
        C = np.linalg.solve(A, b)  # Løs systemet for at finde konstanterne
        return C, funcs

    def full_solution_str(self, C_vals):
        """
        Opretter en strengrepræsentation af den fulde løsning med indsatte konstanter.
        Eksempel: 2·2ⁿ + 1·3ⁿ.
        """
        terms = []  # Liste til at gemme led
        for i, (C, r) in enumerate(zip(C_vals, self.roots), start=1):
            real_c = round(C.real, 3)  # Rund reel del af konstanten
            if abs(C.imag) > 1e-10:
                # Kompleks konstant: behold fuld repræsentation
                terms.append(f"({C})·{pretty_power(r)}")
            else:
                # Reel konstant: brug afrundet værdi
                terms.append(f"{real_c}·{pretty_power(r)}")
        # Sammensæt led til en streng
        return " + ".join(terms)

    def solve(self):
        """
        Udfører fuld løsning af rekursionsligningen.
        Udfører parsing, finder rødder, generel løsning og specifik løsning med konstanter.
        Returnerer koefficienter, rødder, generel løsning og fuld løsning.
        """
        self.parse_equation()  # Parser ligningen
        coeffs = self.build_characteristic_equation()  # Bygger karakteristisk ligning
        self.solve_roots(coeffs)  # Finder rødder
        self.parse_initial_values()  # Parser startværdier
        general = self.general_solution_str()
        C_vals, _ = self.solve_constants()
        full = self.full_solution_str(C_vals)
        return coeffs, self.roots, general, full