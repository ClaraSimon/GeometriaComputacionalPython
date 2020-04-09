import matplotlib.pyplot as plt
import numpy as np
import random

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


class Vertice:
    def __init__(self, punto: MiPunto, adyacenteIzq: MiPunto, adyacenteDer: MiPunto):
        self.punto = punto
        self.adyacenteIzq = adyacenteIzq
        self.adyacenteDer = adyacenteDer
        self.tipo = self.definirTipo()

    def definirTipo(self):
        estaPorEncimadeIzq = self.punto.estaPorEncimaDe(self.adyacenteIzq)
        estaPorEncimadeDer = self.punto.estaPorEncimaDe(self.adyacenteDer)
        esConvexo = self.adyacenteIzq.estaALaDerecha(self.punto, self.adyacenteDer) #Si el adyacente de la derecha está a la derecha de la linea adyIzq y este vertice

        if estaPorEncimadeDer and estaPorEncimadeIzq and esConvexo:
            return "Inicio"
        elif estaPorEncimadeIzq and estaPorEncimadeDer and not esConvexo:
            return "Division"
        elif (estaPorEncimadeIzq and not estaPorEncimadeDer) or (not estaPorEncimadeIzq and estaPorEncimadeDer):
            return "Regular"
        elif esConvexo:
            return "Fin"
        else:
            return "Union"


def pintarPoligono(poligono):
    plt.xlim(0, MAX_COORDS)
    plt.ylim(0, MAX_COORDS)
    x=[]
    y=[]
    for p in poligono:
        x.append(p.getCoordX())
        y.append(p.getCoordY())
    x.append(x[0])
    y.append(y[0])
    plt.scatter(x, y, s=TAMANNO_PUNTOS)
    plt.plot(x, y)
    plt.show()


def crearPoligono():
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

    poligono = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13]

    return poligono


if __name__ == "__main__":
    print("ola")
    poligono = crearPoligono()
    pintarPoligono(poligono)

