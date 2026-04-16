import sys
from PyQt5 import QtWidgets, uic, QtCore
from logica.regresion import CalculadoraRegresion
from logica.lista_ligada import ListaLigada
from logica.integracion import CalculadoraSimpson
from logica.integracion_inversa import CalculadoraInversa
from logica.regresion_completa import CalculadoraRegresionCompleta

# Valores esperados por caso según el PDF (Programa 1)
ESPERADOS = {
    1: {"b0": "-22.55",   "b1": "1.7279",   "r": "0.9545", "r2": "0.9111", "yk": "644.429"},
    2: {"b0": "-4.039",   "b1": "0.1681",   "r": "0.9333", "r2": "0.8711", "yk": "60.858"},
    3: {"b0": "-23.92",   "b1": "1.43097",  "r": "0.9631", "r2": "0.9276", "yk": "528.4294"},
    4: {"b0": "-4.604",   "b1": "0.140164", "r": "0.948",  "r2": "0.8988", "yk": "49.4994"},
}

# Valores esperados para integración inversa (Programa 3)
ESPERADOS_INV = {
    1: {"p": 0.20, "dof": 6,  "x_esperado": 0.55338},
    2: {"p": 0.45, "dof": 15, "x_esperado": 1.75305},
    3: {"p": 0.495, "dof": 4, "x_esperado": 4.60409},
}

# Valores esperados para regresión completa (Programa 4)
ESPERADOS_P4 = {
    1: {
        "r": "0.954496574", "r2": "0.91106371",
        "tail_area": "1.77517E-05",
        "b0": "-22.55253275", "b1": "1.727932426",
        "yk": "644.4293838",
        "rango": "230.0017197",
        "upi": "874.4311035", "lpi": "414.427664"
    },
    2: {
        "r": "0.933306898", "r2": "0.871061766",
        "tail_area": "7.98203E-05",
        "b0": "-4.038881575", "b1": "0.16812665",
        "yk": "60.85800528",
        "rango": "27.55764748",
        "upi": "88.41565276", "lpi": "33.3003578"
    },
}


def formatear_igual(valor, referencia_str):
    """
    Formatea un valor calculado con la misma cantidad de decimales
    que el valor esperado (referencia_str).
    """
    # Manejar notación científica
    if 'E' in referencia_str or 'e' in referencia_str:
        return f"{valor:.5E}"
    if '.' in referencia_str:
        decimales = len(referencia_str.split('.')[1])
    else:
        decimales = 0
    return f"{valor:.{decimales}f}"


class VentanaRegresion(QtWidgets.QWidget):
    sig_volver = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi('gui/interfaz_regresion.ui', self)
        self.btn_case1.clicked.connect(lambda: self.ejecutar_caso(1))
        self.btn_case2.clicked.connect(lambda: self.ejecutar_caso(2))
        self.btn_case3.clicked.connect(lambda: self.ejecutar_caso(3))
        self.btn_case4.clicked.connect(lambda: self.ejecutar_caso(4))
        self.btn_volver.clicked.connect(self.sig_volver.emit)

    def ejecutar_caso(self, num):
        data = {
            1: ([130, 650, 99, 150, 128, 302, 95, 945, 368, 961],
                [186, 699, 132, 272, 291, 331, 199, 1890, 788, 1601], 386),
            2: ([130, 650, 99, 150, 128, 302, 95, 945, 368, 961],
                [15.0, 69.9, 6.5, 22.4, 28.4, 65.9, 19.4, 198.7, 38.8, 138.2], 386),
            3: ([163, 765, 141, 166, 137, 355, 136, 1206, 433, 1130],
                [186, 699, 132, 272, 291, 331, 199, 1890, 788, 1601], 386),
            4: ([163, 765, 141, 166, 137, 355, 136, 1206, 433, 1130],
                [15.0, 69.9, 6.5, 22.4, 28.4, 65.9, 19.4, 198.7, 38.8, 138.2], 386)
        }

        x_vals, y_vals, x_test = data[num]
        lista = ListaLigada()
        for x, y in zip(x_vals, y_vals):
            lista.insertar(x, y)

        calc = CalculadoraRegresion(lista)
        res = calc.calcular_parametros()

        if res:
            yk = calc.predecir_yk(res['b0'], res['b1'], x_test)
            esp = ESPERADOS[num]

            self.lbl_b0_real.setText(esp['b0'])
            self.lbl_b1_real.setText(esp['b1'])
            self.lbl_rxy_real.setText(esp['r'])
            self.lbl_r2_real.setText(esp['r2'])
            self.lbl_yk_real.setText(esp['yk'])

            self.lbl_b0.setText(formatear_igual(res['b0'], esp['b0']))
            self.lbl_b1.setText(formatear_igual(res['b1'], esp['b1']))
            self.lbl_rxy.setText(formatear_igual(res['r'], esp['r']))
            self.lbl_r2.setText(formatear_igual(res['r2'], esp['r2']))
            self.lbl_yk.setText(formatear_igual(yk, esp['yk']))


class VentanaIntegracion(QtWidgets.QWidget):
    sig_volver = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi('gui/interfaz_integracion.ui', self)
        self.btn_calcular.clicked.connect(self.procesar)
        self.btn_volver_int.clicked.connect(self.sig_volver.emit)

    def procesar(self):
        try:
            x = float(self.txt_x.text())
            d = int(self.txt_dof.text())
            calc = CalculadoraSimpson()
            res = calc.integrar(x, d)
            self.lbl_resultado.setText(str(res))
        except:
            self.lbl_resultado.setText("ERROR")


