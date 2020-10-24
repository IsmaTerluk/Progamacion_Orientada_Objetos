class Nodo(object):
    __persona=None
    __siguiente=None
    def __init__(self,persona):
        self.__persona=persona
        self.__siguiente=None
    def setSiguiente(self,siguiente):
        self.__siguiente=siguiente
    def getSiguiente(self):
        return self.__siguiente
    def getDato(self):
        return self.__persona
    def getEdad(self):
        return self.__persona.getEdad()
