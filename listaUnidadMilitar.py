from unidadMilitar import unidadMilitar
class ListaUnidadMilitar():
    def __init__(self):
        self.primero : unidadMilitar = None #cabecera
        self.ultimo = None # final
        self.size = 0
    
    def insertLastunidadMilitar(self, x,y,pelea,ciudad):
        nuevo_unidadMilitar = unidadMilitar(x,y,pelea,ciudad)
        self.size += 1
        if self.primero is None:
            self.primero = nuevo_unidadMilitar
            self.ultimo = nuevo_unidadMilitar
        else:
            
            # Inercion con apuntador "primero"  y "ultimo"
            self.ultimo.setSiguiente(nuevo_unidadMilitar)
            self.ultimo = nuevo_unidadMilitar

    def showUnidadesMilitares(self):
        tmp = self.primero
        print ("------------------------------------------------------")
        while tmp is not None:
            print('- X: ', tmp.getX(), '- Y: ', tmp.getY(), '- Fuerza: ',tmp.getFuerza())
            
            tmp = tmp.getSiguiente()
        print ("------------------------------------------------------")

    def search_item(self, x, y):
        if self.primero is None:
            return
        n = self.primero
        while n is not None:
            if n.pos_x == str(x) and n.pos_y == str(y):
                return n
            n = n.siguiente
        return False