from logica.integracion import CalculadoraSimpson

class CalculadoraInversa:

    def __init__(self, error_aceptable=1e-9):
        self.E = error_aceptable
        self.simpson = CalculadoraSimpson(error_aceptable / 10)

    def buscar_x(self, p, dof):
        x = 1.0
        d = 0.5

        resultado = self.simpson.integrar(x, dof)
        error_actual = p - resultado
        signo_anterior = 1 if error_actual > 0 else -1

        max_iter = 100000
        for _ in range(max_iter):
            if abs(error_actual) < self.E:
                return round(x, 5)

            signo_actual = 1 if error_actual > 0 else -1
            if signo_actual != signo_anterior:
                d /= 2
                signo_anterior = signo_actual

            if error_actual > 0:
                x += d
            else:
                x -= d

            if x <= 0:
                x = d / 2

            resultado = self.simpson.integrar(x, dof)
            error_actual = p - resultado

        return round(x, 5)
