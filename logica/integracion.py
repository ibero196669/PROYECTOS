import math

class CalculadoraSimpson:
    def __init__(self, error_aceptable=1e-8):
        self.E = error_aceptable

    def f(self, x, dof):
        num = math.gamma((dof + 1) / 2)
        den = math.sqrt(dof * math.pi) * math.gamma(dof / 2)
        c = num / den
        return c * (1 + (x**2 / dof)) ** (-(dof + 1) / 2)

    def calcular_area(self, x, dof, n):
        if x == 0:
            return 0.0
        w = x / n
        suma = self.f(0, dof) + self.f(x, dof)
        for i in range(1, n):
            mult = 4 if i % 2 != 0 else 2
            suma += mult * self.f(i * w, dof)
        return (w / 3) * suma

    def integrar(self, x, dof):
        if x <= 0:
            return 0.0
        n = 10
        area_ant = self.calcular_area(x, dof, n)
        while True:
            n *= 2
            area_nueva = self.calcular_area(x, dof, n)
            if abs(area_ant - area_nueva) < self.E:
                return area_nueva
            area_ant = area_nueva