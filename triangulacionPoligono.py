import matplotlib.pyplot as plt
import numpy as np

#Tamanno de los puntos en el gráfico
TAMANNO_PUNTOS = 15
#Coordenadas máximas de los puntos
MAX_COORDS = 10


#Clase Punto que guarda unas coordenadas
class MiPunto:
    #Constructor
    def __init__(self, coordX, coordY):
        self.coords = np.array([coordX, coordY])
        self.quitado = False
    #fin constructor

    #Pasa a string
    def __str__(self):
        cadena = "Coordenadas:" + str(self.coords)
        return cadena
    #fin

    #Devuelve la coordenada x
    def getCoordX(self):
        return self.coords[0]
    #fin getCoordX

    #Devuelve la coordenada y
    def getCoordY(self):
        return self.coords[1]
    #fin getCoordY

    # Devuelve el vector formado por este punto y "otro"
    def calcularVectorCon(self, otro):
        return np.subtract(otro.coords, self.coords)
    #fin calcularVectorCon

    # Devuelve la distancia a otro punto
    def calcularDistanciaA(self, otro):
        vector = self.calcularVectorCon(otro)
        return np.linalg.norm(vector)
    #fin calcularDistanciaA

    #Dice si un otro punto tiene las mismas coordenadas que otro.
    def esDistintoDe(self, otro):
        return self.coords[0] != otro.coords[0] or self.coords[1] != otro.coords[1]
    #fin esDistintoDe

    #Dice si el punto c está a la derecha de la recta que pasa por este punto y b
    def estaALaDerecha(self, b, c):
        vectorAB = self.calcularVectorCon(b)
        vectorAC = self.calcularVectorCon(c)
        matriz = np.array([vectorAB.tolist(), vectorAC.tolist()])
        matrizBase = np.transpose(matriz)
        det = np.linalg.det(matrizBase)
        return det < 0
    #fin estaALaDerecha

    #Dice si el punto está por encima de b
    def estaPorEncimaDe(self, b):
        return self.getCoordY() >= b.getCoordY()
    #fin estaPorEncimaDe


#Clase Arista que contiene los puntos de sus extremos
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
        #Si esta arista y la otra comparten un extremo no se cortan
        coincideInicio = not self.inicio.esDistintoDe(otra.inicio) or not self.inicio.esDistintoDe(otra.fin)
        coincideFin = not self.fin.esDistintoDe(otra.inicio) or not self.fin.esDistintoDe(otra.fin)
        if coincideFin or coincideInicio:
            return False

        #Si una de las aristas esta a la derecha o a la izquierda de la restante tampoco se intersecan
        estaALaDerecha = self.inicio.estaALaDerecha(self.fin, otra.inicio) and self.inicio.estaALaDerecha(self.fin, otra.fin)
        estaALaIzquierda = not self.inicio.estaALaDerecha(self.fin, otra.inicio) and not self.inicio.estaALaDerecha(self.fin, otra.fin)
        estaALaDerecha2 = otra.inicio.estaALaDerecha(otra.fin, self.inicio) and otra.inicio.estaALaDerecha(otra.fin, self.fin)
        estaALaIzquierda2 = not otra.inicio.estaALaDerecha(otra.fin, self.inicio) and not otra.inicio.estaALaDerecha(otra.fin, self.fin)

        if estaALaIzquierda or estaALaDerecha or estaALaDerecha2 or estaALaIzquierda2:
            return False
        else:
            return True
    #fin intersecaCon
#FIN ARISTA


#Clase Vertice de un polígono, contiene su posicion y los Puntos adyacentes
class Vertice:
    def __init__(self, punto: MiPunto, adyacenteIzq: MiPunto, adyacenteDer: MiPunto):
        self.punto = punto
        self.adyacenteIzq = adyacenteIzq
        self.adyacenteDer = adyacenteDer
        self.convexo = False
        self.definirTipo()

    #Dice si un vertice es convexo o no
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
    #fin definirTipo

    #Actualiza el adyacente derecho del vértice y recalcula su tipo
    def cambiarAdyacentesIzq(self, izq):
        self.adyacenteIzq = izq
        self.definirTipo()
    #fin cambiarAdyacentesIzq

    #Actualiza el adyacente izquierdo del vértice y recalcula su tipo
    def cambiarAdyacentesDer(self, der):
        self.adyacenteDer = der
        self.definirTipo()
    #fin cambiarAdyacentesDer

    #Devuelve true si es convexo y false si no lo es
    def esConvexo(self):
        return self.convexo
    #fin esConvexo
