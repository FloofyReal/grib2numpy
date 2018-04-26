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
experiment_name = 'test'
lat_path = './lats_32x32.pkl'
lon_path = './lons_32x32.pkl'

# lat,lon = grb.latlons() # Set the names of the latitude and longitude variables in your input GRIB file
lon = unpickle(lon_path)
lat = unpickle(lat_path)

print('plotting for experiment ' + experiment_name)
source_path = './experiments_samples/' + experiment_name + '/'
filename = ''
endfile = 'diffs/'

path = source_path + filename + endfile
if not os.path.exists(path):
    os.mkdir(path)

file_names = get_all_files(source_path=source_path, filename=filename)
sort_nicely(file_names)
paths = []

diffs = []
for file in file_names:
    if 'sample_diff' in file:
        diffs.append(source_path + filename + file)

print('BEGIN')
counter = 0
for diff in diffs:
    # LOAD DIFF
    data = unpickle(diff)
    data = np.abs(data)
    data = data.reshape([32,32])

    # get name from path
    name = diff.split('.')[1].split('_')[2:]
    title = ' '.join(name)
    name = '_'.join(name)
    print('plotting:', title)

    fig = plt.figure(dpi=500)

    plt.style.use('grayscale')
    plt.title(title)
    m = Basemap(projection='mill', llcrnrlon=13,urcrnrlon=22,llcrnrlat=45,urcrnrlat=54.3,resolution='h')
    x, y = m(lon,lat)
    m.pcolormesh(x,y,data)
    m.drawmapboundary()
    m.drawcoastlines()
    m.drawcountries()

    plt.colorbar(pad=0.10, label='Error')

    superendpath = source_path + endfile + name + '.png'
    plt.savefig(superendpath, bbox_inches = "tight") # Set the output file name
    print('Saved pic ' + superendpath)
    plt.close(fig)
    plt.clf()