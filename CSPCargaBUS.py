#!/usr/bin/env python
#=*=coding:utf=8=*=
import sys
import pathlib
from constraint import *
import time

start_time = time.time()
input = sys.argv[1]

# Abre los fichero de entrada
with open(input,'r') as i:
    students = i.readlines()
problem = Problem()

# Lista 
studentsnames=[]
# Lista
MR=[]

A=[]

# Lista en la que se añadirán los datos del los alumnos del fichero de entrada
students2=[]

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

problem.addVariables(A, range(1,33))
problem.addVariables(MR, [1, 2, 3, 4, 13, 14, 15, 16, 17, 18, 19, 20])

# Con AllDifferentConstraint se comprueba que el valor de una variable es diferente a las de las otras, es decir
# que cada alumno tiene un asiento y es diferente al asiento del resto de alumnos. Asignar 1 asiento a 1 alumno
problem.addConstraint(AllDifferentConstraint())

# Hueco libre movilidad reducida
def movilidadReducida(mr, student):
    """"comprueba que los alumnos con movilidad reducida tienen libre el ariento contiguio
        si está libre devuelve True, en caso contrario, False.
    """
    if mr % 2 == 0 and mr - 1 == student: # si tiene un alumno a la izquierd
        return False
    elif mr % 2 == 1 and mr + 1 == student: # si tiene un alumno a la derecha
        return False
    return True


# Separación de alumnos conflictivos
def alumnoConflictivo(i,j):
        if i%4==0 and i!= j and (j==i-1 or j==i-4 or j==i-5 or j==i+3 or j==i+4):
            return False
        elif i%4==1 and i!= j and (j==i-3 or j==i-4 or j==i+5 or j==i+4 or j==i+1):
            return False
        elif (i%4==2 or i%4==3) and i!= j and (j==i-1 or j==i+1 or j==i-5 or j==i-4 or j==i-3 or j==i+3 or j==i+4 or j==i+5):
            return False
        return True


# Pertenece a ciclo 1
def ciclo1(i,j):
    """Comprueba que los alumnos del ciclo 1 están sentados en los asientos que les corresponden"""
    if i > 16:
        return False
    return True

# Pertenece a ciclo 2
def ciclo2(i,j):
    """Comprueba que los alumnos del ciclo 1 están sentados en los asientos que les corresponden"""
    if i < 17:
        return False
    return True