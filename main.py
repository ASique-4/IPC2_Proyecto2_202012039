
import webbrowser
import PySimpleGUI as sg
from ListaMatrizDispersa import ListaMatrizDispersa
from ListaRobots import ListaRobot
from listaUnidadMilitar import ListaUnidadMilitar
import xml.etree.ElementTree as ET


nombre_archivo = []
lista_matriz = ListaMatrizDispersa()
lista_robots = ListaRobot()

def ObtenerArchivo():

    sg.theme('Purple')

    layout = [[sg.Text('Archivo .xml')],
            [sg.Input(), sg.FileBrowse('Buscar')],
            [sg.Button('Guardar'), sg.Button('Salir')]]

    window = sg.Window('Escoje el archivo de entrada .xml', layout)
    event, values = window.read()
    if values[0] == '' or values[0] == None or event == 'Cancel' or event == sg.WIN_CLOSED:
            print('No escogiste ningún archivo .xml')
            window.close()
    else:
        print('Escogiste el archivo: ',values[0])
        nombre_archivo.append(values[0])
        elementTree(values[0])
        window.close()
        Interfaz()

def Interfaz():

    layout = [[sg.Text('Archivo seleccionado')],
            [sg.Text(nombre_archivo[0])],
            [sg.Button('Mision de rescate de civil')], [sg.Button('Mision de rescate de recursos')],[sg.Button('Cambiar archivo seleccionado')]]

    window = sg.Window('Menú Principal', layout, enable_close_attempted_event=True)

    while True:
        event, values = window.read()
        if (event == 'Mision de rescate de civil'):
            ciudad = sg.popup_get_text(lista_matriz.showCiudades(),'Esoge una ciudad' )
            if lista_matriz.search_item(ciudad) != False:
                insertaTodo(ciudad) 
                if lista_matriz.search_item(ciudad).getCiviles() > 0:
                    
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad+'.pdf')
                    robot = sg.popup_get_text(lista_robots.showRobotsRescue(),'Esoge una un robot' )
                    if lista_robots.search_item(robot,'ChapinRescue'):
                        print('Exito')
                        CaminoCorto(lista_matriz.search_item(ciudad))
                        pass
                    else:
                        sg.popup_error('El robot: "' + robot + '" no existe',title = 'Robot no encontrado')
                else:
                    sg.popup_error('La ciudad: "' + ciudad + '" no tiene unidades civiles',title = 'Sin unidades civiles')
            else:
                sg.popup_error('La ciudad: "' + ciudad + '" no existe',title = 'Ciudad no encontrada')
                
            
        if (event == 'Mision de rescate de recursos'):
            ciudad = sg.popup_get_text(lista_matriz.showCiudades(),'Esoge una ciudad' )
            if lista_matriz.search_item(ciudad) != False:
                insertaTodo(ciudad) 
                if lista_matriz.search_item(ciudad).getRecursos() > 0:
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad+'.pdf')
                    robot = sg.popup_get_text(lista_robots.showRobotsFighter(),'Esoge una un robot' )
                    if lista_robots.search_item(robot,'ChapinFighter') != False:
                        print('Exito')
                        insertarTodoOrdenado(ciudad)
                        webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad+'.pdf')
                        print('Terminó')
                    else:
                        sg.popup_error('El robot: "' + robot + '" no existe',title = 'Robot no encontrado')
                else:
                    sg.popup_error('La ciudad: "' + ciudad + '" no tiene recursos',title = 'Sin recursos')
            else:
                sg.popup_error('La ciudad: "' + ciudad + '" no existe',title = 'Ciudad no encontrada')
        if (event == 'Cambiar archivo seleccionado'):
            window.close()
            ObtenerArchivo()
            break
        if event == sg.WIN_CLOSE_ATTEMPTED_EVENT:
            break

    window.close()

def insertaTodo(ciudad):
    matriz = lista_matriz.search_item(ciudad)    
    with open('Ciudades/'+ciudad+'.txt') as archivo:
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

