import math
from logica.integracion import CalculadoraSimpson


class CalculadoraInversa:

    def __init__(self, error_aceptable=0.00001):
        self.E = error_aceptable
        self.simpson = CalculadoraSimpson(error_aceptable / 10)

    def buscar_x(self, p, dof):
        x = 1.0
        d = 0.5

        resultado = self.simpson.integrar(x, dof)
        error_anterior = p - resultado

        max_iter = 50000
        for _ in range(max_iter):
            error_actual = p - resultado

            if abs(error_actual) < self.E:
                return round(x, 5) if self.E >= 0.00001 else x

            if error_actual * error_anterior < 0:
                d /= 2

            if error_actual > 0:
                x += d
            else:
                x -= d

            if x <= 0:
                x = d / 2

            resultado = self.simpson.integrar(x, dof)
            error_anterior = error_actual

        return round(x, 5) if self.E >= 0.00001 else x
