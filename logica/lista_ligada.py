class Nodo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.siguiente = None

class ListaLigada:
    def __init__(self):
        self.cabeza = None
        self.tamano = 0

    def insertar(self, x, y):
        nuevo_nodo = Nodo(x, y)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.tamano += 1

    def obtener_sumatorias(self):
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        sum_xy = 0
        
        actual = self.cabeza
        while actual:
            sum_x += actual.x
            sum_y += actual.y
            sum_x2 += actual.x ** 2
            sum_y2 += actual.y ** 2
            sum_xy += actual.x * actual.y
            actual = actual.siguiente
            
        return sum_x, sum_y, sum_x2, sum_y2, sum_xy, self.tamano