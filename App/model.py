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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import edge as e
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config
import operator

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador

        stops: Tabla de hash para guardar los vertices del grafo
        connections: Grafo para representar las rutas entre estaciones
        components: Almacena la informacion de los componentes conectados
        paths: Estructura que almancena los caminos de costo minimo desde un
                vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'stops': None,
                    'connections': None,
                    'components': None,
                    'paths': None
                    }

        analyzer['stops'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        analyzer["trips_age"] = m.newMap(numelements=14000,
                                   maptype='PROBING',
                                   comparefunction=compareAges)                                       
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al grafo

def addTrip(analyzer, trip):
    try:
        origin = trip["start station id"]
        destination = trip["end station id"]
        duration = int(trip["tripduration"])
        trips_age = [2020 - int(trip["birth year"]),[origin, destination]]
        addStop(analyzer, origin)
        addStop(analyzer, destination)
        addConnection(analyzer, origin, destination, duration)
        addTripsAge(analyzer, trips_age)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addTrip')

def addStop(analyzer, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], stopid):
            gr.insertVertex(analyzer['connections'], stopid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStation')

def addTripsAge(analyzer, trips_age):
    try: 
        age = trips_age[0]
        if 0 <= age <= 10:
           rango_edad = "0-10" 
        if 11 <= age <= 20:
           rango_edad = "11-20" 
        if 21 <= age <= 30:
           rango_edad = "21-30" 
        if 31 <= age <= 40:
           rango_edad = "31-40" 
        if 41 <= age <= 50:
           rango_edad = "41-50" 
        if 51 <= age <= 60:
           rango_edad = "51-60" 
        if age > 60:
           rango_edad = "60+"       
        if m.get(analyzer['trips_age'], rango_edad) is not None:
           trips_age = m.get(analyzer['trips_age'], rango_edad) 
           trips_age = [trips_age["key"], trips_age["value"]]
        if not m.contains(analyzer['trips_age'], rango_edad):    
           trips_age[1][0] = [trips_age[1][0],1]  
           trips_age[1][1] = [trips_age[1][1],1]  
           m.put(analyzer['trips_age'], rango_edad, trips_age[1])
        elif (trips_age[1][0][1] >= 1) and (trips_age[1][1][1] >= 1):  
           trips_age[1][0][1] = trips_age[1][0][1] + 1
           trips_age[1][1][1] = trips_age[1][1][1] + 1 
           m.put(analyzer['trips_age'], rango_edad, trips_age[1]) 
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStation')

def addConnection(analyzer, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones. Si el arco existe se actualiza su peso con el promedio.
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, duration)
    else:
        e.updateAverageWeight(edge,duration)
    return analyzer        

# ==============================
# Funciones de consulta
# ==============================

def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    return scc.connectedComponents(analyzer['components'])

def sameCC(analyzer, station1, station2): 
    """
    Dados dos estaciones, informa si están fuertemente conectados o no.
    """  
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    return scc.stronglyConnected(analyzer['components'], station1, station2) 

def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], initialStation)
    return analyzer

def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path

def estaciones_criticas(analyzer):
    estaciones = m.valueSet(analyzer["trips_age"])
    estaciones_inicio = {}
    estaciones_final = {}
    for i in range(lt.size(estaciones)):
        station = lt.getElement(estaciones, i) 
        estaciones_inicio[station[0][1]] = station[0][0]
        estaciones_final[station[1][0]] = station[1][1]  
    orden_inicio = sorted(estaciones_inicio, reverse=True)
    orden_final = sorted(estaciones_final, key=operator.itemgetter(1), reverse=True)
    if len(orden_inicio) >= 3:        
       llegada_top = orden_inicio[0], orden_inicio[1], orden_inicio[2]
    else:
       llegada_top = orden_inicio[0]  
    if len(orden_final) >= 3:    
       salida_top = orden_final[0], orden_final[1], orden_final[2]
    else:
       salida_top = orden_final[0]   
    orden_inicio = sorted(estaciones_inicio.items(), key=operator.itemgetter(1))
    orden_final = sorted(estaciones_final.items(), key=operator.itemgetter(1))
    menos_utilizadas = []
    if len(orden_inicio) >= 3 and len(orden_final) >= 3: 
       menos_utilizadas.append(int(orden_inicio[0][1]) + orden_final[0][1]) 
       menos_utilizadas.append(int(orden_inicio[1][1]) + orden_final[1][1]) 
       menos_utilizadas.append(int(orden_final[2][1]) + orden_final[2][1])
    else:
       menos_utilizadas.append([orden_inicio[0][1] + orden_final[0][1], int(orden_inicio[0][0])]) 
       mayor = max(menos_utilizadas[0])
       menos_utilizadas = mayor 
    return llegada_top, salida_top, menos_utilizadas
# ==============================
# Funciones Helper
# ==============================

def recomendadorRutas(analyzer, rango_edad):
    edades = m.keySet(analyzer["trips_age"])
    estaciones = m.valueSet(analyzer["trips_age"])
    mayor_inicio = 0
    mayor_final = 0
    for i in range(m.size(analyzer["trips_age"])):
        station = lt.getElement(estaciones, i)
        age_range = lt.getElement(edades, i)   
        if rango_edad == age_range and station[0][1] > mayor_inicio:
           mayor_inicio = station[0][1]
           mejor_inicio = station[0][0]
        if rango_edad == age_range and station[1][1] > mayor_final:
           mayor_final = station[1][1]
           mejor_final = station[1][0]
    return mejor_inicio, mejor_final

# ==============================
# Funciones de Comparacion
# ==============================

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1 

def compareAges(age1, age2): 
    age2 = age2["key"]
    if (age1 == age2):
        return 0
    elif (age1 > age2):
        return 1
    else:
        return -1 