def insertarTodoOrdenado(ciudad):
    matriz = lista_matriz.search_item(ciudad)    
    with open('Ciudades/'+ciudad+'.txt') as archivo:
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
            matriz.graficarNeatoOrdenar(ciudad,matriz)

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
                            f = open('Ciudades/'+subsubchild.text +'.txt','w')
                            print(subsubchild.text)
                        if subsubchild.tag == 'fila':
                            f.write(subsubchild.text + '\n')
                        if subsubchild.tag == 'unidadMilitar':
                            unidad_militar.insertLastunidadMilitar(subsubchild.attrib['columna'],subsubchild.attrib['fila'],subsubchild.text,nombre)
                    f.close()
                    lista_matriz.insertLastMatrizDispersa(0,unidad_militar,nombre)
                    unidad_militar.showUnidadesMilitares()
                if subchild.tag == 'robot':
                    for subsubchild in subchild:
                        if subsubchild.tag == 'nombre':
                            if 'capacidad' in subsubchild.attrib:
                                lista_robots.insertLastRobot(subsubchild.text,subsubchild.attrib['capacidad'],subsubchild.attrib['tipo'])
                            else:
                                lista_robots.insertLastRobot(subsubchild.text,'0',subsubchild.attrib['tipo'])

def CaminoCorto(ciudad):
    nodoFinal = ciudad.getNodo(sg.popup_get_text('Fila del Civil \n' + ciudad.showNodoCivil(),'Fila'),sg.popup_get_text('Columna del Civil \n' + ciudad.showNodoCivil(),'Columna'))
    if nodoFinal != False:
        tmp = ciudad.filas.primero
        while(tmp is not None):
            nodoTmp = tmp.acceso
            while(nodoTmp is not None):
                if nodoTmp.tipo == 'Entrada':
                    distancia = recorrerCiudad(nodoFinal,nodoTmp,ciudad)
                    if int(nodoFinal.getDistancia()) >  int(distancia):
                        nodoFinal.setDistancia(distancia) 
                        nodoFinal.setEntrada(nodoTmp)
                        nodoFinal.terminal = False
                nodoTmp = nodoTmp.derecha
            tmp = tmp.siguiente
    recorrerCiudadFinal(nodoFinal,ciudad)
    print('Listo')
    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
            

