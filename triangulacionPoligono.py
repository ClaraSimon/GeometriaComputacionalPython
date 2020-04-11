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

    def __str__(self):
        cadena = "Punto Inicial:" + str(self.inicio) + " Punto fin:" + str(self.fin)
        return cadena

    #Dice si interseca con otra arista
    def intersecaCon(self, otra):
        coincideInicio = not self.inicio.esDistintoDe(otra.inicio) or not self.inicio.esDistintoDe(otra.fin)
        coincideFin = not self.fin.esDistintoDe(otra.inicio) or not self.fin.esDistintoDe(otra.fin)
        if coincideFin or coincideInicio:
            return False

        estaALaDerecha = self.inicio.estaALaDerecha(self.fin, otra.inicio) and self.inicio.estaALaDerecha(self.fin, otra.fin)
        estaALaIzquierda = not self.inicio.estaALaDerecha(self.fin, otra.inicio) and not self.inicio.estaALaDerecha(self.fin, otra.fin)
        estaALaDerecha2 = otra.inicio.estaALaDerecha(otra.fin, self.inicio) and otra.inicio.estaALaDerecha(otra.fin, self.fin)
        estaALaIzquierda2 = not otra.inicio.estaALaDerecha(otra.fin, self.inicio) and not otra.inicio.estaALaDerecha(otra.fin, self.fin)

        if estaALaIzquierda or estaALaDerecha or estaALaDerecha2 or estaALaIzquierda2:
            return False
        else:
            return True
#FIN ARISTA


class Vertice:
    def __init__(self, punto: MiPunto, adyacenteIzq: MiPunto, adyacenteDer: MiPunto):
        self.punto = punto
        self.adyacenteIzq = adyacenteIzq
        self.adyacenteDer = adyacenteDer
        self.convexo = False
        self.definirTipo()

    def definirTipo(self):
        #estaPorEncimadeIzq = self.punto.estaPorEncimaDe(self.adyacenteIzq)
        #estaPorEncimadeDer = self.punto.estaPorEncimaDe(self.adyacenteDer)
        # Si el adyacente de la derecha está a la derecha de la linea adyIzq y este vértice

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
        esConvexo = self.adyacenteIzq.estaALaDerecha(self.punto, self.adyacenteDer)
        self.convexo = esConvexo

    def cambiarAdyacentesIzq(self, izq):
        self.adyacenteIzq = izq
        self.definirTipo()

    def cambiarAdyacentesDer(self, der):
        self.adyacenteDer = der
        self.definirTipo()

    def esConvexo(self):
        return self.convexo
#FIN VERTICE


