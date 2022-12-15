import sys
import pathlib
import time


class Node():
    def __init__(self, nombre=None, parent=None, g=None, h=None, f=None, coste_individual=None, tipo1=None, tipo2=None,
                 asiento=None):
        self.nombre = nombre
        self.parent = parent
        self.g = g
        self.h = h
        self.f = f
        self.coste_individual = coste_individual
        self.tipo1 = tipo1
        self.tipo2 = tipo2
        self.asiento = asiento


alumnos = []

input = sys.argv[1]
with open(input, 'r') as i:
    Alumnos1 = i.read()
    al_list = Alumnos1[1:-2].split(",")
    Alumnos = []
    size = len(al_list)
    index = 0
    for al in al_list:
        if index == 0:
            separated = al[1:].split(": ")
            new_elem_init = separated[0][:-1] + separated[1]
        else:
            separated = al[1:].split(": ")
            new_elem_init = separated[0][1:-1] + separated[1]
        index += 1
        Alumnos.append((new_elem_init[0], new_elem_init[1], new_elem_init[2], new_elem_init[3:]))
    print(Alumnos)


def heuristica(nodo, heur):
    # heurística que se basa en el tiempo que tarda cada alumno
    if heur == 1:
        coste2 = 0
        if nodo.tipo1 == "R" and nodo.tipo2 == "C":
            coste2 += 5
        elif nodo.tipo1 == "R":
            coste2 += 3
        elif nodo.tipo2 == "C":
            coste2 += 2
        else:
            coste2 += 1
        return coste2

    if heur == 2:
        coste2 = 0
        if nodo.tipo2 == "C":
            coste2 += 5
        else:
            coste2 += 2
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
    coste += 1

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
    start.h = heuristica(start, heur)
    # start.h = 0 ???
    start.f = start.h + start.g

    start_time = time.process_time()
    openList.append(start)

    # Mientras tengamos nodos que expandir (que la open list tenga algo dentro)
    while len(openList) > 0:
        obligado = False
        # comprueba que si quedan solo dos personas en close list y una R esta no entre la última
        if len(closedList) + 1 == len(lista):
            for i in lista:
                if i[0] not in nombres:
                    obligaciones.append(i)
            for i in obligaciones:
                if i[2] == "R":
                    obligado = True

        if len(closedList) == len(lista) + 1:
            print("Solucion encontrada.")
            print(nombres)
            print(obligaciones)
            # eliminamos nodo start
            nombres = nombres[1:]
            print(nombres)

            fichero_salida = open("hola" + ".stat", "w")
            estadistica = "Tiempo Total: " + str(
                "{:.1f}".format(time.process_time() - start_time)) + "\nCoste Total: " + str(
                nodo_actual.f) + "\nLongitud del plan: " + str(nodo_actual.g) + "\n" + "Nodos expandidos: " + str(
                contador_nodos)
            fichero_salida.write(estadistica)
            fichero_salida.close()

            fichero_solucion = open("solucion" + ".output", "w")
            datos_entrada = open(input, 'r')
            escribir_mensaje = "INICIAL:" + str(datos_entrada.read()) + "\nFINAL:"
            fichero_solucion.write(escribir_mensaje)
            fichero_solucion.close()

            sys.exit(0)

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
                # Combrueba que el nodo no esté ya en la closed list.
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


        print("coste: " + str(coste))

        # Si el nodo padre tiene movilidad reducida y es o no es conflictivo
        if nodo_actual.tipo1 == 'R':
            # lista los alumnos del input
            for i in lista:
                # el que vamos a meter en la open List
                if i[2] == 'X' and i[1] == 'X':
                    # crea un nodo
                    # nombre del alumno de la lista i[0]
                    # padre es el nodo actual
                    # .g el coste es el coste del padre
                    # coste heurística
                    nodo_nuevo = Node(i[0], nodo_actual, nodo_actual.g, None, None, None, "X", "X", i[3])
                    # cuando se mete un nodo en lista abierta el coste de la heurística se reduce
                    # coste2 = coste - 1
                    # coste depende de si tiene R, C
                    # coste2, el coste solo cambia cuando lo metemos en la closeList

                    # calcula la heurística
                    nodo_nuevo.h = heuristica(nodo_nuevo, heur)
                    nodo_nuevo.h = coste - nodo_nuevo.h

                    # coste individual
                    # tiempo que tarda nodo hijo = tiempo nodo padre
                    nodo_nuevo.coste_individual = nodo_actual.coste_individual

                    # f = coste + heurística
                    nodo_nuevo.f = nodo_nuevo.g + nodo_nuevo.h
                    openList.append(nodo_nuevo)
                    # la g no cambia pq suben dos a la dos a la vez.
                    contador_nodos += 1

                elif i[2] == 'X' and i[1] == 'C':
                    nodo_nuevo = Node(i[0], nodo_actual, nodo_actual.g, None, None, None, "X", "C", i[3])
                    # coste2 = coste - 2
                    nodo_nuevo.h = heuristica(nodo_nuevo, heur)
                    nodo_nuevo.h = coste - nodo_nuevo.h

                    # lo que tarda el colfictivo en subir
                    nodo_nuevo.coste_individual = 2 * nodo_actual.coste_individual
                    nodo_nuevo.g += nodo_actual.coste_individual
                    nodo_nuevo.f = nodo_nuevo.g + nodo_nuevo.h
                    openList.append(nodo_nuevo)
                    contador_nodos += 1

        # Si el nodo padre es conflictivo
        elif nodo_actual.tipo2 == 'C':
            for i in lista:
                if i[2] == 'R' and i[1] == 'X':
                    nodo_nuevo = Node(i[0], nodo_actual, nodo_actual.g, None, None, None, "R", "X", i[3])
                    # coste2 = coste - 3
                    nodo_nuevo.h = heuristica(nodo_nuevo, heur)
                    nodo_nuevo.h = coste - nodo_nuevo.h
                    nodo_nuevo.h = nodo_nuevo.h
                    contador = 0
                    # crea contador y cuenta cuantas personas que han subido al bus están sentadas delante de el
                    # si hay 3 en el bus y se sientan delante el contador =3
                    # si solo 3 y uno detrás contador = 2
                    # cuentaa cuantos alumnos de los que están detrás del alumno conlfictivo C en la fila se sientan detrás de C en el bus
                    # si se sientan detrás de C en el bus su tiempo se duplica y si se sientan delante no les influye nada.
                    for asiento in asientos_conflictivos:
                        if asiento < i[3]:
                            contador += 1

                    # coste individual 6 pq delante conflictivo
                    # 2  duplica el tiempo de los alimos conflictivos antes de la cola
                    nodo_nuevo.coste_individual = 6 * (2 ** contador)
                    # se suma g
                    nodo_nuevo.g += nodo_nuevo.coste_individual
                    # se añade
                    nodo_nuevo.f = nodo_nuevo.g + nodo_nuevo.h
                    openList.append(nodo_nuevo)
                    contador_nodos += 1
                # un conlfictivo detrás de otro conflictivo
                elif i[2] == 'X' and i[1] == 'C':
                    nodo_nuevo = Node(i[0], nodo_actual, nodo_actual.g, None, None, None, "X", "C", i[3])
                    # se resta 2 al coste porque es conflictivo
                    # coste2 = coste - 2
                    nodo_nuevo.h = heuristica(nodo_nuevo, heur)
                    nodo_nuevo.h = coste - nodo_nuevo.h
                    contador = 0
                    for asiento in asientos_conflictivos:
                        if asiento < i[3]:
                            contador += 1
                    # tarda 2 pq el anterior era conflictivo y duplica su tiempo
                    nodo_nuevo.coste_individual = 2 * (2 ** contador)
                    nodo_nuevo.g += nodo_nuevo.coste_individual + nodo_actual.coste_individual
                    nodo_nuevo.f = nodo_nuevo.g + nodo_nuevo.h
                    openList.append(nodo_nuevo)
                    contador_nodos += 1
                # movilidad reducida y conflictivo
                elif i[2] == 'R' and i[1] == 'C':
                    nodo_nuevo = Node(i[0], nodo_actual, nodo_actual.g, None, None, None, "R", "C", i[3])
                    # coste2 = coste - 5
                    nodo_nuevo.h = heuristica(nodo_nuevo, heur)
                    nodo_nuevo.h = coste - nodo_nuevo.h
                    contador = 0
                    for asiento in asientos_conflictivos:
                        if asiento < i[3]:
                            contador += 1
                    nodo_nuevo.coste_individual = 6 * (2 ** contador)
                    nodo_nuevo.g += nodo_nuevo.coste_individual + nodo_actual.coste_individual
                    nodo_nuevo.f = nodo_nuevo.g + nodo_nuevo.h
                    openList.append(nodo_nuevo)
                    contador_nodos += 1
                else:
                    nodo_nuevo = Node(i[0], nodo_actual, nodo_actual.g, None, None, None, "X", "X", i[3])
                    # coste2 = coste- 1
                    nodo_nuevo.h = heuristica(nodo_nuevo, heur)
                    nodo_nuevo.h = coste - nodo_nuevo.h
                    contador = 0
                    for asiento in asientos_conflictivos:
                        if asiento < i[3]:
                            contador += 1
                    nodo_nuevo.coste_individual = 2 * (2 ** contador)
                    nodo_nuevo.g += nodo_nuevo.coste_individual
                    nodo_nuevo.f = nodo_nuevo.g + nodo_nuevo.h
                    openList.append(nodo_nuevo)
                    contador_nodos += 1

        # Si el nodo padre es un alumno normal 'XX'
        else:
            for i in lista:
                # siguiente tiene movilidad reducida y no es conflictivo
                if i[2] == 'R' and i[1] == 'X':
                    nodo_nuevo = Node(i[0], nodo_actual, nodo_actual.g, None, None, None, "R", "X", i[3])
                    # coste2=coste - 3
                    nodo_nuevo.h = heuristica(nodo_nuevo, heur)
                    nodo_nuevo.h = coste - nodo_nuevo.h
                    contador = 0
                    for asiento in asientos_conflictivos:
                        if asiento < i[3]:
                            contador += 1
                    # para la gente conflictiva delante te duplica el tiempo
                    nodo_nuevo.coste_individual = 3 * (2 ** contador)
                    nodo_nuevo.g += nodo_nuevo.coste_individual
                    nodo_nuevo.f = nodo_nuevo.g + nodo_nuevo.h
                    openList.append(nodo_nuevo)
                    contador_nodos += 1
                # siguiente no tiene movilidad reducida y es conflictivo
                elif i[2] == 'X' and i[1] == 'C':
                    nodo_nuevo = Node(i[0], nodo_actual, nodo_actual.g, None, None, None, "X", "C", i[3])
                    # coste2 =coste - 2
                    nodo_nuevo.h = heuristica(nodo_nuevo, heur)
                    nodo_nuevo.h = coste - nodo_nuevo.h
                    contador = 0
                    for asiento in asientos_conflictivos:
                        if asiento < i[3]:
                            contador += 1
                    nodo_nuevo.coste_individual = 1 * (2 ** contador)
                    nodo_nuevo.g += nodo_nuevo.coste_individual + nodo_actual.coste_individual
                    nodo_nuevo.f = nodo_nuevo.g + nodo_nuevo.h
                    openList.append(nodo_nuevo)
                    contador_nodos += 1

                # siguiente tiene movilidad reducida y es conflictivo
                elif i[2] == 'R' and i[1] == 'C':
                    nodo_nuevo = Node(i[0], nodo_actual, nodo_actual.g, None, None, None, "R", "C", i[3])
                    # coste2 =coste - 5
                    nodo_nuevo.h = heuristica(nodo_nuevo, heur)
                    nodo_nuevo.h = coste - nodo_nuevo.h

                    contador = 0
                    for asiento in asientos_conflictivos:
                        if asiento < i[3]:
                            contador += 1
                    nodo_nuevo.coste_individual = 3 * (2 ** contador)
                    nodo_nuevo.g += nodo_nuevo.coste_individual + nodo_actual.coste_individual
                    nodo_nuevo.f = nodo_nuevo.g + nodo_nuevo.h
                    openList.append(nodo_nuevo)
                    contador_nodos += 1
                else:
                    nodo_nuevo = Node(i[0], nodo_actual, nodo_actual.g, None, None, None, "X", "X", i[3])
                    # coste2=coste - 1
                    nodo_nuevo.h = heuristica(nodo_nuevo, heur)
                    nodo_nuevo.h = coste - nodo_nuevo.h
                    contador = 0
                    for asiento in asientos_conflictivos:
                        if asiento < i[3]:
                            contador += 1
                    nodo_nuevo.coste_individual = 1 * (2 ** contador)
                    nodo_nuevo.g += nodo_nuevo.coste_individual
                    nodo_nuevo.f = nodo_nuevo.g + nodo_nuevo.h
                    openList.append(nodo_nuevo)
                    contador_nodos += 1
        # Ordena la open list de menor a mayor f
        openList = sorted(openList, key=lambda nodo: nodo.f)
        prev_node = nodo_actual

    # heurística que se basa en que el coste de los alumnos conflictivos es el doble


Astar(Alumnos, 1)