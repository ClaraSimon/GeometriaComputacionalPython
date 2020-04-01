
import matplotlib.pyplot as plt
import numpy as np
import random


TAMANNO_PUNTOS = 15
MAX_COORDS = 101
NUM_PUNTOS = 16


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


def pintarPuntos(listasPuntos):
    plt.xlim(0, MAX_COORDS+10)
    plt.ylim(0, MAX_COORDS+10)

    for lista in listasPuntos:
        x = []
        y = []

        for p in lista:
            x.append(p.getCoordX())
            y.append(p.getCoordY())
        plt.scatter(x, y, s=TAMANNO_PUNTOS)
    plt.show()

def pintarEnvolventes(listaEnvolventes):
    plt.xlim(0, MAX_COORDS + 10)
    plt.ylim(0, MAX_COORDS + 10)

    for env in listaEnvolventes:
        x = []
        y = []

        for p in env:
            x.append(p.getCoordX())
            y.append(p.getCoordY())
        x.append(x[0])
        y.append(y[0])
        plt.scatter(x, y, s=TAMANNO_PUNTOS)
        plt.plot(x, y)
    plt.show()


def eliminarPuntosAlineados(puntos):
    copiaPuntos = puntos
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
#fin estanAlineados


#Dice si c está a la derecha de AB
def estaALaDerecha(a, b, c):
    vectorAB = a.calcularVectorCon(b)
    vectorAC = a.calcularVectorCon(c)
    matriz = np.array([vectorAB.tolist(), vectorAC.tolist()])
    matrizBase = np.transpose(matriz)
    det = np.linalg.det(matrizBase)

    return det < 0


def crearPuntos():
    listaCoordsX = list(range(1, MAX_COORDS))
    random.shuffle(listaCoordsX)
    listaCoordsX = listaCoordsX[0: NUM_PUNTOS]
    listaCoordsX = merge_sort(listaCoordsX)

    listaCoordsY = list(range(1, MAX_COORDS))
    random.shuffle(listaCoordsY)

    listaPuntos = []
    for i in range(NUM_PUNTOS):
        x = listaCoordsX[i]
        y = listaCoordsY[i]
        listaPuntos.append(Punto(x, y))

    return listaPuntos
#fin crearPuntos


def mostrarPuntos(lista):
    for p in lista:
        print(p)


