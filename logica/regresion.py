import math

class CalculadoraRegresion:
    def __init__(self, lista_datos):
        self.lista = lista_datos

    def calcular_parametros(self):
        sum_x, sum_y, sum_x2, sum_y2, sum_xy, n = self.lista.obtener_sumatorias()

        if n < 2: return None

        avg_x = sum_x / n
        avg_y = sum_y / n

        # Fórmulas
        b1 = (sum_xy - (n * avg_x * avg_y)) / (sum_x2 - (n * (avg_x**2)))
        b0 = avg_y - (b1 * avg_x)

        # Correlación
        r_num = (n * sum_xy) - (sum_x * sum_y)
        r_den = math.sqrt(((n * sum_x2) - (sum_x**2)) * ((n * sum_y2) - (sum_y**2)))
        r = r_num / r_den

        return {
            "b0": b0,
            "b1": b1,
            "r": r,
            "r2": r**2,
            "n": n
        }

    def predecir_yk(self, b0, b1, xk):
        return b0 + (b1 * xk)
