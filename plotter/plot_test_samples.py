import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
import numpy as np
import pickle
import re
from os import walk
import os

def unpickle(path):
    with open(path, 'rb') as f:
        data = pickle.load(f, encoding='latin1')
    return data

def tryint(s):
    try:
        return int(s)
    except:
        return s
    
def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)
    
def get_all_files(source_path, filename):
    fullpath = source_path + filename
    f = []
    for (dirpath, dirnames, filenames) in walk(fullpath):
        f.extend(filenames)
        break
    return f

# MAIN CHANGEABLES
experiment_name = 'train_allwvars_32x32_10years_800epochs_lr-0001_v2'
# WVARS - same parameter as in training/testing
wvars = '11111'
lat_path = './lats_32x32.pkl'
lon_path = './lons_32x32.pkl'

# lat,lon = grb.latlons() # Set the names of the latitude and longitude variables in your input GRIB file
lon = unpickle(lon_path)
lat = unpickle(lat_path)

print('plotting for experiment ' + experiment_name)
source_path = './experiments_samples/' + experiment_name + '/'
filename = 'test/'
endfile = 'plots/test/'

path = source_path + endfile
if not os.path.exists(path):
    os.mkdir(path)

file_names = get_all_files(source_path=source_path, filename=filename)
sort_nicely(file_names)
print(file_names)
paths = []

futu = []
orig = []
for file in file_names:
    if 'future' in file:
        futu.append(source_path + filename + file)
    elif 'image' in file:
        orig.append(source_path + filename + file)

print(futu, orig)

print('BEGIN')
for futu_path, orig_path in zip(futu,orig):
    # LOAD ORIGINAL
    data_orig = unpickle(orig_path)
    # LOAD PREDICTION
    data_futu = unpickle(futu_path)

    counter = orig_path.split('.')[1].split('_')[-2]
    print(counter)

    weather_params = ['Temperature', 'Cloud_cover', 'Specific_humidity', 'Logarithm_of_surface_pressure', 'Geopotential']
    par = 0
    for p, k in zip(weather_params, wvars):
        if k == '1':
            print(p)
            original = data_orig[par]
            forecast = data_futu[par]

            init = original[:,0,:,:,:].reshape([32,32])
            real = original[:,1,:,:,:].reshape([32,32])
            gen = forecast[:,1,:,:,:].reshape([32,32])
            diff = np.abs(real - gen).reshape([32,32])

            combined_data = np.array([init, real, gen])
            _min, _max = np.amin(combined_data), np.amax(combined_data)

            fig = plt.figure(dpi=1000)

            print('Plot init frame')
            ax0 = fig.add_subplot(141)
            ax0.set_title("Initial state")
            m = Basemap(projection='mill', llcrnrlon=13,urcrnrlon=22,llcrnrlat=45,urcrnrlat=54.3,resolution='h')
            x, y = m(lon,lat)
            im0 = m.pcolormesh(x,y,init, vmin=_min, vmax=_max)
            cbar0 = fig.colorbar(im0,fraction=0.06, pad=0.05, ax=ax0)
            cbar0.ax.tick_params(labelsize=8)
            m.drawmapboundary()
            m.drawcoastlines()
            m.drawcountries()

            print('Plot real future frame')
            ax1 = fig.add_subplot(142)
            ax1.set_title("Real future")
            m = Basemap(projection='mill', llcrnrlon=13,urcrnrlon=22,llcrnrlat=45,urcrnrlat=54.3,resolution='h')
            x, y = m(lon,lat)
            im1 = m.pcolormesh(x,y,real, vmin=_min, vmax=_max)
            cbar1 = fig.colorbar(im1,fraction=0.06, pad=0.05, ax=ax1)
            cbar1.ax.tick_params(labelsize=8)
            m.drawmapboundary()
            m.drawcoastlines()
            m.drawcountries()

            print('Plot forecast frame')
            ax2 = fig.add_subplot(143)
            ax2.set_title("Forecast")
            m = Basemap(projection='mill', llcrnrlon=13,urcrnrlon=22,llcrnrlat=45,urcrnrlat=54.3,resolution='h')
            x, y = m(lon,lat)
            im2 = m.pcolormesh(x,y,gen, vmin=_min, vmax=_max)
            cbar2 = fig.colorbar(im2,fraction=0.06, pad=0.05, ax=ax2)
            cbar2.ax.tick_params(labelsize=8)
            m.drawmapboundary()
            m.drawcoastlines()
            m.drawcountries()

            print('Plot difference frame')
            ax3 = fig.add_subplot(144)
            ax3.set_title("Diff")
            m = Basemap(projection='mill', llcrnrlon=13,urcrnrlon=22,llcrnrlat=45,urcrnrlat=54.3,resolution='h')
            x, y = m(lon,lat)
            im3 = m.pcolormesh(x,y,diff,cmap='Greys')
            cbar3= fig.colorbar(im3,fraction=0.06, pad=0.05, ax=ax3)
            cbar3.ax.tick_params(labelsize=8)
            m.drawmapboundary()
            m.drawcoastlines()
            m.drawcountries()
            
            plt.tight_layout()
            superendpath = source_path + endfile + p + '_step' + str(counter) + '.png'
            # plt.savefig(superendpath) # Set the output file name
            plt.savefig(superendpath, bbox_inches = "tight") # Set the output file name
            print('Saved pic ' + superendpath)
            plt.close(fig)
            plt.clf()

            par += 1