#FIN VERTICE


#Clase Poligono que contiene un conjunto de vértices y la lógica para triangularlo y pasar la triangulación a un grafo
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

    #Recibe una lista de puntos y crea los vértices
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
    #fin crearVertices

    #Recibe una lista de puntos y crea las aristas del polígono
    def crearAristas(self, listaPuntos):
        aristas = []
        longitud = len(listaPuntos)
        for i in range(longitud):
            puntoInicio = listaPuntos[i]
            puntoFin = listaPuntos[(i + 1) % longitud]
            a = Arista(puntoInicio, puntoFin)
            aristas.append(a)
        self.aristasPoligono = aristas
    #fin crearAristas

    #Realiza la triangulación del polígono mediante el método de recortar orejas
    def calcularTriangulacion(self):
        #Mientras haya más de tres vértices es que se puede triangular
        while len(self.verticesRestantes) > 3:
            #Lista que guarda los vértices que se eliminarán en esta iteración
            verticesAEliminar = []
            longitud = len(self.verticesRestantes)
            #Recorremos la lista de vértices que se podrían recortar
            for i in range(longitud):
                v = self.verticesRestantes[i]
                # Al ser convexo es candidato a ser oreja
                if v.esConvexo():
                    pAnterior = v.adyacenteIzq
                    pSiguiente = v.adyacenteDer
                    aristaNueva = Arista(pAnterior, pSiguiente)
                    # Si la arista que forman los adyacentes de v no interseca con otra es que el vértice es oreja
                    if not self.interseca(aristaNueva):
                        #Guardamos el vértice en la lista para eliminarlo más tarde
                        verticesAEliminar.append(v)
                        #Agregamos la arista de la triangulación
                        self.aristasTriangulacion.append(aristaNueva)
                        self.dibujar()
                        if longitud == 4:
                            break
            #Por último recortamos los vértices que hemos marcado (las "puntas" de las orejas)
            self.actualizarListaDeVertices(verticesAEliminar)

    #Actualiza la lista de vértices que no se han recortado
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
    #fin actualizarListaDeVértices

    #Dice si una arista interseca con el polígono
    def interseca(self, arista):
        for a in self.aristasPoligono:
            if arista.intersecaCon(a):
                return True
        for a in self.aristasTriangulacion:
            if arista.intersecaCon(a):
                return True
        return False
    #fin interseca

    #Muestra el polígono en un gráfica
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
    #fin dibujar

    #Método que convierte a grafo la triangulación obtenida
    def convertirAGrafo(self):
        puntos = []
        for v in self.verticesIniciales:
            puntos.append(v.punto)

        #Creamos el grafo a partir de los puntos
        grafo = Grafo(puntos)

        #Actualizamos las aristas del grafo
        for a in self.aristasTriangulacion:
            grafo.actualizarAdyacentes(a)

        for a in self.aristasPoligono:
            grafo.actualizarAdyacentes(a)

        return grafo
    #fin convertirAGrafo
    '''
    def esMonotono(self):
        for v in self.vertices:
            if v.tipo == "Division" or v.tipo == "Union":
            return False
        return True
    '''
#FIN POLIGONO


#El nodo de un grafo
class Nodo:
    def __init__(self, punto):
        self.punto = punto
        self.adyacentes = []
        self.color = "w"

    #Añade el índice (posición de un adyacente en la lista de nodos del grafo) a los adyacentes
    def annadirAdyacente(self, indice):
        self.adyacentes.append(indice)
#FIN NODO