def recorrerCiudad(nodoFinal,nodoActual,ciudad):
        ciudad.limpiarCaminos()
        casillas_recorridas = 0
        #anterior = nodoActual
        while nodoFinal.terminal is False:
            if nodoActual == nodoFinal :
                nodoFinal.terminal = True
                break
            #Nodo actual arriba y a la izquierda
            if nodoActual.coordenadaX <= nodoFinal.coordenadaX and nodoActual.coordenadaY <= nodoFinal.coordenadaY:
                
                if nodoActual.derecha != None and nodoActual.derecha.tipo == 'Camino':
                    casillas_recorridas += 1
                    nodoActual.derecha.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.derecha
                
                elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Camino' :
                    casillas_recorridas += 1
                    nodoActual.abajo.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.abajo
                    
                elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Camino' :
                    casillas_recorridas += 1
                    nodoActual.izquierda.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.izquierda

                elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Camino' :
                    casillas_recorridas += 1
                    nodoActual.arriba.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.arriba
                #No ha llegado
                elif nodoActual.derecha != False and nodoActual.derecha == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.izquierda != False and nodoActual.izquierda == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.abajo != False and nodoActual.abajo == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.arriba != False and nodoActual.arriba == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                else:
                    #Retroceder
                    if nodoActual.derecha != None and nodoActual.derecha.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        nodoActual.tipo = 'Visitado'
                        #anterior = nodoActual
                        nodoActual = nodoActual.derecha
                        
                    elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        nodoActual.tipo = 'Visitado'
                        #anterior = nodoActual
                        nodoActual = nodoActual.izquierda
                        
                    elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        nodoActual.tipo = 'Visitado'
                        #anterior = nodoActual
                        nodoActual = nodoActual.abajo

                    elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        nodoActual.tipo = 'Visitado'
                        #anterior = nodoActual
                        nodoActual = nodoActual.arriba
                    else:
                        nodoFinal.terminal = True
                        casillas_recorridas = 9999
                        break
            #Nodo actual abajo y a la derecha
            elif nodoActual.coordenadaX >= nodoFinal.coordenadaX and nodoActual.coordenadaY >= nodoFinal.coordenadaY:

                if nodoActual.arriba != None and nodoActual.arriba.tipo == 'Camino' :
                    casillas_recorridas += 1
                    nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba

                elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Camino' :
                    casillas_recorridas += 1
                    nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda

                elif nodoActual.derecha != None and nodoActual.derecha.tipo == 'Camino' :
                    casillas_recorridas += 1
                    nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha

                elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Camino' :
                    casillas_recorridas += 1
                    nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo
                #No ha llegado
                
                elif nodoActual.arriba != False and nodoActual.arriba == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.izquierda != False and nodoActual.izquierda == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.derecha != False and nodoActual.derecha == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.abajo != False and nodoActual.abajo == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                
                else:
                    #Retroceder
                    if nodoActual.arriba != None and nodoActual.arriba.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.arriba

                    elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.izquierda

                    elif nodoActual.derecha != None and nodoActual.derecha.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.derecha

                    elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.abajo
                    else:
                        nodoFinal.terminal = True
                        casillas_recorridas = 9999
                        break

            #Nodo actual abajo y a la izquierda
            elif nodoActual.coordenadaX >= nodoFinal.coordenadaX and nodoActual.coordenadaY <= nodoFinal.coordenadaY:
                if nodoActual.derecha != None and nodoActual.derecha.tipo == 'Camino' :
                    casillas_recorridas += 1
                    nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha
                
                elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Camino' :
                    casillas_recorridas += 1
                    nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba

                elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Camino' :
                    casillas_recorridas += 1
                    nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda

                elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Camino' :
                    casillas_recorridas += 1
                    nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo
                #No ha llegado
                
                elif nodoActual.derecha != False and nodoActual.derecha == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.izquierda != False and nodoActual.izquierda == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.arriba != False and nodoActual.arriba == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.abajo != False and nodoActual.abajo == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                else:
                    #Retroceder
                    if nodoActual.derecha != None and nodoActual.derecha.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.derecha

                    elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.izquierda

                    elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.arriba

                    elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.abajo
                    else:
                        nodoFinal.terminal = True
                        casillas_recorridas = 9999
                        break

            #Nodo actual arriba y a la derecha
            elif nodoActual.coordenadaX <= nodoFinal.coordenadaX and nodoActual.coordenadaY >= nodoFinal.coordenadaY:
                
                if nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Camino' :
                    casillas_recorridas += 1
                    nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda
                
                elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Camino' :
                    casillas_recorridas += 1
                    nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo
                
                elif nodoActual.derecha != None and nodoActual.derecha.tipo == 'Camino' :
                    casillas_recorridas += 1
                    nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha
                
                elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Camino' :
                    casillas_recorridas += 1
                    nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba
                #No ha llegado
                elif nodoActual.izquierda != False and nodoActual.izquierda == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.derecha != False and nodoActual.derecha == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.abajo != False and nodoActual.abajo == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.arriba != False and nodoActual.arriba == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                
                else:
                    #Retroceder
                    if nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.izquierda
                    
                    elif nodoActual.derecha != None and nodoActual.derecha.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.derecha

                    elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.abajo
                    
                    elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.arriba
                    else:
                        nodoFinal.terminal = True
                        casillas_recorridas = 9999
                        break
            else:
                nodoFinal.terminal = True
                break
        return casillas_recorridas

