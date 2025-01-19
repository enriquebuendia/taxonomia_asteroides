# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 00:06:32 2019

@author: Enrique Buendia
"""
import tools
import pandas as pd
import argparse, os, sys
from tabulate import tabulate
import archivos
#%% Parte del CDM
my_parser = argparse.ArgumentParser(description='Clasificacion taxonomia de asteroides')
my_parser.add_argument('txt',
                       metavar='txt',
                       type=str,
                       help='Archivo que contiene los datos del espectro a analizar, la primera columna debe contener la longitud de onda, y la segunda el flujo normalizado')
my_parser.add_argument("--smooth", 
                       help="Bandera para activar el suavizado mediante un spline3",
                    action="store_true")
my_parser.add_argument("--micrometros", 
                       help="Si la longitud de onda de su archivo esta en en micrometros, activar esta bandera",
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
smooth = False; micro = False
if args.smooth:
    print("Se ha realizado un suavizado mediante un spline de tercer orden")
    smooth = True
if args.micrometros:
    micro = True
espec_inter = tools.interpolacion(espectro_txt, smooth, micro) ### interpolamos nuestro espectro para tenerlo en las mismas
espec_demeo = tools.interpolacion_demeo(espec_inter)
demeo_tax = tools.disteuc_demeo(espec_demeo)
bus_tax = tools.disteuc_bus(espec_inter)
d = {' ':range(1,11,1),
     'Bus-DeMeo':demeo_tax[1], 
     'Bus & Binzel':bus_tax[1][:10], 
     'Dist_euc':bus_tax[0][:10]}
tabla = pd.DataFrame(data = d)
#%% Imprimir en terminal
print('')
print(tabulate(tabla, headers=['Bus - DeMeo','Bus & Binzel', 'Dist Euc (B&B)'], showindex=False))
taxos_list=[]
for n in [10,30,50]:
    taxos_prop = tools.datos(bus_tax[1], n)
    taxos_list.append(tools.datos(bus_tax[1], n))
    print("\n Taxonomía propuesta para k = {}: {} con función de peso de {:2f}".format(n, taxos_prop[0], taxos_prop[1]))
#%% Escribir txt resumen
archivos.crea_res(archivo, taxos_list)

 
