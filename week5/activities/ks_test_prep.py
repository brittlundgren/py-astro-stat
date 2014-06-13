#!/usr/bin/python

import scipy
import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
import csv

data = np.loadtxt('data/sdss_quasars.tsv', delimiter=';', usecols=(0,),
        skiprows=66)

f = open('data/sdss_quasars.tsv', 'r')

header = f.readline(76)

# 0 1    2    3    4    5    6   7      8  9  10 11 12 13 14
# z umag gmag rmag imag zmag utf TflagB Lz Hz fR fX fS f* fG

with open('data/sdss_quasars.tsv') as f:
    f_tsv = csv.reader(f, delimiter=';')
    data_array = np.zeros(len(data) - 1)
    data_dict = {'u-r': np.copy(data_array),
                 'uniform_flag': np.copy(data_array),
                 'highz_color_flag': np.copy(data_array),
                 'lowz_color_flag': np.copy(data_array),
                 'rosat_flag': np.copy(data_array)}
    for i, row in enumerate(f_tsv):
        try:
            data_dict['u-r'][i] = float(row[1]) - float(row[3])
            data_dict['uniform_flag'][i] = float(row[6])
            data_dict['highz_color_flag'][i] = float(row[9])
            data_dict['lowz_color_flag'][i] = float(row[8])
            data_dict['rosat_flag'][i] = float(row[11])
        except (TypeError, IndexError, ValueError):
            pass

fle = open('data/sdss_quasars.tsv')
count = len(open('data/sdss_quasars.tsv').readlines(  ))
keys = ["z", "umag", "gmag", "rmag", "imag", "zmag","utf", "TflagB", "Lz", "Hz", "fR", "fX", "fS", "f*", "fG"]
d = dict((el, np.zeros(count)) for el in keys)
for i, line in enumerate(fle):
   if len(line) > 1 and not ('#' in line or 'mag' in line or '--' in line):
       for j, key in enumerate(keys):
           try:
               d[key][i] = line.split()[j]
           except IndexError:
               print("Line "+line+" has too few values")
       #print(len(line.split()))

from scipy.stats import ks_2samp
from random import sample

ur = d['umag'] - d['rmag']

ur_fG = ur[d['fG'] == 1]
ur_fX = ur[d['f*'] == 1]
ur_uni_1 = sample(ur, 10000)
ur_uni_2 = sample(ur, 10000)

ks_2samp(ur_fG, ur_fX)
ks_2samp(ur_uni_1, ur_uni_2)




