import math
from logica.integracion import CalculadoraSimpson
from logica.integracion_inversa import CalculadoraInversa


class CalculadoraRegresionCompleta:

    def __init__(self, lista_datos):
        self.lista = lista_datos
        self.simpson = CalculadoraSimpson(1e-14)
        self.inversa = CalculadoraInversa()

    def _f(self, x, dof):
        num = math.gamma((dof + 1) / 2)
        den = math.sqrt(dof * math.pi) * math.gamma(dof / 2)
        c = num / den
        return c * (1 + (x ** 2 / dof)) ** (-(dof + 1) / 2)

    def _integrar_preciso(self, x, dof, n_segmentos=10000):
        if x <= 0:
            return 0.0
        n = n_segmentos
        if n % 2 != 0:
            n += 1
        w = x / n
        suma = self._f(0, dof) + self._f(x, dof)
        for i in range(1, n):
            mult = 4 if i % 2 != 0 else 2
            suma += mult * self._f(i * w, dof)
        return (w / 3) * suma

    def calcular_todo(self, xk):
        sum_x, sum_y, sum_x2, sum_y2, sum_xy, n = self.lista.obtener_sumatorias()

        if n < 3:
            return None

        avg_x = sum_x / n
        avg_y = sum_y / n

        b1 = (sum_xy - (n * avg_x * avg_y)) / (sum_x2 - (n * (avg_x ** 2)))
        b0 = avg_y - (b1 * avg_x)

        r_num = (n * sum_xy) - (sum_x * sum_y)
        r_den = math.sqrt(((n * sum_x2) - (sum_x ** 2)) * ((n * sum_y2) - (sum_y ** 2)))
        r = r_num / r_den
        r2 = r ** 2

        yk = b0 + (b1 * xk)

        dof = n - 2
        x_sig = abs(r) * math.sqrt(n - 2) / math.sqrt(1 - r2)
        p_sig = self._integrar_preciso(x_sig, dof, 10000)
        tail_area = 1 - (2 * p_sig)

        # Usar t-valor SIN redondear para máxima precisión
        t_valor = self.inversa.buscar_x(0.35, dof, redondear=False)

        suma_errores = 0
        actual = self.lista.cabeza
        while actual:
            residuo = actual.y - b0 - (b1 * actual.x)
            suma_errores += residuo ** 2
            actual = actual.siguiente
        sigma = math.sqrt(suma_errores / (n - 2))

        suma_desv_x = 0
        actual = self.lista.cabeza
        while actual:
            suma_desv_x += (actual.x - avg_x) ** 2
            actual = actual.siguiente

        rango = t_valor * sigma * math.sqrt(1 + (1 / n) + ((xk - avg_x) ** 2) / suma_desv_x)

        upi = yk + rango
        lpi = yk - rango

        return {
            "r": r, "r2": r2, "tail_area": tail_area,
            "b0": b0, "b1": b1, "yk": yk,
            "rango": rango, "upi": upi, "lpi": lpi, "n": n
        }
