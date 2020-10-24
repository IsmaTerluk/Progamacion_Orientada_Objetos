from ClaseNodo import Nodo
class Lista(object):
    __comienzo=None
    __actual=None
    __indice=0
    __tope=0
    def __init__(self):
        self.__comienzo=None
        self.__actual=None
    def __iter__(self):
        return self
    def __next__(self):
        if self.__indice==self.__tope:
            self.__actual=self.__comienzo
            self.__indice=0
            raise StopIteration
        else:
          self.__indice+=1
          dato = self.__actual.getDato()
          self.__actual=self.__actual.getSiguiente()
          return dato
    def listarDatosProfesores(self):
        aux=self.__comienzo
        while aux!=None:
            a=aux.getDato()
            a.mostrarDatos()
            aux=aux.getSiguiente()
    def insertarVehiculoPorCola(self,persona):
        unNodo= Nodo(persona)
        unNodo.setSiguiente(self.__comienzo)
        self.__comienzo=unNodo
        self.__actual=unNodo
        self.__tope+=1   #indica la cantidad de objetos
    def insertarVehiculoAlFinal(self,persona):
        unNodo=Nodo(persona)
        if(self.__comienzo==None):  #si esta vacia hace una carga comun
            unNodo.setSiguiente(self.__comiezo)
            self.__comienzo=unNodo
            self.__actual=unNodo
            self.__tope+=1
        else:
            aux=self.__comienzo #resguardamos la cabeza
            while(aux.getSiguiente()!=None):
                 aux=aux.getSiguiente()
            unNodo.setSiguiente(aux.getSiguiente())  #coloca None en el ultimo Nodo
            aux.setSiguiente(unNodo)  #y el penultimo queda apuntando al ultimo
            self.__actual=unNodo
            self.__tope+=1
    def insertarVehiculoAdentro(self,persona,pos):  #por posicion
        unNodo=Nodo(persona)
        con=1
        if(pos==1): #si desea colocarlo en la primer posicion
            unNodo.setSiguiente(self.__comienzo)
            self.__comienzo=unNodo
            self.__tope+=1
        else:
            aux=self.__comienzo
            while(con<(pos-1)):
                aux=aux.getSiguiente()
                con+=1
            unNodo.setSiguiente(aux.getSiguiente())
            aux.setSiguiente(unNodo)
            self.__tope+=1
    def eliminarPorEdad(self,edad):
        if(self.__comienzo.getEdad()==edad):
            aux=self.__comienzo
            self.__comienzo=self.__comienzo.getSiguiente()
            self.__tope-=1
            del aux
        else:
            aux=self.__comienzo
            while((aux!=None)&(aux.getEdad()!=edad)):
                ant=aux
                aux=aux.getSiguiente()
            ant.setSiguiente(aux.getSiguiente())
            self.__tope-=1
            del aux
    def encontrarObjeto(self,pos):
        if(pos==0):
            print(type(self.__comienzo.getDato()))
        else:
            cont=0
            aux=self.__comienzo
            while(cont<pos):
                aux=aux.getSiguiente()
                cont+=1
            print(type(aux.getDato()))
    def prueba(self):
        print(self.__comienzo.getDato().getEdad())
