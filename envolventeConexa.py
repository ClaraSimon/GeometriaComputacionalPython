
import matplotlib.pyplot as plt
import numpy as np

TAMANNO_PUNTOS = 25

class Punto:

    def __init__(self, coordX, coordY):
        self.coords = np.array([coordX, coordY])
    #fin __init__

    def __str__(self):
        cadena = "Coordenadas:" + str(self.coords)
        return cadena

    def getCoordX(self):
        return self.coords[0]

    def getCoordY(self):
        return self.coords[1]

    def calcularVectorCon(self, otro): # Devuelve un vector direccion este punto con el otro
        return np.subtract(otro.coords, self.coords)

    def calcularDistanciaA(self, otro):
        vector = self.calcularVectorCon(otro)
        return np.linalg.norm(vector)

    def esDistintoDe(self, otro):
        return self.coords[0] != otro.coords[0] or self.coords[1] != otro.coords[1]


def pintarPuntos(listaPuntos):
    x = []
    y = []

    for p in listaPuntos:
        x.append(p.getCoordX())
        y.append(p.getCoordY())
    plt.scatter(x, y, s=TAMANNO_PUNTOS)
    plt.show()


def eliminarPuntosAlineados(puntos):
    copiaPuntos = puntos
    print(copiaPuntos)
    for a in puntos:
        for b in puntos:
            if b.esDistintoDe(a):
                for c in puntos:
                    if c.esDistintoDe(a) and c.esDistintoDe(b):
                        if estanAlineados(a, b, c):
                            distAB = a.calcularDistanciaA(b)
                            distAC = a.calcularDistanciaA(c)
                            if distAB < distAC:
                                copiaPuntos.remove(b)
                            else:
                                copiaPuntos.remove(c)
    return copiaPuntos

def estanAlineados(a, b, c):
    vectorAB = a.calcularVectorCon(b)
    vectorAC = a.calcularVectorCon(c)
    matriz = np.array([vectorAB.tolist(), vectorAC.tolist()])
    matrizBase = np.transpose(matriz)
    det = np.linalg.det(matrizBase)

    return det == 0

if __name__ == "__main__":
    print("Hola")
    punto1 = Punto(1, 2)
    punto2 = Punto(1, 5)
    punto3 = Punto(2, 3)
    punto4 = Punto(7, 6)
    punto5 = Punto(4, 1)
    punto6 = Punto(4, 5)
    print(punto1)
    puntos = [punto1, punto2, punto3, punto4, punto5, punto6]

    pintarPuntos(puntos)
    puntosSinAlinear = eliminarPuntosAlineados(puntos)
    pintarPuntos(puntosSinAlinear)
    if punto1.esDistintoDe(punto2):
        print("NO")
    puntos = eliminarPuntosAlineados(puntos)


