
class Robot():
    def __init__(self,nombre,pelea,tipo):
        self.tipo = tipo
        self.nombre = nombre
        self.fuerza = pelea
        self.siguiente = None
    
    def getNombre(self):
        return self.nombre

    def getTipo(self):
        return self.tipo

    def getFuerza(self):
        return self.fuerza

    def setNombre(self,nombre):
        self.nombre = nombre
    
    def setTipo(self,tipo):
        self.tipo = tipo

    def setFuerza(self,pelea):
        self.fuerza = pelea
    
    def setSiguiente(self,Robot):
        self.siguiente = Robot

    def getSiguiente(self):
        return self.siguiente
    