def calcularEnvolventeConexa(listaPuntos):
    #Esperamos a tener un conjunto pequeño de puntos para calcular su envolvente conexa
    if len(listaPuntos) < 6:

        envolventePequeña = envolventeFuerzaBruta(listaPuntos)
        pintarPuntos([envolventePequeña])
        return envolventePequeña
    else:
        longitud = len(listaPuntos)

        #Dividimos la lista en dos mitades
        mitadUno = listaPuntos[0: longitud//2]
        mitadDos = listaPuntos[longitud//2: longitud]

        pintarPuntos([mitadUno, mitadDos])
        #LLamada recursiva
        envolventeUno = calcularEnvolventeConexa(mitadUno)
        envolventeDos = calcularEnvolventeConexa(mitadDos)
        pintarEnvolventes([envolventeUno, envolventeDos])
        envolventeConjunta = unirEnvolventesConexas(envolventeUno, envolventeDos)
        pintarEnvolventes([envolventeConjunta])
        return envolventeConjunta


def envolventeFuerzaBruta(listPuntos):
    numPuntos = len(listPuntos)
    envolvente = []
    #Cogemos el punto más a la izquierda (ya está ordenado) y buscamos la primera arista
    siguientePunto = listPuntos[0]
    envolvente.append(siguientePunto)

    while siguientePunto.esDistintoDe(envolvente[0]) or len(envolvente) <= 1:
        #Buscamos otro punto de tal manera que conectandolo con sigPunto todos los demás queden a la derecha
        for p in listPuntos:
            contadorPuntosALaDerecha = 0
            if p.esDistintoDe(siguientePunto):
                for q in listPuntos:
                    if q.esDistintoDe(siguientePunto) and q.esDistintoDe(p):
                        if estaALaDerecha(siguientePunto, p, q):
                            contadorPuntosALaDerecha = contadorPuntosALaDerecha+1
            #Si todos los demas puntos estan a la derecha, hemos encontrado el siguiente vértice
            if contadorPuntosALaDerecha == numPuntos-2:
                envolvente.append(p)
                siguientePunto = p
                #Con break salimos del bucle for
                break

    #Quitamos el elemento repetido
    envolvente.pop()

    return envolvente


def unirEnvolventesConexas(envolventeUno, envolventeDos):
    envolventeConjunta = []
    indicesSuperiores = calcularTangenteSuperior(envolventeUno, envolventeDos)
    indicesInferiores = calcularTangenteInferior(envolventeUno, envolventeDos)

    envolventeConjunta += envolventeUno[0: indicesSuperiores[0]+1]
    if indicesInferiores[1] == 0:
        envolventeConjunta += envolventeDos[indicesSuperiores[1]: len(envolventeDos)]
        envolventeConjunta.append(envolventeDos[0])
    else:
        envolventeConjunta += envolventeDos[indicesSuperiores[1]: indicesInferiores[1]+1]
    if indicesInferiores[0] != 0:
        envolventeConjunta += envolventeUno[indicesInferiores[0]: len(envolventeUno)]

    return envolventeConjunta


def calcularTangenteSuperior(envolventeUno, envolventeDos):

    tamEnvolventeDos = len(envolventeDos)
    tamEnvolventeUno = len(envolventeUno)

    # Cogemos la posición en la lista del punto más a la derecha de la primera envolvente
    indiceUnoSuperior = calcularPuntoMasALaDerecha(envolventeUno)
    # Cogemos la posición en la lista del punto más a la izquierda de la segunda envolvente
    indiceDosSuperior = 0  # En este caso será siempre la primera

    p = envolventeUno[indiceUnoSuperior]
    q1 = envolventeDos[indiceDosSuperior]
    q2 = envolventeDos[indiceDosSuperior+1]

    encontrada = False

    while not encontrada:
        encontrada = True

        while not estaALaDerecha(p, q1, q2):
            indiceDosSuperior = (indiceDosSuperior+1) % tamEnvolventeDos
            q1 = envolventeDos[indiceDosSuperior]
            q2 = envolventeDos[(indiceDosSuperior+1) % tamEnvolventeDos]

        verticeDosSuperior = q1
        p1 = p
        p2 = envolventeUno[indiceUnoSuperior - 1]
        while estaALaDerecha(verticeDosSuperior, p1, p2):
            indiceUnoSuperior = (tamEnvolventeUno + indiceUnoSuperior - 1) % tamEnvolventeUno
            p1 = envolventeUno[indiceUnoSuperior]
            p2 = envolventeUno[(indiceUnoSuperior - 1)]
            encontrada = False
        p = p1

    return [indiceUnoSuperior, indiceDosSuperior]


def calcularTangenteInferior(envolventeUno, envolventeDos):

    tamEnvolventeDos = len(envolventeDos)
    tamEnvolventeUno = len(envolventeUno)

    # Cogemos la posición en la lista del punto más a la derecha de la primera envolvente
    indiceUnoSuperior = calcularPuntoMasALaDerecha(envolventeUno)
    # Cogemos la posición en la lista del punto más a la izquierda de la segunda envolvente
    indiceDosSuperior = len(envolventeDos)-1  # En este caso será siempre la primera

    p = envolventeUno[indiceUnoSuperior]
    q1 = envolventeDos[0]
    q2 = envolventeDos[indiceDosSuperior]

    encontrada = False

    while not encontrada:
        encontrada = True

        while not estaALaDerecha(p, q1, q2):
            indiceDosSuperior = (tamEnvolventeDos + indiceDosSuperior - 1) % tamEnvolventeDos
            q1 = envolventeDos[indiceDosSuperior]
            q2 = envolventeDos[indiceDosSuperior-1]

        verticeDosSuperior = q1
        p1 = p
        p2 = envolventeUno[(indiceUnoSuperior + 1) % tamEnvolventeUno]
        while estaALaDerecha(verticeDosSuperior, p1, p2):
            indiceUnoSuperior = (indiceUnoSuperior + 1) % tamEnvolventeUno
            p1 = envolventeUno[indiceUnoSuperior]
            p2 = envolventeUno[(indiceUnoSuperior + 1) % tamEnvolventeUno]
            encontrada = False
        p = p1

    return [indiceUnoSuperior, indiceDosSuperior]


def calcularPuntoMasALaDerecha(envolvente):
    max = 0
    indice = 0
    for i in range(len(envolvente)):
        coordX = envolvente[i].getCoordX()
        if coordX > max:
            indice = i
            max = coordX
    return indice

def split(input_list):
    input_list_len = len(input_list)
    midpoint = input_list_len // 2
    return input_list[:midpoint], input_list[midpoint:]


def merge_sorted_lists(list_left, list_right):
    # Special case: one or both of lists are empty
    if len(list_left) == 0:
        return list_right
    elif len(list_right) == 0:
        return list_left

    # General case
    index_left = index_right = 0
    list_merged = []
    list_len_target = len(list_left) + len(list_right)
    while len(list_merged) < list_len_target:
        if list_left[index_left] <= list_right[index_right]:
            list_merged.append(list_left[index_left])
            index_left += 1
        else:
            list_merged.append(list_right[index_right])
            index_right += 1

        if index_right == len(list_right):
            list_merged += list_left[index_left:]
            break
        elif index_left == len(list_left):
            list_merged += list_right[index_right:]
            break

    return list_merged


def merge_sort(input_list):
    if len(input_list) <= 1:
        return input_list
    else:
        left, right = split(input_list)
        # The following line is the most important piece in this whole thing
        return merge_sorted_lists(merge_sort(left), merge_sort(right))


if __name__ == "__main__":

    puntos = crearPuntos()
    pintarPuntos([puntos])
    puntosNoAlineados = eliminarPuntosAlineados(puntos)
    pintarPuntos([puntosNoAlineados])
    mostrarPuntos(puntosNoAlineados)
    calcularEnvolventeConexa(puntosNoAlineados)