#Grafo con una lista de nodos
class Grafo:
    COLORES = "rgbmkc"

    def __init__(self, puntos):
        self.nodos = []
        for p in puntos:
            self.nodos.append(Nodo(p))

    #Devuelve en qué posición está un punto
    def buscarPosicionDeElemento(self, p):
        for i in range(len(self.nodos)):
            n = self.nodos[i]
            if not n.punto.esDistintoDe(p):
                return i
    #fin buscarPosiciónDeElemento

    #Recibe una arista y añade los extremos de la misma como adyacentes.
    def actualizarAdyacentes(self, arista):
        posInicio = self.buscarPosicionDeElemento(arista.inicio)
        posFin = self.buscarPosicionDeElemento(arista.fin)
        #Adyacente fin al nodo inicio
        self.nodos[posInicio].annadirAdyacente(posFin)
        #Adyacente inicio al nodo fin
        self.nodos[posFin].annadirAdyacente(posInicio)
    #fin actualizarAdyacentes

    #Muestra el grafo en una gráfica
    def dibujarGrafo(self):
        plt.xlim(0, MAX_COORDS)
        plt.ylim(0, MAX_COORDS)
        x = []
        y = []
        col = []
        for n in self.nodos:
            x.append(n.punto.getCoordX())
            y.append(n.punto.getCoordY())
            col.append(n.color)
            for ady in n.adyacentes:
                x1 = self.nodos[ady].punto.getCoordX()
                x2 = n.punto.getCoordX()
                y1 = self.nodos[ady].punto.getCoordY()
                y2 = n.punto.getCoordY()
                plt.plot([x1, x2], [y1, y2], c="y", linewidth = 0.2)
        x.append(x[0])
        y.append(y[0])
        col.append(col[0])
        plt.scatter(x, y, c=col, s=TAMANNO_PUNTOS)
        plt.show()
    #fin dibujarGrafo

    #Colorea el grafo
    def pintarNodos(self):
        #Vector de booleanos que dice si un nodo está pintado o no
        pintados = []
        for i in range(len(self.nodos)):
            pintados.append(False)

        #Pintamos el primer nodo del color que queramos
        nodoActual = self.nodos[0]
        nodoActual.color = "r"
        pintados[0] = True
        #Recorremos en anchura el grafo para pintarlo
        nodosPorPintar = self.cogerAdyacentesDe(0, pintados)

        #Mientras que no estén todos los nodos pintados
        while not self.estanPintados():
            #Cogemos el siguiente nodo a pintar
            indiceActual = nodosPorPintar.pop(0)
            nodoActual = self.nodos[indiceActual]
            #Escogemos un color inicial para intentarlo pintar así
            c = 0
            #Hasta que no hayamos pintado el nodo actual
            while not pintados[indiceActual]:
                #Intentamos pintarlo del color número c
                color = self.COLORES[c]
                pintar = True
                #Si tienen algún adyacente del mismo color no podemos pintarlo
                for i in nodoActual.adyacentes:
                    if self.nodos[i].color == self.COLORES[c]:
                        print("IGUAL")
                        pintar = False
                        break
                #Si lo podemos pintar lo pintamos
                if pintar:
                    nodoActual.color = color
                    pintados[indiceActual] = True
                #Si no intentamos con el siguiente color
                else:
                    c = c + 1
            #Como hemos pintado el nodo actual ya podemos añadir a la cola sus adyacentes no pintados
            nodosPorPintar += self.cogerAdyacentesDe(indiceActual, pintados)
    #fin pintarNodos

    #Devuelve los adyacentes no pintados del nodo en la posición (de la lista de nodos) índice
    def cogerAdyacentesDe(self, indice, recorridos):
        lista = []
        for i in self.nodos[indice].adyacentes:
            if not recorridos[i]:
                lista.append(i)
        return lista
    #fin cogerAdyacentesDe

    #Devuelve true si todos los nodos tienen un color
    def estanPintados(self):
        for n in self.nodos:
            if n.color == "w":
                return False
        return True
    #fin estanPintados
#FIN GRAFO

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

#SE DEBEN PONER LOS PUNTOS DEL POLÍGONO EN SENTIDO HORARIO
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
    grafoTriangulacion = poligono.convertirAGrafo()
    grafoTriangulacion.pintarNodos()
    grafoTriangulacion.dibujarGrafo()
