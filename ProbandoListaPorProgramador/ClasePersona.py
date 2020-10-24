class Persona:
    __nombre=''
    __edad=0
    def __init__(self,n,e):
        self.__nombre=n
        self.__edad=int(e)
    def getEdad(self):
        return self.__edad
    def mostrarDatos(self):
        print ("NOMBRE {}   EDAD{}   ".format(self.__nombre,self.__edad))
