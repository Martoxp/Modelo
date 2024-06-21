import csv
from random import randint, seed


seed(700)

#Zona de cada comuna
zonas_ = {"Penalolen":[1,2,3,4,5,6],"LaReina":[7,8,9,10,11],"Nunoa":[12,13,14,15,16],"Macul":[17,18,19,20]}

#Numero comuna
ncomuna = {"Penalolen":1,"LaReina":2,"Nunoa":3,"Macul":4}

#Terreno por zona de cada comuna
cantidad_terrenos = 1
terrenos_ = {}
for n in ncomuna.keys():
    terrenos_[ncomuna[n]] = {}
    for e in zonas_[n]:
        lista = []
        num = randint(3,5)
        for z in range(cantidad_terrenos, cantidad_terrenos + num):
            lista.append(z)
        cantidad_terrenos = cantidad_terrenos + num
        terrenos_[ncomuna[n]][e] = lista


#Capital Inicial
Alfa = 5000000000 #5.000.000.000 pesos
#Big M
M = 1000000000000000
#Trabajadores de la empresa
TE = 700
#Energia Promedio
EP = 18.8


with open("Flujos.csv", 'r') as flujos_csv:
    reader = csv.reader(flujos_csv)
    data_flujos = list(reader)
    comunas_ = []
    for i in range(len(data_flujos)):
        comunas_.append(data_flujos[i].pop(0))
F_ie = {}
for i in comunas_:
    F_ie[ncomuna[i]] = {}
    ind = 0
    for e in zonas_[i]:
       F_ie[ncomuna[i]][e] = int(data_flujos[ncomuna[i] - 1][ind])
       ind += 1


with open("Potencia.csv", 'r') as potencia_csv:
    reader = csv.reader(potencia_csv)
    data_potencia = list(reader)
    electrolineras_ = []
    for i in range(len(data_potencia)):
        electrolineras_.append(data_potencia[i].pop(0))
P_j = {j : int(data_potencia[j - 1][0]) for j in range(1, len(electrolineras_) + 1)} 


with open("Necesidad_insumos.csv", 'r') as necesidad_csv:
    reader = csv.reader(necesidad_csv)
    data_necesidad = list(reader)
    for i in range(len(data_necesidad)):
        data_necesidad[i].pop(0)
        if i == 0:
            insumos_ = [k for k in range(1, len(data_necesidad[i]) + 1)]
NI_jK = {j : {k : int(data_necesidad[i - 1][k - 1]) for k in insumos_} for j in range(1, len(electrolineras_) + 1)} 


with open("Espacio_electrolinera.csv", 'r') as espacio_e_csv:
    reader = csv.reader(espacio_e_csv)
    data_espacio_e = list(reader)
    for i in range(len(data_potencia)):
        data_espacio_e[i].pop(0)
E_j = {j : int(data_espacio_e[j - 1][0]) for j in range(1, len(electrolineras_) + 1)}


with open("Adyacencia.csv", 'r') as adyacencia_csv:
    reader = csv.reader(adyacencia_csv)
    data_adyacencia = list(reader)
A_he = {e : {h: float(data_adyacencia[e - 1][h - 1]) for h in range(1, len(data_adyacencia) + 1)} for e in range(1, len(data_adyacencia) + 1)}


with open("Necesidad_trabajadores.csv", 'r') as necesidad_t_csv:
    reader = csv.reader(necesidad_t_csv)
    data_necesidad_t = list(reader)
    for i in range(len(data_necesidad_t)):
        data_necesidad_t[i].pop(0)
NE_j = {j : int(data_necesidad_t[j - 1][0]) for j in range(1, len(data_necesidad_t) + 1)} 


with open("Tiempo_demora.csv", 'r') as tiempo_csv:
    reader = csv.reader(tiempo_csv)
    data_tiempo = list(reader)
    for i in range(len(data_tiempo)):
        data_tiempo[i].pop(0)
TD_j = {j : int(data_tiempo[j - 1][0]) for j in range(1, len(electrolineras_) + 1)}


with open("Necesidad_insumos.csv", 'r') as necesidad_csv:
    reader = csv.reader(necesidad_csv)
    data_necesidad = list(reader)
    for i in range(len(data_necesidad)):
        data_necesidad[i].pop(0)
        if i == 0:
            insumos_ = [k for k in range(1, len(data_necesidad[i]) + 1)]
NI_jK = {j : {k : int(data_necesidad[i - 1][k - 1]) for k in insumos_} for j in range(1, len(electrolineras_) + 1)} 


ED_iez = {ncomuna[i]: {e: {z: randint(1200,1800) for z in terrenos_[ncomuna[i]][e]} for e in zonas_[i]} for i in comunas_}


with open("capacidad_bodega.csv", 'r') as capacidad_csv:
    reader = csv.reader(capacidad_csv)
    data_capacidad = list(reader)[1:]
    for i in range(len(data_capacidad)):
        data_capacidad[i].pop(0)
CN_k = {k : int(data_capacidad[k - 1][0]) for k in insumos_}


#C_jit

#Costo electrolinera en pesos tipo j 
Cj = [53291759,37944034,21438535]
#Factor Comunal (VALOR UF/M^2)
Fi = [0.74 , 1 , 0.99 , 0.73]
#Factor Anual de infiacion
Inflacion = 1.03

C_jit = {j: {i: {t : int(Cj[j - 1]*Fi[i - 1]*(Inflacion**((t-1)//12))) for t in range(1,121)} for i in range(1, len(comunas_) + 1)} for j in range(1, len(electrolineras_) + 1)}


Precio_base_k = [200000,500000,100000,2000000,300000,100000,3000000,17000000,50000000,50000,500000,1500000,500000,200000,75000]
Variacion_por_estacion = [1.25,0.75,0.75,1]
CI_kt = {}
for k in insumos_:
    CI_kt[k] = {}
    restar = 0
    for t in range(1, 121):
        if t > 12:
            restar = 12*((t-1)//12)
        CI_kt[k][t] = int(Variacion_por_estacion[int((t - 1 - restar)//3)]*Precio_base_k[k-1]*(Inflacion**((t-1)//12)))


Y_jiezt = {j:{ncomuna[i]:{e:{z:{t: 1 if max(0, 121 - t - TD_j[j]) > 0 else 0 for t in range(1,121)} for z in terrenos_[ncomuna[i]][e]} for e in zonas_[i]} for i in comunas_} for j in range(1, len(electrolineras_) + 1)}
print(A_he[8][11])
print(A_he[4][11])
print(A_he[12][11])
print(A_he[10][11])

print("\n")

print(A_he[4][8])
print(A_he[5][8])
print(A_he[6][8])
print(A_he[7][8])
print(A_he[9][8])
print(A_he[10][8])
print(A_he[11][8])