def recorrerCiudadFinal(nodoFinal,ciudad):
        ciudad.limpiarCaminos()
        nodoActual = nodoFinal.getEntrada()
        nodoFinal.terminal = False
        while nodoFinal.terminal is False:
            if nodoActual == nodoFinal :
                ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                nodoFinal.terminal = True
                webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                break
            #Nodo actual arriba y a la izquierda
            if nodoActual.coordenadaX <= nodoFinal.coordenadaX and nodoActual.coordenadaY <= nodoFinal.coordenadaY:
                
                if nodoActual.derecha != None and nodoActual.derecha.tipo == 'Camino':
                    nodoActual.derecha.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.derecha
                
                elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Camino' :
                    nodoActual.abajo.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.abajo
                    
                elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Camino' :
                    nodoActual.izquierda.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.izquierda

                elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Camino' :
                    nodoActual.arriba.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.arriba
                #No ha llegado
                elif nodoActual.derecha != False and nodoActual.derecha == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.izquierda != False and nodoActual.izquierda == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.abajo != False and nodoActual.abajo == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.arriba != False and nodoActual.arriba == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                else:
                    #Retroceder
                    if nodoActual.derecha != None and nodoActual.derecha.tipo == 'Caminando' :
                        nodoActual.tipo = 'Visitado'
                        #anterior = nodoActual
                        nodoActual = nodoActual.derecha
                        
                    elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Caminando' :
                        nodoActual.tipo = 'Visitado'
                        #anterior = nodoActual
                        nodoActual = nodoActual.izquierda
                        
                    elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Caminando' :
                        nodoActual.tipo = 'Visitado'
                        #anterior = nodoActual
                        nodoActual = nodoActual.abajo

                    elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Caminando' :
                        nodoActual.tipo = 'Visitado'
                        #anterior = nodoActual
                        nodoActual = nodoActual.arriba
            #Nodo actual abajo y a la derecha
            elif nodoActual.coordenadaX >= nodoFinal.coordenadaX and nodoActual.coordenadaY >= nodoFinal.coordenadaY:

                if nodoActual.arriba != None and nodoActual.arriba.tipo == 'Camino' :
                    nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba

                elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Camino' :
                    nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda

                elif nodoActual.derecha != None and nodoActual.derecha.tipo == 'Camino' :
                    nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha

                elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Camino' :
                    nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo
                #No ha llegado
                
                elif nodoActual.arriba != False and nodoActual.arriba == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.izquierda != False and nodoActual.izquierda == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.derecha != False and nodoActual.derecha == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.abajo != False and nodoActual.abajo == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                
                else:
                    #Retroceder
                    if nodoActual.arriba != None and nodoActual.arriba.tipo == 'Caminando' :
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.arriba

                    elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Caminando' :
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.izquierda

                    elif nodoActual.derecha != None and nodoActual.derecha.tipo == 'Caminando' :
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.derecha

                    elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Caminando' :
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.abajo
    
            #Nodo actual abajo y a la izquierda
            elif nodoActual.coordenadaX >= nodoFinal.coordenadaX and nodoActual.coordenadaY <= nodoFinal.coordenadaY:
                if nodoActual.derecha != None and nodoActual.derecha.tipo == 'Camino' :
                    nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha
                
                elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Camino' :
                    nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba

                elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Camino' :
                    nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda

                elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Camino' :
                    nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo
                #No ha llegado
                
                elif nodoActual.derecha != False and nodoActual.derecha == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.izquierda != False and nodoActual.izquierda == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.arriba != False and nodoActual.arriba == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.abajo != False and nodoActual.abajo == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                else:
                    #Retroceder
                    if nodoActual.derecha != None and nodoActual.derecha.tipo == 'Caminando' :
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.derecha

                    elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Caminando' :
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.izquierda

                    elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Caminando' :
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.arriba

                    elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Caminando' :
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.abajo

            #Nodo actual arriba y a la derecha
            elif nodoActual.coordenadaX <= nodoFinal.coordenadaX and nodoActual.coordenadaY >= nodoFinal.coordenadaY:
                
                if nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Camino' :
                    nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda
                
                elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Camino' :
                    nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo
                
                elif nodoActual.derecha != None and nodoActual.derecha.tipo == 'Camino' :
                    nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha
                
                elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Camino' :
                    nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba
                #No ha llegado
                elif nodoActual.izquierda != False and nodoActual.izquierda == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.derecha != False and nodoActual.derecha == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.abajo != False and nodoActual.abajo == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.arriba != False and nodoActual.arriba == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                
                else:
                    #Retroceder
                    if nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Caminando' :
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.izquierda
                    
                    elif nodoActual.derecha != None and nodoActual.derecha.tipo == 'Caminando' :
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.derecha

                    elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Caminando' :
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.abajo
                    
                    elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Caminando' :
                        nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.arriba
            else:
                ciudad.graficarNeatoOrdenar(ciudad.getCiudad(),ciudad)
                nodoFinal.terminal = True
                webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                break

ObtenerArchivo()
