# !/usr/bin/env python
# =*=coding:utf=8=*=
import sys
import pathlib
from constraint import *
import time

start_time = time.time()
input = sys.argv[1]

# Abre los fichero de entrada
with open(input, 'r') as i:
    students = i.readlines()
problem = Problem()

# Lista
studentsnames = []

# Lista
MR = []

A = []

# Lista en la que se añadirán los datos del los alumnos del fichero de entrada
students2 = []

# Añade en students2 los alumnos del fichero de entrada
for i in students:
    students2.append(list(i.rstrip('\n').split(",")))

# Recorre los datos de cada alumo, si tienen movilidad reducida los añade en MR


for i in students2:
    # para saber si un alumno tiene movilidad reducida debemos ir a la posición 3
    # donde nos encontramos una R si la tiene y una X en caso contrario
    if i[3] == 'R':
        MR.append(i[0])
    else:
        A.append(i[0])

# En este problema tenemos tantas variables como alumnos contenga el fichero de entrada
# El dominio son los asientos que el autobús tiene disponible para los alumnos
# pero no todas las variables tienen el mismo dominio ya que los alumnos con movilidad
# reducida solo se pueden sentar en los asientos establecidos [1, 2, 3, 4, 13, 14, 15, 16, 17, 18, 19, 20]

problem.addVariables(A, range(1, 33))
problem.addVariables(MR, [1, 2, 3, 4, 13, 14, 15, 16, 17, 18, 19, 20])

# Con AllDifferentConstraint se comprueba que el valor de una variable es diferente a las de las otras, es decir
# que cada alumno tiene un asiento y es diferente al asiento del resto de alumnos. Asignar 1 asiento a 1 alumno
problem.addConstraint(AllDifferentConstraint())


# Hueco libre movilidad reducida
def movilidadReducida(mr, student):
    """"comprueba que los alumnos con movilidad reducida tienen libre el ariento contiguio
        si está libre devuelve True, en caso contrario, False.
    """
    if mr % 2 == 0 and mr - 1 == student:  # si tiene un alumno a la izquierd
        return False
    elif mr % 2 == 1 and mr + 1 == student:  # si tiene un alumno a la derecha
        return False
    return True


# Separación de alumnos conflictivos
def alumnoConflictivo(i, j):
    if i % 4 == 0 and i != j and (j == i - 1 or j == i - 4 or j == i - 5 or j == i + 3 or j == i + 4):
        return False
    elif i % 4 == 1 and i != j and (j == i - 3 or j == i - 4 or j == i + 5 or j == i + 4 or j == i + 1):
        return False
    elif (i % 4 == 2 or i % 4 == 3) and i != j and (
            j == i - 1 or j == i + 1 or j == i - 5 or j == i - 4 or j == i - 3 or j == i + 3 or j == i + 4 or j == i + 5):
        return False
    return True


# Pertenece a ciclo 1
def ciclo1(i, j):
    """Comprueba que los alumnos del ciclo 1 están sentados en los asientos que les corresponden"""
    if i >= 17:
        return False
    else:
        return True


# Pertenece a ciclo 2
def ciclo2(i, j):
    """Comprueba que los alumnos del ciclo 1 están sentados en los asientos que les corresponden"""
    if i < 17:
        return False
    else:
        return True


# Pertenecen al mismo ciclo
def mismociclo(i, j):
    if (i < 17 and j < 17) or (i >= 17 and j >= 17):
        return True
    return False


# Colocación hermanos
def colocacionHermanos(i, j):
    if (i % 2 == 0 and i - 1 == j) or (j % 2 == 0 and j - 1 == i):
        return True
    return False


# Colocación hermanos ciclo 1 mayor en pasillo
def colocacionHermanosC1(i, j):
    """"comprueba que el hemano mayor está sentado en el pasillo"""
    if i % 4 == 2 and i - 1 == j and i < 17:
        return True
    elif i % 4 == 3 and i + 1 == j and i < 17:
        return True
    return False


# Main loop
# A continuacion se anyaden las restricciones del problema mediante la funcion addConstraint proporcionada por la libreria
for i in students2:
    # Hueco libre movilidad reducida
    if i[3] == "R":
        for j in students2:
            problem.addConstraint(movilidadReducida, (i[0], j[0]))
    # Es conflictivo
    if i[2] == "C":
        for j in students2:
            # Si no es hermano de j se añaden restricciones
            if j[0] != i[4]:
                # Si j es conflictivo
                if j[2] == "C":
                    problem.addConstraint(alumnoConflictivo, (i[0], j[0]))
                # Si j tiene movilidad reducida
                elif j[3] == "R":
                    problem.addConstraint(alumnoConflictivo, (i[0], j[0]))
    # Tiene hemano
    if i[4] != "0":
        j = students2[int(i[4]) - 1]
        # Si el o el hermano tienen movilidad reducida van en el mismo ciclo
        if i[3] == "R" or j[3] == "R":
            problem.addConstraint(mismociclo, (i[0], j[0]))
        else:
            # Si son del mismo ciclo
            if i[1] == j[1]:
                problem.addConstraint(colocacionHermanos, (i[0], j[0]))
            # Si no son del mismo ciclo
            elif i[1] > j[1]:
                problem.addConstraint(colocacionHermanosC1, (i[0], j[0]))
            else:
                problem.addConstraint(colocacionHermanosC1, (j[0], i[0]))
    else:
        # Pertenece al ciclo 1
        if int(i[1]) == 1:
            problem.addConstraint(ciclo1, (i[0], i[0]))
        # Pertenece al ciclo 2
        else:
            problem.addConstraint(ciclo2, (i[0], i[0]))

print(problem.getSolution())
# print(problem.getSolutions())
print(time.time() - start_time)
solutions = problem.getSolutions()
contador = 0
solutions2 = len(solutions)
# print(solutions2)
solution = problem.getSolution()
current_path = pathlib.Path().absolute()
output_name = input[:-4] + ".output"

for i in students2:
    add = i[2] + i[3]
    i[0] += add

lista = list(solution.keys())
# print(students2)


keys = list(solution)
# print(keys)
# numero de soluciones
a = []
for j in students2:
    elem = j[0]
    a.append(elem)
# print(keys)
# print(a)

# Las claves con sus valores ordenados
contador = 0
for i in keys:
    elem = int(keys[contador])
    e = elem - 1
    meter = a[e]
    keys[contador] = meter
    contador += 1
# print(keys)

# sustituir las claves
keys2 = list(solution)
x = 0
for k in keys2:
    keys2[x] = keys[x]

    x += 1
y = 0
for i in list(solution):
    solution[keys2[y]] = solution.pop(i)

    y += 1
print(solution)
buena = solution

for elem in solutions:
    # sustituir las claves
    keys3 = list(elem)
    x = 0
    for k in keys3:
        keys3[x] = keys[x]

        x += 1
    y = 0
    for i in list(elem):
        elem[keys2[y]] = elem.pop(i)

        y += 1
# print(solutions)


with open(output_name, "w") as file:
    file.write('Numero de soluciones:')
    file.write(str(solutions2))
    file.write('\n')
    # file.write(str(buena))
    file.write('\n')
    file.write(str(solutions))
    file.close()