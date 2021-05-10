# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 00:06:32 2019

@author: Enrique Buendia
"""

from os import path
import tools
import pandas as pd
import argparse
import os
import sys
from tabulate import tabulate
import numpy as np

my_parser = argparse.ArgumentParser(description='Clasificacion taxonomia de asteroides')
my_parser.add_argument('txt',
                       metavar='txt',
                       type=str,
                       help='archivo que contiene los datos del espectro a analizar')
my_parser.add_argument("--smooth", 
                       help="bandera para activar el suavizado mediante un spline3",
                    action="store_true")
args = my_parser.parse_args()
  
script_dir = path.dirname(__file__) #<-- absolute dir the script is in
archivo = args.txt
abs_file_path = path.join(script_dir, 'espectro_txt/' + archivo)
while not os.path.isfile(abs_file_path):
    print('El archivo no existe')
    sys.exit()  
txt = open(abs_file_path,'r')
espectro_txt = pd.read_csv(txt,header=None,delim_whitespace=True) ### El archivo no debe tener encabezados, y el delimitador debe se espacio en blanco
txt.close()

smooth = False
if args.smooth:
    print("Se ha realizado un suavizado mediante un spline de tercer orden")
    smooth = True
espec_inter = tools.interpolacion(espectro_txt, smooth) ### interpolamos nuestro espectro para tenerlo en las mismas
espec_demeo = tools.interpolacion_demeo(espec_inter)
demeo_tax = tools.disteuc_demeo(espec_demeo)
bus_tax = tools.disteuc_bus(espec_inter)
d = {' ':range(1,11,1),
     'Bus-DeMeo':demeo_tax[1], 
     'Bus & Binzel':bus_tax[1][:10], 
     'Dist_euc':bus_tax[0][:10]}
tabla = pd.DataFrame(data = d)
print('')
print(tabulate(tabla, headers=['Bus - DeMeo','Bus & Binzel', 'Dist Euc (B&B)'], showindex=False))

