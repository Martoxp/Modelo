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
#Parametros

P_j = {}
Alfa = {}
C_jiezt = {} 
NE_jie = {}
TD_jiez = {}
F_ie = {}
CI_kt = {}
CN_k = {}
G_jiezt = {} 
NI_jK = {}
TE = {}
M = {}
Beta_xe = {} 
A_xe = {}
ED_iez = {}
E_j = {}
EP = {}


hh = 1000000

#Conjuntos
comunas = [i for i in range(1, hh + 1)] 
electrolineras = [j for j in range(1, hh + 1)] 
dias = [t for t in range(1, hh + 1)] 
insumos = [k for k in range(1, hh + 1)]
zonas = [e for e in range(1, hh + 1)]
terrenos = [z for z in range(1, hh + 1)]


#Generación del modelo de optimización:

from gurobipy import GRB, Model, quicksum

modelo = Model("Tarea 2")

#Variables

x = modelo.addVars(electrolineras, comunas, zonas, terrenos, dias, vtype = GRB.INTEGER, name = "X" )
w = modelo.addVars(comunas, zonas, dias, vtype = GRB.INTEGER, name = "W" )
y = modelo.addVars(electrolineras, comunas, zonas, terrenos, dias, vtype = GRB.BINARY, name = "Y" )
n = modelo.addVars(dias, vtype = GRB.INTEGER, name = "N" )
l = modelo.addVars(insumos, dias, vtype = GRB.INTEGER, name = "L" )
i = modelo.addVars(insumos, dias, vtype = GRB.INTEGER, name = "I" )
t = modelo.addVars(electrolineras, comunas, zonas, terrenos, dias, vtype = GRB.INTEGER, name = "T" )
pn = modelo.addVars(comunas, zonas, dias, vtype = GRB.INTEGER, name = "PN" )

#Función Objetivo
modelo.setObjective(quicksum(quicksum(i[pn[i,e,dias[-1]]] for e in zonas) for i in comunas), GRB.MINIMIZE)
modelo.update()


#Restrcciones

#No hay electrolineras terminadas el primer día
modelo.addConstrs((t[j,i,e,z, 1] == 0 
                   for j in electrolineras 
                   for i in comunas 
                   for e in zonas 
                   for z in terrenos), name = f"No hay electrolineras terminadas el primer día")

#Solo 1 sembrado por cuadrante
modelo.addConstrs((t[j,i,e,z, t + TD_jiez[j,i,e,z]] == x[j,i,e,z,t] 
                   for j in electrolineras 
                   for i in comunas 
                   for e in zonas
                   for z in terrenos 
                   for t in dias), 
                   name = f"Electrolineras empezadas el día t son terminadas el día t + TD")

#Inventario de dinero

modelo.addConstrs((n[1] == Alfa - quicksum(quicksum(quicksum(quicksum(C_jiezt[j][i][e][z][1]*x[j,i,e,z,1] 
                                                                      for j in electrolineras)
                                                                      for z in terrenos) 
                                                                      for e in zonas) 
                                                                      for i in comunas) 
                                                                      - quicksum(CI_kt[k][1]*l[k,1] 
                                                                                 for k in insumos)), 
                            name = f"Condición borde inventario de dinero")

#Condición borde inventario de dinero
modelo.addConstr((n[t] == n[t-1] + quicksum(quicksum(quicksum(quicksum(C_jiezt[j][i][e][z][1]*x[j,i,e,z,1] 
                                                                      for j in electrolineras)
                                                                      for z in terrenos) 
                                                                      for e in zonas) 
                                                                      for i in comunas) 
                                                                      - quicksum(CI_kt[k][1]*l[k,1] 
                                                                                 for k in insumos)),
                 name = f"Inventario de dinero")

#Hasta aca esta listo, falta arreglar esta que esta aca arriba



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