from MatrizDispersa import MatrizDispersa
class ListaMatrizDispersa():
    def __init__(self):
        self.primero : MatrizDispersa = None #cabecera
        self.ultimo = None # final
        self.size = 0
    
    def insertLastMatrizDispersa(self, capa,unidadesMilitares,ciudad):
        nuevo_MatrizDispersa = MatrizDispersa(capa,ciudad)
        nuevo_MatrizDispersa.setUnidadesMilitares(unidadesMilitares)
        self.size += 1
        if self.primero is None:
            self.primero = nuevo_MatrizDispersa
            self.ultimo = nuevo_MatrizDispersa
        else:
            
            # Inercion con apuntador "primero"  y "ultimo"
            self.ultimo.setSiguiente(nuevo_MatrizDispersa)
            self.ultimo = nuevo_MatrizDispersa

    def showCiudades(self):
        tmp = self.primero
        txt = ''
        while tmp is not None:
            txt += ('- ' + tmp.getCiudad() + '\n')
            tmp = tmp.getSiguiente()
        return txt

    def search_item(self, ciudad):
        if self.primero is None:
            return
        n = self.primero
        while n is not None:
            if n.getCiudad() == ciudad:
                return n
            n = n.siguiente
        return False
    
    def eliminarCiudad(self, ciudad):
        tmp = self.primero
        while tmp is not None:
            if tmp.ciudad == ciudad:
                self.primero = tmp.siguiente
                tmp.siguiente = None
                print('Estudiante',ciudad, 'eliminado.')
                break
            elif tmp.siguiente is not None:
                if tmp.siguiente.ciudad == ciudad:
                    Nodo_a_borrar = tmp.siguiente
                    tmp.siguiente = Nodo_a_borrar.siguiente
                    Nodo_a_borrar.siguiente = None
                    print('Estudiante', ciudad,'eliminado.')
                    break
            tmp = tmp.siguiente