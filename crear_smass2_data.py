#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 02:56:39 2021

@author: ubuntu
"""
import os
import pandas as pd
import numpy as np

script_dir = os.path.dirname(__file__) 

smass = sorted(os.listdir('./data/smassN'))
abs_file_path = os.path.join('data/' + 'smassN.txt')
kk = range(4350,9275,25)
LO=[]
for num in kk:
    LO.append(num/10000)   
txt = open(abs_file_path,'w')
suma=0
for n in range(0,len(smass)):
    kk = pd.read_csv('data/smassN/'+smass[n], header=None, delim_whitespace=True )
    flu = kk.iloc[:,1]; flu = flu.to_numpy()
    lo = kk.iloc[:,0]; lo = lo.to_list()
    new_flu = np.zeros(len(LO))
    txt.write(smass[n].split('.')[0]+'\t')
    for i in lo:
        while True:
            try:
                new_flu[LO.index(i)]=flu[lo.index(i)]
                break
            except ValueError:
                break
    for k in new_flu:
        txt.write(str(k)+'\t')
    txt.write('\n')
    suma +=1
txt.close()