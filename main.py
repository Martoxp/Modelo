#Modelo grupo 35
import csv
import pandas as pd
from bases_datos import *

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

hh = 1000000

#Conjuntos
comunas = [i for i in range(1, len(comunas_) + 1)] 
electrolineras = [j for j in range(1, len(electrolineras_) + 1)] 
dias = [t for t in range(1, hh + 1)] 
insumos = [k for k in range(1, hh + 1)]
zonas = [e for e in range(1, hh + 1)]
terrenos = [z for z in range(1, hh + 1)]



#Generación del modelo de optimización:

from gurobipy import GRB, Model, quicksum

modelo = Model("Proyecto")

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

# 1er: No hay electrolineras terminadas el primer día
modelo.addConstrs((t[j,i,e,z, 1] == 0 
                   for j in electrolineras 
                   for i in comunas 
                   for e in zonas 
                   for z in terrenos), name = f"No hay electrolineras terminadas el primer día")


# 2da: Solo 1 sembrado por cuadrante
modelo.addConstrs((t[j,i,e,z, t + TD_jiez[j,i,e,z]] == x[j,i,e,z,t] 
                   for j in electrolineras 
                   for i in comunas 
                   for e in zonas
                   for z in terrenos 
                   for t in dias[:dias[-1] - TD_jiez[j,i,e,z]]), 
                   name = f"Electrolineras empezadas el día t son terminadas el día t + TD")
#lo tendremos en cuenta

# 3era: Condición borde inventario de dinero
modelo.addConstrs((n[1] == Alfa - quicksum(quicksum(quicksum(quicksum(C_jiezt[j][i][e][z][1]*x[j,i,e,z,1] 
                                                                      for z in terrenos)
                                                                      for e in zonas) 
                                                                      for i in comunas ) 
                                                                      for j in electrolineras) 
                                                                      - quicksum(CI_kt[k][1]*l[k,1] 
                                                                                 for k in insumos)), 
                            name = f"Condición borde inventario de dinero")


# 4ta: Inventario de dinero
modelo.addConstrs((n[t] == n[t-1] - quicksum(quicksum(quicksum(quicksum(C_jiezt[j][i][e][z][t]*x[j,i,e,z,t]
                                                                       for z in terrenos)
                                                                       for e in zonas) 
                                                                       for i in comunas ) 
                                                                       for j in electrolineras)  
                                                                       - quicksum(CI_kt[k][t]*l[k,t] 
                                                                                  for k in insumos) 
                                                                                  for t in dias[1:]),
                 name = f"Inventario de dinero")


# 5ta: Condición borde inventario de insumos
modelo.addConstrs((i[k,1] == l[k,1] - quicksum(quicksum(quicksum(quicksum(NI_jK[j][k]*x[j,i,e,z,1] 
                                                                          for z in terrenos)
                                                                          for e in zonas) 
                                                                          for i in comunas ) 
                                                                          for j in electrolineras)  
                                                                          for k in insumos), 
                            name = f"Condición borde inventario de insumos")


# 6ta: Inventario de insumos
modelo.addConstrs((i[k,t] == i[k,t - 1] + l[k,t] - quicksum(quicksum(quicksum(quicksum(NI_jK[j][k]*x[j,i,e,z,t] 
                                                                      for z in terrenos)
                                                                      for e in zonas) 
                                                                      for i in comunas ) 
                                                                      for j in electrolineras)  
                                                                      for k in insumos
                                                                      for t in dias[1:]),
                 name = f"Inventario de insumos")


# 7ma: Cantidad de insumos no supera capacidad de bodega
modelo.addConstrs((CN_k[k] >= i[k,t] 
                   for k in insumos 
                   for t in dias), 
                   name = f"Cantidad de insumos guardados debe caber en la bodega")


# 8va: 
modelo.addConstrs((pn[i,e,1] == F_ie[i][e]*EP - quicksum(quicksum(P_j[j]*x[j,i,e,z,1] for z in terrenos) for j in electrolineras) 
                  - quicksum(quicksum(quicksum(A_xe[i,e,h]*P_j[j]*x[j,i,e,z,1] for z in terrenos) for h in zonas) for j in electrolineras) 
                  for i in comunas
                  for e in zonas),
                  name = f"")

#Acordarse de definir en el A que e = h es 0
# 9na:
modelo.addConstrs((pn[i,e,t] == pn[i,e,t-1] - quicksum(quicksum(quicksum(P_j[j]*x[j,i,e,z,tx] for z in terrenos) for tx in dias[:t]) for j in electrolineras) 
                  - quicksum(quicksum(quicksum(quicksum(A_xe[i,e,h]*P_j[j]*x[j,i,e,z,tx] for z in terrenos) for h in zonas) for tx in dias[:t]) for j in electrolineras) 
                  for i in comunas
                  for e in zonas
                  for t in dias[1:]),
                  name = f"")


# 10ma: 
modelo.addConstrs((y[j,i,e,z,t]  <= max(0, dias[-1] + 1 - t - TD_jiez[j][i][e][z][t]) 
                   for j in electrolineras
                   for i in comunas
                   for e in zonas
                   for z in terrenos
                   for t in dias), 
                   name = f"")


# 11va:
modelo.addConstrs((x[j,i,e,z,t]  <= M*y[j,i,e,z,t]
                   for j in electrolineras
                   for i in comunas
                   for e in zonas
                   for z in terrenos
                   for t in dias), 
                   name = f"")


# 12va:
modelo.addConstrs((w[i,e,t] == quicksum(NE_jie[j][i][e][t]*(quicksum(quicksum(x[j,i,e,z,tx] - t[j,i,e,z,tx] for z in terrenos)) for tx in dias[:t]) 
                                        for j in electrolineras) 
                                        for i in comunas 
                                        for e in zonas
                                        for t in dias),
                                        name = f"")


# 13va:
modelo.addConstrs((TE >= quicksum(quicksum(w[i,e,t] for e in zonas) for i in comunas)
                   for t in dias),
                   name = f"")


# 14va:
modelo.addConstrs((ED_iez[i][e][z] >= quicksum(quicksum(E_j[j]*x[j,i,e,z,tx] for j in electrolineras) for tx in dias[:t])
                  for e in comunas
                  for z in terrenos
                  for t in dias),
                  name = f"")


#Naturaleza de las variables
modelo.addConstrs((x[j,i,e,z,t] >= 0 
                   for j in electrolineras
                   for i in comunas
                   for e in zonas
                   for z in terrenos
                   for t in dias))

modelo.addConstrs((w[i,e,t] >= 0 
                   for i in comunas
                   for e in zonas
                   for t in dias))

modelo.addConstrs((n[t] >= 0 
                   for t in dias))

modelo.addConstrs((n[t] >= 0 
                   for t in dias))

modelo.addConstrs((l[k,t] >= 0 
                   for k in insumos
                   for t in dias))

modelo.addConstrs((i[k,t] >= 0 
                   for k in insumos
                   for t in dias))

modelo.addConstrs((t[j,i,e,z,t] >= 0 
                   for j in electrolineras
                   for i in comunas
                   for e in zonas
                   for z in terrenos
                   for t in dias))

modelo.addConstrs((pn[i,e,t] >= 0 
                   for i in comunas
                   for e in zonas
                   for t in dias))

modelo.update()
#modelo.display()
#modelo.optimize()

#Valor optimo de la función
print(f"\nEl valor optimo del modelo es: {modelo.ObjVal} pesos\n")