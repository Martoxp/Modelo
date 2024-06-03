import csv

Alfa = 5000000000

M = 1000000000000000

TE = 4560

EP = 18.8

with open("Flujos.csv", 'r') as flujos_csv:
    reader = csv.reader(flujos_csv)
    data_flujos = list(reader)
    comunas_ = []
    for i in range(len(data_flujos)):
        comunas_.append(data_flujos[i].pop(0))

F_ie = {i : {e : float(data_flujos[i - 1][e - 1]) for e in range(1, len(data_flujos[i - 1]) + 1)} for i in range(1, len(comunas_) + 1)}

with open("Potencia.csv", 'r') as potencia_csv:
    reader = csv.reader(potencia_csv)
    data_potencia = list(reader)
    electrolineras_ = []
    for i in range(len(data_potencia)):
        electrolineras_.append(data_potencia[i].pop(0))

P_j = {i : int(data_potencia[i - 1][0]) for i in range(1, len(electrolineras_) + 1)} 




P_j
#Tipo 1 entrega: 2 cargadores maxima potencia (50-79kW)
#Tipo 2 entrega: 4 cargadores media potencia (22-49kW) #Sacar promedio y sumar cantidad???
#Tipo 3 entrega: 8 cargadores baja potencia (11-21kW)

Alfa #Primer informe 5000mil millones

C_jiezt = {} #la muerte chaval

NE_jie = {} # falta

TD_jiez = {} #falta

F_ie  #Excel juanisimo, Definir comunas????

CI_kt = {} #Costo insumos en excel y aplicar su variacion del tiempo con diccionarios

CN_k = {} #Falta

NI_jK = {}#falta¿

TE #4560 trabajdores en promedio

M #Big M

Beta_xe = {} #falta


A_xe = {}#pura matriz de zonas

ED_iez = {} #Suelo vacante por municipio¿

E_j = {300} #Espacio que requiere una electroliner en m^2

EP #Energia promedio que necesita un auto electrico en kW/km