import csv
from random import randint

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
print(terrenos_)

Alfa = 5000000000

M = 1000000000000000

TE = 700

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
A_eh = {e : {h: float(data_adyacencia[e - 1][h - 1]) for h in range(1, len(data_adyacencia) + 1)} for e in range(1, len(data_adyacencia) + 1)}


with open("Necesidad_trabajadores.csv", 'r') as necesidad_t_csv:
    reader = csv.reader(necesidad_t_csv)
    data_necesidad_t = list(reader)
    for i in range(len(data_necesidad_t)):
        data_necesidad_t[i].pop(0)
NE_j = {j : int(data_necesidad_t[j - 1][0]) for j in range(1, len(data_necesidad_t) + 1)} 

ED_iez = {}

print("P_j:", P_j)
#Tipo 1 entrega: 2 cargadores maxima potencia (50-79kW)
#Tipo 2 entrega: 4 cargadores media potencia (22-49kW) #Sacar promedio y sumar cantidad???
#Tipo 3 entrega: 8 cargadores baja potencia (11-21kW)

print("Alfa:",Alfa) #Primer informe 5000mil millones

C_jiezt = {} #la muerte chaval

print("Necesidad de trabajadores:",NE_j) # falta

TD_jiez = {} #falta

print("Flujos:",F_ie)  #Excel juanisimo, Definir comunas????

CI_kt = {} #Costo insumos en excel y aplicar su variacion del tiempo con diccionarios

CN_k = {} #Falta

print("Necesidad:",NI_jK) #falta¿

print("Trabajadores de empresa:",TE) #4560 trabajdores en promedio

print("Big M:", M) #Big M

print("Adyacencia:",A_eh)#pura matriz de zonas

ED_iez = {} #Suelo vacante por municipio¿

print("Espacio de electrolineras:", E_j) #Espacio que requiere una electroliner en m^2

print("Energía promedio autos:", EP) #Energia promedio que necesita un auto electrico en kW/km




