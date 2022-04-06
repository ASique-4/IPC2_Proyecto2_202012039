from Nodo_Encabezado import Nodo_Encabezado
from Lista_Encabezado import Lista_Encabezado

from listaUnidadMilitar import ListaUnidadMilitar
import os
import webbrowser

# -----------------------------Codigo de MATRIZ DISPERSA ----------------
# -------- Clase NodoOrtogonal, con 4 apuntadores -> Nodos Internos

class Nodo_Interno(): # Nodos ortogonales
    def __init__(self, x, y, caracter):# 'caracter' puede ser cualquier valor
        self.caracter = caracter
        self.coordenadaX = x  # fila
        self.coordenadaY = y  # columna
        self.terminal = False
        self.tipo = None
        self.arriba = None
        self.abajo = None
        self.derecha = None  # self.siguiente
        self.izquierda = None  # self.anterior
        self.entrada_mas_cercana = None
        self.distancia = 9999
    
    def getDistancia(self):
        return self.distancia
    def setDistancia(self,distancia):
        self.distancia = distancia

    def getEntrada(self):
        return self.entrada_mas_cercana
    def setEntrada(self,entrada):
        self.entrada_mas_cercana = entrada
    
    
class MatrizDispersa():
    def __init__(self, capa,ciudad):
        self.capa = capa
        self.ciudad = ciudad
        self.filas = Lista_Encabezado('fila')
        self.columnas = Lista_Encabezado('columna')
        self.unidadesMilitares = ListaUnidadMilitar()
        self.civiles = 0
        self.recursos = 0
        self.siguiente = None

    def getUnidadesMilitares(self):
        return self.unidadesMilitares
    
    def setUnidadesMilitares(self,unidadesMilitares):
        self.unidadesMilitares = unidadesMilitares
    
    def getCiudad(self):
        return self.ciudad
    
    def getCiviles(self):
        return self.civiles

    def getRecursos(self):
        return self.recursos
    
    def setCiviles(self,civiles):
        self.civiles = civiles

    def setRecursos(self,recursos):
        self.recursos = recursos

    def setSiguiente(self,MatrizDispersa):
        self.siguiente = MatrizDispersa

    def getSiguiente(self):
        return self.siguiente
    
    def getNodo(self,fila,columna):
        tmp = self.filas.primero
        while(tmp is not None):
            nodoTmp = tmp.acceso
            while(nodoTmp is not None):
                if(str(nodoTmp.coordenadaX) == str(fila) and str(nodoTmp.coordenadaY) == str(columna)):
                    return nodoTmp
                nodoTmp = nodoTmp.derecha
            tmp = tmp.siguiente
        return None

    def getNodoPorTipo(self,tipo):
            tmp = self.filas.primero
            while(tmp is not None):
                nodoTmp = tmp.acceso
                while(nodoTmp is not None):
                    if(str(nodoTmp.tipo) == str(tipo)):
                        return nodoTmp
                    nodoTmp = nodoTmp.derecha
                tmp = tmp.siguiente
            return None
    def showNodoCivil(self):
        self.setCiviles(0)
        tmp = self.filas.primero
        txt = ''
        while(tmp is not None):
            nodoTmp = tmp.acceso
            while(nodoTmp is not None):
                if(str(nodoTmp.tipo) == 'Civil'):
                    self.setCiviles(int(self.getCiviles()) + 1)
                    txt += '-Fila: ' + str(nodoTmp.coordenadaX) + ' -Columna: ' + str(nodoTmp.coordenadaY) + '\n'
                nodoTmp = nodoTmp.derecha
            tmp = tmp.siguiente
        if int(self.getCiviles()) <= 1:
            return '1' 
        else:
            return txt
    
    def showNodoRecurso(self):
        self.setRecursos(0)
        tmp = self.filas.primero
        txt = ''
        while(tmp is not None):
            nodoTmp = tmp.acceso
            while(nodoTmp is not None):
                if(str(nodoTmp.tipo) == 'Recurso'):
                    self.setRecursos(int(self.getRecursos()) + 1)
                    txt += '-Fila: ' + str(nodoTmp.coordenadaX) + ' -Columna: ' + str(nodoTmp.coordenadaY) + '\n'
                nodoTmp = nodoTmp.derecha
            tmp = tmp.siguiente
        if int(self.getRecursos()) <= 1:
            return '1' 
        else:
            return txt
    
    def showNodoEntrada(self):
        tmp = self.filas.primero
        txt = ''
        while(tmp is not None):
            nodoTmp = tmp.acceso
            while(nodoTmp is not None):
                if(str(nodoTmp.tipo) == 'Entrada'):
                    txt += '-Fila: ' + str(nodoTmp.coordenadaX) + ' -Columna: ' + str(nodoTmp.coordenadaY) + '\n'
                nodoTmp = nodoTmp.derecha
            tmp = tmp.siguiente
        return txt
    
    def limpiarCaminos(self):
        tmp = self.filas.primero
        while(tmp is not None):
            nodoTmp = tmp.acceso
            while(nodoTmp is not None):
                if nodoTmp.tipo == 'Visitado' or nodoTmp.tipo == 'Caminando':
                    nodoTmp.tipo = 'Camino'
                elif nodoTmp.tipo == 'Vencido':
                    nodoTmp.tipo = 'UnidadMilitar'
                elif nodoTmp.tipo == 'CaminandoEntrada' or nodoTmp.tipo == 'VisitadoEntrada':
                    nodoTmp.tipo = 'Entrada'
                elif nodoTmp.tipo == 'CaminandoCivil' or nodoTmp.tipo == 'VisitadoCivil':
                    nodoTmp.tipo = 'Civil'
                nodoTmp = nodoTmp.derecha
            tmp = tmp.siguiente


    # (filas = x, columnas = y)
    def insert(self, pos_x, pos_y, caracter):
        nuevo = Nodo_Interno(pos_x, pos_y, caracter) # se crea nodo interno

        nodo_X = self.filas.getEncabezado(pos_x)
        nodo_Y = self.columnas.getEncabezado(pos_y)

        if nodo_X == None: 
            nodo_X = Nodo_Encabezado(pos_x)
            self.filas.insertar_nodoEncabezado(nodo_X)

        if nodo_Y == None: 
            nodo_Y = Nodo_Encabezado(pos_y)
            self.columnas.insertar_nodoEncabezado(nodo_Y)

        # ----- INSERTAR NUEVO EN FILA
        if nodo_X.acceso == None: 
            nodo_X.acceso = nuevo
        else:
            if nuevo.coordenadaY < nodo_X.acceso.coordenadaY: 
                nuevo.derecha = nodo_X.acceso              
                nodo_X.acceso.izquierda = nuevo
                nodo_X.acceso = nuevo
            else:
                #de no cumplirse debemos movernos de izquierda a derecha buscando donde posicionar el NUEVO nodoInterno
                tmp : Nodo_Interno = nodo_X.acceso     # nodo_X:F1 --->      NI 1,2; NI 1,3; NI 1,5;
                while tmp != None:                      #NI 1,6
                    if nuevo.coordenadaY < tmp.coordenadaY:
                        nuevo.derecha = tmp
                        nuevo.izquierda = tmp.izquierda
                        tmp.izquierda.derecha = nuevo
                        tmp.izquierda = nuevo
                        break;
                    elif nuevo.coordenadaX == tmp.coordenadaX and nuevo.coordenadaY == tmp.coordenadaY: #validamos que no haya repetidas
                        break;
                    else:
                        if tmp.derecha == None:
                            tmp.derecha = nuevo
                            nuevo.izquierda = tmp
                            break;
                        else:
                            tmp = tmp.derecha 
           
        # ----- INSERTAR NUEVO EN COLUMNA
        if nodo_Y.acceso == None:
            nodo_Y.acceso = nuevo
        else: 
            if nuevo.coordenadaX < nodo_Y.acceso.coordenadaX:
                nuevo.abajo = nodo_Y.acceso
                nodo_Y.acceso.arriba = nuevo
                nodo_Y.acceso = nuevo
            else:
                # de no cumplirse, debemos movernos de arriba hacia abajo buscando donde posicionar el NUEVO
                tmp2 : Nodo_Interno = nodo_Y.acceso
                while tmp2 != None:
                    if nuevo.coordenadaX < tmp2.coordenadaX:
                        nuevo.abajo = tmp2
                        nuevo.arriba = tmp2.arriba
                        tmp2.arriba.abajo = nuevo
                        tmp2.arriba = nuevo
                        break;
                    elif nuevo.coordenadaX == tmp2.coordenadaX and nuevo.coordenadaY == tmp2.coordenadaY: #validamos que no haya repetidas
                        break;
                    else:
                        if tmp2.abajo == None:
                            tmp2.abajo = nuevo
                            nuevo.arriba = tmp2
                            break
                        else:
                            tmp2 = tmp2.abajo

    def graficarNeato(self, nombre,matriz):
        contenido = '''digraph G{
    node[shape=box, width=1, height=1, fontname="Arial", fillcolor="white", style=filled]
    edge[style = "invis" arrowhead="none" arrowtail="none"]
    node[label = "0,0" fillcolor="darkolivegreen1" pos = "-1,1!"]raiz;'''
        contenido += '''label = "{}" \nfontname="Arial Black" \nfontsize="25pt" \n
                    \n'''.format(nombre)

        # --graficar nodos ENCABEZADO
        # --graficar nodos fila
        pivote = self.filas.primero
        posx = 0
        while pivote != None:
            contenido += '\n\tnode[label = "{}" fillcolor="azure" pos="-1,-{}!" shape=box]x{};'.format(pivote.id, 
            posx, pivote.id)
            pivote = pivote.siguiente
            posx += 1
        pivote = self.filas.primero
        while pivote.siguiente != None:
            contenido += '\n\tx{}->x{}[color="white"];'.format(pivote.id, pivote.siguiente.id)
            contenido += '\n\tx{}->x{}[dir=back color="white"];'.format(pivote.id, pivote.siguiente.id)
            pivote = pivote.siguiente
        contenido += '\n\traiz->x{}[color="white"];'.format(self.filas.primero.id)

        # --graficar nodos columna
        pivotey = self.columnas.primero
        posy = 0
        while pivotey != None:
            contenido += '\n\tnode[label = "{}" fillcolor="azure" pos = "{},1!" shape=box]y{};'.format(pivotey.id, 
            posy, pivotey.id)
            pivotey = pivotey.siguiente
            posy += 1
        pivotey = self.columnas.primero
        while pivotey.siguiente != None:
            contenido += '\n\ty{}->y{}[color="white"];'.format(pivotey.id, pivotey.siguiente.id)
            contenido += '\n\ty{}->y{}[dir=back color="white"];'.format(pivotey.id, pivotey.siguiente.id)
            pivotey = pivotey.siguiente
        contenido += '\n\traiz->y{}[color="white"];'.format(self.columnas.primero.id)

        #ya con las cabeceras graficadas, lo siguiente es los nodos internos, o nodosCelda
        pivote = self.filas.primero
        posx = 0
        while pivote != None:
            pivote_celda : Nodo_Interno = pivote.acceso
            while pivote_celda != None:
                # --- buscamos posy
                pivotey = self.columnas.primero
                posy_celda = 0
                while pivotey != None:
                    if pivotey.id == pivote_celda.coordenadaY: break
                    posy_celda += 1
                    pivotey = pivotey.siguiente
                if pivote_celda.caracter == '*':
                    pivote_celda.tipo = 'NoPasar'
                    contenido += '\n\tnode[label="" fillcolor="black" pos="{},-{}!" shape=box]i{}_{};'.format( #pos="{},-{}!"
                        posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif pivote_celda.caracter == 'E':
                    pivote_celda.tipo = 'Entrada'
                    contenido += '\n\tnode[label="" fillcolor="green" pos="{},-{}!" shape=box]i{}_{};'.format( #pos="{},-{}!"
                        posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif pivote_celda.caracter == 'C':
                    pivote_celda.tipo = 'Civil'
                    
                    contenido += '\n\tnode[label="" fillcolor="blue" pos="{},-{}!" shape=box]i{}_{};'.format( #pos="{},-{}!"
                        posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif pivote_celda.caracter == 'R':
                    pivote_celda.tipo = 'Recurso'
                    matriz.setRecursos(int(matriz.getRecursos()) + 1)
                    contenido += '\n\tnode[label="" fillcolor="gray" pos="{},-{}!" shape=box]i{}_{};'.format( #pos="{},-{}!"
                        posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif matriz.getUnidadesMilitares().search_item(pivote_celda.coordenadaX,pivote_celda.coordenadaY) != False:
                    pivote_celda.tipo = 'UnidadMilitar'
                    contenido += '\n\tnode[label="" fillcolor="red" pos="{},-{}!" shape=box]i{}_{};'.format( #pos="{},-{}!"
                        posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                else:
                    pivote_celda.tipo = 'Camino'
                    contenido += '\n\tnode[label=" " fillcolor="white" pos="{},-{}!" shape=box]i{}_{};'.format( # pos="{},-{}!"
                        posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    ) 
                pivote_celda = pivote_celda.derecha
            
            pivote_celda = pivote.acceso
            while pivote_celda != None:
                if pivote_celda.derecha != None:
                    contenido += '\n\ti{}_{}->i{}_{}[color="white"];'.format(pivote_celda.coordenadaX, pivote_celda.coordenadaY,
                    pivote_celda.derecha.coordenadaX, pivote_celda.derecha.coordenadaY)
                    contenido += '\n\ti{}_{}->i{}_{}[dir=back color="white"];'.format(pivote_celda.coordenadaX, pivote_celda.coordenadaY,
                    pivote_celda.derecha.coordenadaX, pivote_celda.derecha.coordenadaY)
                pivote_celda = pivote_celda.derecha
        
            contenido += '\n\tx{}->i{}_{}[color="white"];'.format(pivote.id, pivote.acceso.coordenadaX, pivote.acceso.coordenadaY)
            contenido += '\n\tx{}->i{}_{}[dir=back color="white"];'.format(pivote.id, pivote.acceso.coordenadaX, pivote.acceso.coordenadaY)
            pivote = pivote.siguiente
            posx += 1
        
        pivote = self.columnas.primero
        while pivote != None:
            pivote_celda : Nodo_Interno = pivote.acceso
            while pivote_celda != None:
                if pivote_celda.abajo != None:
                    contenido += '\n\ti{}_{}->i{}_{}[color="white"];'.format(pivote_celda.coordenadaX, pivote_celda.coordenadaY,
                    pivote_celda.abajo.coordenadaX, pivote_celda.abajo.coordenadaY)
                    contenido += '\n\ti{}_{}->i{}_{}[dir=back color="white"];'.format(pivote_celda.coordenadaX, pivote_celda.coordenadaY,
                    pivote_celda.abajo.coordenadaX, pivote_celda.abajo.coordenadaY) 
                pivote_celda = pivote_celda.abajo
            contenido += '\n\ty{}->i{}_{}[color="white"];'.format(pivote.id, pivote.acceso.coordenadaX, pivote.acceso.coordenadaY)
            contenido += '\n\ty{}->i{}_{}[dir=back color="white"];'.format(pivote.id, pivote.acceso.coordenadaX, pivote.acceso.coordenadaY)
            pivote = pivote.siguiente
                
        contenido += '\n}'
        #--- se genera DOT y se procede a ecjetuar el comando
        dot = "PDF/matriz_{}_dot.txt".format(nombre)
        with open(dot, 'w') as grafo:
            grafo.write(contenido)
        result = "matriz_{}.pdf".format(nombre)
        os.system("neato -Tpdf " + dot + " -o " + result)


    def graficarNeatoOrdenar(self, nombre,matriz,robot,nodoFinal,fuerzaInicial):
        contenido = '''digraph G{
    node[shape=box, width=1, height=1, fontname="Arial", fillcolor="white", style=filled]
    edge[style = "invis" arrowhead="none" arrowtail="none"]
    node[label = "0,0" fillcolor="azure" pos = "-1,1!"]raiz;'''
        if robot.getTipo() == 'ChapinFighter':
            contenido += '''label = "{}" \nfontname="Arial Black" \nfontsize="25pt" \n
                        \n'''.format('Tipo de misión: Extracción de recursos'  +'\n Recurso extraido: ' + str(nodoFinal.coordenadaX) + ',' + str(nodoFinal.coordenadaY)
                        +'\n Robot utilizado: ' + str(robot.getNombre()) + '(ChapinFighter - Capacidad de combate inicial '+str(fuerzaInicial) +', Capacidad de combate final '+str(robot.getFuerza())+')'
                        )
        elif robot.getTipo() == 'ChapinRescue':
            contenido += '''label = "{}" \nfontname="Arial Black" \nfontsize="25pt" \n
                    \n'''.format('Tipo de misión: Rescate'  +'\n Unidad civil rescatada: ' + str(nodoFinal.coordenadaX) + ',' + str(nodoFinal.coordenadaY)
                    +'\n Robot utilizado: ' + str(robot.getNombre()) + '(ChapinRescue)'
                    )

        # --graficar nodos ENCABEZADO
        # --graficar nodos fila
        pivote = self.filas.primero
        posx = 0
        while pivote != None:
            contenido += '\n\tnode[label = "{}" fillcolor="azure" pos="-1,-{}!" shape=box]x{};'.format(pivote.id, 
            posx, pivote.id)
            pivote = pivote.siguiente
            posx += 1
        pivote = self.filas.primero
        while pivote.siguiente != None:
            contenido += '\n\tx{}->x{}[color="white"];'.format(pivote.id, pivote.siguiente.id)
            contenido += '\n\tx{}->x{}[dir=back color="white"];'.format(pivote.id, pivote.siguiente.id)
            pivote = pivote.siguiente
        contenido += '\n\traiz->x{}[color="white"];'.format(self.filas.primero.id)

        # --graficar nodos columna
        pivotey = self.columnas.primero
        posy = 0
        while pivotey != None:
            contenido += '\n\tnode[label = "{}" fillcolor="azure" pos = "{},1!" shape=box]y{};'.format(pivotey.id, 
            posy, pivotey.id)
            pivotey = pivotey.siguiente
            posy += 1
        pivotey = self.columnas.primero
        while pivotey.siguiente != None:
            contenido += '\n\ty{}->y{}[color="white"];'. format(pivotey.id, pivotey.siguiente.id)
            contenido += '\n\ty{}->y{}[dir=back color="white"];'.format(pivotey.id, pivotey.siguiente.id)
            pivotey = pivotey.siguiente
        contenido += '\n\traiz->y{}[color="white"];'.format(self.columnas.primero.id)

        #ya con las cabeceras graficadas, lo siguiente es los nodos internos, o nodosCelda
        pivote = self.filas.primero
        posx = 0
        while pivote != None:
            pivote_celda : Nodo_Interno = pivote.acceso
            while pivote_celda != None:
                # --- buscamos posy
                pivotey = self.columnas.primero
                posy_celda = 0
                while pivotey != None:
                    if pivotey.id == pivote_celda.coordenadaY: break
                    posy_celda += 1
                    pivotey = pivotey.siguiente
                if pivote_celda.tipo == 'NoPasar':
                    contenido += '\n\tnode[label="" fillcolor="black" pos="{},-{}!" shape=box]i{}_{};'.format( #pos="{},-{}!"
                        posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif pivote_celda.tipo == 'Civil' or pivote_celda.tipo == 'VisitadoCivil':
                    contenido += '\n\tnode[label="" fillcolor="blue" pos="{},-{}!" shape=box]i{}_{};'.format( #pos="{},-{}!"
                        posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif pivote_celda.tipo == 'CaminandoCivil':
                    contenido += '\n\tnode[label="" fillcolor="blue4" pos="{},-{}!" shape=box]i{}_{};'.format( #pos="{},-{}!"
                        posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif pivote_celda.tipo == 'Entrada' or pivote_celda.tipo == 'VisitadoEntrada':
                    contenido += '\n\tnode[label="" fillcolor="green" pos="{},-{}!" shape=box]i{}_{};'.format( #pos="{},-{}!"
                        posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif  pivote_celda.tipo == 'CaminandoEntrada':
                    contenido += '\n\tnode[label="" fillcolor="greenyellow" pos="{},-{}!" shape=box]i{}_{};'.format( #pos="{},-{}!"
                        posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif pivote_celda.tipo == 'Caminando':
                    contenido += '\n\tnode[label="" fillcolor="purple" pos="{},-{}!" shape=box]i{}_{};'.format( #pos="{},-{}!"
                        posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif pivote_celda.tipo == 'Recurso':
                    contenido += '\n\tnode[label="" fillcolor="gray" pos="{},-{}!" shape=box]i{}_{};'.format( #pos="{},-{}!"
                        posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif pivote_celda.tipo == 'Vencido':
                    contenido += '\n\tnode[label="" fillcolor="yellow" pos="{},-{}!" shape=box]i{}_{};'.format( #pos="{},-{}!"
                        posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif matriz.getUnidadesMilitares().search_item(pivote_celda.coordenadaX,pivote_celda.coordenadaY) != False:
                    contenido += '\n\tnode[label="" fillcolor="red" pos="{},-{}!" shape=box]i{}_{};'.format( #pos="{},-{}!"
                        posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                elif pivote_celda.tipo == 'Camino' or pivote_celda.tipo == 'Visitado':
                    pivote_celda.tipo = 'Camino'
                    contenido += '\n\tnode[label="" fillcolor="white" pos="{},-{}!" shape=box]i{}_{};'.format( #pos="{},-{}!"
                    posy_celda, posx, pivote_celda.coordenadaX, pivote_celda.coordenadaY
                    )
                
                pivote_celda = pivote_celda.derecha
            
            pivote_celda = pivote.acceso
            while pivote_celda != None:
                if pivote_celda.derecha != None:
                    contenido += '\n\ti{}_{}->i{}_{}[color="white"];'.format(pivote_celda.coordenadaX, pivote_celda.coordenadaY,
                    pivote_celda.derecha.coordenadaX, pivote_celda.derecha.coordenadaY)
                    contenido += '\n\ti{}_{}->i{}_{}[dir=back color="white"];'.format(pivote_celda.coordenadaX, pivote_celda.coordenadaY,
                    pivote_celda.derecha.coordenadaX, pivote_celda.derecha.coordenadaY)
                pivote_celda = pivote_celda.derecha
        
            contenido += '\n\tx{}->i{}_{}[color="white"];'.format(pivote.id, pivote.acceso.coordenadaX, pivote.acceso.coordenadaY)
            contenido += '\n\tx{}->i{}_{}[dir=back color="white"];'.format(pivote.id, pivote.acceso.coordenadaX, pivote.acceso.coordenadaY)
            pivote = pivote.siguiente
            posx += 1
        
        pivote = self.columnas.primero
        while pivote != None:
            pivote_celda : Nodo_Interno = pivote.acceso
            while pivote_celda != None:
                if pivote_celda.abajo != None:
                    contenido += '\n\ti{}_{}->i{}_{}[color="white"];'.format(pivote_celda.coordenadaX, pivote_celda.coordenadaY,
                    pivote_celda.abajo.coordenadaX, pivote_celda.abajo.coordenadaY)
                    contenido += '\n\ti{}_{}->i{}_{}[dir=back color="white"];'.format(pivote_celda.coordenadaX, pivote_celda.coordenadaY,
                    pivote_celda.abajo.coordenadaX, pivote_celda.abajo.coordenadaY) 
                pivote_celda = pivote_celda.abajo
            contenido += '\n\ty{}->i{}_{}[color="white"];'.format(pivote.id, pivote.acceso.coordenadaX, pivote.acceso.coordenadaY)
            contenido += '\n\ty{}->i{}_{}[dir=back color="white"];'.format(pivote.id, pivote.acceso.coordenadaX, pivote.acceso.coordenadaY)
            pivote = pivote.siguiente
                
        contenido += '\n}'
        #--- se genera DOT y se procede a ecjetuar el comando
        dot = "PDF/matriz_{}_dot.txt".format(nombre)
        with open(dot, 'w') as grafo:
            grafo.write(contenido)
        result = "matriz_{}.pdf".format(nombre)
        os.system("neato -Tpdf " + dot + " -o " + result)

