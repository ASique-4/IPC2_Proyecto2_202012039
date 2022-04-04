
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
                    
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.replace(" ","")+'.pdf')
                    robot = sg.popup_get_text(lista_robots.showRobotsRescue(),'Esoge una un robot' )
                    if lista_robots.search_item(robot,'ChapinRescue'):
                        print('Exito')
                        CaminoCortoParaCivil(lista_matriz.search_item(ciudad),robot)
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
                        CaminoCortoParaRecurso(lista_matriz.search_item(ciudad),robot)
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
    with open('Ciudades/'+ciudad.replace(" ","")+'.txt') as archivo:
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
            matriz.graficarNeato(ciudad.replace(" ",""),matriz)

def insertarTodoOrdenado(ciudad):
    matriz = lista_matriz.search_item(ciudad)    
    with open('Ciudades/'+ciudad.replace(" ","")+'.txt') as archivo:
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
            matriz.graficarNeatoOrdenar(ciudad.replace(" ",""),matriz)

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
                            if lista_matriz.search_item(nombre) != False:
                                lista_matriz.eliminarCiudad(nombre)
                            f = open('Ciudades/'+subsubchild.text.replace(" ","") +'.txt','w')
                            print(subsubchild.text)
                        if subsubchild.tag == 'fila':
                            f.write(subsubchild.text + '\n')
                        if subsubchild.tag == 'unidadMilitar':
                            unidad_militar.insertLastunidadMilitar(subsubchild.attrib['fila'],subsubchild.attrib['columna'],subsubchild.text,nombre)
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

def CaminoCortoParaCivil(ciudad,robot):
    nodoFinal = ciudad.getNodo(sg.popup_get_text('Fila del Civil \n' + ciudad.showNodoCivil(),'Fila'),sg.popup_get_text('Columna del Civil \n' + ciudad.showNodoCivil(),'Columna'))
    if nodoFinal != False and nodoFinal.tipo == 'Civil':
        tmp = ciudad.filas.primero
        while(tmp is not None):
            nodoTmp = tmp.acceso
            while(nodoTmp is not None):
                if nodoTmp.tipo == 'Entrada':
                    distancia = recorrerCiudad(nodoFinal,nodoTmp,ciudad,robot)
                    if distancia != 0 and int(nodoFinal.getDistancia()) >  int(distancia):
                        nodoFinal.setDistancia(distancia) 
                        nodoFinal.setEntrada(nodoTmp)
                        nodoFinal.terminal = False
                nodoTmp = nodoTmp.derecha
            tmp = tmp.siguiente
    else:
        sg.popup_error('La posición indicada no tiene ningún civil')
    if nodoFinal != False and nodoFinal.getEntrada() != None:
        recorrerCiudadFinal(nodoFinal,ciudad,robot)
        print('Listo')
        webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+str(ciudad.getCiudad()).replace(" ","")+'.pdf')
    else:
        sg.popup_error('No hay forma de llegar al civil :(')
            
def CaminoCortoParaRecurso(ciudad,robot):
    nodoFinal = ciudad.getNodo(sg.popup_get_text('Fila del Recurso \n' + ciudad.showNodoRecurso(),'Fila'),sg.popup_get_text('Columna del Recurso \n' + ciudad.showNodoRecurso(),'Columna'))
    if nodoFinal != False and nodoFinal.tipo == 'Recurso':
        tmp = ciudad.filas.primero
        while(tmp is not None):
            nodoTmp = tmp.acceso
            while(nodoTmp is not None):
                if nodoTmp.tipo == 'Entrada':
                    distancia = recorrerCiudad(nodoFinal,nodoTmp,ciudad,robot)
                    if distancia != 0 and int(nodoFinal.getDistancia()) >  int(distancia):
                        nodoFinal.setDistancia(distancia) 
                        nodoFinal.setEntrada(nodoTmp)
                        nodoFinal.terminal = False
                nodoTmp = nodoTmp.derecha
            tmp = tmp.siguiente
    else:
        sg.popup_error('La posición indicada no tiene ningún recurso')
    if nodoFinal != False and nodoFinal.getEntrada() != None:
        recorrerCiudadFinal(nodoFinal,ciudad,robot)
        print('Listo')
        webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+str(ciudad.getCiudad()).replace(" ","")+'.pdf')
    else:
        sg.popup_error('No hay forma de llegar al Recurso :(')

