# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 00:06:32 2019

@author: Enrique Buendia
"""

import pandas as pd
from scipy.interpolate import interp1d ###                                           
import numpy as np
from os import path
from scipy.signal import savgol_filter
#from sklearn import model_selection, neighbors, metrics, pipeline, preprocessing
import pickle
import rocks
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

script_dir = path.dirname(__file__) #<-- absolute dir the script is in

### Función para interpolar el espectro de nuestro asteroide ###

def interpolacion(espec, smooth, micras):### Debemos proporcionar el espectro en formato pandas
				                 ### en la primera columna debe de estar el flujo y en la segunda la longitud de onda que debe 
                                 ### estar en angstroms 
    flujo = espec.iloc[:,1];flujo = flujo.to_numpy() ### cargam
    LO = espec.iloc[:,0];LO = LO.to_numpy() ### cargam
    newLO = []; flux = []

    if micras == True:
        LO = LO*10000

    for n in range(len(LO)):
        if LO[n] > 4200 and LO[n] < 9400:
            newLO.append(LO[n]/10000)
            flux.append(flujo[n])
    flux = np.asarray(flux); newLO = np.asarray(newLO)
    LOC = np.linspace(0.44, 0.92, 49) ### Longitudes de onda en la que queremos interpolar, son 49 puntos entre 4400 y 9200 
    
    if smooth == True:
        suav = savgol_filter(flux, 7, 3)
        inter = interp1d(newLO, suav, fill_value='extrapolate') ### interpolación lineal
        fluxinter = inter(LOC) ### 49 Flujos evaluados en las longitudes de onda que definimos antes 
    else:
        inter = interp1d(newLO, flux, fill_value='extrapolate') ### interpolación lineal
        fluxinter = inter(LOC) ### 49 Flujos evaluados en las longitudes de onda que definimos antes 
        suav=flux
    return fluxinter,suav, newLO ### Regresa el flujo interpolado para 49 puntos en formato numpy
    
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
    for n in range(50): ### Solo utilizaremos las 50 menores distancias espectrales
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
    return nclases, peso
    
def KNN(espec_inter):
    espec_inter=espec_inter.reshape(1,-1)
    # load the PCA from disk
    pca_reload = pickle.load(open("data/PCA",'rb'))
    espec_pca=pca_reload.transform(espec_inter)

    # load the NCA from disk
    nca_reload = pickle.load(open("data/NCA",'rb'))
    espec_nca=nca_reload.transform(espec_inter)
    
    # load the model knn from disk
    knn_reload = pickle.load(open("data/knnoriginal",'rb'))
    knn_predic=knn_reload.predict_proba(espec_inter)
    
    # load the model from disk
    knnPCA_reload = pickle.load(open("data/knnPCA",'rb'))
    knn_predic_PCA=knnPCA_reload.predict_proba(espec_pca)

    # load the model from disk
    knnNCA_reload = pickle.load(open("data/knnNCA",'rb'))
    knn_predic_NCA=knnNCA_reload.predict_proba(espec_nca)

    return knn_predic, knn_predic_PCA, knn_predic_NCA

def graficar(flujo,wl,numero):
    #y=np.linspace(4400,9200,49)
    ident=rocks.identify(numero)
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(wl, flujo, 'black', lw=0.65, )
    plt.ylim((0.6,1.4))
    plt.xlim((0.44,0.9200))
    ax.xaxis.set_minor_locator(MultipleLocator(0.02))
    plt.xlabel(r'Wavelength ($\mu$m)', fontsize=15)
    plt.ylabel('Reflectance', fontsize=15)
    ax.text(0.4500, 1.3, '({0}) {1}'.format(numero,ident[0]), size='x-large')
    results_dir = path.join(script_dir, 'output/')
    plt.savefig(results_dir+str(numero)+ident[0]+'.pdf', bbox_inches='tight')

