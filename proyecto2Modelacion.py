import tabulate
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


rutaCritica = ''

actividades = [
    {
        'numero': 1,
        'nombre': 'A',
        'duracion': 3,
        'predecesoras': [],
        'sucesoras': [],
        'inicioTemprano': None,
        'culminacionTemprana': None,
        'inicioTardio': None,
        'culminacionTardia': None,
        'holgura': None
    },
    {
        'numero': 2,
        'nombre': 'B',
        'duracion': 2,
        'predecesoras': [1],
        'sucesoras': [],
        'inicioTemprano': None,
        'culminacionTemprana': None,
        'inicioTardio': None,
        'culminacionTardia': None,
        'holgura': None
    },
    {
        'numero': 3,
        'nombre': 'C',
        'duracion': 1,
        'predecesoras': [2, 5],
        'sucesoras': [],
        'inicioTemprano': None,
        'culminacionTemprana': None,
        'inicioTardio': None,
        'culminacionTardia': None,
        'holgura': None
    },
    {
        'numero': 4,
        'nombre': 'D',
        'duracion': 3,
        'predecesoras': [5],
        'sucesoras': [],
        'inicioTemprano': None,
        'culminacionTemprana': None,
        'inicioTardio': None,
        'culminacionTardia': None,
        'holgura': None
    },
    {
        'numero': 5,
        'nombre': 'E',
        'duracion': 2,
        'predecesoras': [1],
        'sucesoras': [],
        'inicioTemprano': None,
        'culminacionTemprana': None,
        'inicioTardio': None,
        'culminacionTardia': None,
        'holgura': None
    },
    {
        'numero': 6,
        'nombre': 'F',
        'duracion': 2,
        'predecesoras': [3, 4],
        'sucesoras': [],
        'inicioTemprano': None,
        'culminacionTemprana': None,
        'inicioTardio': None,
        'culminacionTardia': None,
        'holgura': None
    },
    {
        'numero': 7,
        'nombre': 'G',
        'duracion': 2,
        'predecesoras': [6],
        'sucesoras': [],
        'inicioTemprano': None,
        'culminacionTemprana': None,
        'inicioTardio': None,
        'culminacionTardia': None,
        'holgura': None
    },
]

def findIndex(numero):
    for index, actividad in enumerate(actividades):
        if actividad['numero'] == numero:
            return index
def find(numero):
    for index, actividad in enumerate(actividades):
        if actividad['numero'] == numero:
            return actividad

# RELLENA LAS LISTAS DE SUCESORAS DE CADA ACTIVIDAD
def colocarSucesoras():
    for actividad in actividades:
        for predecesor in actividad['predecesoras']:
            actividades[findIndex(predecesor)]['sucesoras'].append(actividad['numero'])


def identificarInicio():
    for index, actividad in enumerate(actividades):
        if actividad['predecesoras'] == []:
            return index

def identificarFinal():
    for index, actividad in enumerate(actividades):
        if actividad['sucesoras'] == []:
            actividad['culminacionTardia'] = actividad['culminacionTemprana']
            actividad['inicioTardio'] = actividad['inicioTemprano']
            return index

def actualizarDatosTempranos(index):
    mayor = 0
    for predecesor in actividades[index]['predecesoras']:
        if find(predecesor)['culminacionTemprana'] > mayor:
            mayor = find(predecesor)['culminacionTemprana']
    actividades[index]['inicioTemprano'] = mayor
    actividades[index]['culminacionTemprana'] = actividades[index]['inicioTemprano'] + actividades[index]['duracion']

def actualizarDatosTardios(index):
    menor = 99999
    for sucesor in actividades[index]['sucesoras']:
        if find(sucesor)['inicioTardio'] < menor:
            menor = find(sucesor)['inicioTardio']
    actividades[index]['culminacionTardia'] = menor
    actividades[index]['inicioTardio'] = actividades[index]['culminacionTardia'] - actividades[index]['duracion']

def vueltaAdelante():
    cola = [identificarInicio()]
    while cola:
        for sucesor in actividades[cola[0]]['sucesoras']:
            cola.append(findIndex(sucesor))
        actualizarDatosTempranos(cola.pop(0))

def vueltaAtras():
    cola = [identificarFinal()]
    for predecesor in actividades[cola[0]]['predecesoras']:
            cola.append(findIndex(predecesor))
    cola.pop(0)
    while cola:
        for predecesor in actividades[cola[0]]['predecesoras']:
            cola.append(findIndex(predecesor))
        actualizarDatosTardios(cola.pop(0))

def calcularHolguras():
    for actividad in actividades:
        actividad['holgura'] = actividad['inicioTardio'] - actividad['inicioTemprano']


def calcularRutaCritica():
    global rutaCritica
    actual = identificarInicio()
    rutaCritica += str(actividades[actual]['numero'])
    recursivo(actual)

def recursivo(nodoInic):
    global rutaCritica
    for numSucesor in actividades[nodoInic]['sucesoras']:
        if actividades[findIndex(numSucesor)]['holgura'] == 0:
            rutaCritica = rutaCritica + ' - ' + str(actividades[findIndex(numSucesor)]['numero'])
            recursivo(findIndex(numSucesor))

def construirMatrizDeAdyacencia():
    global matriz;
    matriz = [ [ 0 for i in actividades ] for j in actividades ]
    for x in actividades:
        origen = x['numero']
        destino = x['sucesoras']
        if(isinstance(destino, list)):
            for x in destino:
                matriz[origen-1][x-1] = 1

colocarSucesoras()
vueltaAdelante()
vueltaAtras()
calcularHolguras()
calcularRutaCritica()
header = actividades[0].keys()
rows =  [x.values() for x in actividades]
print (tabulate.tabulate(rows, header, tablefmt='grid'))
print('La ruta critica es: '+rutaCritica)


construirMatrizDeAdyacencia()

A = np.matrix(matriz)
G = nx.from_numpy_matrix(A)
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()