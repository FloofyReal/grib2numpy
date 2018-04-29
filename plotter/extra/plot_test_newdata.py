import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
import numpy as np
import pickle
import datetime
import os
 
plt.figure(figsize=(12,8))

# choose size to plot
# size = '64x64'
size = '64x64'

path_t_n = '../../data_parsed/' + size + '/train_Temperature_32x32.pkl'
path_sh_n = '../../data_parsed/' + size + '/train_Specific_humidity_32x32.pkl'
path_cc_n = '../../data_parsed/' + size + '/train_Cloud_cover_32x32.pkl'

size = '32x32'

# path to dataset
path_t = '../../data_parsed/' + size + '/train_Temperature_32x32.pkl'
path_sh = '../../data_parsed/' + size + '/train_Specific_humidity_32x32.pkl'
path_cc = '../../data_parsed/' + size + '/train_Cloud_cover_32x32.pkl'


# path to longitutes and latitudes for plotting
lat_path = './lats_32x32.pkl'
lon_path = './lons_32x32.pkl'


def unpickle(path):
    with open(path, 'rb') as f:
        data = pickle.load(f, encoding='bytes')
    return data
    
# choose parameter to work with

name = 'Temperature'
# name = 'Specific_humidity'
# name = 'Cloud_cover'
# name = 'Surface_pressure'
# name = 'Geopotential'

path = path_t
# path = path_sh
# path = path_cc
# path = path_sp
# path = path_geo

path2 = path_t_n

data_all = unpickle(path)
data_all_new = unpickle(path2)

# first date of dataset
date_zero = datetime.datetime(2008,1,1,0,0)
date_zero_small = datetime.datetime(2010,1,1,0,0)

# choose date/time to plot
date_desired = datetime.datetime(2013,12,10,7,0)
# date_desired = datetime.datetime(2013,12,10,22,0)

# based on the date create folder to save files to
endfile = 'plots/' + date_desired.ctime().replace(':','').replace(' ','_') + '/'
endfile_single = 'plots/test/'

if not os.path.exists(endfile):
    os.makedirs(endfile)

# define diff between desired time and time_zero of the dataset (1.1.2008 00:00)
diff = date_desired - date_zero
diff_small = date_desired - date_zero_small

hours_diff = diff.days * 24 + diff.seconds // 3600
hours_diff_small = diff_small.days * 24 + diff_small.seconds // 3600

# if plotting series or just single frame
plot_series = False
# if series: series lenght in hours
series = int(7*24)

if not plot_series:
    data_32 = data_all[hours_diff_small] 
    data_64 = data_all_new[hours_diff] 
    data_n = [data_32, data_64]
    nnn = ['data_32', 'data_64']
    for data,nn in zip(data_n,nnn):
        print(data[0].shape)

        # lat,lon = grb.latlons() # Set the names of the latitude and longitude variables in your input GRIB file
        lon = unpickle(lon_path)
        lat = unpickle(lat_path)
        print(len(lat))
        print(len(lon))
        
        if size == '64x64':
            # "area": "58.8/8.1/40/27",
            m=Basemap(projection='mill', llcrnrlon=8.1,urcrnrlon=27,llcrnrlat=40,urcrnrlat=58.8,resolution='h')
        elif size == '32x32':
            # "area": "54.3/13/45/22",
            m=Basemap(projection='mill', llcrnrlon=13,urcrnrlon=22,llcrnrlat=45,urcrnrlat=54.3,resolution='h')
        else:
            print('ERROR - BAD SIZE')


        x, y = m(lon,lat)

        # cs = m.pcolormesh(x,y,data-273.15,cmap=plt.cm.hot)

        if name == 'Temperature':
            cs = m.pcolormesh(x,y,data[0]-273.15)
            # plt.colorbar(pad=0.10, label='degree Celsius')
        elif name == 'Surface_pressure':
            cs = m.pcolormesh(x,y,(np.exp(data[0])/1000))
            # plt.colorbar(pad=0.10, label='kPa')
        elif name == 'Specific_humidity':
            cs = m.pcolormesh(x,y,data[0])
            # plt.colorbar(pad=0.10, label='kg / kg')
        elif name == 'Cloud_cover':
            cs = m.pcolormesh(x,y,data[0])
            # plt.colorbar(pad=0.10, label='% of cloud cover')
        elif name == 'Geopotential':
            cs = m.pcolormesh(x,y,data[0])
            # plt.colorbar(pad=0.10, label='m^2 / s^2')
        else:
            cs = m.pcolormesh(x,y,data[0])
            # plt.colorbar(pad=0.10, label=name)


        my_coast = m.drawcoastlines()
        my_states = m.drawcountries()
        # my_p = m.drawparallels(np.arange(40,60,2),labels=[1,1,0,0])
        # my_m = m.drawmeridians(np.arange(10,28,2),labels=[0,0,0,1])
        # plt.colorbar(pad=0.10, label=name)
        plt.title(name) # Set the name of the variable to plot
        print(data[1].ctime())
        # ple_sing + date_desired.ctime().replace(':','').replace(' ','_')
        plt.savefig(endfile_single + name + '_' + nn + size + '.png') # Set the output file name
        plt.clf()
        # plt.show()
else:
    name_orig = name
    counter = 1
    for i in range(hours_diff, hours_diff+series):
        name = name_orig + str(counter)
        counter += 1

        data = data_all[i] 
        print(data[0].shape)

        # lat,lon = grb.latlons() # Set the names of the latitude and longitude variables in your input GRIB file
        lon = unpickle(lon_path)
        lat = unpickle(lat_path)
        print(len(lat))
        print(len(lon))
        
        if size == '64x64':
            # "area": "58.8/8.1/40/27",
            m=Basemap(projection='mill', llcrnrlon=8.1,urcrnrlon=27,llcrnrlat=40,urcrnrlat=58.8,resolution='h')
        elif size == '32x32':
            # "area": "54.3/13/45/22",
            m=Basemap(projection='mill', llcrnrlon=13,urcrnrlon=22,llcrnrlat=45,urcrnrlat=54.3,resolution='h')
        else:
            print('ERROR - BAD SIZE')


        x, y = m(lon,lat)

        # cs = m.pcolormesh(x,y,data-273.15,cmap=plt.cm.hot)
        if name_orig == 'Temperature':
            cs = m.pcolormesh(x,y,data[0]-273.15)
        else:
            cs = m.pcolormesh(x,y,data[0])

        my_coast = m.drawcoastlines()
        my_states = m.drawcountries()
        # my_p = m.drawparallels(np.arange(40,60,2),labels=[1,1,0,0])
        # my_m = m.drawmeridians(np.arange(10,28,2),labels=[0,0,0,1])
        
        # plt.colorbar(pad=0.10, label=name)
        plt.title(name) # Set the name of the variable to plot
        print(data[1].ctime())
        
        plt.savefig(endfile + 'series_' + name + '_' + size + '.png') # Set the output file name
        print('saved pic: ' + name)