import sympy as sp

class Term:
    def __init__(self, coef, power):
        if power < 0:
            raise ValueError("power < 0")

        self._coef = coef
        self._power = power
    
    @property
    def coef(self):
        return self._coef
    @property
    def power(self):
        return self._power
    
    def __str__(self):
        if self.power > 0:
            if self.coef == 1:
                return "x^{}".format(self.power)
            elif self.coef == -1:
                return "-x^{}".format(self.power)
            elif self.coef == int(self.coef):
                return "{}*x^{}".format(self.coef, self.power)
            else:
                return "{}*x^{}".format(self.coef.evalf(), self.power)
        elif self.coef == int(self.coef):
            return str(self.coef)
        else:
            return str(self.coef.evalf())

class Polynomial:
    def __init__(self, coefs):
        if len(coefs) == 0:
            raise ValueError("len(coefs) == 0")
        if len(coefs) == 1:
            self._coefs = coefs
            self._terms = [Term(coefs[0], 0)]
            return
        
        coefsTrim = []
        start = False
        for coef in coefs:
            if start or coef != 0:
                start = True
                coefsTrim.append(coef)
        if len(coefsTrim) == 0:
            self._coefs = [0]
        else:
            self._coefs = coefsTrim
        self._terms = []
        n = len(self._coefs)
        for i in range(n):
            self._terms.append(Term(self._coefs[i], n - i - 1))

    @property
    def coefs(self):
        return self._coefs
    
    @property
    def deg(self):
        if len(self.coefs) == 1 and self.coefs[0] == 0:
            return -1
        return len(self.coefs) - 1

    @property
    def terms(self):
        return self._terms

    @staticmethod
    def from_terms(terms):
        if len(terms) == 0:
            raise ValueError("len(terms) == 0")
        coefs = []
        for i in range(len(terms)):
            coefs.append(terms[i].coef)
            if i + 1 < len(terms):
                coefs += (terms[i].power - terms[i + 1].power - 1)*[0]
        coefs += terms[-1].power*[0]
        return Polynomial(coefs)
        

    def __str__(self):
        result = str(self.terms[0])
        for i in range(1, len(self.terms)):
            term = self.terms[i]
            if term.coef > 0:
                result += " + " + str(self.terms[i])
            elif term.coef < 0:
                result += " - " + str(Term(-term.coef, term.power))
        return result

    def __eq__(self, other):
        return self.coefs == other.coefs

    def __call__(self, x):
        result = 0
        for term in self.terms:
            result += term.coef * (x**term.power)
        return result

    def __neg__(self):
        coefs = []
        for coef in self.coefs:
            coefs.append(-coef)
        return Polynomial(coefs)

    def __add__(self, other):
        c1 = self.coefs.copy()
        c2 = other.coefs.copy()
        if len(c1) > len(c2):
            c1, c2 = c2, c1
        
        diff = len(c1) - len(c2)
        if diff > 0:
            c2 = diff*[0] + c2
        coefs = []
        for i in range(len(c1)):
            coefs.append(c1[i] + c2[i])
        return Polynomial(coefs)
    
    def __sub__(self, other):
        return self + (-other)

    def __truediv__(self, other):
        f = self
        g = other

        if g.deg == -1:
            raise ValueError("делитель = 0")
        
        if g.deg > f.deg:
            return Polynomial.ZERO, Polynomial(f.coefs)
        
        temp = f
        q_terms = []
        while True:
            q_terms.append(Term(temp.coefs[0]/g.coefs[0], temp.deg - g.deg))
            temp -= Polynomial([temp.coefs[0]*coef/g.coefs[0] for coef in g.coefs] + (temp.deg - g.deg)*[0])
            if temp.deg < g.deg:
                break
        q = Polynomial.from_terms(q_terms)
        r = temp
        return q, r


Polynomial.ZERO = Polynomial([0])