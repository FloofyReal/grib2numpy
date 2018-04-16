import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
import numpy as np
import pickle
import datetime
import os
 
plt.figure(figsize=(12,8))

# choose size to plot
size = '64x64'
# size = '32x32'

# path to dataset
path_t = '../../../../../../experiments/data_parsed/' + size + '/Temperature.pkl'
path_sh = '../../../../../../experiments/data_parsed/' + size + '/Specific_humidity.pkl'
path_cc = '../../../../../../experiments/data_parsed/' + size + '/Cloud_cover.pkl'
path_sp = '../../../../../../experiments/data_parsed/' + size + '/Logarithm_of_surface_pressure.pkl'
path_geo = '../../../../../../experiments/data_parsed/' + size + '/Geopotential.pkl'

# path to longitutes and latitudes for plotting
lat_path = './lats_' + size + '.pkl'
lon_path = './lons_' + size + '.pkl'


def unpickle(path):
    with open(path, 'rb') as f:
        data = pickle.load(f, encoding='bytes')
    return data
    
# choose parameter to work with

# name = 'Temperature'
# name = 'Specific_humidity'
# name = 'Cloud_cover'
name = 'Surface_pressure'
# name = 'Geopotential'

# path = path_t
# path = path_sh
# path = path_cc
path = path_sp
# path = path_geo

data_all = unpickle(path)

# first date of dataset
date_zero = datetime.datetime(2008,1,1,0,0)

# choose date/time to plot
date_desired = datetime.datetime(2013,12,10,7,0)
# date_desired = datetime.datetime(2013,12,10,22,0)

# based on the date create folder to save files to
endfile = 'plots/' + date_desired.ctime().replace(':','').replace(' ','_') + '/'
endfile_single = 'plots/singles/'
if not os.path.exists(endfile):
    os.makedirs(endfile)

# define diff between desired time and time_zero of the dataset (1.1.2008 00:00)
diff = date_desired - date_zero
hours_diff = diff.days * 24 + diff.seconds // 3600

# if plotting series or just single frame
plot_series = False
# if series: series lenght in hours
series = int(7*24)

if not plot_series:
    data = data_all[hours_diff] 
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
        plt.colorbar(pad=0.10, label='degree Celsius')
    elif name == 'Surface_pressure':
        cs = m.pcolormesh(x,y,(np.exp(data[0])/1000))
        plt.colorbar(pad=0.10, label='kPa')
    elif name == 'Specific_humidity':
        cs = m.pcolormesh(x,y,data[0])
        plt.colorbar(pad=0.10, label='kg / kg')
    elif name == 'Cloud_cover':
        cs = m.pcolormesh(x,y,data[0])
        plt.colorbar(pad=0.10, label='% of cloud cover')
    elif name == 'Geopotential':
        cs = m.pcolormesh(x,y,data[0])
        plt.colorbar(pad=0.10, label='m^2 / s^2')
    else:
        cs = m.pcolormesh(x,y,data[0])
        plt.colorbar(pad=0.10, label=name)


    my_coast = m.drawcoastlines()
    my_states = m.drawcountries()
    # my_p = m.drawparallels(np.arange(40,60,2),labels=[1,1,0,0])
    # my_m = m.drawmeridians(np.arange(10,28,2),labels=[0,0,0,1])
    # plt.colorbar(pad=0.10, label=name)
    plt.title(name) # Set the name of the variable to plot
rint(data[1].ctime())
    ple_sing + date_desired.ctime().replace(':','').replace(' ','_')
    # plt.savefig(endfile + name + '_' + size + '.png') # Set the output file name
    plt.show()
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
        
        plt.savefig(endfile + 'seri
es_' + name + '_' + size + '.png') # Set the output file name
        print('saved pic: ' + name)