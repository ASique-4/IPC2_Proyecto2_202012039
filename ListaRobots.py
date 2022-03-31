from Robot import Robot
class ListaRobot():
    def __init__(self):
        self.primero : Robot = None #cabecera
        self.ultimo = None # final
        self.size = 0
    
    def insertLastRobot(self, nombre,pelea,tipo):
        nuevo_Robot = Robot(nombre,pelea,tipo)
        self.size += 1
        if self.primero is None:
            self.primero = nuevo_Robot
            self.ultimo = nuevo_Robot
        else:
            
            # Inercion con apuntador "primero"  y "ultimo"
            self.ultimo.setSiguiente(nuevo_Robot)
            self.ultimo = nuevo_Robot
        
    def showRobotsRescue(self):
        tmp = self.primero
        txt = ''
        while tmp is not None:
            if tmp.getTipo() == 'ChapinRescue':
                txt += ('- Nombre: ' + tmp.getNombre() +'\n')
            tmp = tmp.getSiguiente()
        return txt

    def showRobotsFighter(self):
        tmp = self.primero
        txt = ''
        while tmp is not None:
            if tmp.getTipo() == 'ChapinFighter':
                txt += ('- Nombre: ' + tmp.getNombre() +'- Capacidad: ' + str(tmp.getFuerza()) +'\n')
            tmp = tmp.getSiguiente()
        return txt

    def search_item(self, nombre,tipo):
        if self.primero is None:
            return
        n = self.primero
        while n is not None:
            if n.getNombre() == nombre and n.getTipo() == tipo:
                return n
            n = n.siguiente
        return False