class VentanaIntegracionInversa(QtWidgets.QWidget):
    sig_volver = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi('gui/interfaz_integracion_inversa.ui', self)
        self.btn_calcular_inv.clicked.connect(self.procesar)
        self.btn_test1.clicked.connect(lambda: self.ejecutar_test(1))
        self.btn_test2.clicked.connect(lambda: self.ejecutar_test(2))
        self.btn_test3.clicked.connect(lambda: self.ejecutar_test(3))
        self.btn_volver_inv.clicked.connect(self.sig_volver.emit)

    def procesar(self):
        try:
            p = float(self.txt_p.text())
            dof = int(self.txt_dof.text())
            calc = CalculadoraInversa()
            x = calc.buscar_x(p, dof)
            self.lbl_resultado_inv.setText(f"x = {x}")
        except:
            self.lbl_resultado_inv.setText("ERROR")

    def ejecutar_test(self, num):
        caso = ESPERADOS_INV[num]
        self.txt_p.setText(str(caso["p"]))
        self.txt_dof.setText(str(caso["dof"]))
        calc = CalculadoraInversa()
        x = calc.buscar_x(caso["p"], caso["dof"])
        self.lbl_resultado_inv.setText(f"x = {x}")


class VentanaRegresionCompleta(QtWidgets.QWidget):
    sig_volver = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi('gui/interfaz_regresion_completa.ui', self)
        self.btn_test1_r4.clicked.connect(lambda: self.ejecutar_test(1))
        self.btn_test2_r4.clicked.connect(lambda: self.ejecutar_test(2))
        self.btn_volver_reg4.clicked.connect(self.sig_volver.emit)

    def ejecutar_test(self, num):
        data = {
            1: ([130, 650, 99, 150, 128, 302, 95, 945, 368, 961],
                [186, 699, 132, 272, 291, 331, 199, 1890, 788, 1601], 386),
            2: ([130, 650, 99, 150, 128, 302, 95, 945, 368, 961],
                [15.0, 69.9, 6.5, 22.4, 28.4, 65.9, 19.4, 198.7, 38.8, 138.2], 386),
        }

        x_vals, y_vals, xk = data[num]
        lista = ListaLigada()
        for x, y in zip(x_vals, y_vals):
            lista.insertar(x, y)

        calc = CalculadoraRegresionCompleta(lista)
        res = calc.calcular_todo(xk)
        esp = ESPERADOS_P4[num]

        if res:
            # Columna esperado
            self.lbl_r_esp.setText(esp['r'])
            self.lbl_r2_esp.setText(esp['r2'])
            self.lbl_tail_esp.setText(esp['tail_area'])
            self.lbl_b0_esp.setText(esp['b0'])
            self.lbl_b1_esp.setText(esp['b1'])
            self.lbl_yk_esp.setText(esp['yk'])
            self.lbl_range_esp.setText(esp['rango'])
            self.lbl_upi_esp.setText(esp['upi'])
            self.lbl_lpi_esp.setText(esp['lpi'])

            # Columna calculado
            self.lbl_r_calc.setText(formatear_igual(res['r'], esp['r']))
            self.lbl_r2_calc.setText(formatear_igual(res['r2'], esp['r2']))
            self.lbl_tail_calc.setText(formatear_igual(res['tail_area'], esp['tail_area']))
            self.lbl_b0_calc.setText(formatear_igual(res['b0'], esp['b0']))
            self.lbl_b1_calc.setText(formatear_igual(res['b1'], esp['b1']))
            self.lbl_yk_calc.setText(formatear_igual(res['yk'], esp['yk']))
            self.lbl_range_calc.setText(formatear_igual(res['rango'], esp['rango']))
            self.lbl_upi_calc.setText(formatear_igual(res['upi'], esp['upi']))
            self.lbl_lpi_calc.setText(formatear_igual(res['lpi'], esp['lpi']))


class MenuPrincipal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui/menu_principal.ui', self)

        self.v1 = VentanaRegresion()
        self.v2 = VentanaIntegracion()
        self.v3 = VentanaIntegracionInversa()
        self.v4 = VentanaRegresionCompleta()

        self.content_area.addWidget(self.v1)
        self.content_area.addWidget(self.v2)
        self.content_area.addWidget(self.v3)
        self.content_area.addWidget(self.v4)

        self.btn_nav_prog1.clicked.connect(lambda: self.ir_a(1))
        self.btn_nav_prog2.clicked.connect(lambda: self.ir_a(2))
        self.btn_nav_prog3.clicked.connect(lambda: self.ir_a(3))
        self.btn_nav_prog4.clicked.connect(lambda: self.ir_a(4))
        self.btn_cerrar.clicked.connect(self.close)

        self.v1.sig_volver.connect(lambda: self.ir_a(0))
        self.v2.sig_volver.connect(lambda: self.ir_a(0))
        self.v3.sig_volver.connect(lambda: self.ir_a(0))
        self.v4.sig_volver.connect(lambda: self.ir_a(0))

    def ir_a(self, idx):
        self.content_area.setCurrentIndex(idx)
        if idx == 0:
            self.btn_nav_prog1.setChecked(False)
            self.btn_nav_prog2.setChecked(False)
            self.btn_nav_prog3.setChecked(False)
            self.btn_nav_prog4.setChecked(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = MenuPrincipal()
    m.show()
    sys.exit(app.exec_())
