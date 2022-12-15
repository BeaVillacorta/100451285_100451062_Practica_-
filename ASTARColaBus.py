import sys
import pathlib
import time

  
class Node():
    def __init__(self, nombre=None, parent=None,g=None, h=None, f=None, coste_individual=None, tipo1=None, tipo2=None, asiento= None):
        self.nombre=nombre
        self.parent = parent
        self.g = g
        self.h = h
        self.f = f
        self.coste_individual = coste_individual
        self.tipo1 = tipo1
        self.tipo2 = tipo2
        self.asiento=asiento
    

alumnos=[]
    
input = sys.argv[1]
with open(input,'r') as i:
    Alumnos1 = i.read()
    al_list = Alumnos1[1:-2].split(",")
    Alumnos = []
    size = len(al_list)
    index = 0
    for al in al_list:
        if index == 0:
            separated = al[1:].split(": ")
            new_elem_init = separated[0][:-1]+separated[1]
        else:
            separated = al[1:].split(": ")
            new_elem_init = separated[0][1:-1]+separated[1]
        index += 1
        Alumnos.append((new_elem_init[0],new_elem_init[1],new_elem_init[2],new_elem_init[3:]))
    print(Alumnos)
    


def heuristica(nodo, heur):
        # heurística que se basa en el tiempo que tarda cada alumno
        if heur == 1:
            coste2 = 0
            if nodo.tipo1=="R" and nodo.tipo2 == "C":
                coste2+=5
            elif nodo.tipo1=="R":
                coste2+=3
            elif nodo.tipo2=="C":
                coste2+=2
            else:
                coste2+=1
            return coste2
        
        if heur == 2:
            coste2=0
            if nodo.tipo2=="C":
                coste2+=5
            else:
                coste2+=2
            return coste2
        else:
            print("Error: El nombre de la heuristica debe ser 1 o 2.")
            sys.exit(-1)

def Astar(lista, heur):
    """Da coste total tardan todos los alumnos en montarse al autobús"""
    coste = 0
    for i in lista:
        if i[2] == 'R' and i[1] == 'C':
            coste += 5
        elif i[1] == 'C':
            coste += 2
        elif i[2] == 'R':
            coste += 3
        else:
            coste += 1

    # Creacion de estado inicial PONER QUE h Y f SEAN DE LA HEURISTICA
    coste+=1

    # variable que valdrá false hasta que falten solo dos alumnos por entrar a la close list (autobús) y uno de los dos tenga movilidad reducida, si esto ocurre, valdrá true.
    obligado = False
    # Creacion de la lista Abierta, en la que se encuentran los nodos generados 
    openList = []
    # Creacion de la lista Cerrada, en la que se encuentran los nodos expandidos
    closedList = []
    nombres = []
    obligaciones = []
    # Lista que contiene los asientos ocupados con los alumnos conflitivos (C) que servirá para duplicar el tiempo de los alumnos que se sienten detrás
    asientos_conflictivos = []
    # Contador de nodos que se expanden
    contador_nodos = 0
    # Creacion nodo predecesor
    prev_node = Node("pred", None, 0, None, None, 1, "X", "X", None)
   
    # Creacion de estado inicial PONER QUE h Y f SEAN DE LA HEURISTICA
    # nodo con el que se empieza en la lista abierta
    start = Node("start", prev_node, 0, 0, 0, 1, "X", "X", None)
    contador_nodos+=1
    start.h = heuristica(start, heur)
    # start.h = 0 ???
    start.f = start.h + start.g
    
    start_time = time.process_time()
    openList.append(start)

    # Mientras tengamos nodos que expandir (que la open list tenga algo dentro)
    while len(openList) > 0:
        obligado=False
        # comprueba que si quedan solo dos personas en close list y una R esta no entre la última
        if len(closedList) + 1 == len(lista):
            for i in lista:
                if i[0] not in nombres:
                    obligaciones.append(i)
            for i in obligaciones:
                if i[2] == "R":
                    obligado = True

        nodo_actual = None

        # variable que se mantiene en True si el nodo que se escoge de la openlist está en la closelist
        # encontrado será = false si el nodo solo se encuentra en la openlist y permitirá que se espanda ese nodo.
        encontrado = True
        
        # Mete el nodo con menor f de la open list en la closed list
        while encontrado == True:
            encontrado = False
            if len(openList) > 0:
                # el primero open_list, el que mejor f tiene
                nodo_actual = openList.pop(0)
                #Combrueba que el nodo no esté ya en la closed list.
                for nodo in closedList:
                    # si el nodo se encuentra en la close list
                    if nodo_actual.nombre == nodo.nombre:
                        encontrado = True
                        break
                # comprueba que el padre es el ultimo que ha metido en la cerrada para que podamos expandirlo
                # si el padre de el nodo que queremos expandir es el padre, lo expandimos
                # tb comprueba que el útimo no tenga movilidad reducida (R) y de que alumno de movilidad reducida (R) no esté detrás de otro movilidad reducida (R)
                if prev_node.nombre == nodo_actual.parent.nombre:
                    if encontrado == False and obligado == False:
                        closedList.append(nodo_actual)
                        # Se introduce el nombre del nodo en la lista "nombres"
                        nombres.append(nodo_actual.nombre)
                        # Si el alumno es conflictivo y se encuentra en la closelist añadimos el asiento a la lista de asientos conflictivos
                        if nodo_actual.tipo2 == "C":
                            asientos_conflictivos.append(nodo_actual.asiento)
                            
                    # cuando estamos penúltimo nodo (quedan dos alumnos por meter en el bus)
                    # y nodo actual que se va a expandir no está closeList y se le mete si: 
                    # olbigado = True y uno de los dos tiene mov reducida
                    elif encontrado == False and obligado == True:
                        # hay que tener en cuenta que el último alumno que se sube al bus no puede tener movilidad reducida porque necesita ayuda para subir.
                        # buscamos el nodo de tipo R 
                        # si el que se expande si tiene movilidad redicida le introdue en la lista cerrada
                        if nodo_actual.tipo1 == "R":
                            closedList.append(nodo_actual)
                            nombres.append(nodo_actual.nombre)
                            # si además de tener movilidad reducida es conflictivo, tambíen se añade el asiento a la lista de asientos conflictivos
                            if nodo_actual.tipo2 == "C":
                                asientos_conflictivos.append(nodo_actual.asiento)
                        else:
                            encontrado = True
                else:
                    encontrado = True

            else:
                print('No hay solución')
                sys.exit(0)
        print(obligado)
        print(nodo_actual.nombre)

        contador_nodos +=1
        print("coste: " + str(coste))
        #Ordena la open list de menor a mayor f
        openList = sorted(openList, key=lambda nodo: nodo.f)
        prev_node=nodo_actual
        
          
    # heurística que se basa en que el coste de los alumnos conflictivos es el doble
Astar(Alumnos,1)