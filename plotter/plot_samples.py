import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.basemap import Basemap
import numpy as np
import pickle
import re
from os import walk

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
experiment_name = '32x32_temp_resize'
batch_size = 3
lat_path = './lats_32x32.pkl'
lon_path = './lons_32x32.pkl'

# lat,lon = grb.latlons() # Set the names of the latitude and longitude variables in your input GRIB file
lon = unpickle(lon_path)
lat = unpickle(lat_path)


print('plotting for experiment ' + experiment_name)
source_path = './experiments_samples/' + experiment_name + '/'
filename = 'samples/'
endfile = 'plots/'

file_names = get_all_files(source_path=source_path, filename=filename)
sort_nicely(file_names)
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
counter = 0
for future, original in zip(futu,orig):
    path = original
    path2 = future
    
    # LOAD ORIGINAL
    data_orig = unpickle(path)
    # LOAD PREDICTION
    data2_futu = unpickle(path2)

    for index in range(batch_size):
        data = data_orig[index]
        data = data.reshape((32,32))

        data2 = data2_futu[index]
        data2 = data2.reshape((32,32))

        # print(data)
        # print(data2)
        
        fig = plt.figure(dpi=500)

        plt.style.use('grayscale')
        ax = fig.add_subplot(211)
        ax.set_title("Original")
        m = Basemap(projection='mill', llcrnrlon=13,urcrnrlon=22,llcrnrlat=45,urcrnrlat=54.3,resolution='h')
        x, y = m(lon,lat)
        m.pcolormesh(x,y,data)
        m.drawmapboundary()
        m.drawcoastlines()
        m.drawcountries()

        ax = fig.add_subplot(221)
        ax.set_title("Forecast")
        m = Basemap(projection='mill', llcrnrlon=13,urcrnrlon=22,llcrnrlat=45,urcrnrlat=54.3,resolution='h')
        x, y = m(lon,lat)
        m.pcolormesh(x,y,data2-273.15)
        m.drawmapboundary()
        m.drawcoastlines()
        m.drawcountries()
        
        # fig.colorbar(pad=0.10, label='Teplota')
        # fig.title('Teplota') # Set the name of the variable to plot
        # 
        superendpath = source_path + endfile + 'temp_32_batch' + str(index) + '_pic' + str(counter) + 'GREYS.png'
        plt.savefig(superendpath, bbox_inches = "tight") # Set the output file name
        print('Saved pic ' + superendpath)
        plt.close(fig)

    counter = counter + 200