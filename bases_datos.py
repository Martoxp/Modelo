import csv

zonas_ = {}

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
#Los datos en esta lista vienen ordenados como zona {1,2,3,4,5,6},{7,8,9...etc}

F_ie = {i : {e : int(data_flujos[i - 1][e - 1]) for e in range(1, len(data_flujos[i - 1]) + 1)} for i in range(1, len(comunas_) + 1)}

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


print("P_j:", P_j)
#Tipo 1 entrega: 2 cargadores maxima potencia (50-79kW)
#Tipo 2 entrega: 4 cargadores media potencia (22-49kW) #Sacar promedio y sumar cantidad???
#Tipo 3 entrega: 8 cargadores baja potencia (11-21kW)

print("Alfa:",Alfa) #Primer informe 5000mil millones

C_jiezt = {} #la muerte chaval

NE_jie = {} # falta

TD_jiez = {} #falta

print("Flujos:",F_ie)  #Excel juanisimo, Definir comunas????

CI_kt = {} #Costo insumos en excel y aplicar su variacion del tiempo con diccionarios

CN_k = {} #Falta

print("Necesidad:",NI_jK) #falta¿

print("Trabajadores de empresa:",TE) #4560 trabajdores en promedio

print("Big M:", M) #Big M

A_he = {}#pura matriz de zonas

ED_iez = {} #Suelo vacante por municipio¿

print("Espacio de electrolineras:", E_j) #Espacio que requiere una electroliner en m^2

print("Energía promedio autos:", EP) #Energia promedio que necesita un auto electrico en kW/km




