import math

class CalculadoraSimpson:
    def __init__(self, error_aceptable=0.00001):
        self.E = error_aceptable

    def gamma(self, x):
        if x == 1: return 1.0
        if x == 0.5: return math.sqrt(math.pi)
        if x % 1 == 0: return math.factorial(int(x) - 1)
        res, actual = 1.0, x - 1
        while actual > 0:
            res *= actual
            actual -= 1
        return res * math.sqrt(math.pi)

    def f(self, x, dof):
        num = self.gamma((dof + 1) / 2)
        den = math.sqrt(dof * math.pi) * self.gamma(dof / 2)
        c = num / den
        return c * (1 + (x**2 / dof))**(-(dof + 1) / 2)

    def calcular_area(self, x, dof, n):
        w = x / n
        suma = self.f(0, dof) + self.f(x, dof)
        for i in range(1, n):
            mult = 4 if i % 2 != 0 else 2
            suma += mult * self.f(i * w, dof)
        return (w / 3) * suma

    def integrar(self, x, dof):
        n = 10
        area_ant = self.calcular_area(x, dof, n)
        while True:
            n *= 2
            area_nueva = self.calcular_area(x, dof, n)
            if abs(area_ant - area_nueva) < self.E:
                return round(area_nueva, 5)
            area_ant = area_nueva