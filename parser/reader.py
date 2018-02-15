import numpy as np
import pickle

name = '../ECMWF/PARSED/64x64/temperature_2016.pkl'

with open(name,'rb') as f:
    x = pickle.load(f, encoding='latin1')
    print(len(x))
    print(len(x)/24)
    print(x[0])
