
class unidadMilitar():
    def __init__(self,x,y,pelea,ciudad):
        self.ciudad = ciudad
        self.pos_x = x
        self.pos_y = y
        self.fuerza = pelea
        self.siguiente = None
    
    def getX(self):
        return self.pos_x

    def getCiudad(self):
        return self.ciudad

    def getY(self):
        return self.pos_y

    def getFuerza(self):
        return self.fuerza

    def setX(self,x):
        self.pos_x = x
    
    def setCiudad(self,ciudad):
        self.ciudad = ciudad

    def setY(self,y):
        self.pos_y = y

    def setFuerza(self,pelea):
        self.fuerza = pelea
    
    def setSiguiente(self,unidadMilitar):
        self.siguiente = unidadMilitar

    def getSiguiente(self):
        return self.siguiente
    
