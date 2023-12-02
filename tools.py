# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 00:06:32 2019

@author: Enrique Buendia
"""

import pandas as pd
from scipy.interpolate import interp1d ###                                           
import numpy as np
from os import path
from astropy.convolution import Gaussian1DKernel, convolve

script_dir = path.dirname(__file__) #<-- absolute dir the script is in

### Función para interpolar el espectro de nuestro asteroide ###

def interpolacion(espec, smooth, micro):### Debemos proporcionar el espectro en formato pandas
				                 ### en la primera columna debe de estar el flujo y en la segunda la longitud de onda que debe 
                                 ### estar en nanometro 
    flujo = espec.iloc[:,1];flujo = flujo.to_numpy() ### cargam
    LO = espec.iloc[:,0];LO = LO.to_numpy() ### cargam
    if micro == True:
        LO = LO*10000
    newLO = []; flux = []
    for n in range(len(LO)):
        if LO[n] > 4200 and LO[n] < 9400:
            newLO.append(LO[n]/10000)
            flux.append(flujo[n])
    flux = np.asarray(flux); newLO = np.asarray(newLO)
    LOC = np.linspace(0.44, 0.92, 49) ### Longitudes de onda en la que queremos interpolar, son 49 puntos entre 4400 y 9200 
    
    if smooth == True:
        suav = convolve(flux,Gaussian1DKernel(stddev=1))
        interpolacion = interp1d(newLO, suav, fill_value='extrapolate') ### interpolación lineal
        fluxinter = interpolacion(LOC) ### 49 Flujos evaluados en las longitudes de onda que definimos antes 
    else:
        interpolacion = interp1d(newLO, flux, fill_value='extrapolate') ### interpolación lineal
        fluxinter = interpolacion(LOC) ### 49 Flujos evaluados en las longitudes de onda que definimos antes 
    
    return fluxinter ### Regresa el flujo interpolado para 49 puntos en formato numpy
    
def interpolacion_demeo(espec_inter):
    espec_demeo = []
    for n in range(1,49,5):
       espec_demeo.append(espec_inter[n])
    return espec_demeo
    
### Función para calcular la distacia euclidiana entre dos espectros con la clasificacion Bus-Demeo ###

def disteuc_demeo(flujo_evaluar):### Primero debemos proporcionar los flujos de nuestro espectro     
    demeo=pd.read_excel('data/busdemeo-meanspectra.xlsx'); tax_demeo=[] 
    demeo_tax=[]
    for n in range(1,51,2):
        tax_demeo.append(demeo.iloc[1:11,n])
        demeo_tax.append(demeo.iloc[0,n])
    Distancia=np.zeros((25,1))
    for n in range(len(tax_demeo)):
        suma=0; 
        for k in range(len(tax_demeo[0])):
            suma=((flujo_evaluar[k]-tax_demeo[n].iloc[k])**2)+suma    
        Distancia[n]=np.sqrt(suma)
    demeo_index = np.argsort(np.transpose(Distancia)); demeo_index=demeo_index.tolist()
    demeo_sort = []
    for n in range(len(demeo_tax)):
        demeo_sort.append(demeo_tax[demeo_index[0][n]])
    demeo_sort = np.array(demeo_sort[0:10])
    return Distancia, demeo_sort, tax_demeo[demeo_index[0][0]]
    
def disteuc_bus(espec_evaluar):
    smass1367 = pd.read_csv('data/tabla_smass.csv', header=0, sep=",")
    clasificacion = smass1367.iloc[:,49];clasificacion = clasificacion.to_numpy() ### Leemos la columna que contiene las clasificaciones del SMASSII
    flujo= smass1367.iloc[:,:-1]; flujo = flujo.to_numpy() ### Se lee los flujos de la base SMASSII-E
    cuadrado = np.zeros(flujo.shape)
    distancias = np.zeros(1367)
    for fila in range(1367):
        for columna in range(49):
            cuadrado[fila,columna] = np.power((espec_evaluar[columna]-flujo[fila,columna]),2)
        distancias[fila] = np.sqrt(np.sum(cuadrado[fila]))
    menores_indices=np.argsort(distancias)
    distancias=np.sort(distancias)
    taxos = []
    for n in range(50): ### Solo utilizaremos las 50 merores distancias espectrales
        taxos.append(clasificacion[menores_indices[n]])
    return distancias, taxos

def datos(taxos, n):
    nclases = list(dict.fromkeys(taxos[:n]))
    porc=[]; suma=0; puntaje = []; peso = []
    freq_total_lbl={'C':142, 'B':60, 'Sk':16, 'V':35, 'S':383, 'L':34, 'Ch':138, 
                    'X':111, 'Sl':49, 'Xk':39, 'Cb':33, 'Sq':52, 'Cgh':15, 'Xc':60,
                    'Sa':34, 'Xe':28, 'K':31, 'T':14, 'Cg':9, 'Ld':13, 'A':16,
                    'D':9, 'R':4, 'Sr':15, 'Q':21, 'O':6}
    for i in nclases:
        porc.append((taxos[:n].count(i))/freq_total_lbl[i])
        conta = n
        suma = 0
        for m in taxos[:n]:
            if m==i:
                suma=suma+conta
            conta -=1
        puntaje.append(suma)
        
    for k in range(len(puntaje)):
        peso.append(puntaje[k]*porc[k])
    peso = np.array(peso)
    taxo_finales = np.argsort(peso)
    return nclases[taxo_finales[-1]], peso[taxo_finales[-1]]/np.sum(peso)
    
    
    
		

    
