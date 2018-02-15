import pygrib
import numpy as np

from matplotlib import pyplot as plt
from matplotlib import colors
from mpl_toolkits.basemap import Basemap, addcyclic

def grb_to_grid(grb_obj):
    n_levels = len(grb_obj)
    levels = np.array([grb_element['level'] for grb_element in grb_obj])
    indexes = np.argsort(levels)[::-1]
    cube = np.zeros([n_levels, grb_obj[0].values.shape[0], grb_obj[0].values.shape[1]])
    for i in range(n_levels):
        cube[i,:,:] = grb_obj[indexes[i]].values
    cube_dict = {
                 'data' : cube,
                 'units' : grb_obj[0]['units'],
                 'levels' : levels[indexes]
                 }
    return cube, cube_dict

filename1 = './data/ECMWF/BIG/europe_4p_201601.grb'
filename2 = './data/ECMWF/BIG/europe_geopress_201601.grb'
filename3 = './data/ECMWF/BIG/europe_wind_201601.grb'

myfile1 = pygrib.open(filename)
myfile2 = pygrib.open(filename)
myfile3 = pygrib.open(filename)

grb_temp = myfile1.select(name='Temperature')
grb_cloud = myfile1.select(name='Cloud cover')
grb_hum = myfile1.select(name='Specific humidity')
grb_geo = myfile.select(name='Geopotential')
grb_pressure = myfile.select(name='Logarithm of surface pressure')
grb_windU = myfile.select(name='U component of wind')
grb_windV = myfile.select(name='V component of wind')

temp = grb_to_grid(grb_temp)
cloud = grb_to_grid(grb_cloud)
hum = grb_to_grid(grb_hum)
geo = grb_to_grid(grb_geo)
pressure = grb_to_grid(grb_pressure)
windU = grb_to_grid(grb_windU)
windV = grb_to_grid(grb_windV)

"""

for each

cs = m.pcolormesh(x,y,temp[0],cmap=plt.cm.hot)

my_coast = m.drawcoastlines()
my_states = m.drawstates()
my_p = m.drawparallels(np.arange(20,80,4),labels=[1,1,0,0])
my_m = m.drawmeridians(np.arange(-140,-60,4),labels=[0,0,0,1])

fig.save('./plot')
plt.show()

"""
