#!/usr/bin/env python
#=*=coding:utf=8=*=
import sys
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
print(problem.getSolution())