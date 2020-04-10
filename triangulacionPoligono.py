import matplotlib.pyplot as plt
import numpy as np
import random
import collections

TAMANNO_PUNTOS = 15
MAX_COORDS = 10
NUM_PUNTOS = 50


class MiPunto:

    def __init__(self, coordX, coordY):
        self.coords = np.array([coordX, coordY])
        self.quitado = False

    def __str__(self):
        cadena = "Coordenadas:" + str(self.coords)
        return cadena

    def getCoordX(self):
        return self.coords[0]

    def getCoordY(self):
        return self.coords[1]

    # Devuelve el vector formado por este punto y "otro"
    def calcularVectorCon(self, otro):
        return np.subtract(otro.coords, self.coords)

    # Devuelve la distancia a otro punto
    def calcularDistanciaA(self, otro):
        vector = self.calcularVectorCon(otro)
        return np.linalg.norm(vector)

    #Dice si un otro punto tiene las mismas coordenadas que otro.
    def esDistintoDe(self, otro):
        return self.coords[0] != otro.coords[0] or self.coords[1] != otro.coords[1]

    #Dice si el punto c está a la derecha de la recta que pasa por este punto y b
    def estaALaDerecha(self, b, c):
        vectorAB = self.calcularVectorCon(b)
        vectorAC = self.calcularVectorCon(c)
        matriz = np.array([vectorAB.tolist(), vectorAC.tolist()])
        matrizBase = np.transpose(matriz)
        det = np.linalg.det(matrizBase)
        return det < 0

    #Dice si el punto está por encima de b
    def estaPorEncimaDe(self, b):
        return self.getCoordY() >= b.getCoordY()


class Arista:
    def __init__(self, inicio: MiPunto, fin: MiPunto):
        self.inicio = inicio
        self.fin = fin
    #fin __init__

    #Dice si interseca con otra arista (asumimos que sus extremos no coinciden en el mismo punto)
    def intersecaCon(self, otra):
        estaALaDerecha = self.inicio.estaALaDerecha(self.fin, otra.inicio) and self.inicio.estaALaDerecha(self.fin, otra.fin)
        estaALaIzquierda = not self.inicio.estaALaDerecha(self.fin, otra.inicio) and not self.inicio.estaALaDerecha(self.fin, otra.fin)

        return estaALaDerecha or estaALaIzquierda

class Vertice:
    def __init__(self, punto: MiPunto, adyacenteIzq: MiPunto, adyacenteDer: MiPunto):
        self.punto = punto
        self.adyacenteIzq = adyacenteIzq
        self.adyacenteDer = adyacenteDer
        self.convexo = self.definirTipo()

    def definirTipo(self):
        #estaPorEncimadeIzq = self.punto.estaPorEncimaDe(self.adyacenteIzq)
        #estaPorEncimadeDer = self.punto.estaPorEncimaDe(self.adyacenteDer)
        # Si el adyacente de la derecha está a la derecha de la linea adyIzq y este vértice
        esConvexo = self.adyacenteIzq.estaALaDerecha(self.punto, self.adyacenteDer)

        '''if estaPorEncimadeDer and estaPorEncimadeIzq and esConvexo:
            return "Inicio"
        elif estaPorEncimadeIzq and estaPorEncimadeDer and not esConvexo:
            return "Division"
        elif (estaPorEncimadeIzq and not estaPorEncimadeDer) or (not estaPorEncimadeIzq and estaPorEncimadeDer):
            return "Regular"
        elif esConvexo:
            return "Fin"
        else:
            return "Union"'''
        return esConvexo

    def cambiarAdyacentes(self, izq, der):
        self.adyacenteIzq = izq
        self.adyacenteDer = der


class Poligono:
    def __init__(self, listaPuntos):
        #Vértices iniciales del polígono que nos guardamos para pintar
        self.verticesIniciales = self.crearVertices(listaPuntos)
        #Lista de vértices que actualizaremos al hacer el método de las "orejas"
        self.verticesRestantes = self.verticesIniciales
        #Lista de aristas iniciales del polígono
        self.aristasExteriores = self.crearAristas(listaPuntos)
        #Lista de aristas interiores de la triangulación que iremos actualizando
        self.aristasTriangulacion = []
        self.puntero = 0

    def esMonotono(self):
        for v in self.vertices:
            if v.tipo == "Division" or v.tipo == "Union":
                return False
        return True

    def crearVertices(self, listaPuntos):
        vertices = []
        longitud = len(listaPuntos)
        for i in range(longitud):
            puntoIzq = listaPuntos[(longitud + i - 1) % longitud]
            punto = listaPuntos[i]
            puntoDer = listaPuntos[(i + 1) % longitud]
            v = Vertice(punto, puntoIzq, puntoDer)
            vertices.append(v)
        return vertices

    def crearAristas(self, listaPuntos):
        vertices

'''
def elegirColor(v):
    if v.tipo == "Inicio": #Azul
        return "b"
    if v.tipo == "Division": #Rojo
        return "r"
    if v.tipo == "Regular": #Verde
        return "g"
    if v.tipo == "Fin": #Amarillo
        return "y"
    if v.tipo == "Union": #Morado
        return "m"
'''


def pintarPoligono(poligono):
    plt.xlim(0, MAX_COORDS)
    plt.ylim(0, MAX_COORDS)
    x = []
    y = []
    col = []
    for v in poligono:
        x.append(v.punto.getCoordX())
        y.append(v.punto.getCoordY())
        col.append(elegirColor(v))
    x.append(x[0])
    y.append(y[0])
    col.append(col[0])
    plt.scatter(x, y, c=col, s=TAMANNO_PUNTOS)
    plt.plot(x, y)
    plt.show()


def crearPuntos():
    p1 = MiPunto(1, 2)
    p2 = MiPunto(2, 1)
    p3 = MiPunto(3, 2)
    p4 = MiPunto(3, 4)
    p5 = MiPunto(5, 2)
    p6 = MiPunto(6, 4)
    p7 = MiPunto(5, 3)
    p8 = MiPunto(4, 7)
    p9 = MiPunto(2, 8)
    p10 = MiPunto(3, 6)
    p11 = MiPunto(1, 7)
    p12 = MiPunto(2, 3)
    p13 = MiPunto(1, 2)

    #Sentido horario
    puntos = [p13, p12, p11, p10, p9, p8, p7, p6, p5, p4, p3, p2, p1]

    return puntos


def crearPoligono(listaPuntos):
    poligono = []
    longitud = len(listaPuntos)
    for i in range(longitud):
        puntoIzq = listaPuntos[(longitud+i-1)%longitud]
        punto = listaPuntos[i]
        puntoDer = listaPuntos[(i+1)%longitud]
        v = Vertice(punto, puntoIzq, puntoDer)
        poligono.append(v)
    return Poligono(poligono)


if __name__ == "__main__":
    puntos = crearPuntos()
    poligono = Poligono(puntos)
    pintarPoligono(poligono.vertices)
    print(poligono.esMonotono())

    cola = collections.que