def recorrerCiudad(nodoFinal,nodoActual,ciudad,robot):
        nodoFinal.terminal = False
        fuerza_tmp = 0
        if lista_robots.search_item(robot,'ChapinFighter') != False :
            fuerza_tmp = int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())
        Entrada = nodoActual
        ciudad.limpiarCaminos()
        casillas_recorridas = 0
        #anterior = nodoActual
        while nodoFinal.terminal is False:

            #Nodo actual arriba y a la izquierda
            if nodoActual.coordenadaX <= nodoFinal.coordenadaX and nodoActual.coordenadaY <= nodoFinal.coordenadaY:

                if nodoActual.derecha != None and (nodoActual.derecha.tipo == 'Camino' or nodoActual.derecha.tipo == 'Entrada' or nodoActual.derecha.tipo == 'Civil') and nodoActual.derecha!= nodoFinal and nodoActual.derecha!= Entrada and nodoActual.coordenadaX >= nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.derecha.tipo == 'Entrada':
                        nodoActual.derecha.tipo = 'CaminandoEntrada'
                    elif nodoActual.derecha.tipo == 'Civil':
                        nodoActual.derecha.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.derecha.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.derecha
                elif nodoActual.arriba != None and (nodoActual.arriba.tipo == 'Camino' or nodoActual.arriba.tipo == 'Entrada' or nodoActual.arriba.tipo == 'Civil') and nodoActual.arriba != nodoFinal and nodoActual.arriba != Entrada and nodoActual.coordenadaX >= nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.arriba.tipo == 'Entrada':
                        nodoActual.arriba.tipo = 'CaminandoEntrada'
                    elif nodoActual.arriba.tipo == 'Civil':
                        nodoActual.arriba.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.arriba.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.arriba
                    
                elif nodoActual.abajo != None and (nodoActual.abajo.tipo == 'Camino' or nodoActual.abajo.tipo == 'Entrada' or nodoActual.abajo.tipo == 'Civil') and nodoActual.abajo!= nodoFinal and nodoActual.abajo!= Entrada and nodoActual.coordenadaX >= nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.abajo.tipo == 'Entrada':
                        nodoActual.abajo.tipo = 'CaminandoEntrada'
                    elif nodoActual.abajo.tipo == 'Civil':
                        nodoActual.abajo.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.abajo.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.abajo
                    
                elif nodoActual.izquierda != None and (nodoActual.izquierda.tipo == 'Camino' or nodoActual.izquierda.tipo == 'Entrada' or nodoActual.izquierda.tipo == 'Civil') and nodoActual.izquierda != nodoFinal and nodoActual.izquierda != Entrada and nodoActual.coordenadaX >= nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.izquierda.tipo == 'Entrada':
                        nodoActual.izquierda.tipo = 'CaminandoEntrada'
                    elif nodoActual.izquierda.tipo == 'Civil':
                        nodoActual.izquierda.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.izquierda.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.izquierda

                

                elif nodoActual.abajo != None and (nodoActual.abajo.tipo == 'Camino' or nodoActual.abajo.tipo == 'Entrada' or nodoActual.abajo.tipo == 'Civil') and nodoActual.abajo!= nodoFinal and nodoActual.abajo!= Entrada and nodoActual.coordenadaX < nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.abajo.tipo == 'Entrada':
                        nodoActual.abajo.tipo = 'CaminandoEntrada'
                    elif nodoActual.abajo.tipo == 'Civil':
                        nodoActual.abajo.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.abajo.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.abajo
                elif nodoActual.derecha != None and (nodoActual.derecha.tipo == 'Camino' or nodoActual.derecha.tipo == 'Entrada' or nodoActual.derecha.tipo == 'Civil') and nodoActual.derecha!= nodoFinal and nodoActual.derecha!= Entrada and nodoActual.coordenadaX < nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.derecha.tipo == 'Entrada':
                        nodoActual.derecha.tipo = 'CaminandoEntrada'
                    elif nodoActual.derecha.tipo == 'Civil':
                        nodoActual.derecha.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.derecha.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.derecha
                    
                elif nodoActual.izquierda != None and (nodoActual.izquierda.tipo == 'Camino' or nodoActual.izquierda.tipo == 'Entrada' or nodoActual.izquierda.tipo == 'Civil') and nodoActual.izquierda != nodoFinal and nodoActual.izquierda != Entrada and nodoActual.coordenadaX < nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.izquierda.tipo == 'Entrada':
                        nodoActual.izquierda.tipo = 'CaminandoEntrada'
                    elif nodoActual.izquierda.tipo == 'Civil':
                        nodoActual.izquierda.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.izquierda.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.izquierda

                elif nodoActual.arriba != None and (nodoActual.arriba.tipo == 'Camino' or nodoActual.arriba.tipo == 'Entrada' or nodoActual.arriba.tipo == 'Civil') and nodoActual.arriba != nodoFinal and nodoActual.arriba != Entrada and nodoActual.coordenadaX < nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.arriba.tipo == 'Entrada':
                        nodoActual.arriba.tipo = 'CaminandoEntrada'
                    elif nodoActual.arriba.tipo == 'Civil':
                        nodoActual.arriba.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.arriba.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.arriba
                
                #No hay que pelear                
                elif (nodoActual.derecha != None and nodoActual.derecha.tipo == 'UnidadMilitar'
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.derecha.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.derecha
                
                elif (nodoActual.abajo != None and nodoActual.abajo.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.abajo.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.abajo
                    
                elif (nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY) != False 
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    casillas_recorridas += 1
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    nodoActual.izquierda.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.izquierda

                elif (nodoActual.arriba != None and nodoActual.arriba.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.arriba.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.arriba
                #No ha llegado
                elif nodoActual.derecha != None and nodoActual.derecha == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.izquierda != None and nodoActual.izquierda == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.abajo != None and nodoActual.abajo == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.arriba != None and nodoActual.arriba == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                else:
                    #No ha regresado al inicio
                    if nodoActual.derecha != None and nodoActual.derecha == Entrada :
                        if (nodoActual.derecha.derecha.tipo == 'Camino' or nodoActual.derecha.derecha.tipo == 'Entrada' or nodoActual.derecha.derecha.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.derecha.derecha.tipo == 'Entrada':
                                nodoActual.derecha.derecha.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.derecha.derecha
                            elif nodoActual.derecha.derecha.tipo == 'Civil':
                                nodoActual.derecha.derecha.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.derecha.derecha
                            else:
                                nodoActual.derecha.derecha.tipo = 'Caminando'
                                nodoActual = nodoActual.derecha.derecha
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                    elif nodoActual.izquierda != None and nodoActual.izquierda == Entrada :
                        if nodoActual.izquierda.izquierda!= None and (nodoActual.izquierda.izquierda.tipo == 'Camino' or nodoActual.izquierda.izquierda.tipo == 'Entrada' or nodoActual.izquierda.izquierda.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.izquierda.izquierda.tipo == 'Entrada':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.izquierda.izquierda
                            elif nodoActual.izquierda.izquierda.tipo == 'Civil':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.izquierda.izquierda
                            else:
                                nodoActual.izquierda.tipo = 'Caminando'
                                nodoActual = nodoActual.izquierda.izquierda
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                        
                    elif nodoActual.abajo != None and nodoActual.abajo == Entrada :
                        if nodoActual.abajo.abajo != None and (nodoActual.abajo.abajo.tipo == 'Camino' or nodoActual.abajo.abajo.tipo == 'Entrada' or nodoActual.abajo.abajo.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.abajo.tipo == 'Entrada':
                                nodoActual.abajo.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.abajo.abajo
                            elif nodoActual.abajo.abajo.tipo == 'Civil':
                                nodoActual.abajo.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.abajo.abajo
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.abajo.abajo
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                        
                    elif nodoActual.arriba!= None and nodoActual.arriba== Entrada :
                        if nodoActual.arriba.arriba != None and (nodoActual.arriba.arriba.tipo == 'Camino' or nodoActual.arriba.arriba.tipo == 'Entrada' or nodoActual.arriba.arriba.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.arriba.arriba.tipo == 'Entrada':
                                nodoActual.arriba.arriba.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.arriba.arriba
                            elif nodoActual.arriba.arriba.tipo == 'Civil':
                                nodoActual.arriba.arriba.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.arriba.arriba
                            else:
                                nodoActual.arriba.tipo = 'Caminando'
                                nodoActual = nodoActual.arriba.arriba
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                        
                    #Retroceder
                    if nodoActual.derecha != None and nodoActual.derecha.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        #anterior = nodoActual
                        nodoActual = nodoActual.derecha
                        
                    elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        #anterior = nodoActual
                        nodoActual = nodoActual.izquierda
                        
                    elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        #anterior = nodoActual
                        nodoActual = nodoActual.abajo

                    elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        #anterior = nodoActual
                        nodoActual = nodoActual.arriba
                    else:
                        nodoFinal.terminal = True
                        casillas_recorridas = 10000
                        break
            #Nodo actual abajo y a la derecha
            elif nodoActual.coordenadaX >= nodoFinal.coordenadaX and nodoActual.coordenadaY >= nodoFinal.coordenadaY:
                if nodoActual.izquierda != None and (nodoActual.izquierda.tipo == 'Camino' or nodoActual.izquierda.tipo == 'Entrada' or nodoActual.izquierda.tipo == 'Civil') and nodoActual.izquierda != nodoFinal and nodoActual.izquierda != Entrada and nodoActual.coordenadaX <= nodoFinal.coordenadaX :
                    casillas_recorridas += 1
                    if nodoActual.izquierda.tipo == 'Entrada':
                        nodoActual.izquierda.tipo = 'CaminandoEntrada'
                    elif nodoActual.izquierda.tipo == 'Civil':
                        nodoActual.izquierda.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda

                elif nodoActual.arriba != None and (nodoActual.arriba.tipo == 'Camino' or nodoActual.arriba.tipo == 'Entrada' or nodoActual.arriba.tipo == 'Civil') and nodoActual.arriba != nodoFinal and nodoActual.arriba != Entrada and nodoActual.coordenadaX <= nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.arriba.tipo == 'Entrada':
                        nodoActual.arriba.tipo = 'CaminandoEntrada'
                    elif nodoActual.arriba.tipo == 'Civil':
                        nodoActual.arriba.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba

                elif nodoActual.derecha != None and (nodoActual.derecha.tipo == 'Camino' or nodoActual.derecha.tipo == 'Entrada' or nodoActual.derecha.tipo == 'Civil') and nodoActual.derecha!= nodoFinal and nodoActual.derecha!= Entrada and nodoActual.coordenadaX <= nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.derecha.tipo == 'Entrada':
                        nodoActual.derecha.tipo = 'CaminandoEntrada'
                    elif nodoActual.derecha.tipo == 'Civil':
                        nodoActual.derecha.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha

                elif nodoActual.abajo != None and (nodoActual.abajo.tipo == 'Camino' or nodoActual.abajo.tipo == 'Entrada' or nodoActual.abajo.tipo == 'Civil') and nodoActual.abajo!= nodoFinal and nodoActual.abajo!= Entrada and nodoActual.coordenadaX <= nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.abajo.tipo == 'Entrada':
                        nodoActual.abajo.tipo = 'CaminandoEntrada'
                    elif nodoActual.abajo.tipo == 'Civil':
                        nodoActual.abajo.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo

                
                elif nodoActual.arriba != None and (nodoActual.arriba.tipo == 'Camino' or nodoActual.arriba.tipo == 'Entrada' or nodoActual.arriba.tipo == 'Civil') and nodoActual.arriba != nodoFinal and nodoActual.arriba != Entrada and nodoActual.coordenadaX > nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.arriba.tipo == 'Entrada':
                        nodoActual.arriba.tipo = 'CaminandoEntrada'
                    elif nodoActual.arriba.tipo == 'Civil':
                        nodoActual.arriba.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba
                elif nodoActual.izquierda != None and (nodoActual.izquierda.tipo == 'Camino' or nodoActual.izquierda.tipo == 'Entrada' or nodoActual.izquierda.tipo == 'Civil') and nodoActual.izquierda != nodoFinal and nodoActual.izquierda != Entrada and nodoActual.coordenadaX > nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.izquierda.tipo == 'Entrada':
                        nodoActual.izquierda.tipo = 'CaminandoEntrada'
                    elif nodoActual.izquierda.tipo == 'Civil':
                        nodoActual.izquierda.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda

                elif nodoActual.derecha != None and (nodoActual.derecha.tipo == 'Camino' or nodoActual.derecha.tipo == 'Entrada' or nodoActual.derecha.tipo == 'Civil') and nodoActual.derecha!= nodoFinal and nodoActual.derecha!= Entrada and nodoActual.coordenadaX > nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.derecha.tipo == 'Entrada':
                        nodoActual.derecha.tipo = 'CaminandoEntrada'
                    elif nodoActual.derecha.tipo == 'Civil':
                        nodoActual.derecha.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha

                elif nodoActual.abajo != None and (nodoActual.abajo.tipo == 'Camino' or nodoActual.abajo.tipo == 'Entrada' or nodoActual.abajo.tipo == 'Civil') and nodoActual.abajo!= nodoFinal and nodoActual.abajo!= Entrada and nodoActual.coordenadaX > nodoFinal.coordenadaX :
                    casillas_recorridas += 1
                    if nodoActual.abajo.tipo == 'Entrada':
                        nodoActual.abajo.tipo = 'CaminandoEntrada'
                    elif nodoActual.abajo.tipo == 'Civil':
                        nodoActual.abajo.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo

                #No ha llegado
                elif nodoActual.arriba != None and nodoActual.arriba == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.izquierda != None and nodoActual.izquierda == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.derecha != None and nodoActual.derecha == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.abajo != None and nodoActual.abajo == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                #No hay que pelear     
                elif (nodoActual.arriba != None and nodoActual.arriba.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.arriba.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.arriba
                
                elif (nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY) != False 
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    casillas_recorridas += 1
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    nodoActual.izquierda.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.izquierda

                elif (nodoActual.derecha != None and nodoActual.derecha.tipo == 'UnidadMilitar'
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.derecha.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.derecha
                
                elif (nodoActual.abajo != None and nodoActual.abajo.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.abajo.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.abajo
                    

                else:
                    #No ha regresado al inicio
                    if nodoActual.derecha != None and nodoActual.derecha == Entrada :
                        if (nodoActual.derecha.derecha.tipo == 'Camino' or nodoActual.derecha.derecha.tipo == 'Entrada' or nodoActual.derecha.derecha.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.tipo == 'Entrada':
                                nodoActual.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.derecha.derecha
                            elif nodoActual.abajo.tipo == 'Civil':
                                nodoActual.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.derecha.derecha
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.derecha.derecha
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                        casillas_recorridas = 10000
                        nodoFinal.terminal = True
                        break
                    elif nodoActual.izquierda != None and nodoActual.izquierda == Entrada :
                        if nodoActual.izquierda.izquierda!= None and (nodoActual.izquierda.izquierda.tipo == 'Camino' or nodoActual.izquierda.izquierda.tipo == 'Entrada' or nodoActual.izquierda.izquierda.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.izquierda.izquierda.tipo == 'Entrada':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.izquierda.izquierda
                            elif nodoActual.izquierda.izquierda.tipo == 'Civil':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.izquierda.izquierda
                            else:
                                nodoActual.izquierda.tipo = 'Caminando'
                                nodoActual = nodoActual.izquierda.izquierda
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                        
                    elif nodoActual.abajo != None and nodoActual.abajo == Entrada :
                        if nodoActual.abajo.abajo != None and (nodoActual.abajo.abajo.tipo == 'Camino' or nodoActual.abajo.abajo.tipo == 'Entrada' or nodoActual.abajo.abajo.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.abajo.tipo == 'Entrada':
                                nodoActual.abajo.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.abajo.abajo
                            elif nodoActual.abajo.abajo.tipo == 'Civil':
                                nodoActual.abajo.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.abajo.abajo
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.abajo.abajo
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                        casillas_recorridas = 10000
                        nodoFinal.terminal = True
                        break
                    elif nodoActual.arriba!= None and nodoActual.arriba== Entrada :
                        if nodoActual.arriba.arriba != None and (nodoActual.arriba.arriba.tipo == 'Camino' or nodoActual.arriba.arriba.tipo == 'Entrada' or nodoActual.arriba.arriba.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.arriba.arriba.tipo == 'Entrada':
                                nodoActual.arriba.arriba.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.arriba.arriba
                            elif nodoActual.arriba.arriba.tipo == 'Civil':
                                nodoActual.arriba.arriba.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.arriba.arriba
                            else:
                                nodoActual.arriba.tipo = 'Caminando'
                                nodoActual = nodoActual.arriba.arriba
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break

                    #Retroceder
                    if nodoActual.arriba != None and nodoActual.arriba.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.arriba

                    elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.izquierda

                    elif nodoActual.derecha != None and nodoActual.derecha.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.derecha

                    elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.abajo
                    else:
                        nodoFinal.terminal = True
                        casillas_recorridas = 10000
                        break

            #Nodo actual abajo y a la izquierda
            elif nodoActual.coordenadaX >= nodoFinal.coordenadaX and nodoActual.coordenadaY <= nodoFinal.coordenadaY:
                if nodoActual.derecha != None and (nodoActual.derecha.tipo == 'Camino' or nodoActual.derecha.tipo == 'Entrada' or nodoActual.derecha.tipo == 'Civil') and nodoActual.derecha!= nodoFinal and nodoActual.derecha!= Entrada and nodoActual.coordenadaX >= nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.derecha.tipo == 'Entrada':
                        nodoActual.derecha.tipo = 'CaminandoEntrada'
                    elif nodoActual.derecha.tipo == 'Civil':
                        nodoActual.derecha.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha
                
                elif nodoActual.arriba != None and (nodoActual.arriba.tipo == 'Camino' or nodoActual.arriba.tipo == 'Entrada' or nodoActual.arriba.tipo == 'Civil') and nodoActual.arriba != nodoFinal and nodoActual.arriba != Entrada and nodoActual.coordenadaX >= nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.arriba.tipo == 'Entrada':
                        nodoActual.arriba.tipo = 'CaminandoEntrada'
                    elif nodoActual.arriba.tipo == 'Civil':
                        nodoActual.arriba.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba

                elif nodoActual.izquierda != None and (nodoActual.izquierda.tipo == 'Camino' or nodoActual.izquierda.tipo == 'Entrada' or nodoActual.izquierda.tipo == 'Civil') and nodoActual.izquierda != nodoFinal and nodoActual.izquierda != Entrada and nodoActual.coordenadaX >= nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.izquierda.tipo == 'Entrada':
                        nodoActual.izquierda.tipo = 'CaminandoEntrada'
                    elif nodoActual.izquierda.tipo == 'Civil':
                        nodoActual.izquierda.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda

                elif nodoActual.abajo != None and (nodoActual.abajo.tipo == 'Camino' or nodoActual.abajo.tipo == 'Entrada' or nodoActual.abajo.tipo == 'Civil') and nodoActual.abajo!= nodoFinal and nodoActual.abajo!= Entrada and nodoActual.coordenadaX >= nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.abajo.tipo == 'Entrada':
                        nodoActual.abajo.tipo = 'CaminandoEntrada'
                    elif nodoActual.abajo.tipo == 'Civil':
                        nodoActual.abajo.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo

                elif nodoActual.arriba != None and (nodoActual.arriba.tipo == 'Camino' or nodoActual.arriba.tipo == 'Entrada' or nodoActual.arriba.tipo == 'Civil') and nodoActual.arriba != nodoFinal and nodoActual.arriba != Entrada and nodoActual.coordenadaX < nodoFinal.coordenadaX:
                        casillas_recorridas += 1
                        if nodoActual.arriba.tipo == 'Entrada':
                            nodoActual.arriba.tipo = 'CaminandoEntrada'
                        elif nodoActual.arriba.tipo == 'Civil':
                            nodoActual.arriba.tipo = 'CaminandoCivil'
                        else:
                            nodoActual.arriba.tipo = 'Caminando'
                        nodoActual = nodoActual.arriba
                elif nodoActual.derecha != None and (nodoActual.derecha.tipo == 'Camino' or nodoActual.derecha.tipo == 'Entrada' or nodoActual.derecha.tipo == 'Civil') and nodoActual.derecha!= nodoFinal and nodoActual.derecha!= Entrada and nodoActual.coordenadaX < nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.derecha.tipo == 'Entrada':
                        nodoActual.derecha.tipo = 'CaminandoEntrada'
                    elif nodoActual.derecha.tipo == 'Civil':
                        nodoActual.derecha.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha

                elif nodoActual.izquierda != None and (nodoActual.izquierda.tipo == 'Camino' or nodoActual.izquierda.tipo == 'Entrada' or nodoActual.izquierda.tipo == 'Civil') and nodoActual.izquierda != nodoFinal and nodoActual.izquierda != Entrada and nodoActual.coordenadaX < nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.izquierda.tipo == 'Entrada':
                        nodoActual.izquierda.tipo = 'CaminandoEntrada'
                    elif nodoActual.izquierda.tipo == 'Civil':
                        nodoActual.izquierda.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda

                elif nodoActual.abajo != None and (nodoActual.abajo.tipo == 'Camino' or nodoActual.abajo.tipo == 'Entrada' or nodoActual.abajo.tipo == 'Civil') and nodoActual.abajo!= nodoFinal and nodoActual.abajo!= Entrada and nodoActual.coordenadaX < nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.abajo.tipo == 'Entrada':
                        nodoActual.abajo.tipo = 'CaminandoEntrada'
                    elif nodoActual.abajo.tipo == 'Civil':
                        nodoActual.abajo.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo

                #No ha llegado
                
                elif nodoActual.derecha != None and nodoActual.derecha == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.izquierda != None and nodoActual.izquierda == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.arriba != None and nodoActual.arriba == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.abajo != None and nodoActual.abajo == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                    #No hay que pelear   

                elif (nodoActual.derecha != None and nodoActual.derecha.tipo == 'UnidadMilitar'
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.derecha.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.derecha
                
                elif (nodoActual.arriba != None and nodoActual.arriba.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.arriba.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.arriba
                
                elif (nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY) != False 
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    casillas_recorridas += 1
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    nodoActual.izquierda.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.izquierda
                
                elif (nodoActual.abajo != None and nodoActual.abajo.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.abajo.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.abajo
                else:
                    #No ha regresado al inicio
                    if nodoActual.derecha != None and nodoActual.derecha == Entrada :
                        if (nodoActual.derecha.derecha.tipo == 'Camino' or nodoActual.derecha.derecha.tipo == 'Entrada' or nodoActual.derecha.derecha.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.tipo == 'Entrada':
                                nodoActual.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.derecha.derecha
                            elif nodoActual.abajo.tipo == 'Civil':
                                nodoActual.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.derecha.derecha
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.derecha.derecha
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break

                    elif nodoActual.izquierda != None and nodoActual.izquierda == Entrada :
                        if nodoActual.izquierda.izquierda!= None and (nodoActual.izquierda.izquierda.tipo == 'Camino' or nodoActual.izquierda.izquierda.tipo == 'Entrada' or nodoActual.izquierda.izquierda.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.izquierda.izquierda.tipo == 'Entrada':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.izquierda.izquierda
                            elif nodoActual.izquierda.izquierda.tipo == 'Civil':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.izquierda.izquierda
                            else:
                                nodoActual.izquierda.tipo = 'Caminando'
                                nodoActual = nodoActual.izquierda.izquierda
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                        
                    elif nodoActual.abajo != None and nodoActual.abajo == Entrada :
                        if nodoActual.abajo.abajo != None and (nodoActual.abajo.abajo.tipo == 'Camino' or nodoActual.abajo.abajo.tipo == 'Entrada' or nodoActual.abajo.abajo.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.abajo.tipo == 'Entrada':
                                nodoActual.abajo.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.abajo.abajo
                            elif nodoActual.abajo.abajo.tipo == 'Civil':
                                nodoActual.abajo.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.abajo.abajo
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.abajo.abajo
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                    elif nodoActual.arriba!= None and nodoActual.arriba== Entrada :
                        if nodoActual.arriba.arriba != None and (nodoActual.arriba.arriba.tipo == 'Camino' or nodoActual.arriba.arriba.tipo == 'Entrada' or nodoActual.arriba.arriba.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.arriba.arriba.tipo == 'Entrada':
                                nodoActual.arriba.arriba.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.arriba.arriba
                            elif nodoActual.arriba.arriba.tipo == 'Civil':
                                nodoActual.arriba.arriba.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.arriba.arriba
                            else:
                                nodoActual.arriba.tipo = 'Caminando'
                                nodoActual = nodoActual.arriba.arriba
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break

                    #Retroceder
                    if nodoActual.derecha != None and nodoActual.derecha.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.derecha

                    elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.izquierda

                    elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.arriba

                    elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.abajo
                    else:
                        nodoFinal.terminal = True
                        casillas_recorridas = 10000
                        break

            #Nodo actual arriba y a la derecha
            elif nodoActual.coordenadaX <= nodoFinal.coordenadaX and nodoActual.coordenadaY >= nodoFinal.coordenadaY:
                if nodoActual.izquierda != None and (nodoActual.izquierda.tipo == 'Camino' or nodoActual.izquierda.tipo == 'Entrada' or nodoActual.izquierda.tipo == 'Civil') and nodoActual.izquierda != nodoFinal and nodoActual.izquierda != Entrada and nodoActual.coordenadaX <= nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.izquierda.tipo == 'Entrada':
                        nodoActual.izquierda.tipo = 'CaminandoEntrada'
                    elif nodoActual.izquierda.tipo == 'Civil':
                        nodoActual.izquierda.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda
                
                elif nodoActual.abajo != None and (nodoActual.abajo.tipo == 'Camino' or nodoActual.abajo.tipo == 'Entrada' or nodoActual.abajo.tipo == 'Civil') and nodoActual.abajo!= nodoFinal and nodoActual.abajo!= Entrada and nodoActual.coordenadaX <= nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.abajo.tipo == 'Entrada':
                        nodoActual.abajo.tipo = 'CaminandoEntrada'
                    elif nodoActual.abajo.tipo == 'Civil':
                        nodoActual.abajo.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo
                
                elif nodoActual.derecha != None and (nodoActual.derecha.tipo == 'Camino' or nodoActual.derecha.tipo == 'Entrada' or nodoActual.derecha.tipo == 'Civil') and nodoActual.derecha!= nodoFinal and nodoActual.derecha!= Entrada and nodoActual.coordenadaX <= nodoFinal.coordenadaX :
                    casillas_recorridas += 1
                    if nodoActual.derecha.tipo == 'Entrada':
                        nodoActual.derecha.tipo = 'CaminandoEntrada'
                    elif nodoActual.derecha.tipo == 'Civil':
                        nodoActual.derecha.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha
                
                elif nodoActual.arriba != None and (nodoActual.arriba.tipo == 'Camino' or nodoActual.arriba.tipo == 'Entrada' or nodoActual.arriba.tipo == 'Civil') and nodoActual.arriba != nodoFinal and nodoActual.arriba != Entrada and nodoActual.coordenadaX <= nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.arriba.tipo == 'Entrada':
                        nodoActual.arriba.tipo = 'CaminandoEntrada'
                    elif nodoActual.arriba.tipo == 'Civil':
                        nodoActual.arriba.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba

                elif nodoActual.abajo != None and (nodoActual.abajo.tipo == 'Camino' or nodoActual.abajo.tipo == 'Entrada' or nodoActual.abajo.tipo == 'Civil') and nodoActual.abajo!= nodoFinal and nodoActual.abajo!= Entrada and nodoActual.coordenadaX > nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.abajo.tipo == 'Entrada':
                        nodoActual.abajo.tipo = 'CaminandoEntrada'
                    elif nodoActual.abajo.tipo == 'Civil':
                        nodoActual.abajo.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo
                elif nodoActual.izquierda != None and (nodoActual.izquierda.tipo == 'Camino' or nodoActual.izquierda.tipo == 'Entrada' or nodoActual.izquierda.tipo == 'Civil') and nodoActual.izquierda != nodoFinal and nodoActual.izquierda != Entrada and nodoActual.coordenadaX > nodoFinal.coordenadaX :
                    casillas_recorridas += 1
                    if nodoActual.izquierda.tipo == 'Entrada':
                        nodoActual.izquierda.tipo = 'CaminandoEntrada'
                    elif nodoActual.izquierda.tipo == 'Civil':
                        nodoActual.izquierda.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda
                
                elif nodoActual.derecha != None and (nodoActual.derecha.tipo == 'Camino' or nodoActual.derecha.tipo == 'Entrada' or nodoActual.derecha.tipo == 'Civil') and nodoActual.derecha!= nodoFinal and nodoActual.derecha!= Entrada and nodoActual.coordenadaX > nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.derecha.tipo == 'Entrada':
                        nodoActual.derecha.tipo = 'CaminandoEntrada'
                    elif nodoActual.derecha.tipo == 'Civil':
                        nodoActual.derecha.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha
                
                elif nodoActual.arriba != None and (nodoActual.arriba.tipo == 'Camino' or nodoActual.arriba.tipo == 'Entrada' or nodoActual.arriba.tipo == 'Civil') and nodoActual.arriba != nodoFinal and nodoActual.arriba != Entrada and nodoActual.coordenadaX > nodoFinal.coordenadaX:
                    casillas_recorridas += 1
                    if nodoActual.arriba.tipo == 'Entrada':
                        nodoActual.arriba.tipo = 'CaminandoEntrada'
                    elif nodoActual.arriba.tipo == 'Civil':
                        nodoActual.arriba.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba

                #No ha llegado
                elif nodoActual.izquierda != None and nodoActual.izquierda == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.derecha != None and nodoActual.derecha == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.abajo != None and nodoActual.abajo == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                elif nodoActual.arriba != None and nodoActual.arriba == nodoFinal :
                    casillas_recorridas += 1
                    nodoActual.tipo = 'Caminando'
                    nodoFinal.terminal = True
                    break
                #No hay que pelear   
                elif (nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY) != False 
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    casillas_recorridas += 1
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    nodoActual.izquierda.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.izquierda
                
                elif (nodoActual.abajo != None and nodoActual.abajo.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.abajo.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.abajo
                elif (nodoActual.derecha != None and nodoActual.derecha.tipo == 'UnidadMilitar'
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.derecha.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.derecha
                
                elif (nodoActual.arriba != None and nodoActual.arriba.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.arriba.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.arriba
                
                
                else:
                    #No ha regresado al inicio
                    if nodoActual.derecha != None and nodoActual.derecha == Entrada :
                        if (nodoActual.derecha.derecha.tipo == 'Camino' or nodoActual.derecha.derecha.tipo == 'Entrada' or nodoActual.derecha.derecha.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.tipo == 'Entrada':
                                nodoActual.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.derecha.derecha
                            elif nodoActual.abajo.tipo == 'Civil':
                                nodoActual.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.derecha.derecha
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.derecha.derecha
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break

                    elif nodoActual.izquierda != None and nodoActual.izquierda == Entrada :
                        if nodoActual.izquierda.izquierda!= None and (nodoActual.izquierda.izquierda.tipo == 'Camino' or nodoActual.izquierda.izquierda.tipo == 'Entrada' or nodoActual.izquierda.izquierda.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.izquierda.izquierda.tipo == 'Entrada':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.izquierda.izquierda
                            elif nodoActual.izquierda.izquierda.tipo == 'Civil':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.izquierda.izquierda
                            else:
                                nodoActual.izquierda.tipo = 'Caminando'
                                nodoActual = nodoActual.izquierda.izquierda
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                        
                    elif nodoActual.abajo != None and nodoActual.abajo == Entrada :
                        if nodoActual.abajo.abajo != None and (nodoActual.abajo.abajo.tipo == 'Camino' or nodoActual.abajo.abajo.tipo == 'Entrada' or nodoActual.abajo.abajo.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.abajo.tipo == 'Entrada':
                                nodoActual.abajo.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.abajo.abajo
                            elif nodoActual.abajo.abajo.tipo == 'Civil':
                                nodoActual.abajo.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.abajo.abajo
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.abajo.abajo
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break

                    elif nodoActual.arriba!= None and nodoActual.arriba== Entrada :
                        if nodoActual.arriba.arriba != None and (nodoActual.arriba.arriba.tipo == 'Camino' or nodoActual.arriba.arriba.tipo == 'Entrada' or nodoActual.arriba.arriba.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.arriba.arriba.tipo == 'Entrada':
                                nodoActual.arriba.arriba.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.arriba.arriba
                            elif nodoActual.arriba.arriba.tipo == 'Civil':
                                nodoActual.arriba.arriba.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.arriba.arriba
                            else:
                                nodoActual.arriba.tipo = 'Caminando'
                                nodoActual = nodoActual.arriba.arriba
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break

                    #Retroceder
                    if nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.izquierda
                    
                    elif nodoActual.derecha != None and nodoActual.derecha.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.derecha

                    elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.abajo
                    
                    elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Caminando' :
                        casillas_recorridas -= 1
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.arriba
                    else:
                        nodoFinal.terminal = True
                        casillas_recorridas = 10000
                        break
            
            else:
                    if nodoActual.derecha != None and nodoActual.derecha == Entrada :
                        if (nodoActual.derecha.derecha.tipo == 'Camino' or nodoActual.derecha.derecha.tipo == 'Entrada' or nodoActual.derecha.derecha.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.tipo == 'Entrada':
                                nodoActual.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.derecha.derecha
                            elif nodoActual.abajo.tipo == 'Civil':
                                nodoActual.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.derecha.derecha
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.derecha.derecha
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break

                    elif nodoActual.izquierda != None and nodoActual.izquierda == Entrada :
                        if nodoActual.izquierda.izquierda!= None and (nodoActual.izquierda.izquierda.tipo == 'Camino' or nodoActual.izquierda.izquierda.tipo == 'Entrada' or nodoActual.izquierda.izquierda.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.izquierda.izquierda.tipo == 'Entrada':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.izquierda.izquierda
                            elif nodoActual.izquierda.izquierda.tipo == 'Civil':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.izquierda.izquierda
                            else:
                                nodoActual.izquierda.tipo = 'Caminando'
                                nodoActual = nodoActual.izquierda.izquierda
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                        
                    elif nodoActual.abajo != None and nodoActual.abajo == Entrada :
                        if nodoActual.abajo.abajo != None and (nodoActual.abajo.abajo.tipo == 'Camino' or nodoActual.abajo.abajo.tipo == 'Entrada' or nodoActual.abajo.abajo.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.abajo.tipo == 'Entrada':
                                nodoActual.abajo.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.abajo.abajo
                            elif nodoActual.abajo.abajo.tipo == 'Civil':
                                nodoActual.abajo.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.abajo.abajo
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.abajo.abajo
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break

                    elif nodoActual.arriba!= None and nodoActual.arriba== Entrada :
                        if nodoActual.arriba.arriba != None and (nodoActual.arriba.arriba.tipo == 'Camino' or nodoActual.arriba.arriba.tipo == 'Entrada' or nodoActual.arriba.arriba.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.arriba.arriba.tipo == 'Entrada':
                                nodoActual.arriba.arriba.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.arriba.arriba
                            elif nodoActual.arriba.arriba.tipo == 'Civil':
                                nodoActual.arriba.arriba.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.arriba.arriba
                            else:
                                nodoActual.arriba.tipo = 'Caminando'
                                nodoActual = nodoActual.arriba.arriba
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break

        if lista_robots.search_item(robot,'ChapinFighter') != False :
            lista_robots.search_item(robot,'ChapinFighter').setFuerza(fuerza_tmp )
        ciudad.limpiarCaminos()
        return casillas_recorridas

def recorrerCiudadFinal(nodoFinal,ciudad,robot):

        ciudad.limpiarCaminos()
        nodoActual = nodoFinal.getEntrada()
        Entrada = nodoActual
        nodoFinal.terminal = False
        casillas_recorridas = 0
        while nodoFinal.terminal is False:

            #Nodo actual arriba y a la izquierda
            if nodoActual.coordenadaX <= nodoFinal.coordenadaX and nodoActual.coordenadaY <= nodoFinal.coordenadaY:
                
                if nodoActual.derecha != None and (nodoActual.derecha.tipo == 'Camino' or nodoActual.derecha.tipo == 'Entrada' or nodoActual.derecha.tipo == 'Civil') and nodoActual.derecha!= nodoFinal and nodoActual.derecha!= Entrada and nodoActual.coordenadaX >= nodoFinal.coordenadaX:
                    if nodoActual.derecha.tipo == 'Entrada':
                        nodoActual.derecha.tipo = 'CaminandoEntrada'
                    elif nodoActual.derecha.tipo == 'Civil':
                        nodoActual.derecha.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.derecha.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.derecha
                elif nodoActual.arriba != None and (nodoActual.arriba.tipo == 'Camino' or nodoActual.arriba.tipo == 'Entrada' or nodoActual.arriba.tipo == 'Civil') and nodoActual.arriba != nodoFinal and nodoActual.arriba != Entrada and nodoActual.coordenadaX >= nodoFinal.coordenadaX :
                    if nodoActual.arriba.tipo == 'Entrada':
                        nodoActual.arriba.tipo = 'CaminandoEntrada'
                    elif nodoActual.arriba.tipo == 'Civil':
                        nodoActual.arriba.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.arriba.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.arriba
                elif nodoActual.abajo != None and (nodoActual.abajo.tipo == 'Camino' or nodoActual.abajo.tipo == 'Entrada' or nodoActual.abajo.tipo == 'Civil') and nodoActual.abajo!= nodoFinal and nodoActual.abajo!= Entrada  and nodoActual.coordenadaX >= nodoFinal.coordenadaX:
                    if nodoActual.abajo.tipo == 'Entrada':
                        nodoActual.abajo.tipo = 'CaminandoEntrada'
                    elif nodoActual.abajo.tipo == 'Civil':
                        nodoActual.abajo.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.abajo.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.abajo
                    
                elif nodoActual.izquierda != None and (nodoActual.izquierda.tipo == 'Camino' or nodoActual.izquierda.tipo == 'Entrada' or nodoActual.izquierda.tipo == 'Civil') and nodoActual.izquierda != nodoFinal and nodoActual.izquierda != Entrada  and nodoActual.coordenadaX >= nodoFinal.coordenadaX:
                    if nodoActual.izquierda.tipo == 'Entrada':
                        nodoActual.izquierda.tipo = 'CaminandoEntrada'
                    elif nodoActual.izquierda.tipo == 'Civil':
                        nodoActual.izquierda.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.izquierda.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.izquierda

                
                elif nodoActual.abajo != None and (nodoActual.abajo.tipo == 'Camino' or nodoActual.abajo.tipo == 'Entrada' or nodoActual.abajo.tipo == 'Civil') and nodoActual.abajo!= nodoFinal and nodoActual.abajo!= Entrada  and nodoActual.coordenadaX < nodoFinal.coordenadaX:
                    if nodoActual.abajo.tipo == 'Entrada':
                        nodoActual.abajo.tipo = 'CaminandoEntrada'
                    elif nodoActual.abajo.tipo == 'Civil':
                        nodoActual.abajo.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.abajo.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.abajo
                elif nodoActual.derecha != None and (nodoActual.derecha.tipo == 'Camino' or nodoActual.derecha.tipo == 'Entrada' or nodoActual.derecha.tipo == 'Civil') and nodoActual.derecha!= nodoFinal and nodoActual.derecha!= Entrada and nodoActual.coordenadaX < nodoFinal.coordenadaX:
                    if nodoActual.derecha.tipo == 'Entrada':
                        nodoActual.derecha.tipo = 'CaminandoEntrada'
                    elif nodoActual.derecha.tipo == 'Civil':
                        nodoActual.derecha.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.derecha.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.derecha
                    
                elif nodoActual.izquierda != None and (nodoActual.izquierda.tipo == 'Camino' or nodoActual.izquierda.tipo == 'Entrada' or nodoActual.izquierda.tipo == 'Civil') and nodoActual.izquierda != nodoFinal and nodoActual.izquierda != Entrada  and nodoActual.coordenadaX < nodoFinal.coordenadaX:
                    if nodoActual.izquierda.tipo == 'Entrada':
                        nodoActual.izquierda.tipo = 'CaminandoEntrada'
                    elif nodoActual.izquierda.tipo == 'Civil':
                        nodoActual.izquierda.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.izquierda.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.izquierda

                elif nodoActual.arriba != None and (nodoActual.arriba.tipo == 'Camino' or nodoActual.arriba.tipo == 'Entrada' or nodoActual.arriba.tipo == 'Civil') and nodoActual.arriba != nodoFinal and nodoActual.arriba != Entrada and nodoActual.coordenadaX < nodoFinal.coordenadaX :
                    if nodoActual.arriba.tipo == 'Entrada':
                        nodoActual.arriba.tipo = 'CaminandoEntrada'
                    elif nodoActual.arriba.tipo == 'Civil':
                        nodoActual.arriba.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.arriba.tipo = 'Caminando'
                    #anterior = nodoActual
                    nodoActual = nodoActual.arriba
                #No ha llegado
                elif nodoActual.derecha != None and nodoActual.derecha == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad().replace(" ",""),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.izquierda != None and nodoActual.izquierda == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad().replace(" ",""),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.abajo != None and nodoActual.abajo == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad().replace(" ",""),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.arriba != None and nodoActual.arriba == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad().replace(" ",""),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                #No hay que pelear                
                elif (nodoActual.derecha != None and nodoActual.derecha.tipo == 'UnidadMilitar'
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.derecha.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.derecha
                
                elif (nodoActual.abajo != None and nodoActual.abajo.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoAPctual.abajo.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.abajo.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.abajo
                    
                elif (nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY) != False 
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    casillas_recorridas += 1
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    nodoActual.izquierda.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.izquierda

                elif (nodoActual.arriba != None and nodoActual.arriba.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.izquierda.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.arriba
                else:
                    #No ha regresado al inicio
                    if nodoActual.derecha != None and nodoActual.derecha == Entrada :
                        if (nodoActual.derecha.derecha.tipo == 'Camino' or nodoActual.derecha.derecha.tipo == 'Entrada' or nodoActual.derecha.derecha.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.derecha.derecha.tipo == 'Entrada':
                                nodoActual.derecha.derecha.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.derecha.derecha
                            elif nodoActual.derecha.derecha.tipo == 'Civil':
                                nodoActual.derecha.derecha.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.derecha.derecha
                            else:
                                nodoActual.derecha.derecha.tipo = 'Caminando'
                                nodoActual = nodoActual.derecha.derecha
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                    elif nodoActual.izquierda != None and nodoActual.izquierda == Entrada :
                        if nodoActual.izquierda.izquierda!= None and (nodoActual.izquierda.izquierda.tipo == 'Camino' or nodoActual.izquierda.izquierda.tipo == 'Entrada' or nodoActual.izquierda.izquierda.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.izquierda.izquierda.tipo == 'Entrada':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.izquierda.izquierda
                            elif nodoActual.izquierda.izquierda.tipo == 'Civil':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.izquierda.izquierda
                            else:
                                nodoActual.izquierda.tipo = 'Caminando'
                                nodoActual = nodoActual.izquierda.izquierda
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                        
                    elif nodoActual.abajo != None and nodoActual.abajo == Entrada :
                        if nodoActual.abajo.abajo != None and (nodoActual.abajo.abajo.tipo == 'Camino' or nodoActual.abajo.abajo.tipo == 'Entrada' or nodoActual.abajo.abajo.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.abajo.tipo == 'Entrada':
                                nodoActual.abajo.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.abajo.abajo
                            elif nodoActual.abajo.abajo.tipo == 'Civil':
                                nodoActual.abajo.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.abajo.abajo
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.abajo.abajo
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                        
                    elif nodoActual.arriba!= None and nodoActual.arriba== Entrada :
                        if nodoActual.arriba.arriba != None and (nodoActual.arriba.arriba.tipo == 'Camino' or nodoActual.arriba.arriba.tipo == 'Entrada' or nodoActual.arriba.arriba.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.arriba.arriba.tipo == 'Entrada':
                                nodoActual.arriba.arriba.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.arriba.arriba
                            elif nodoActual.arriba.arriba.tipo == 'Civil':
                                nodoActual.arriba.arriba.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.arriba.arriba
                            else:
                                nodoActual.arriba.tipo = 'Caminando'
                                nodoActual = nodoActual.arriba.arriba
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                    #Retroceder
                    if nodoActual.derecha != None and nodoActual.derecha.tipo == 'Caminando' :
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        #anterior = nodoActual
                        nodoActual = nodoActual.derecha
                        
                    elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Caminando' :
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        #anterior = nodoActual
                        nodoActual = nodoActual.izquierda
                        
                    elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Caminando' :
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        #anterior = nodoActual
                        nodoActual = nodoActual.abajo

                    elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Caminando' :
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        #anterior = nodoActual
                        nodoActual = nodoActual.arriba
            #Nodo actual abajo y a la derecha
            elif nodoActual.coordenadaX >= nodoFinal.coordenadaX and nodoActual.coordenadaY >= nodoFinal.coordenadaY:

                if nodoActual.izquierda != None and (nodoActual.izquierda.tipo == 'Camino' or nodoActual.izquierda.tipo == 'Entrada' or nodoActual.izquierda.tipo == 'Civil') and nodoActual.izquierda != nodoFinal and nodoActual.izquierda != Entrada and nodoActual.coordenadaX <= nodoFinal.coordenadaX:
                    if nodoActual.izquierda.tipo == 'Entrada':
                        nodoActual.izquierda.tipo = 'CaminandoEntrada'
                    elif nodoActual.izquierda.tipo == 'Civil':
                        nodoActual.izquierda.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda
                elif nodoActual.arriba != None and (nodoActual.arriba.tipo == 'Camino' or nodoActual.arriba.tipo == 'Entrada' or nodoActual.arriba.tipo == 'Civil') and nodoActual.arriba != nodoFinal and nodoActual.arriba != Entrada and nodoActual.coordenadaX <= nodoFinal.coordenadaX:
                    if nodoActual.arriba.tipo == 'Entrada':
                        nodoActual.arriba.tipo = 'CaminandoEntrada'
                    elif nodoActual.arriba.tipo == 'Civil':
                        nodoActual.arriba.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba

                elif nodoActual.derecha != None and (nodoActual.derecha.tipo == 'Camino' or nodoActual.derecha.tipo == 'Entrada' or nodoActual.derecha.tipo == 'Civil') and nodoActual.derecha!= nodoFinal and nodoActual.derecha!= Entrada and nodoActual.coordenadaX <= nodoFinal.coordenadaX:
                    if nodoActual.derecha.tipo == 'Entrada':
                        nodoActual.derecha.tipo = 'CaminandoEntrada'
                    elif nodoActual.derecha.tipo == 'Civil':
                        nodoActual.derecha.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha

                elif nodoActual.abajo != None and (nodoActual.abajo.tipo == 'Camino' or nodoActual.abajo.tipo == 'Entrada' or nodoActual.abajo.tipo == 'Civil') and nodoActual.abajo!= nodoFinal and nodoActual.abajo!= Entrada and nodoActual.coordenadaX <= nodoFinal.coordenadaX:
                    if nodoActual.abajo.tipo == 'Entrada':
                        nodoActual.abajo.tipo = 'CaminandoEntrada'
                    elif nodoActual.abajo.tipo == 'Civil':
                        nodoActual.abajo.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo

                elif nodoActual.arriba != None and (nodoActual.arriba.tipo == 'Camino' or nodoActual.arriba.tipo == 'Entrada' or nodoActual.arriba.tipo == 'Civil') and nodoActual.arriba != nodoFinal and nodoActual.arriba != Entrada and nodoActual.coordenadaX > nodoFinal.coordenadaX:
                    if nodoActual.arriba.tipo == 'Entrada':
                        nodoActual.arriba.tipo = 'CaminandoEntrada'
                    elif nodoActual.arriba.tipo == 'Civil':
                        nodoActual.arriba.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba

                elif nodoActual.izquierda != None and (nodoActual.izquierda.tipo == 'Camino' or nodoActual.izquierda.tipo == 'Entrada' or nodoActual.izquierda.tipo == 'Civil') and nodoActual.izquierda != nodoFinal and nodoActual.izquierda != Entrada and nodoActual.coordenadaX > nodoFinal.coordenadaX:
                    if nodoActual.izquierda.tipo == 'Entrada':
                        nodoActual.izquierda.tipo = 'CaminandoEntrada'
                    elif nodoActual.izquierda.tipo == 'Civil':
                        nodoActual.izquierda.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda

                elif nodoActual.derecha != None and (nodoActual.derecha.tipo == 'Camino' or nodoActual.derecha.tipo == 'Entrada' or nodoActual.derecha.tipo == 'Civil') and nodoActual.derecha!= nodoFinal and nodoActual.derecha!= Entrada and nodoActual.coordenadaX > nodoFinal.coordenadaX:
                    if nodoActual.derecha.tipo == 'Entrada':
                        nodoActual.derecha.tipo = 'CaminandoEntrada'
                    elif nodoActual.derecha.tipo == 'Civil':
                        nodoActual.derecha.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha

                elif nodoActual.abajo != None and (nodoActual.abajo.tipo == 'Camino' or nodoActual.abajo.tipo == 'Entrada' or nodoActual.abajo.tipo == 'Civil') and nodoActual.abajo!= nodoFinal and nodoActual.abajo!= Entrada and nodoActual.coordenadaX > nodoFinal.coordenadaX:
                    if nodoActual.abajo.tipo == 'Entrada':
                        nodoActual.abajo.tipo = 'CaminandoEntrada'
                    elif nodoActual.abajo.tipo == 'Civil':
                        nodoActual.abajo.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo
                #No ha llegado
                
                elif nodoActual.arriba != None and nodoActual.arriba == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad().replace(" ",""),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.izquierda != None and nodoActual.izquierda == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad().replace(" ",""),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.derecha != None and nodoActual.derecha == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad().replace(" ",""),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.abajo != None and nodoActual.abajo == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad().replace(" ",""),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                #No hay que pelear     
                elif (nodoActual.arriba != None and nodoActual.arriba.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.arriba.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.arriba
                
                elif (nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY) != False 
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    casillas_recorridas += 1
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    nodoActual.izquierda.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.izquierda

                elif (nodoActual.derecha != None and nodoActual.derecha.tipo == 'UnidadMilitar'
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.derecha.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.derecha
                
                elif (nodoActual.abajo != None and nodoActual.abajo.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.abajo.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.abajo
                    
                else:
                    #No ha regresado al inicio
                    if nodoActual.derecha != None and nodoActual.derecha == Entrada :
                        if (nodoActual.derecha.derecha.tipo == 'Camino' or nodoActual.derecha.derecha.tipo == 'Entrada' or nodoActual.derecha.derecha.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.tipo == 'Entrada':
                                nodoActual.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.derecha.derecha
                            elif nodoActual.abajo.tipo == 'Civil':
                                nodoActual.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.derecha.derecha
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.derecha.derecha
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                        casillas_recorridas = 10000
                        nodoFinal.terminal = True
                        break
                    elif nodoActual.izquierda != None and nodoActual.izquierda == Entrada :
                        if nodoActual.izquierda.izquierda!= None and (nodoActual.izquierda.izquierda.tipo == 'Camino' or nodoActual.izquierda.izquierda.tipo == 'Entrada' or nodoActual.izquierda.izquierda.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.izquierda.izquierda.tipo == 'Entrada':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.izquierda.izquierda
                            elif nodoActual.izquierda.izquierda.tipo == 'Civil':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.izquierda.izquierda
                            else:
                                nodoActual.izquierda.tipo = 'Caminando'
                                nodoActual = nodoActual.izquierda.izquierda
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                        
                    elif nodoActual.abajo != None and nodoActual.abajo == Entrada :
                        if nodoActual.abajo.abajo != None and (nodoActual.abajo.abajo.tipo == 'Camino' or nodoActual.abajo.abajo.tipo == 'Entrada' or nodoActual.abajo.abajo.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.abajo.tipo == 'Entrada':
                                nodoActual.abajo.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.abajo.abajo
                            elif nodoActual.abajo.abajo.tipo == 'Civil':
                                nodoActual.abajo.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.abajo.abajo
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.abajo.abajo
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break

                    elif nodoActual.arriba!= None and nodoActual.arriba== Entrada :
                        if nodoActual.arriba.arriba != None and (nodoActual.arriba.arriba.tipo == 'Camino' or nodoActual.arriba.arriba.tipo == 'Entrada' or nodoActual.arriba.arriba.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.arriba.arriba.tipo == 'Entrada':
                                nodoActual.arriba.arriba.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.arriba.arriba
                            elif nodoActual.arriba.arriba.tipo == 'Civil':
                                nodoActual.arriba.arriba.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.arriba.arriba
                            else:
                                nodoActual.arriba.tipo = 'Caminando'
                                nodoActual = nodoActual.arriba.arriba
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                    #Retroceder
                    if nodoActual.arriba != None and nodoActual.arriba.tipo == 'Caminando' :
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.arriba

                    elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Caminando' :
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.izquierda

                    elif nodoActual.derecha != None and nodoActual.derecha.tipo == 'Caminando' :
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.derecha

                    elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Caminando' :
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.abajo
    
            #Nodo actual abajo y a la izquierda
            elif nodoActual.coordenadaX >= nodoFinal.coordenadaX and nodoActual.coordenadaY <= nodoFinal.coordenadaY:
                if nodoActual.derecha != None and (nodoActual.derecha.tipo == 'Camino' or nodoActual.derecha.tipo == 'Entrada' or nodoActual.derecha.tipo == 'Civil') and nodoActual.derecha!= nodoFinal and nodoActual.derecha!= Entrada and nodoActual.coordenadaX >= nodoFinal.coordenadaX :
                    if nodoActual.derecha.tipo == 'Entrada':
                        nodoActual.derecha.tipo = 'CaminandoEntrada'
                    elif nodoActual.derecha.tipo == 'Civil':
                        nodoActual.derecha.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha
                
                elif nodoActual.arriba != None and (nodoActual.arriba.tipo == 'Camino' or nodoActual.arriba.tipo == 'Entrada' or nodoActual.arriba.tipo == 'Civil') and nodoActual.arriba != nodoFinal and nodoActual.arriba != Entrada and nodoActual.coordenadaX >= nodoFinal.coordenadaX:
                    if nodoActual.arriba.tipo == 'Entrada':
                        nodoActual.arriba.tipo = 'CaminandoEntrada'
                    elif nodoActual.arriba.tipo == 'Civil':
                        nodoActual.arriba.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba

                elif nodoActual.izquierda != None and (nodoActual.izquierda.tipo == 'Camino' or nodoActual.izquierda.tipo == 'Entrada' or nodoActual.izquierda.tipo == 'Civil') and nodoActual.izquierda != nodoFinal and nodoActual.izquierda != Entrada and nodoActual.coordenadaX >= nodoFinal.coordenadaX:
                    if nodoActual.izquierda.tipo == 'Entrada':
                        nodoActual.izquierda.tipo = 'CaminandoEntrada'
                    elif nodoActual.izquierda.tipo == 'Civil':
                        nodoActual.izquierda.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda

                elif nodoActual.abajo != None and (nodoActual.abajo.tipo == 'Camino' or nodoActual.abajo.tipo == 'Entrada' or nodoActual.abajo.tipo == 'Civil') and nodoActual.abajo!= nodoFinal and nodoActual.abajo!= Entrada and nodoActual.coordenadaX >= nodoFinal.coordenadaX:
                    if nodoActual.abajo.tipo == 'Entrada':
                        nodoActual.abajo.tipo = 'CaminandoEntrada'
                    elif nodoActual.abajo.tipo == 'Civil':
                        nodoActual.abajo.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo
                
                elif nodoActual.arriba != None and (nodoActual.arriba.tipo == 'Camino' or nodoActual.arriba.tipo == 'Entrada' or nodoActual.arriba.tipo == 'Civil') and nodoActual.arriba != nodoFinal and nodoActual.arriba != Entrada and nodoActual.coordenadaX < nodoFinal.coordenadaX:
                    if nodoActual.arriba.tipo == 'Entrada':
                        nodoActual.arriba.tipo = 'CaminandoEntrada'
                    elif nodoActual.arriba.tipo == 'Civil':
                        nodoActual.arriba.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba
                elif nodoActual.derecha != None and (nodoActual.derecha.tipo == 'Camino' or nodoActual.derecha.tipo == 'Entrada' or nodoActual.derecha.tipo == 'Civil') and nodoActual.derecha!= nodoFinal and nodoActual.derecha!= Entrada and nodoActual.coordenadaX < nodoFinal.coordenadaX :
                    if nodoActual.derecha.tipo == 'Entrada':
                        nodoActual.derecha.tipo = 'CaminandoEntrada'
                    elif nodoActual.derecha.tipo == 'Civil':
                        nodoActual.derecha.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha

                elif nodoActual.izquierda != None and (nodoActual.izquierda.tipo == 'Camino' or nodoActual.izquierda.tipo == 'Entrada' or nodoActual.izquierda.tipo == 'Civil') and nodoActual.izquierda != nodoFinal and nodoActual.izquierda != Entrada and nodoActual.coordenadaX < nodoFinal.coordenadaX:
                    if nodoActual.izquierda.tipo == 'Entrada':
                        nodoActual.izquierda.tipo = 'CaminandoEntrada'
                    elif nodoActual.izquierda.tipo == 'Civil':
                        nodoActual.izquierda.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda

                elif nodoActual.abajo != None and (nodoActual.abajo.tipo == 'Camino' or nodoActual.abajo.tipo == 'Entrada' or nodoActual.abajo.tipo == 'Civil') and nodoActual.abajo!= nodoFinal and nodoActual.abajo!= Entrada and nodoActual.coordenadaX < nodoFinal.coordenadaX:
                    if nodoActual.abajo.tipo == 'Entrada':
                        nodoActual.abajo.tipo = 'CaminandoEntrada'
                    elif nodoActual.abajo.tipo == 'Civil':
                        nodoActual.abajo.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo
                #No ha llegado
                
                elif nodoActual.derecha != None and nodoActual.derecha == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad().replace(" ",""),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.izquierda != None and nodoActual.izquierda == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad().replace(" ",""),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.arriba != None and nodoActual.arriba == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad().replace(" ",""),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.abajo != None and nodoActual.abajo == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad().replace(" ",""),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                #No hay que pelear   

                elif (nodoActual.derecha != None and nodoActual.derecha.tipo == 'UnidadMilitar'
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.derecha.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.derecha
                
                elif (nodoActual.arriba != None and nodoActual.arriba.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.arriba.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.arriba
                
                elif (nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY) != False 
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    casillas_recorridas += 1
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    nodoActual.izquierda.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.izquierda
                
                elif (nodoActual.abajo != None and nodoActual.abajo.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.abajo.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.abajo
                else:
                    #No ha regresado al inicio
                    if nodoActual.derecha != None and nodoActual.derecha == Entrada :
                        if (nodoActual.derecha.derecha.tipo == 'Camino' or nodoActual.derecha.derecha.tipo == 'Entrada' or nodoActual.derecha.derecha.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.tipo == 'Entrada':
                                nodoActual.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.derecha.derecha
                            elif nodoActual.abajo.tipo == 'Civil':
                                nodoActual.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.derecha.derecha
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.derecha.derecha
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break

                    elif nodoActual.izquierda != None and nodoActual.izquierda == Entrada :
                        if nodoActual.izquierda.izquierda!= None and (nodoActual.izquierda.izquierda.tipo == 'Camino' or nodoActual.izquierda.izquierda.tipo == 'Entrada' or nodoActual.izquierda.izquierda.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.izquierda.izquierda.tipo == 'Entrada':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.izquierda.izquierda
                            elif nodoActual.izquierda.izquierda.tipo == 'Civil':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.izquierda.izquierda
                            else:
                                nodoActual.izquierda.tipo = 'Caminando'
                                nodoActual = nodoActual.izquierda.izquierda
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                        
                    elif nodoActual.abajo != None and nodoActual.abajo == Entrada :
                        if nodoActual.abajo.abajo != None and (nodoActual.abajo.abajo.tipo == 'Camino' or nodoActual.abajo.abajo.tipo == 'Entrada' or nodoActual.abajo.abajo.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.abajo.tipo == 'Entrada':
                                nodoActual.abajo.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.abajo.abajo
                            elif nodoActual.abajo.abajo.tipo == 'Civil':
                                nodoActual.abajo.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.abajo.abajo
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.abajo.abajo
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                    elif nodoActual.arriba!= None and nodoActual.arriba== Entrada :
                        if nodoActual.arriba.arriba != None and (nodoActual.arriba.arriba.tipo == 'Camino' or nodoActual.arriba.arriba.tipo == 'Entrada' or nodoActual.arriba.arriba.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.arriba.arriba.tipo == 'Entrada':
                                nodoActual.arriba.arriba.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.arriba.arriba
                            elif nodoActual.arriba.arriba.tipo == 'Civil':
                                nodoActual.arriba.arriba.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.arriba.arriba
                            else:
                                nodoActual.arriba.tipo = 'Caminando'
                                nodoActual = nodoActual.arriba.arriba
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break

                    #Retroceder
                    if nodoActual.derecha != None and nodoActual.derecha.tipo == 'Caminando' :
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.derecha

                    elif nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Caminando' :
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.izquierda

                    elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Caminando' :
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.arriba

                    elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Caminando' :
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.abajo

            #Nodo actual arriba y a la derecha
            elif nodoActual.coordenadaX <= nodoFinal.coordenadaX and nodoActual.coordenadaY >= nodoFinal.coordenadaY:
                
                if nodoActual.izquierda != None and (nodoActual.izquierda.tipo == 'Camino' or nodoActual.izquierda.tipo == 'Entrada' or nodoActual.izquierda.tipo == 'Civil') and nodoActual.izquierda != nodoFinal and nodoActual.izquierda != Entrada and nodoActual.coordenadaX <= nodoFinal.coordenadaX:
                    if nodoActual.izquierda.tipo == 'Entrada':
                        nodoActual.izquierda.tipo = 'CaminandoEntrada'
                    elif nodoActual.izquierda.tipo == 'Civil':
                        nodoActual.izquierda.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda
                
                elif nodoActual.abajo != None and (nodoActual.abajo.tipo == 'Camino' or nodoActual.abajo.tipo == 'Entrada' or nodoActual.abajo.tipo == 'Civil') and nodoActual.abajo!= nodoFinal and nodoActual.abajo!= Entrada and nodoActual.coordenadaX <= nodoFinal.coordenadaX:
                    if nodoActual.abajo.tipo == 'Entrada':
                        nodoActual.abajo.tipo = 'CaminandoEntrada'
                    elif nodoActual.abajo.tipo == 'Civil':
                        nodoActual.abajo.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo
                
                elif nodoActual.derecha != None and (nodoActual.derecha.tipo == 'Camino' or nodoActual.derecha.tipo == 'Entrada' or nodoActual.derecha.tipo == 'Civil') and nodoActual.derecha!= nodoFinal and nodoActual.derecha!= Entrada and nodoActual.coordenadaX <= nodoFinal.coordenadaX:
                    if nodoActual.derecha.tipo == 'Entrada':
                        nodoActual.derecha.tipo = 'CaminandoEntrada'
                    elif nodoActual.derecha.tipo == 'Civil':
                        nodoActual.derecha.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha
                
                elif nodoActual.arriba != None and (nodoActual.arriba.tipo == 'Camino' or nodoActual.arriba.tipo == 'Entrada' or nodoActual.arriba.tipo == 'Civil') and nodoActual.arriba != nodoFinal and nodoActual.arriba != Entrada and nodoActual.coordenadaX <= nodoFinal.coordenadaX:
                    if nodoActual.arriba.tipo == 'Entrada':
                        nodoActual.arriba.tipo = 'CaminandoEntrada'
                    elif nodoActual.arriba.tipo == 'Civil':
                        nodoActual.arriba.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba
                
                elif nodoActual.abajo != None and (nodoActual.abajo.tipo == 'Camino' or nodoActual.abajo.tipo == 'Entrada' or nodoActual.abajo.tipo == 'Civil') and nodoActual.abajo!= nodoFinal and nodoActual.abajo!= Entrada and nodoActual.coordenadaX > nodoFinal.coordenadaX:
                    if nodoActual.abajo.tipo == 'Entrada':
                        nodoActual.abajo.tipo = 'CaminandoEntrada'
                    elif nodoActual.abajo.tipo == 'Civil':
                        nodoActual.abajo.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.abajo.tipo = 'Caminando'
                    nodoActual = nodoActual.abajo
                elif nodoActual.izquierda != None and (nodoActual.izquierda.tipo == 'Camino' or nodoActual.izquierda.tipo == 'Entrada' or nodoActual.izquierda.tipo == 'Civil') and nodoActual.izquierda != nodoFinal and nodoActual.izquierda != Entrada and nodoActual.coordenadaX > nodoFinal.coordenadaX:
                    if nodoActual.izquierda.tipo == 'Entrada':
                        nodoActual.izquierda.tipo = 'CaminandoEntrada'
                    elif nodoActual.izquierda.tipo == 'Civil':
                        nodoActual.izquierda.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.izquierda.tipo = 'Caminando'
                    nodoActual = nodoActual.izquierda
                
                elif nodoActual.derecha != None and (nodoActual.derecha.tipo == 'Camino' or nodoActual.derecha.tipo == 'Entrada' or nodoActual.derecha.tipo == 'Civil') and nodoActual.derecha!= nodoFinal and nodoActual.derecha!= Entrada and nodoActual.coordenadaX > nodoFinal.coordenadaX:
                    if nodoActual.derecha.tipo == 'Entrada':
                        nodoActual.derecha.tipo = 'CaminandoEntrada'
                    elif nodoActual.derecha.tipo == 'Civil':
                        nodoActual.derecha.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.derecha.tipo = 'Caminando'
                    nodoActual = nodoActual.derecha
                
                elif nodoActual.arriba != None and (nodoActual.arriba.tipo == 'Camino' or nodoActual.arriba.tipo == 'Entrada' or nodoActual.arriba.tipo == 'Civil') and nodoActual.arriba != nodoFinal and nodoActual.arriba != Entrada and nodoActual.coordenadaX > nodoFinal.coordenadaX:
                    if nodoActual.arriba.tipo == 'Entrada':
                        nodoActual.arriba.tipo = 'CaminandoEntrada'
                    elif nodoActual.arriba.tipo == 'Civil':
                        nodoActual.arriba.tipo = 'CaminandoCivil'
                    else:
                        nodoActual.arriba.tipo = 'Caminando'
                    nodoActual = nodoActual.arriba
                #No ha llegado
                elif nodoActual.izquierda != None and nodoActual.izquierda == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad().replace(" ",""),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.derecha != None and nodoActual.derecha == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad().replace(" ",""),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.abajo != None and nodoActual.abajo == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad().replace(" ",""),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                elif nodoActual.arriba != None and nodoActual.arriba == nodoFinal :
                    nodoActual.tipo = 'Caminando'
                    ciudad.graficarNeatoOrdenar(ciudad.getCiudad().replace(" ",""),ciudad)
                    nodoFinal.terminal = True
                    webbrowser.open('C:/Users/Angel/Desktop/VSCode/Carpeta para Github/Proyecto 2 IPC2/PDF/matriz_'+ciudad.getCiudad()+'.pdf')
                    break
                #No hay que pelear   
                elif (nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY) != False 
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    casillas_recorridas += 1
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.izquierda.coordenadaX,nodoActual.izquierda.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    nodoActual.izquierda.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.izquierda
                
                elif (nodoActual.abajo != None and nodoActual.abajo.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.abajo.coordenadaX,nodoActual.abajo.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.abajo.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.abajo
                elif (nodoActual.derecha != None and nodoActual.derecha.tipo == 'UnidadMilitar'
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.derecha.coordenadaX,nodoActual.derecha.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.derecha.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.derecha
                
                elif (nodoActual.arriba != None and nodoActual.arriba.tipo == 'UnidadMilitar' 
                    and ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY) != False
                    and lista_robots.search_item(robot,'ChapinFighter') != False
                    and  int(ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY).getFuerza()) <= int(lista_robots.search_item(robot,'ChapinFighter').getFuerza())):
                    capacidad1 = lista_robots.search_item(robot,'ChapinFighter').getFuerza()
                    capacidad2 = ciudad.getUnidadesMilitares().search_item(nodoActual.arriba.coordenadaX,nodoActual.arriba.coordenadaY).getFuerza()
                    lista_robots.search_item(robot,'ChapinFighter').setFuerza(int(capacidad1) - int(capacidad2))
                    casillas_recorridas += 1
                    nodoActual.arriba.tipo = 'Vencido'
                    #anterior = nodoActual
                    nodoActual = nodoActual.arriba
                
                
                else:
                    #No ha regresado al inicio
                    if nodoActual.derecha != None and nodoActual.derecha == Entrada :
                        if (nodoActual.derecha.derecha.tipo == 'Camino' or nodoActual.derecha.derecha.tipo == 'Entrada' or nodoActual.derecha.derecha.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.tipo == 'Entrada':
                                nodoActual.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.derecha.derecha
                            elif nodoActual.abajo.tipo == 'Civil':
                                nodoActual.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.derecha.derecha
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.derecha.derecha
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break

                    elif nodoActual.izquierda != None and nodoActual.izquierda == Entrada :
                        if nodoActual.izquierda.izquierda!= None and (nodoActual.izquierda.izquierda.tipo == 'Camino' or nodoActual.izquierda.izquierda.tipo == 'Entrada' or nodoActual.izquierda.izquierda.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.izquierda.izquierda.tipo == 'Entrada':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.izquierda.izquierda
                            elif nodoActual.izquierda.izquierda.tipo == 'Civil':
                                nodoActual.izquierda.izquierda.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.izquierda.izquierda
                            else:
                                nodoActual.izquierda.tipo = 'Caminando'
                                nodoActual = nodoActual.izquierda.izquierda
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break
                        
                    elif nodoActual.abajo != None and nodoActual.abajo == Entrada :
                        if nodoActual.abajo.abajo != None and (nodoActual.abajo.abajo.tipo == 'Camino' or nodoActual.abajo.abajo.tipo == 'Entrada' or nodoActual.abajo.abajo.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.abajo.tipo == 'Entrada':
                                nodoActual.abajo.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.abajo.abajo
                            elif nodoActual.abajo.abajo.tipo == 'Civil':
                                nodoActual.abajo.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.abajo.abajo
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.abajo.abajo
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break

                    elif nodoActual.arriba!= None and nodoActual.arriba== Entrada :
                        if nodoActual.arriba.arriba != None and (nodoActual.arriba.arriba.tipo == 'Camino' or nodoActual.arriba.arriba.tipo == 'Entrada' or nodoActual.arriba.arriba.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.arriba.arriba.tipo == 'Entrada':
                                nodoActual.arriba.arriba.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.arriba.arriba
                            elif nodoActual.arriba.arriba.tipo == 'Civil':
                                nodoActual.arriba.arriba.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.arriba.arriba
                            else:
                                nodoActual.arriba.tipo = 'Caminando'
                                nodoActual = nodoActual.arriba.arriba
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break

                    #Retroceder
                    if nodoActual.izquierda != None and nodoActual.izquierda.tipo == 'Caminando' :
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.izquierda
                    
                    elif nodoActual.derecha != None and nodoActual.derecha.tipo == 'Caminando' :
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.derecha

                    elif nodoActual.abajo != None and nodoActual.abajo.tipo == 'Caminando' :
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.abajo
                    
                    elif nodoActual.arriba != None and nodoActual.arriba.tipo == 'Caminando' :
                        if nodoActual.tipo == 'Entrada' or nodoActual.tipo == 'CaminandoEntrada':
                            nodoActual.tipo = 'VisitadoEntrada'
                        elif nodoActual.tipo == 'Civil' or nodoActual.tipo == 'CaminandoCivil':
                            nodoActual.tipo = 'VisitadoCivil'
                        else:
                            nodoActual.tipo = 'Visitado'
                        nodoActual = nodoActual.arriba
            else:
                if nodoActual.derecha != None and nodoActual.derecha == Entrada :
                        if (nodoActual.derecha.derecha.tipo == 'Camino' or nodoActual.derecha.derecha.tipo == 'Entrada' or nodoActual.derecha.derecha.tipo == 'Civil'):
                            casillas_recorridas = 1
                            if nodoActual.abajo.tipo == 'Entrada':
                                nodoActual.abajo.tipo = 'CaminandoEntrada'
                                nodoActual = nodoActual.derecha.derecha
                            elif nodoActual.abajo.tipo == 'Civil':
                                nodoActual.abajo.tipo = 'CaminandoCivil'
                                nodoActual = nodoActual.derecha.derecha
                            else:
                                nodoActual.abajo.tipo = 'Caminando'
                                nodoActual = nodoActual.derecha.derecha
                        else:
                            casillas_recorridas = 10000
                            nodoFinal.terminal = True
                            break

                elif nodoActual.izquierda != None and nodoActual.izquierda == Entrada :
                    if nodoActual.izquierda.izquierda!= None and (nodoActual.izquierda.izquierda.tipo == 'Camino' or nodoActual.izquierda.izquierda.tipo == 'Entrada' or nodoActual.izquierda.izquierda.tipo == 'Civil'):
                        casillas_recorridas = 1
                        if nodoActual.izquierda.izquierda.tipo == 'Entrada':
                            nodoActual.izquierda.izquierda.tipo = 'CaminandoEntrada'
                            nodoActual = nodoActual.izquierda.izquierda
                        elif nodoActual.izquierda.izquierda.tipo == 'Civil':
                            nodoActual.izquierda.izquierda.tipo = 'CaminandoCivil'
                            nodoActual = nodoActual.izquierda.izquierda
                        else:
                            nodoActual.izquierda.tipo = 'Caminando'
                            nodoActual = nodoActual.izquierda.izquierda
                    else:
                        casillas_recorridas = 10000
                        nodoFinal.terminal = True
                        break
                    
                elif nodoActual.abajo != None and nodoActual.abajo == Entrada :
                    if nodoActual.abajo.abajo != None and (nodoActual.abajo.abajo.tipo == 'Camino' or nodoActual.abajo.abajo.tipo == 'Entrada' or nodoActual.abajo.abajo.tipo == 'Civil'):
                        casillas_recorridas = 1
                        if nodoActual.abajo.abajo.tipo == 'Entrada':
                            nodoActual.abajo.abajo.tipo = 'CaminandoEntrada'
                            nodoActual = nodoActual.abajo.abajo
                        elif nodoActual.abajo.abajo.tipo == 'Civil':
                            nodoActual.abajo.abajo.tipo = 'CaminandoCivil'
                            nodoActual = nodoActual.abajo.abajo
                        else:
                            nodoActual.abajo.tipo = 'Caminando'
                            nodoActual = nodoActual.abajo.abajo
                    else:
                        casillas_recorridas = 10000
                        nodoFinal.terminal = True
                        break

                elif nodoActual.arriba!= None and nodoActual.arriba== Entrada :
                    if nodoActual.arriba.arriba != None and (nodoActual.arriba.arriba.tipo == 'Camino' or nodoActual.arriba.arriba.tipo == 'Entrada' or nodoActual.arriba.arriba.tipo == 'Civil'):
                        casillas_recorridas = 1
                        if nodoActual.arriba.arriba.tipo == 'Entrada':
                            nodoActual.arriba.arriba.tipo = 'CaminandoEntrada'
                            nodoActual = nodoActual.arriba.arriba
                        elif nodoActual.arriba.arriba.tipo == 'Civil':
                            nodoActual.arriba.arriba.tipo = 'CaminandoCivil'
                            nodoActual = nodoActual.arriba.arriba
                        else:
                            nodoActual.arriba.tipo = 'Caminando'
                            nodoActual = nodoActual.arriba.arriba
                    else:
                        casillas_recorridas = 10000
                        nodoFinal.terminal = True
                        break
        nodoFinal.entrada_mas_cercana = None
        nodoFinal.distancia = 9999

ObtenerArchivo()
