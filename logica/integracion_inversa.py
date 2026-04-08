import math
from logica.integracion import CalculadoraSimpson


class CalculadoraInversa:
    
    def __init__(self, error_aceptable=0.00001):
        self.E = error_aceptable
        self.simpson = CalculadoraSimpson(error_aceptable)

    def buscar_x(self, p, dof):

        x = 1.0
        d = 0.5

        # Primera integración
        resultado = self.simpson.integrar(x, dof)
        error_anterior = p - resultado

        # Iterar hasta convergencia
        max_iter = 1000
        for _ in range(max_iter):
            error_actual = p - resultado

            # Verificar convergencia
            if abs(error_actual) < self.E:
                return round(x, 5)

            # Si el signo del error cambió, reducir d a la mitad
            if error_actual * error_anterior < 0:
                d /= 2

            # Ajustar x según el signo del error
            if error_actual > 0:
                x += d
            else:
                x -= d

            # Proteger contra x <= 0
            if x <= 0:
                x = d / 2

            # Integrar con el nuevo x
            resultado = self.simpson.integrar(x, dof)
            error_anterior = error_actual

        # Si no convergió, devolver el mejor resultado
        return round(x, 5)