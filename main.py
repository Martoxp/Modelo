#Modelo grupo 35
from bases_datos import *

#Conjuntos
comunas = [ncomuna[i] for i in comunas_] 
electrolineras = [j for j in range(1, len(electrolineras_) + 1)] 
dias = [t for t in range(1, 121)] #meses que dura el proyecto (se me olvido cambiar el nombre a meses y para cuando me di cuenta ya no alcanzaba)
insumos = [k for k in range(1, len(insumos_) + 1)]
zonas = [[e for e in zonas_[i]] for i in comunas_]
terrenos = [[[z for z in terrenos_[ncomuna[i]][e]] for e in zonas_[i]] for i in comunas_]

arcos = []
for j in electrolineras:
    for i in comunas:
        for e in zonas[i-1]:
            for z in terrenos_[i][e]:
                for t in dias:
                    arcos.append((j,i,e,z,t))

arcos2 = [(i,e,t) for i in comunas for e in zonas[i - 1] for t in dias]


#Generación del modelo de optimización:
from gurobipy import GRB, Model, quicksum

modelo = Model("Proyecto")

#Variables
x = modelo.addVars(arcos, vtype = GRB.INTEGER, name = "X" ) # Cantidad construida
w = modelo.addVars(arcos2, vtype = GRB.INTEGER, name = "W" ) # 
#y = modelo.addVars(arcos, vtype = GRB.BINARY, name = "Y" )
n = modelo.addVars(dias, vtype = GRB.CONTINUOUS, name = "N" ) # Dinero disponible
l = modelo.addVars(insumos, dias, vtype = GRB.INTEGER, name = "L" )
i = modelo.addVars(insumos, dias, vtype = GRB.INTEGER, name = "I" )
tt = modelo.addVars(arcos, vtype = GRB.INTEGER, name = "T" ) 
pn = modelo.addVars(arcos2, vtype = GRB.CONTINUOUS, name = "PN" ) #Potencia necesitada

#Función Objetivo
modelo.setObjective(quicksum(quicksum(pn[i,zonas[i-1][e],dias[-1]] for e in range(len(zonas[i-1])) ) for i in comunas), GRB.MINIMIZE)
modelo.update()

#Restrcciones

# 1er: No hay electrolineras terminadas el primer día
modelo.addConstrs((tt[j,i,e,z, 1] == 0 
                   for j in electrolineras 
                   for i in comunas 
                   for e in zonas[i-1] 
                   for z in terrenos_[i][e]), name = f"No hay electrolineras terminadas el primer día")

# 2da: 
modelo.addConstrs((tt[j,i,e,z, t + TD_j[j]] == x[j,i,e,z,t] 
                   for j in electrolineras 
                   for i in comunas 
                   for e in zonas[i-1] 
                   for z in terrenos_[i][e] 
                   for t in dias[:dias[-1] - TD_j[j]]), 
                   name = f"Electrolineras empezadas el día t son terminadas el día t + TD")

# 3era: Condición borde inventario de dinero
modelo.addConstr((n[1] == Alfa - quicksum(quicksum(quicksum(quicksum(C_jit[j][i][1]*x[j,i,e,z,1] 
                                                                      for z in terrenos_[i][e])
                                                                      for e in zonas[i-1]) 
                                                                      for i in comunas) 
                                                                      for j in electrolineras) 
                                                                      - quicksum(CI_kt[k][1]*l[k,1] 
                                                                                 for k in insumos)) 
                            ,name = f"Condición borde inventario de dinero")

# 4ta: Inventario de dinero
modelo.addConstrs((n[t] == n[t-1] - quicksum(quicksum(quicksum(quicksum(C_jit[j][i][t]*x[j,i,e,z,t]
                                                                       for z in terrenos_[i][e])
                                                                       for e in zonas[i-1]) 
                                                                       for i in comunas ) 
                                                                       for j in electrolineras)  
                                                                       - quicksum(CI_kt[k][t]*l[k,t] 
                                                                                  for k in insumos) 
                                                                                  for t in dias[1:]),
                 name = f"Inventario de dinero")

