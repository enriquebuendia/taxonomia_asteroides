# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 00:06:32 2019

@author: Enrique Buendia
"""
import tools
import pandas as pd
import argparse, os, sys
from tabulate import tabulate
#import archivos
import numpy as np

#%% Parte del CDM
my_parser = argparse.ArgumentParser(description='Clasificacion taxonomia de asteroides')
my_parser.add_argument('txt',
                       metavar='txt',
                       type=str,
                       help='Archivo que contiene los datos del espectro a analizar, la primera columna debe contener la longitud de onda, y la segunda el flujo normalizado')
my_parser.add_argument("--smooth", 
                       help="Bandera para activar el suavizado mediante un spline3",
                    action="store_true")
my_parser.add_argument("--micras", 
                       help="Si la longitud de onda de su archivo esta en en micras, activar esta bandera",
                    action="store_true")
args = my_parser.parse_args()
archivo = args.txt

#%% Leer txt
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
abs_file_path = os.path.join(script_dir, 'espectro_txt/' + archivo)
while not os.path.isfile(abs_file_path):
    print('El archivo no existe')
    sys.exit()  
txt = open(abs_file_path,'r')
espectro_txt = pd.read_csv(txt,header=None,delim_whitespace=True) ### El archivo no debe tener encabezados, y el delimitador debe se espacio en blanco
txt.close()
#%% Llamada de funciones aux
smooth = False; micras = False
if args.smooth:
    print("Se ha realizado un suavizado mediante un spline de tercer orden")
    smooth = True
if args.micras:
    micras = True
espec_inter,suavizado, newLO = tools.interpolacion(espectro_txt, smooth, micras) ### interpolamos nuestro espectro para tenerlo en las mismas
espec_demeo = tools.interpolacion_demeo(espec_inter)
demeo_tax = tools.disteuc_demeo(espec_demeo)
bus_tax = tools.disteuc_bus(espec_inter)
proba=tools.KNN(espec_inter)
proba=np.asarray(proba)
proba=proba.reshape(3,5)
#%%Crear tabla (DataFrame)
d = {' ':range(1,11,1),
     'Bus-DeMeo':demeo_tax[1], 
     'Bus & Binzel':bus_tax[1][:10], 
     'Dist_euc':bus_tax[0][:10]}
tabla = pd.DataFrame(data = d)
#%% Imprimir en terminal
print('')
print(tabulate(tabla, headers=['Bus - DeMeo','Bus & Binzel', 'Dist Euc (B&B)'], showindex=False))
taxos_list=[]
for n in [10]:
    taxo_prop, pesos = tools.datos(bus_tax[1], n)
    taxos_list.append(tools.datos(bus_tax[1], n))
    peso_mayor=pesos[np.argmax(pesos)]/np.sum(pesos)
    print('\nFunciones de peso por clases: \n{}'.format({tax:wf for tax,wf in zip(taxo_prop, pesos/np.sum(pesos))}))
    print("\nTaxonomía propuesta para k = {}: {} con función de peso de {:2f}".format(n, taxo_prop[np.argmax(pesos)], peso_mayor))
print('\nProbabilidades de tipos para el KNN original')
#%%Crear tabla (DataFrame)
#probas=np.array(proba,dtype=[('S','<i4'),('C','<i4'),('X','<i4'),('PS','<i4'),('NS','<i4')])
filas= np.array([0,1,2], dtype=np.intp)
#print(proba[filas,[0,0,0]])
d = {'Tipo S':proba[filas,[0,0,0]], 
     'Tipo C':proba[filas,[1,1,1]], 
     'Tipo X':proba[filas,[2,2,2]],
     'Positive Slope':proba[filas,[3,3,3]],
     'Negative Slope':proba[filas,[4,4,4]]}
tablaKNN = pd.DataFrame(data = d, index=(['KNN_Original','KNN_PCA','KNN_NCA']))
#%% Imprimir en terminal
print('')
print(tabulate(tablaKNN, headers=['Tipo S','Tipo C', 'Tipo X', 'PS', 'NS'], showindex=True))
predicKNN=np.array([np.argmax(proba[0]),np.max(proba[0])])
predicPCA=np.array([np.argmax(proba[1]),np.max(proba[1])])
predicNCA=np.array([np.argmax(proba[2]),np.max(proba[2])])
#print(predicPCA[0],predicPCA[1])
#%% Escribir txt resumen
#archivos.crea_res(archivo, taxos_list[-1],predicKNN,predicPCA,predicNCA)
tools.graficar(suavizado,newLO,int(archivo[1:7]))
 