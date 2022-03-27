
import PySimpleGUI as sg
from ListaMatrizDispersa import ListaMatrizDispersa
from MatrizDispersa import MatrizDispersa
from listaUnidadMilitar import ListaUnidadMilitar
import xml.etree.ElementTree as ET
'''
matriz.insert(10, 10, '*')
matriz.graficarNeato('PrimerNodo')
matriz.insert(1, 1, '*')
matriz.insert(1, 2, '*')
matriz.insert(1, 3, '*')
matriz.insert(1, 4, '*')
matriz.insert(2, 1, '*')
matriz.insert(2, 2, '*')
matriz.insert(2, 3, '*')
matriz.insert(2, 4, '*')
matriz.insert(3, 1, '*')
matriz.insert(3, 2, '*')
matriz.insert(3, 3, '*')
matriz.insert(3, 4, '*')
matriz.insert(4, 1, '*')
matriz.insert(4, 2, '*')
matriz.insert(4, 3, '*')
matriz.insert(4, 4, '*')
matriz.insert(8, 9, '*')
matriz.insert(9, 8, '*')
matriz.graficarNeato('Final')
'''


nombre_archivo = []
lista_matriz = ListaMatrizDispersa()


def ObtenerArchivo():

    sg.theme('Black')

    layout = [[sg.Text('Filename')],
            [sg.Input(), sg.FileBrowse()],
            [sg.Button('Guardar'), sg.Button('Salir')]]

    window = sg.Window('Get filename example', layout)
    event, values = window.read()
    if values[0] == '' or values[0] == None or event == 'Cancel' or event == sg.WIN_CLOSED:
            print('No escogiste ningún archivo .xml')
            window.close()
    else:
        print('Escogiste el archivo: ',values[0])
        nombre_archivo.append(values[0])
        window.close()
        Interfaz()
        
    
def Interfaz():

    layout = [[sg.Text('Archivo seleccionado')],
            [sg.Text(nombre_archivo[0])],
            [sg.Button('Mision de rescate de civil')], [sg.Button('Mision de rescate de recursos')]]

    window = sg.Window('Window Title', layout, enable_close_attempted_event=True)

    while True:
        event, values = window.read()
        print(event, values)
        if (event == 'Mision de rescate de civil'):
            break
        if (event == 'Mision de rescate de recursos'):
            break
        if event == sg.WIN_CLOSE_ATTEMPTED_EVENT:
            break

    window.close()
def insertaTodo(ciudad):
    matriz = lista_matriz.search_item(ciudad)    
    with open(ciudad+'.txt') as archivo:
        l = 0
        c = 0
        lineas = archivo.readlines()
        for linea in lineas:
            columnas = linea.replace('"','')
            l += 1
            for col in columnas:
                if col != '\n':
                    c += 1
                    matriz.insert(l, c, col)
            c = 0
            matriz.graficarNeato(ciudad,matriz)

def insertaSeleccion(ciudad): #este metodo a diferencia del otro, solo va a insertar nodos en la matriz
    matriz = ListaMatrizDispersa.search_item(ciudad)        # cuando en el archivo de entrada, encuentre el caracter '*', los demas, los ignora
    with open('ciuedad1.txt') as archivo:
        l = 0
        c = 0
        lineas = archivo.readlines()
        for linea in lineas:
            columnas = linea
            l += 1
            for col in columnas:
                if col != '\n':
                    c += 1
                    if col =='*':
                        matriz.insert(l, c, col)
            c = 0
            matriz.graficarNeato('ejemplo')

def elementTree(ruta):
        tree = ET.parse(ruta)
        raiz = tree.getroot()
        for r in raiz:
            for subchild in r: 
                if subchild.tag == 'ciudad':
                    unidad_militar = ListaUnidadMilitar()
                    
                    for subsubchild in subchild:
                        if subsubchild.tag == 'nombre':
                            nombre = subsubchild.text
                            f = open(subsubchild.text +'.txt','w')
                            print(subsubchild.text)
                        if subsubchild.tag == 'fila':
                            f.write(subsubchild.text + '\n')
                        if subsubchild.tag == 'unidadMilitar':
                            unidad_militar.insertLastunidadMilitar(subsubchild.attrib['columna'],subsubchild.attrib['fila'],subsubchild.text,nombre)
                    f.close()
                    lista_matriz.insertLastMatrizDispersa(0,unidad_militar,nombre)
                    unidad_militar.showUnidadesMilitares()
        





elementTree('ArchivoPrueba(2).xml')
#ObtenerArchivo()
insertaTodo('Atlantis')
#insertaSeleccion()