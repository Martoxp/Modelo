#Modelo grupo 35

import csv
import pandas as pd

#Parametros
with open("capacidad_por_saco.csv", 'r') as capacidad_csv:
    reader = csv.reader(capacidad_csv)
    data_capacidad = list(reader)
alfa_j = {j : float(data_capacidad[j - 1][0]) for j in range(1, len(data_capacidad) + 1)}


with open("costo_saco.csv", 'r') as costo_csv:
    reader = csv.reader(costo_csv)
    data_costo = list(reader)
c_jt = {j: {t: float(data_costo[j - 1][t - 1]) for t in range(1, len(data_costo[j -  1]) + 1)} for j in range(1, len(data_costo) + 1)}

with open("tiempo_demora.csv", 'r') as tiempo_csv:
    reader = csv.reader(tiempo_csv)
    data_tiempo = list(reader)
theta_j = {j: int(data_tiempo[j - 1][0]) for j in range(1, len(data_tiempo) + 1)}


with open("kilos_fruta.csv", 'r') as fruta_csv:
    reader = csv.reader(fruta_csv)
    data_fruta = list(reader)
lambda_j = {j: float(data_fruta[j - 1][0]) for j in range(1, len(data_fruta) + 1)}


with open("precio_venta.csv", 'r') as precio_csv:
    reader = csv.reader(precio_csv)
    data_precio = list(reader)
beta_jt = {j: {t: float(data_precio[j - 1][t - 1]) for t in range(1, len(data_precio[j - 1]) + 1)} for j in range(1, len(data_precio) + 1)}


with open("capital_inicial.csv", 'r') as capital_csv:
    reader = csv.reader(capital_csv)
    gammma_ = int(list(reader)[0][0])

with open("cantidad_cuadrantes.csv", 'r') as cuadrantes_csv:
    reader = csv.reader(cuadrantes_csv)
    K = int(list(reader)[0][0])


#Conjuntos
regiones = [j for j in range(1, len(alfa_j) + 1)] #Tipos de semillas
electrolineras = [t for t in range(1, len(c_jt[1]) + 1)] #Meses del problema 
dias = [k for k in range(1, K + 1)] #Cuadrantes del sector


#Generación del modelo de optimización:

from gurobipy import GRB, Model, quicksum

modelo = Model("Tarea 2")

#Variables

x = modelo.addVars(Semillas, Cuadrantes, Meses, vtype = GRB.BINARY, name = "X" )
y = modelo.addVars(Semillas, Cuadrantes, Meses, vtype = GRB.BINARY, name = "Y" )
i = modelo.addVars(Meses, vtype = GRB.INTEGER, name = "I" )
u = modelo.addVars(Semillas, Meses, vtype = GRB.INTEGER, name = "U" )
w = modelo.addVars(Semillas, Meses, vtype = GRB.INTEGER, name = "W" )

#Función Objetivo
modelo.setObjective(i[Meses[-1]], GRB.MAXIMIZE)
modelo.update()


#Restrcciones

#Activación sembrado
modelo.addConstrs((quicksum(y[j,k,l] for l in range(t, min(t + theta_j[j] - 1, Meses[-1]) + 1)) >= theta_j[j]*x[j,k,t] 
                   for j in Semillas 
                   for k in Cuadrantes
                   for t in Meses), name = f"Activación sembrado")

#Solo 1 sembrado por cuadrante
modelo.addConstrs((quicksum(y[j,k,t] for j in Semillas) <= 1 
                   for k in Cuadrantes 
                   for t in Meses), 
                   name = f"Solo 1 sembrado por cuadrante")

#Inventario de dinero
modelo.addConstrs((i[t-1] - quicksum(c_jt[j][t]*w[j,t] for j in Semillas) + 
                   quicksum(quicksum(x[j,k,t - theta_j[j]] * lambda_j[j] * beta_jt[j][t] for k in Cuadrantes) 
                            for j in Semillas if t - theta_j[j] >= 1) == i[t] 
                            for t in Meses[1:]), 
                            name = f"Inventario de dinero")

#Condición borde inventario de dinero
modelo.addConstr((gammma_ - quicksum(c_jt[j][1]*w[j,1] for j in Semillas) == i[1]), 
                 name = f"Condición borde inventario de dinero")

#Inventario de semillas
modelo.addConstrs((u[j,t-1] + alfa_j[j]*w[j,t] - quicksum(x[j,k,t] for k in Cuadrantes) == u[j,t] 
                           for t in Meses[1:] 
                           for j in Semillas), 
                           name = f"Inventario de semillas")

#Condición borde inventario de semillas
modelo.addConstrs((u[j,1] == alfa_j[j]*w[j,1] - quicksum(x[j,k,1] for k in Cuadrantes) 
                       for j in Semillas), 
                       name = f"Condición borde inventario de semillas")

#Terminar cosecha antes de volver a cosechar
modelo.addConstrs((1 - x[j,k,t] >= quicksum(x[j,k,l] for l in range(t + 1, min(t + theta_j[j] - 1, Meses[-1]) + 1)) 
                              for j in Semillas 
                              for k in Cuadrantes
                              for t in Meses[:-1]), 
                              name = f"Terminar cosecha antes de volver a cosechar")
            

#Naturaleza de las variables
modelo.addConstrs((i[t] >= 0 
                   for t in Meses),
                   name = "Naturaleza de las variables de inventario de dinero")

modelo.addConstrs((u[j,t] >= 0 
                   for j in Semillas 
                   for t in Meses), 
                   name = "Naturaleza de las variables de inventario de semillas")
modelo.addConstrs((w[j,t] >= 0 
                   for j in Semillas 
                   for t in Meses), 
                   name = "Naturaleza de las variables de semillas compradas")

modelo.update()
#modelo.display()
modelo.optimize() 

#Valor optimo de la función
print(f"\nEl valor optimo del modelo es: {modelo.ObjVal} pesos\n")