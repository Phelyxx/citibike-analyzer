"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

initialStation = None
recursionLimit = 20000

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de viajes en bicicleta")
    print("3- Conocer la cantidad de clusters de viajes")
    print("4- Obtener información sobre ruta turística circular")
    print("5- Conocer las estaciones críticas ")
    print("6- Conocer ruta turística por resistencia ")
    print("7- Recomendar rutas por rango de edad ")
    print("8- Identificar estaciones para publicidad ")
    print("9- Identificar bicicletas para mantenimiento ")    
    print("0- Salir")
    print("*******************************************")

def optionTwo():
    print("\nCargando información de viajes en bicicleta ....")
    controller.loadTrips(cont)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))


def optionThree():
    print('\nEl total de clusters en el grafo es: ' +
          str(controller.connectedComponents(cont)))
    same_cluster = controller.getsameCC(cont, station1, station2)
    if same_cluster == True:
       print("Las dos estaciones pertenecen al mismo cluster")
    else:
       print("Las dos estaciones no pertenecen al mismo cluster")  

def optionFour():
    controller.minimumCostPaths(cont, initialStation)


def optionFive():
    res = controller.getestacionesCriticas(cont)
    print("Las estaciones top 3 de llegada son:",res[0])
    print("Las estaciones top 3 de salida son:",res[1])
    print("Las 3 estaciones menos utilizadas son:",res[2])

def optionSix():
    print("Escriba..")

def optionSeven():
    print("Rangos de edad: 0-10, 11-20, 21-30, 31-40, 41-50, 51-60, 60+")
    rango_edad = input("Escriba su rango de edad: ")
    res = controller.getRecomendadorRutas(cont, rango_edad)
    print("Estación donde se empiezan más viajes:", res[0])
    print("Estación donde se terminan más viajes:", res[1])
    controller.getminimumCostPaths(cont, res[0])
    path = controller.getminimumCostPath(cont, res[1])
    if path is not None:
        pathlen = stack.size(path)
        print('El camino es de longitud: ' + str(pathlen))
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            print(stop)
    else:
        print('No hay camino')


def optionEight():
    maxvert, maxdeg = controller.servedRoutes(cont)
    print('Estación: ' + maxvert + '  Total rutas servidas: '
          + str(maxdeg))

def optionNine():
    maxvert, maxdeg = controller.servedRoutes(cont)
    print('Estación: ' + maxvert + '  Total rutas servidas: '
          + str(maxdeg))

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        station1 = input("Id de la primera estación: ")
        station2 = input("Id de la segunda estación: ") 
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        initialStation = input(msg)
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 6:
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 7:
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 8:
        executiontime = timeit.timeit(optionEight, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 9:
        executiontime = timeit.timeit(optionNine, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    else:
        sys.exit(0)
sys.exit(0)
