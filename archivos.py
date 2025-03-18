# -*- coding: utf-8 -*-
"""
Created on Sun May 16 16:03:55 2021

@author: ubuntu
"""

from astroquery.mpc import MPC
from datetime import date
from os import path

def crea_res(archivo, FP, KNN, PCA, NCA):
    abs_file_path = path.join('output', 'summary_' + archivo)
    fecha=date.today()
    txt = open(abs_file_path,'w')
    txt.write(
        '# Programa: Clasificación Taxonómica de Asteroides ' +
        '\n# Autor: Enrique Buendia-Verdiguel' +
        '\n# Archivo: {}'.format(archivo) + 
        '\n# Fecha de creación: ' + str(fecha) + 
        '\n# Taxonomía propuesta con k= 10: {} con FP {:.2f}' 
          .format(FP[0][0],FP[0][1])+
        '\n# Taxonomía propuesta con k= 30: {} con FP {:.2f}'
          .format(FP[1][0],FP[1][1])+
        '\n# Taxonomía propuesta con k= 50: {} con FP {:.2f}'
          .format(FP[2][0],FP[2][1])     
              )            
    coor = input('\n ¿Desea obtener las efemérides de su objeto? \n Teclee Si para si o cualquier otra tecla para no: ')
    if coor == 'S' or coor == 'Si' or coor == 'si' or coor == 'SI' or coor == 's':
        coordenadas = coordenadas2()
        txt.write(
            '\n# Fecha de observación: ' + str(coordenadas['Date'][0]) +
            '\n# RA (Deg) = ' + str(coordenadas[0]['RA']) + '\n# Dec (Deg) = ' + str(coordenadas[0]['Dec']) +
            '\n# Delta (UA) = ' + str(coordenadas[0]['Delta']) + '\n# r (UA) = ' + str(coordenadas[0]['r']) +
            '\n# Fase (Deg) = ' + str(coordenadas[0]['Phase']) + '\n# V (Mag) = ' + str(coordenadas[0]['V'])
                  )            
    txt.close()
    print('\n ¡Archivo listo!')
          
def coordenadas2():
    num = input('\n Número de su asteroide: ')
    UT = input('\n UT (HH:MM): ')
    DATE = input('\n DATE (AAAA-MM-DD): ')
    fecha = DATE + 'T' + UT   
    eph = MPC.get_ephemeris(str(num), ra_format={'sep': ':', 'precision': 1, 'unit': 'hourangle'},
                        dec_format={'sep': ':', 'precision': 1}, location=('250d', '31d', '2480m'),
                        start=fecha, number=1)
    #result = MPC.query_object('asteroid', number = num)
    return eph