class Poligono:
    def __init__(self, listaPuntos):
        #Vértices iniciales del polígono que nos guardamos para pintar
        self.verticesIniciales = None
        self.crearVertices(listaPuntos)
        #Lista de vértices que actualizaremos al hacer el método de las "orejas"
        self.verticesRestantes = self.verticesIniciales[:]
        #Lista de aristas iniciales del polígono
        self.aristasPoligono = None
        self.crearAristas(listaPuntos)
        #Lista de aristas interiores de la triangulación que iremos actualizando
        self.aristasTriangulacion = []
        self.puntero = 0

    def crearVertices(self, listaPuntos):
        vertices = []
        longitud = len(listaPuntos)
        for i in range(longitud):
            puntoIzq = listaPuntos[(longitud + i - 1) % longitud]
            punto = listaPuntos[i]
            puntoDer = listaPuntos[(i + 1) % longitud]
            v = Vertice(punto, puntoIzq, puntoDer)
            vertices.append(v)
        self.verticesIniciales = vertices

    def crearAristas(self, listaPuntos):
        aristas = []
        longitud = len(listaPuntos)
        for i in range(longitud):
            puntoInicio = listaPuntos[i]
            puntoFin = listaPuntos[(i + 1) % longitud]
            a = Arista(puntoInicio, puntoFin)
            aristas.append(a)
        self.aristasPoligono = aristas

    def calcularTriangulacion(self):
        while len(self.verticesRestantes) > 3:
            verticesAEliminar = []
            longitud = len(self.verticesRestantes)
            for i in range(longitud):
                v = self.verticesRestantes[i]
                if v.esConvexo(): #Al ser convexo es candidato a ser oreja
                    pAnterior = v.adyacenteIzq
                    pSiguiente = v.adyacenteDer
                    aristaNueva = Arista(pAnterior, pSiguiente)
                    if not self.interseca(aristaNueva): #Si la arista no interseca con otra es que el vértice es oreja
                        verticesAEliminar.append(v)
                        self.aristasTriangulacion.append(aristaNueva)
                        self.dibujar()
                        if longitud == 4:
                            break
            self.actualizarListaDeVertices(verticesAEliminar)

    def actualizarListaDeVertices(self, lista):
        #Quitamos los vértices que están en el punto medio de la oreja
        for v in lista:
            self.verticesRestantes.remove(v)

        longitud = len(self.verticesRestantes)
        #Actualizamos la adyacencia de vértices
        for i in range(longitud):
            puntoIzq = self.verticesRestantes[(longitud + i - 1) % longitud].punto
            puntoDer = self.verticesRestantes[(i + 1) % longitud].punto
            self.verticesRestantes[i].cambiarAdyacentesIzq(puntoIzq)
            self.verticesRestantes[i].cambiarAdyacentesDer(puntoDer)

    def interseca(self, arista):
        for a in self.aristasPoligono:
            if arista.intersecaCon(a):
                return True
        for a in self.aristasTriangulacion:
            if arista.intersecaCon(a):
                return True
        return False

    def dibujar(self):
        plt.xlim(0, MAX_COORDS)
        plt.ylim(0, MAX_COORDS)
        x = []
        y = []
        for v in self.verticesIniciales:
            x.append(v.punto.getCoordX())
            y.append(v.punto.getCoordY())
        x.append(x[0])
        y.append(y[0])
        plt.scatter(x, y, s=TAMANNO_PUNTOS)
        plt.plot(x, y)

        for a in self.aristasTriangulacion:
            x.clear()
            y.clear()
            x.append(a.inicio.getCoordX())
            y.append(a.inicio.getCoordY())
            x.append(a.fin.getCoordX())
            y.append(a.fin.getCoordY())
            plt.plot(x, y, c="m")
        plt.show()

    def convertirAGrafo(self):
        puntos = []
        for v in self.verticesIniciales:
            puntos.append(v.punto)

        grafo = Grafo(puntos)

        for a in self.aristasTriangulacion:
            grafo.actualizarAdyacentes(a)

        for a in self.aristasPoligono:
            grafo.actualizarAdyacentes(a)

        return grafo
    '''
    def esMonotono(self):
        for v in self.vertices:
            if v.tipo == "Division" or v.tipo == "Union":
            return False
        return True
    '''
#FIN POLIGONO


class Nodo:
    def __init__(self, punto):
        self.punto = punto
        self.adyacentes = []
        self.color = "w"

    def annadirAdyacente(self, indice):
        self.append(indice)


class Grafo:
    def __init__(self, nodos):
        self.nodos = nodos

    def buscarPosicionDeElemento(self, punto):
        for i in range(self.nodos):
            n = self.nodos[i]
            if not n.punto.esDistintoDe(punto):
                return i

    def actualizarAdyacentes(self, arista):
        posInicio = self.buscarPosicionDeElemento(arista.inicio)
        posFin = self.buscarPosicionDeElemento(arista.fin)

        self.nodos[posInicio].annadirAdyacente(posFin)
        self.nodos[posFin].annadirAdyacente(posInicio)


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

    #Sentido horario
    puntos = [p12, p11, p10, p9, p8, p7, p6, p5, p4, p3, p2, p1]

    return puntos


if __name__ == "__main__":
    puntos = crearPuntos()
    poligono = Poligono(puntos)
    poligono.dibujar()
    poligono.calcularTriangulacion()

