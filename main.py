import sys
from PyQt5 import QtWidgets, uic, QtCore
from logica.regresion import CalculadoraRegresion
from logica.lista_ligada import ListaLigada
from logica.integracion import CalculadoraSimpson
from logica.integracion_inversa import CalculadoraInversa

# Valores esperados por caso según el PDF
ESPERADOS = {
    1: {"b0": -22.55,   "b1": 1.7279,   "r": 0.9545, "r2": 0.9111, "yk": 644.429},
    2: {"b0": -4.039,   "b1": 0.1681,   "r": 0.9333, "r2": 0.8711, "yk": 60.858},
    3: {"b0": -23.92,   "b1": 1.43097,  "r": 0.9631, "r2": 0.9276, "yk": 528.4294},
    4: {"b0": -4.604,   "b1": 0.140164, "r": 0.9480, "r2": 0.8988, "yk": 49.4994},
}

# Valores esperados para integración inversa (Programa 3)
ESPERADOS_INV = {
    1: {"p": 0.20, "dof": 6,  "x_esperado": 0.55338},
    2: {"p": 0.45, "dof": 15, "x_esperado": 1.75305},
    3: {"p": 0.495, "dof": 4, "x_esperado": 4.60409},
}

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

            # Valor real (esperado)
            self.lbl_b0_real.setText(f"{esp['b0']}")
            self.lbl_b1_real.setText(f"{esp['b1']}")
            self.lbl_rxy_real.setText(f"{esp['r']}")
            self.lbl_r2_real.setText(f"{esp['r2']}")
            self.lbl_yk_real.setText(f"{esp['yk']}")

            # Valor actual (calculado)
            self.lbl_b0.setText(f"{res['b0']:.4f}")
            self.lbl_b1.setText(f"{res['b1']:.4f}")
            self.lbl_rxy.setText(f"{res['r']:.4f}")
            self.lbl_r2.setText(f"{res['r2']:.4f}")
            self.lbl_yk.setText(f"{yk:.4f}")


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
        self.lbl_resultado_inv.setText(
            f"x calculado = {x}  |  x esperado = {caso['x_esperado']}"
        )


class MenuPrincipal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui/menu_principal.ui', self)

        self.v1 = VentanaRegresion()
        self.v2 = VentanaIntegracion()
        self.v3 = VentanaIntegracionInversa()

        self.content_area.addWidget(self.v1)
        self.content_area.addWidget(self.v2)
        self.content_area.addWidget(self.v3)

        self.btn_nav_prog1.clicked.connect(lambda: self.ir_a(1))
        self.btn_nav_prog2.clicked.connect(lambda: self.ir_a(2))
        self.btn_nav_prog3.clicked.connect(lambda: self.ir_a(3))
        self.btn_cerrar.clicked.connect(self.close)

        self.v1.sig_volver.connect(lambda: self.ir_a(0))
        self.v2.sig_volver.connect(lambda: self.ir_a(0))
        self.v3.sig_volver.connect(lambda: self.ir_a(0))

    def ir_a(self, idx):
        self.content_area.setCurrentIndex(idx)
        if idx == 0:
            self.btn_nav_prog1.setChecked(False)
            self.btn_nav_prog2.setChecked(False)
            self.btn_nav_prog3.setChecked(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = MenuPrincipal()
    m.show()
    sys.exit(app.exec_())