# 5ta: Condición borde inventario de insumos
modelo.addConstrs((i[k,1] == l[k,1] - quicksum(quicksum(quicksum(quicksum(NI_jK[j][k]*x[j,i,e,z,1] 
                                                                          for z in terrenos_[i][e])
                                                                          for e in zonas[i-1])  
                                                                          for i in comunas ) 
                                                                          for j in electrolineras)  
                                                                          for k in insumos), 
                            name = f"Condición borde inventario de insumos")


# 6ta: Inventario de insumos
modelo.addConstrs((i[k,t] == i[k,t - 1] + l[k,t] - quicksum(quicksum(quicksum(quicksum(NI_jK[j][k]*x[j,i,e,z,t] 
                                                                                       for z in terrenos_[i][e])
                                                                                       for e in zonas[i-1])  
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


#modelo.addConstrs((Y_jiezt[j][i][e][z][t]  <= max(0, dias[-1] + 1 - t - TD_j[j]) 
#                   for j in electrolineras
#                   for i in comunas
#                   for e in zonas[i-1] 
#                   for z in terrenos_[i][e]
#                   for t in dias), 
#                   name = f"")

# 8va:
modelo.addConstrs((x[j,i,e,z,t]  <= M*Y_jiezt[j][i][e][z][t]
                   for j in electrolineras
                   for i in comunas
                   for e in zonas[i-1] 
                   for z in terrenos_[i][e]
                   for t in dias), 
                   name = f"")


# 9na: 
modelo.addConstrs((w[i,e,t] == quicksum(NE_j[j]*quicksum(quicksum(x[j,i,e,z,tx] - tt[j,i,e,z,tx] for z in terrenos_[i][e]) for tx in dias[:t]) for j in electrolineras) 
                                        for i in comunas 
                                        for e in zonas[i-1]
                                        for t in dias),
                                        name = f"")


# 10ma:
modelo.addConstrs((TE >= quicksum(quicksum(w[i,e,t] for e in zonas[i-1]) for i in comunas)
                   for t in dias),
                   name = f"")


# 11va:
modelo.addConstrs((ED_iez[i][e][z] >= quicksum(quicksum(E_j[j]*x[j,i,e,z,tx] for j in electrolineras) for tx in dias[:t])
                  for i in comunas
                  for e in zonas[i-1] 
                  for z in terrenos_[i][e]),
                  name = f"")


# 12va:
modelo.addConstrs((pn[i,e,1] == round(F_ie[i][e]*EP) - quicksum(quicksum(P_j[j]*x[j,i,e,z,1] for z in terrenos_[i][e]) for j in electrolineras) 
                  - quicksum(quicksum(quicksum(A_he[h][e]*P_j[j]*x[j,i,h,z,1] for z in terrenos_[i][h]) for h in zonas[i-1]) for j in electrolineras) 
                  for i in comunas
                  for e in zonas[i-1]),
                  name = f"")



# 13va:
modelo.addConstrs((pn[i,e,t] == pn[i,e,t-1] - quicksum(quicksum(quicksum(P_j[j]*x[j,i,e,z,tx] for z in terrenos_[i][e]) for tx in dias[:t]) for j in electrolineras) 
                  - quicksum(quicksum(quicksum(quicksum(A_he[h][e]*P_j[j]*x[j,i,h,z,tx] for z in terrenos_[i][h]) for h in zonas[i-1]) for tx in dias[:t]) for j in electrolineras) 
                  for i in comunas
                  for e in zonas[i-1]
                  for t in dias[1:]),
                  name = f"")



#Naturaleza de las variables
modelo.addConstrs((x[j,i,e,z,t] >= 0 
                   for j in electrolineras
                   for i in comunas
                   for e in zonas[i-1] 
                   for z in terrenos_[i][e]
                   for t in dias))

modelo.addConstrs((w[i,e,t] >= 0 
                   for i in comunas
                   for e in zonas[i-1]
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

modelo.addConstrs((tt[j,i,e,z,t] >= 0 
                   for j in electrolineras
                   for i in comunas
                   for e in zonas[i-1] 
                   for z in terrenos_[i][e]
                   for t in dias))

modelo.addConstrs((pn[i,e,t] >= 0 
                   for i in comunas
                   for e in zonas[i-1] 
                   for t in dias))

modelo.update()
modelo.optimize()

#representacion de datos y generación de archivos

print("\n")
for i in comunas:
    for j in list(ncomuna.items()):
        if i in j:
            Comuna = j[0]

    for e in zonas[i - 1]:
        print(f"La potencia necesitada el año 2035 en la zona {e}, perteneciente a {Comuna}, será {pn[i,e,dias[-1]].x}kW")
        if round(F_ie[i][e]*EP) >= round(pn[i,e,dias[-1]].x):
            print(f"El valor de la potencia necesitada se ha reducido de {round(F_ie[i][e]*EP)}kW  a {pn[i,e,dias[-1]].x}kW\n")
        elif float(round(F_ie[i][e]*EP)) == pn[i,e,dias[-1]].x:
            print("El valor de la potencia necesitada no disminuyó durante los 10 años de planificación\n")

for t in dias:
    for j in electrolineras:
        for i in comunas:
            for e in zonas[i-1]:
                for z in terrenos_[i][e]:
                       if int(abs(x[j,i,e,z,t].x)) != 0:
                           print(f'El mes {t} se construyeron {x[j,i,e,z,t].x} electrolineras tipo {j} en la zona {e}')

print(f"\nDel presupuesto inicial, {Alfa} pesos, se ocupo {Alfa - n[dias[-1]].x} pesos")

potencia_inicial = sum(round(F_ie[i][e]*EP) for i in comunas for e in zonas[i - 1])
potencia_final = sum(pn[i,e,dias[-1]].x for i in comunas for e in zonas[i - 1])

print(f"\nLa potencia necesitada entre las 4 comunas se redujo de {potencia_inicial}kW a {potencia_final}kW")
print(f"Es decir, se redujo en {potencia_inicial-potencia_final}kW")

import pandas as pd

# Genera un archivo excel que muestra la potencia necesitada en cada zona de cada comuna
# en cada mes que dura el proyecto.
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
excel = pd.ExcelWriter("Potencia_necesitada.xlsx")
for t in dias:
    tabla = []
    for i in ncomuna.keys():
        zon = []
        for e in range(1,21):
            if e not in zonas_[i]:
                zon.append(0)
            else:
                zon.append(pn[ncomuna[i],e,t].x)
        tabla.append(zon)
    data = pd.DataFrame(tabla, columns = range(1,21), index = range(1,5))
    data.to_excel(excel, sheet_name=f"{meses[(t - 1)%12]} del {2025 + (t-1)//12}", index=True)
excel.close()

# Genera un archivo excel que muestra la potencia necesitada en cada comuna, y la potencia 
# necesitada entre las 4 comunas, a final de cada año. 
excel2 = pd.ExcelWriter("PN_anualmente.xlsx")
anos = [[] for i in range(5)]
for t in dias:
    if (t - 1)%12 == 11:
        for i in comunas:
            suma = 0
            for e in zonas[i-1]:
                suma += pn[i,e,t].x
            anos[i-1].append(suma)
            if i == 4:
                total = 0
                for i in comunas:
                    total += anos[i-1][-1]
                anos[4].append(total)
for i in comunas:
    suma = sum(round(F_ie[i][e]*EP) for e in zonas[i - 1])
    anos[i-1].insert(0,suma)
    if i == 4:
        total = sum(anos[i-1][0] for i in comunas)
        anos[4].insert(0,total)

ind_anos = [2025 + i for i in range(10)]
ind_anos.insert(0,"Previo al proyecto")
data = pd.DataFrame(anos, columns = ind_anos, index = [1,2,3,4,"Necesidad total"])
data.to_excel(excel2, index=True)
excel2.close()

# Genera archivo excel que muestra, por cada tipo, la cantidad de electrolineras 
# construidas por zona
excel3 = pd.ExcelWriter("Electrolineras_contruidas.xlsx")
tabla = [[0 for e in range(1,21)] for j in electrolineras]
for j in electrolineras:
    for i in ncomuna.keys():
        for e in range(1,21):
            if e in zonas_[i]:
                suma = 0
                for t in dias:
                    for z in terrenos_[ncomuna[i]][e]:
                        suma += x[j,ncomuna[i],e,z,t].x
                tabla[j - 1][e - 1] = suma
        
data = pd.DataFrame(tabla, columns = range(1,21), index = range(1,4))
data.to_excel(excel3, index=True)
excel3.close()
# Electrolineras construidas para el 2035