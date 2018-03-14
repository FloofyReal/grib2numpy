import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
import numpy as np
import pickle
 
plt.figure(figsize=(12,8))

path = './Temperature.pkl'
lat_path = './lats_32x32.pkl'
lon_path = './lons_32x32.pkl'

def unpickle(path):
    with open(path, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
    return data

data = unpickle(path)

n_of_frames = 24
starting_frame = 1
name = 'teplota0101'

for n in range(n_of_frames):
    print(n)
    data_state = data[n] 

    print('shape:')
    print(data_state.shape)

    print('min/max:')
    print(max(data_state[0] - 273.15))
    print(min(data_state[0] - 273.15))

    # lat,lon = grb.latlons() # Set the names of the latitude and longitude variables in your input GRIB file
    lon = unpickle(lon_path)
    lat = unpickle(lat_path)
    # print(len(lat))
    # print(len(lon))

    m=Basemap(projection='mill', llcrnrlon=13,urcrnrlon=22,llcrnrlat=45,urcrnrlat=54.3,resolution='h')

    x, y = m(lon,lat)

    # cs = m.pcolormesh(x,y,data-273.15,cmap=plt.cm.hot)
    cs = m.pcolormesh(x,y,data_state-273.15)

    my_coast = m.drawcoastlines()
    my_states = m.drawcountries()
    # my_p = m.drawparallels(np.arange(40,60,2),labels=[1,1,0,0])
    # my_m = m.drawmeridians(np.arange(10,28,2),labels=[0,0,0,1])
    
    plt.title('Teplota ' + str(n)) # Set the name of the variable to plot
    # 
    print('saving picture')
    plt.savefig('./gif/' + name + '/temp_32_' + str(n).zfill(2) + '.png') # Set the output file name

# BIG 
        # "area": "70/-15/30/30",
# m=Basemap(projection='mill', llcrnrlon=-15,urcrnrlon=30,llcrnrlat=30,urcrnrlat=70,resolution='h')

# 64x64
        # "area": "58.8/8.1/40/27",
# m=Basemap(projection='mill', llcrnrlon=8.1,urcrnrlon=27,llcrnrlat=40,urcrnrlat=58.8,resolution='h')

# 32x32
        # "area": "54.3/13/45/22",